# OmniMirror

### Cast Your Phone

**OmniMirror** is a Windows desktop GUI for [Genymobile scrcpy](https://github.com/Genymobile/scrcpy). It makes Android screen mirroring and device control easier through a modern graphical interface—without requiring users to manually enter scrcpy commands.

**Developed by Md. Arfan Ahmed**  
**Powered by scrcpy 5.0.1**

---

## Features

- Graphical interface for Android screen mirroring.
- USB and wireless ADB connection support.
- Android device detection and connection management.
- Access to scrcpy configuration options through the GUI.
- Persistent application settings.
- Android audio forwarding support, with different methods for Android 10 and Android 11+.
- Portable Windows application distribution.

OmniMirror is designed as a GUI layer around scrcpy. The upstream scrcpy core is not modified.

## Android Compatibility and Audio Forwarding

Audio forwarding works differently depending on the Android version.

### Android 11 and newer

OmniMirror uses **scrcpy's native audio forwarding**.

- Connect your Android phone through USB or wireless ADB.
- Enable audio forwarding in OmniMirror.
- Start screen mirroring.
- Audio is forwarded from the phone to the PC through scrcpy.

This is the recommended method for Android 11 and newer devices.

### Android 10

Android 10 does not support scrcpy's native audio forwarding in the same way as Android 11 and newer.

To support Android 10, OmniMirror uses **sndcpy**, an alternative audio-forwarding solution originally developed by the scrcpy project author.

The Android 10 workflow is:

1. Connect your phone to the PC using USB.
2. Make sure ADB detects the device.
3. Start screen mirroring through OmniMirror.
4. OmniMirror uses scrcpy for video and sndcpy for audio.
5. VLC Media Player is used on the PC to receive and play the forwarded audio.

**Important Android 10 notes:**

- VLC Media Player must be installed on the PC.
- OmniMirror needs to locate the VLC executable.
- Depending on the device and audio-routing behavior, the phone speaker may continue playing audio while the PC also receives it.
- If duplicate audio occurs, setting the phone's media volume to zero can prevent sound from playing through the phone speaker while retaining the forwarded PC audio.
- Audio routing and compatibility may vary between Android devices and applications.

Android 10 audio forwarding is therefore a workaround, not the same native audio experience available on Android 11+.

## Requirements

- Windows 10 or Windows 11.
- An Android device with USB debugging enabled.
- ADB access through USB or wireless connection.
- scrcpy 5.0.1 runtime files.
- VLC Media Player for the Android 10 audio workaround.

## Project Structure

The repository is organized as follows:

```text
OmniMirror/
├── LICENSE
├── README.md
├── .gitignore
└── scrcpy-gui/
    ├── assets/
    │   ├── omnimirror-logo.png
    │   └── omnimirror.ico
    ├── main.py
    ├── sndcpy_manager.py
    ├── OmniMirror.spec
    └── OmniMirror-Lite.spec
```

The `scrcpy-runtime` directory is not included in this source repository because it contains third-party executable binaries and dependencies.

## Runtime Setup

OmniMirror requires the scrcpy runtime files to be available in a directory named `scrcpy-runtime` at the project root.

Obtain the official **scrcpy 5.0.1 Windows release** from:

https://github.com/Genymobile/scrcpy/releases/tag/v5.0.1

Extract the required runtime files into:

```text
OmniMirror/
└── scrcpy-runtime/
    ├── adb.exe
    ├── scrcpy.exe
    ├── scrcpy-server
    ├── SDL3.dll
    ├── libusb-1.0.dll
    └── ...
```

For Android 10 audio forwarding, also obtain sndcpy from its upstream repository:

https://github.com/rom1v/sndcpy

Place its required files in the expected runtime structure:

```text
scrcpy-runtime/
└── sndcpy/
    ├── sndcpy
    ├── sndcpy.apk
    └── sndcpy.bat
```

Keep the original third-party license notices with their respective runtime distributions.

## Running from Source

1. Clone this repository.
2. Set up the required `scrcpy-runtime` directory as described above.
3. Create and activate a Python virtual environment.
4. Install the Python dependencies required by the application.
5. Run the application.

Example:

```powershell
git clone https://github.com/YOUR_USERNAME/OmniMirror.git
cd OmniMirror

python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install the application's required Python dependencies.
# Refer to the project configuration for the exact dependencies.

python .\scrcpy-gui\main.py
```

## Building

The project includes PyInstaller specification files:

- `OmniMirror.spec`
- `OmniMirror-Lite.spec`

These can be used with the corresponding PyInstaller build configuration after preparing the runtime and Python environment.

## Troubleshooting

**Device not detected**

- Enable USB debugging on the Android phone.
- Check the USB cable and connection.
- Accept the USB debugging authorization prompt on the phone.
- Verify that ADB can detect the device.

**Android 10 audio is not working**

- Verify that VLC is installed.
- Make sure the sndcpy runtime files are present.
- Check that the phone is connected and authorized through ADB.
- Remember that Android 10 uses the sndcpy workaround rather than native scrcpy audio forwarding.

**Audio plays from both the phone and PC**

This can happen with the Android 10 workaround. Try setting the phone's media volume to zero while keeping the PC playback volume at the desired level.

**USB connection keeps disconnecting**

- Try another USB cable or port.
- Avoid loose USB connections.
- Reconnect the device and authorize ADB again if necessary.

## Third-Party Software and Licenses

OmniMirror uses third-party software:

| Component | License |
|---|---|
| OmniMirror GUI code | MIT |
| scrcpy | Apache License 2.0 |
| sndcpy | MIT |
| Other runtime dependencies | Their respective licenses |

The OmniMirror MIT License applies only to the original OmniMirror code. It does not replace or override the licenses of scrcpy, sndcpy, FFmpeg, SDL, ADB, or other third-party components.

See the respective upstream projects for their license terms:

- [scrcpy](https://github.com/Genymobile/scrcpy)
- [sndcpy](https://github.com/rom1v/sndcpy)

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

If you encounter a problem:

1. Check the troubleshooting section.
2. Open a GitHub issue.
3. Include your Windows version, Android version, device model, and relevant application logs.
4. Describe the steps required to reproduce the issue.

## License

OmniMirror's original GUI code is licensed under the [MIT License](LICENSE).

Third-party components remain under their respective licenses.
