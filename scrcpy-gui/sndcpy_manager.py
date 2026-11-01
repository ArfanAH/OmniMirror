
import os
import shutil
import subprocess
from pathlib import Path

from PySide6.QtCore import QTimer


class SndcpyManager:
    PORT = 28200
    PACKAGE = "com.rom1v.sndcpy"

    def __init__(self, adb_path, runtime_dir, parent=None):
        self.adb = Path(adb_path)
        self.runtime = Path(runtime_dir)
        self.apk = self.runtime / "sndcpy" / "sndcpy.apk"
        self.parent = parent

        self.serial = None
        self.forwarded = False
        self.vlc_process = None
        self.vlc_path = ""

    def find_vlc(self, preferred=""):
        candidates = []

        if preferred.strip():
            candidates.append(Path(preferred.strip().strip('"')))

        path = shutil.which("vlc.exe") or shutil.which("vlc")
        if path:
            candidates.append(Path(path))

        for variable in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            root = os.environ.get(variable)
            if root:
                candidates.extend([
                    Path(root) / "VideoLAN" / "VLC" / "vlc.exe",
                    Path(root) / "Programs" / "VideoLAN" / "VLC" / "vlc.exe",
                ])

        try:
            import winreg

            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                for key_name in (
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\vlc.exe",
                    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\vlc.exe",
                ):
                    try:
                        with winreg.OpenKey(hive, key_name) as key:
                            value, _ = winreg.QueryValueEx(key, None)
                            candidates.append(Path(value.strip('"')))
                    except OSError:
                        pass
        except ImportError:
            pass

        checked = set()
        for candidate in candidates:
            try:
                candidate = candidate.expanduser().resolve()
                key = str(candidate).casefold()
                if key not in checked:
                    checked.add(key)
                    if candidate.is_file() and candidate.name.casefold() == "vlc.exe":
                        return str(candidate)
            except (OSError, RuntimeError):
                pass

        return ""

    def adb_run(self, serial, *args, timeout=30):
        result = subprocess.run(
            [str(self.adb), "-s", serial, *args],
            cwd=str(self.runtime),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )

        if result.returncode != 0:
            message = (result.stderr or result.stdout or "ADB command failed").strip()
            raise RuntimeError(message)

        return result.stdout.strip()

    def get_android_api(self, serial):
        output = self.adb_run(
            serial, "shell", "getprop", "ro.build.version.sdk", timeout=10
        )
        try:
            return int(output)
        except ValueError as exc:
            raise RuntimeError(
                f"Could not detect Android API level: {output!r}"
            ) from exc

    def start(self, serial, preferred_vlc=""):
        if self.serial:
            raise RuntimeError("sndcpy is already running.")

        if not self.apk.is_file():
            raise FileNotFoundError(f"sndcpy APK not found:\n{self.apk}")

        vlc = self.find_vlc(preferred_vlc)
        if not vlc:
            raise FileNotFoundError(
                "VLC was not found. Install VLC or browse to vlc.exe in OmniMirror."
            )

        self.vlc_path = vlc

        # Install or update the official sndcpy APK.
        try:
            self.adb_run(
                serial, "install", "-t", "-r", "-g", str(self.apk),
                timeout=60,
            )
        except Exception as install_error:
            # Retry using the official launcher's uninstall fallback.
            try:
                self.adb_run(
                    serial, "uninstall", self.PACKAGE, timeout=30
                )
                self.adb_run(
                    serial, "install", "-t", "-g", str(self.apk),
                    timeout=60,
                )
            except Exception as retry_error:
                raise RuntimeError(
                    f"Could not install sndcpy.\n"
                    f"Initial error: {install_error}\n"
                    f"Retry error: {retry_error}"
                ) from retry_error

        self.adb_run(
            serial, "shell", "appops", "set",
            self.PACKAGE, "PROJECT_MEDIA", "allow",
        )

        # Do not overwrite an existing forwarding rule.
        rules = self.adb_run(serial, "forward", "--list")
        for line in rules.splitlines():
            fields = line.split()
            if len(fields) >= 2 and fields[1] == f"tcp:{self.PORT}":
                raise RuntimeError(
                    f"ADB port {self.PORT} is already forwarded. "
                    "Close the existing sndcpy session first."
                )

        self.adb_run(
            serial, "forward", f"tcp:{self.PORT}",
            "localabstract:sndcpy",
        )
        self.serial = serial
        self.forwarded = True

        try:
            self.adb_run(
                serial, "shell", "am", "start", "-n",
                f"{self.PACKAGE}/.MainActivity",
            )
        except Exception:
            self.stop()
            raise

        # Let the phone's media-projection screen appear before VLC connects.
        QTimer.singleShot(1800, self._launch_vlc)

    def _launch_vlc(self):
        if not self.serial or not self.forwarded:
            return

        try:
            self.vlc_process = subprocess.Popen(
                [
                    self.vlc_path,
                    "-Idummy",
                    "--demux", "rawaud",
                    "--network-caching=0",
                    "--play-and-exit",
                    f"tcp://127.0.0.1:{self.PORT}",
                ],
                cwd=str(Path(self.vlc_path).parent),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception:
            self.stop()
            raise

    def stop(self):
        process = self.vlc_process
        self.vlc_process = None

        if process is not None and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=3)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass

        serial = self.serial
        remove_forward = self.forwarded

        self.serial = None
        self.forwarded = False

        if serial and remove_forward:
            try:
                subprocess.run(
                    [
                        str(self.adb), "-s", serial,
                        "forward", "--remove", f"tcp:{self.PORT}",
                    ],
                    cwd=str(self.runtime),
                    capture_output=True,
                    timeout=5,
                    creationflags=getattr(
                        subprocess, "CREATE_NO_WINDOW", 0
                    ),
                )
            except Exception:
                pass
