
import os
import sys
import shlex
import subprocess
from sndcpy_manager import SndcpyManager
from pathlib import Path

from PySide6.QtGui import QIcon, QPixmap

from PySide6.QtCore import QSettings, QTimer, Qt
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QPushButton, QTabWidget, QVBoxLayout, QWidget, QScrollArea,QInputDialog,
)

# ============================================================
# PATHS — official scrcpy runtime remains unchanged
# ============================================================

if getattr(sys, "frozen", False):
    RUNTIME_DIR = Path(sys._MEIPASS) / "scrcpy-runtime"
else:
    RUNTIME_DIR = Path(__file__).resolve().parent.parent / "scrcpy-runtime"

SCRCPY_PATH = RUNTIME_DIR / "scrcpy.exe"
ADB_PATH = RUNTIME_DIR / "adb.exe"
LOG_PATH = RUNTIME_DIR / "scrcpy-gui-last.log"

ORG_NAME = "ArfanApps"
APP_NAME = "OmniMirror"

# ============================================================
# MODERN UI
# ============================================================


STYLE = """
/* =========================
   MAIN WINDOW
========================= */
QMainWindow, QWidget {
    background: #F5F8F8;
    color: #243333;
    font-family: "Segoe UI";
    font-size: 13px;
}

/* =========================
   PANELS / CARDS
========================= */
QFrame#Panel {
    background: #FFFFFF;
    border: 1px solid #DCE8E6;
    border-radius: 12px;
}

/* =========================
   HEADINGS AND LABELS
========================= */
QLabel#Brand {
    background: transparent;
    color: #163D3A;
    font-size: 25px;
    font-weight: 700;
    padding: 0;
    border: none;
}

QLabel#Title {
    background: transparent;
    color: #163D3A;
    font-size: 22px;
    font-weight: 700;
    padding: 0;
    border: none;
}

QLabel#Section {
    background: transparent;
    color: #245650;
    font-size: 12px;
    font-weight: 700;
    padding: 0;
    border: none;
}

QLabel#Muted {
    background: transparent;
    color: #708582;
    padding: 0;
    border: none;
}

QLabel#Status {
    background: transparent;
    color: #0D9488;
    font-weight: 600;
    padding: 4px 0;
    border: none;
}

/* =========================
   BUTTONS
========================= */
QPushButton {
    background: #FFFFFF;
    color: #36514E;
    border: 1px solid #D2E1DE;
    border-radius: 7px;
    padding: 8px 13px;
    min-height: 18px;
    font-weight: 500;
}

QPushButton:hover {
    background: #EFFAF8;
    border-color: #7CCFC2;
    color: #087F73;
}

QPushButton:pressed {
    background: #D9F3EE;
    border-color: #54B8AA;
}

QPushButton:disabled {
    background: #F1F5F4;
    color: #A0AEAB;
    border-color: #E2EAE8;
}

QPushButton#Primary {
    background: #0D9488;
    color: #FFFFFF;
    border: 1px solid #0D9488;
    border-radius: 8px;
    padding: 10px 18px;
    min-height: 20px;
    font-weight: 700;
}

QPushButton#Primary:hover {
    background: #0F766E;
    border-color: #0F766E;
}

QPushButton#Primary:pressed {
    background: #115E59;
    border-color: #115E59;
}

QPushButton#Stop {
    background: #FFF7F6;
    color: #C2413B;
    border: 1px solid #F2D2CE;
    border-radius: 7px;
    padding: 8px 13px;
    font-weight: 600;
}

QPushButton#Stop:hover {
    background: #FDECEA;
    border-color: #EBA9A2;
}

/* =========================
   INPUTS AND DEVICE SELECTOR
========================= */
QComboBox, QLineEdit {
    background: #FFFFFF;
    color: #243333;
    border: 1px solid #D2E1DE;
    border-radius: 7px;
    padding: 8px 10px;
    min-height: 19px;
    selection-background-color: #BCEDE5;
    selection-color: #163D3A;
}

QComboBox:hover, QLineEdit:hover {
    border-color: #7CCFC2;
}

QComboBox:focus, QLineEdit:focus {
    border: 1px solid #0D9488;
}

QComboBox::drop-down {
    width: 26px;
    border: none;
    border-left: 1px solid #E4ECEA;
    border-top-right-radius: 7px;
    border-bottom-right-radius: 7px;
}

QComboBox QAbstractItemView {
    background: #FFFFFF;
    color: #243333;
    border: 1px solid #D2E1DE;
    selection-background-color: #D9F3EE;
    selection-color: #087F73;
    outline: none;
    padding: 4px;
}

/* =========================
   CHECKBOXES
========================= */
QCheckBox {
    background: transparent;
    color: #36514E;
    spacing: 8px;
    padding: 3px 0;
    border: none;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #B8CBC7;
    border-radius: 4px;
    background: #FFFFFF;
}

QCheckBox::indicator:hover {
    border-color: #0D9488;
}

QCheckBox::indicator:checked {
    background: #0D9488;
    border-color: #0D9488;
}

/* =========================
   TABS
========================= */
QTabWidget::pane {
    background: #FFFFFF;
    border: 1px solid #DCE8E6;
    border-radius: 10px;
    top: -1px;
}

QTabBar::tab {
    background: transparent;
    color: #708582;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 9px 13px;
    margin-right: 3px;
    margin-bottom: 4px;
}

QTabBar::tab:hover {
    background: #EFFAF8;
    color: #087F73;
}

QTabBar::tab:selected {
    background: #D9F3EE;
    color: #087F73;
    border: 1px solid #BCE8DF;
    font-weight: 700;
}

/* =========================
   SCROLL AREA
========================= */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: #F0F5F4;
    width: 8px;
    margin: 2px;
    border: none;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #C5D9D5;
    min-height: 25px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #8FBDB4;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
    border: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

/* =========================
   TOOLTIPS
========================= */
QToolTip {
    background: #163D3A;
    color: #FFFFFF;
    border: 1px solid #285B55;
    border-radius: 5px;
    padding: 5px 8px;
}






QLabel {
    background-color: transparent;
    color: #36514E;
    border: none;
}

QComboBox {
    background-color: #FFFFFF;
    color: #243333;
    border: 1px solid #D2E1DE;
    border-radius: 7px;
    padding: 8px 10px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #243333;
    selection-background-color: #D9F3EE;
    selection-color: #087F73;
}
"""

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()

class ScrcpyGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.settings = QSettings(ORG_NAME, APP_NAME)
        self.process = None
        self.log_handle = None
        self.restoring = False

        self.sndcpy = SndcpyManager(
            adb_path=ADB_PATH,
            runtime_dir=RUNTIME_DIR,
            parent=self,
        )

        self.setWindowTitle("OmniMirror")
        self.resize(1200, 860)
        self.setMinimumSize(900, 650)

        logo_path = Path(__file__).resolve().parent / "assets" / "omnimirror-logo.png"

        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))
        

        self.build_ui()
        self.restore_settings()
        self.connect_autosave()

        self.timer = QTimer(self)
        self.timer.setInterval(700)
        self.timer.timeout.connect(self.check_process)

        QTimer.singleShot(250, self.refresh_devices)
        
        self.device_refresh_timer = QTimer(self)
        self.device_refresh_timer.setInterval(6000)
        self.device_refresh_timer.timeout.connect(self.refresh_devices)
        self.device_refresh_timer.start()


    # --------------------------------------------------------
    # REUSABLE UI HELPERS
    # --------------------------------------------------------

    def panel(self, title):
        frame = QFrame()
        frame.setObjectName("Panel")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(17, 15, 17, 15)
        layout.setSpacing(12)

        label = QLabel(title)
        label.setObjectName("Section")
        layout.addWidget(label)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        layout.addLayout(form)
        return frame, form, layout

    def scroll_page(self):
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(8, 10, 8, 8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(2, 2, 8, 10)
        content_layout.setSpacing(14)

        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        return page, content_layout

    def combo(self, form, label, options, default=None):
        widget = NoScrollComboBox()
        widget.addItems(options)
        if default is not None:
            widget.setCurrentText(default)
        form.addRow(label, widget)
        return widget

    def line(self, form, label, placeholder=""):
        widget = QLineEdit()
        widget.setPlaceholderText(placeholder)
        form.addRow(label, widget)
        return widget

    def check(self, form, label, tooltip=""):
        widget = QCheckBox(label)
        if tooltip:
            widget.setToolTip(tooltip)
        form.addRow(widget)
        return widget

    # --------------------------------------------------------
    # MAIN WINDOW
    # --------------------------------------------------------

    
    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(22, 18, 22, 18)
        outer.setSpacing(14)

        
        # Header
        header = QHBoxLayout()
        header.setSpacing(12)

        # App logo
        logo_label = QLabel()
        logo_label.setFixedSize(54, 54)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet(
            "background: transparent; border: none; padding: 0;"
        )

        logo_path = Path(__file__).resolve().parent / "assets" / "omnimirror-logo.png"

        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            logo_label.setPixmap(
                pixmap.scaled(
                    54,
                    54,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            logo_label.setText("OM")
            logo_label.setStyleSheet(
                "background: #D9F3EE; color: #0D9488;"
                "font-size: 18px; font-weight: 700;"
                "border-radius: 12px;"
            )

        header.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        # App name and subtitle
        heading = QVBoxLayout()
        heading.setSpacing(3)

        brand = QLabel("OmniMirror")
        brand.setObjectName("Brand")
        heading.addWidget(brand)

        subtitle = QLabel("Cast Your Phone")
        subtitle.setObjectName("Muted")
        heading.addWidget(subtitle)

        header.addLayout(heading)
        header.addStretch()

        developer_label = QLabel("Developed by Md. Arfan Ahmed")
        developer_label.setObjectName("Muted")
        header.addWidget(
            developer_label, 0, Qt.AlignmentFlag.AlignVCenter
        )

        version_label = QLabel("Powered by scrcpy 5.0.1")
        version_label.setObjectName("Muted")
        header.addWidget(
            version_label, 0, Qt.AlignmentFlag.AlignVCenter
        )

        outer.addLayout(header)


        # Device connection panel
        device_panel, _, device_layout = self.panel(
            "DEVICE CONNECTION"
        )

        device_row = QHBoxLayout()
        device_row.setSpacing(8)

        self.device_combo = QComboBox()
        self.device_combo.addItem(
            "Searching for devices...", None
        )
        device_row.addWidget(self.device_combo, 1)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(
            self.refresh_devices
        )
        device_row.addWidget(self.refresh_button)

        device_layout.addLayout(device_row)

        wireless_row = QHBoxLayout()
        wireless_row.setSpacing(8)

        self.wireless_pair_button = QPushButton(
            "Pair Wireless Device"
        )
        self.wireless_pair_button.clicked.connect(
            self.pair_wireless_adb
        )
        wireless_row.addWidget(self.wireless_pair_button)

        self.wireless_connect_button = QPushButton(
            "Connect Wireless"
        )
        self.wireless_connect_button.clicked.connect(
            self.connect_wireless_adb
        )
        wireless_row.addWidget(self.wireless_connect_button)

        self.wireless_disconnect_button = QPushButton(
            "Disconnect Wireless"
        )
        self.wireless_disconnect_button.clicked.connect(
            self.disconnect_wireless_adb
        )
        wireless_row.addWidget(self.wireless_disconnect_button)

        device_layout.addLayout(wireless_row)

        self.status = QLabel("Checking connected devices...")
        self.status.setObjectName("Status")
        self.status.setWordWrap(True)
        device_layout.addWidget(self.status)

        outer.addWidget(device_panel)

        # Main settings tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(
            self.create_video_tab(), "Video Display"
        )
        self.tabs.addTab(
            self.create_audio_tab(), "Audio Recording"
        )
        self.tabs.addTab(
            self.create_control_tab(), "Device Control"
        )
        self.tabs.addTab(
            self.create_advanced_tab(), "Advanced"
        )

        outer.addWidget(self.tabs, 1)

        # Bottom actions
        actions = QHBoxLayout()
        actions.setSpacing(8)

        open_log = QPushButton("Open Log")
        open_log.clicked.connect(self.open_log)
        actions.addWidget(open_log)

        reset = QPushButton("Reset Settings")
        reset.clicked.connect(self.reset_settings)
        actions.addWidget(reset)

        actions.addStretch()

        self.start_button = QPushButton("Start Mirroring")
        self.start_button.setObjectName("Primary")
        self.start_button.clicked.connect(
            self.start_mirroring
        )
        actions.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Mirroring")
        self.stop_button.setObjectName("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(
            self.stop_mirroring
        )
        actions.addWidget(self.stop_button)

        outer.addLayout(actions)


    # --------------------------------------------------------
    # VIDEO AND DISPLAY
    # --------------------------------------------------------

    def create_video_tab(self):
        page, content = self.scroll_page()

        frame, form, _ = self.panel("VIDEO QUALITY")

        self.resolution = self.combo(
            form, "Maximum resolution",
            [
                "Device default", "2560 px", "1920 px", "1600 px",
                "1280 px", "1024 px", "800 px", "640 px",
            ],
            "Device default",
        )

        self.fps = self.combo(
            form, "Frame rate",
            [
                "Device default", "120 FPS", "90 FPS", "60 FPS",
                "50 FPS", "30 FPS", "25 FPS", "15 FPS",
            ],
            "Device default",
        )

        self.bitrate = self.combo(
            form, "Video bitrate",
            [
                "Low — 2 Mbps",
                "Balanced — 4 Mbps",
                "High — 8 Mbps",
                "Very High — 12 Mbps",
                "Maximum — 16 Mbps",
            ],
            "High — 8 Mbps",
        )

        self.video_codec = self.combo(
            form, "Video codec",
            [
                "Default (H.264)", "H.264", "H.265 / HEVC",
                "AV1", "VP8", "VP9",
            ],
            "Default (H.264)",
        )

        self.hwdec = self.combo(
            form, "Computer video decoder",
            [
                "Automatic", "Disabled (software)",
                "Direct3D 11 (Windows)",
            ],
            "Automatic",
        )

        self.video_buffer = self.combo(
            form, "Video delay buffer",
            ["Default (0 ms)", "50 ms", "100 ms", "200 ms", "500 ms"],
            "Default (0 ms)",
        )

        self.render_fit = self.combo(
            form, "Fit video to window",
            [
                "Preserve proportions", "Stretch to fill",
                "Pixel size (unscaled)",
            ],
            "Preserve proportions",
        )

        self.orientation = self.combo(
            form, "Display orientation",
            [
                "Device default",
                "Portrait (0°)",
                "Rotate clockwise (90°)",
                "Upside-down (180°)",
                "Rotate counterclockwise (270°)",
            ],
            "Device default",
        )

        content.addWidget(frame)

        frame2, form2, _ = self.panel("WINDOW & DISPLAY")

        self.fullscreen = self.check(form2, "Start fullscreen")
        self.always_on_top = self.check(form2, "Keep window always on top")
        self.borderless = self.check(form2, "Borderless window")
        self.no_aspect_lock = self.check(
            form2, "Allow free window proportions"
        )
        self.disable_screensaver = self.check(
            form2, "Disable computer screensaver while mirroring"
        )

        self.window_title = self.line(
            form2, "Window title", "Optional custom title"
        )
        self.window_x = self.line(
            form2, "Window horizontal position", "Automatic or number"
        )
        self.window_y = self.line(
            form2, "Window vertical position", "Automatic or number"
        )
        self.window_width = self.line(
            form2, "Window width", "Automatic or pixel value"
        )
        self.window_height = self.line(
            form2, "Window height", "Automatic or pixel value"
        )
        self.display_id = self.line(
            form2, "Android display ID", "Default: 0"
        )
        self.crop = self.line(
            form2, "Screen crop", "width:height:x:y (optional)"
        )

        content.addWidget(frame2)
        content.addStretch()
        return page

    # --------------------------------------------------------
    # AUDIO AND RECORDING
    # --------------------------------------------------------

    def create_audio_tab(self):
        page, content = self.scroll_page()

        frame, form, _ = self.panel("AUDIO")

        self.no_audio = self.check(form, "Disable audio forwarding")

        self.audio_codec = self.combo(
            form, "Audio codec",
            ["Default (Opus)", "Opus", "AAC", "FLAC", "Raw"],
            "Default (Opus)",
        )

        self.audio_source = self.combo(
            form, "Audio source",
            [
                "Default device audio",
                "App playback",
                "Microphone",
                "Unprocessed microphone",
                "Camcorder microphone",
                "Voice recognition microphone",
                "Voice communication microphone",
                "Voice call",
                "Voice call uplink",
                "Voice call downlink",
                "Voice performance",
            ],
            "Default device audio",
        )

        self.audio_bitrate = self.combo(
            form, "Audio bitrate",
            ["Default (128 Kbps)", "64 Kbps", "96 Kbps", "128 Kbps",
             "192 Kbps", "256 Kbps"],
            "Default (128 Kbps)",
        )

        self.audio_buffer = self.combo(
            form, "Audio delay buffer",
            ["Default (50 ms)", "100 ms", "200 ms", "300 ms", "500 ms"],
            "Default (50 ms)",
        )

        self.audio_dup = self.check(
            form,
            "Keep audio playing on phone too",
            "Works only with App playback audio source.",
        )

        content.addWidget(frame)

        frame2, form2, _ = self.panel("RECORDING & CLIPBOARD")

        self.recording_path = self.line(
            form2, "Recording file", "Choose an output file"
        )

        browse = QPushButton("Browse...")
        browse.clicked.connect(self.choose_recording_path)
        form2.addRow("Select file", browse)

        self.record_format = self.combo(
            form2, "Recording format",
            [
                "Automatic (from file extension)", "MKV", "MP4",
                "M4A", "MKA", "Opus", "AAC", "FLAC", "WAV",
            ],
            "Automatic (from file extension)",
        )

        self.no_clipboard = self.check(
            form2, "Disable clipboard synchronization"
        )
        self.legacy_paste = self.check(
            form2, "Use legacy clipboard paste"
        )

        content.addWidget(frame2)

        note = QLabel(
            "Audio capture depends on Android version and source. "
            "Some call and microphone sources may be restricted by Android."
        )
        note.setObjectName("Muted")
        note.setWordWrap(True)
        content.addWidget(note)
        content.addStretch()
        return page

    # --------------------------------------------------------
    # DEVICE AND CONTROL
    # --------------------------------------------------------

    def create_control_tab(self):
        page, content = self.scroll_page()

        frame, form, _ = self.panel("PHONE SCREEN & INPUT")

        self.stay_awake = self.check(
            form, "Keep phone awake while connected"
        )
        self.turn_screen_off = self.check(
            form, "Turn phone screen off while mirroring"
        )
        self.no_power_on = self.check(
            form, "Do not turn phone screen on at startup"
        )
        self.power_off_on_close = self.check(
            form, "Turn phone screen off when closing scrcpy"
        )
        self.keep_active = self.check(
            form, "Keep phone active by simulating user activity"
        )
        self.show_touches = self.check(
            form, "Show physical touches on phone"
        )
        self.no_control = self.check(
            form, "Read-only mode (disable phone control)"
        )
        self.no_key_repeat = self.check(
            form, "Disable repeated key events"
        )
        self.raw_key_events = self.check(
            form, "Send raw keyboard events"
        )
        self.prefer_text = self.check(
            form, "Prefer text input for letters and spaces"
        )
        self.no_mouse_hover = self.check(
            form, "Disable mouse hover forwarding"
        )

        content.addWidget(frame)

        frame2, form2, _ = self.panel("KEYBOARD, MOUSE & GAMEPAD")

        self.keyboard_mode = self.combo(
            form2, "Keyboard control",
            [
                "Default", "Disabled", "Android SDK",
                "Physical keyboard (UHID)", "AOA keyboard",
            ],
            "Default",
        )

        self.mouse_mode = self.combo(
            form2, "Mouse control",
            [
                "Default", "Disabled", "Android SDK",
                "Physical mouse (UHID)", "AOA mouse",
            ],
            "Default",
        )

        self.gamepad_mode = self.combo(
            form2, "Gamepad control",
            [
                "Default", "Disabled",
                "Physical gamepad (UHID)", "AOA gamepad",
            ],
            "Default",
        )

        self.shortcut_mod = self.combo(
            form2, "Shortcut modifier",
            [
                "Default (Left Alt / Super)",
                "Left Alt", "Left Ctrl",
                "Left Super", "Right Super",
                "Left Ctrl or Left Super",
            ],
            "Default (Left Alt / Super)",
        )

        content.addWidget(frame2)

        frame3, form3, _ = self.panel("ANDROID APP")

        self.start_app = self.line(
            form3, "Launch app package", "Optional Android package name"
        )
        self.push_target = self.line(
            form3, "File transfer destination",
            "Default: /sdcard/Download/",
        )

        content.addWidget(frame3)
        content.addStretch()
        return page

    # --------------------------------------------------------
    # ADVANCED
    # --------------------------------------------------------

    def create_advanced_tab(self):
        page, content = self.scroll_page()

        frame, form, layout = self.panel("ADVANCED OPTIONS")

        self.verbosity = self.combo(
            form, "Log detail",
            ["Default (Info)", "Verbose", "Debug", "Info", "Warning", "Error"],
            "Default (Info)",
        )

        self.no_cleanup = self.check(
            form, "Do not restore device state on exit"
        )
        self.no_downsize = self.check(
            form, "Disable automatic resolution fallback on encoder errors"
        )
        self.no_video = self.check(form, "Disable video forwarding")
        self.no_window = self.check(
            form, "Do not open a mirroring window"
        )
        self.no_video_playback = self.check(
            form, "Disable computer video playback"
        )
        self.no_audio_playback = self.check(
            form, "Disable computer audio playback"
        )
        self.no_mipmaps = self.check(
            form, "Disable mipmap generation"
        )
        self.flex_display = self.check(
            form, "Resize virtual display to match the window"
        )
        self.require_audio = self.check(
            form, "Fail if audio capture cannot start"
        )
        self.print_fps = self.check(
            form, "Print FPS counter to the log"
        )
        self.force_adb_forward = self.check(
            form, "Force ADB forward connection"
        )

        self.time_limit = self.line(
            form, "Maximum session duration",
            "Seconds; blank means unlimited"
        )
        self.screen_timeout = self.line(
            form, "Phone screen timeout",
            "Seconds; optional"
        )
        self.background_color = self.line(
            form, "Video background color",
            "#222 or #222222"
        )
        self.angle = self.line(
            form, "Video rotation angle",
            "Clockwise degrees; optional"
        )
        self.tcpip_address = self.line(
            form, "TCP/IP device address",
            "Optional IP:port, e.g. 192.168.1.10:5555"
        )

        self.new_display = self.line(
            form, "Create virtual display",
            "Optional: 1920x1080 or 1920x1080/420"
        )

        self.extra_args = self.line(
            form, "Additional scrcpy arguments",
            "Optional advanced options"
        )

        layout.addWidget(QLabel(
            "Only enter options supported by scrcpy 5.0.1. "
            "Avoid repeating an option already configured above."
        ))

        help_button = QPushButton("Show all installed scrcpy options")
        help_button.clicked.connect(self.show_scrcpy_help)
        layout.addWidget(help_button)

        list_layout = QHBoxLayout()

        self.list_displays_button = QPushButton("List displays")
        self.list_displays_button.clicked.connect(
            lambda: self.run_scrcpy_utility("--list-displays")
        )
        list_layout.addWidget(self.list_displays_button)

        self.list_cameras_button = QPushButton("List cameras")
        self.list_cameras_button.clicked.connect(
            lambda: self.run_scrcpy_utility("--list-cameras")
        )
        list_layout.addWidget(self.list_cameras_button)

        self.list_encoders_button = QPushButton("List encoders")
        self.list_encoders_button.clicked.connect(
            lambda: self.run_scrcpy_utility("--list-encoders")
        )
        list_layout.addWidget(self.list_encoders_button)

        layout.addLayout(list_layout)
        content.addWidget(frame)
        content.addStretch()
        return page

    # --------------------------------------------------------
    # SAVE AND RESTORE PREFERENCES
    # --------------------------------------------------------

    def preference_widgets(self):
        result = {}

        for name, value in vars(self).items():
            if name.startswith("_"):
                continue
            if isinstance(value, (QComboBox, QCheckBox, QLineEdit)):
                result[name] = value

        return result

    def restore_settings(self):
        self.restoring = True

        for name, widget in self.preference_widgets().items():
            key = "preferences/" + name

            if not self.settings.contains(key):
                continue

            value = self.settings.value(key)

            if isinstance(widget, QComboBox):
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)

            elif isinstance(widget, QCheckBox):
                widget.setChecked(
                    str(value).lower() in ("true", "1", "yes")
                )

            elif isinstance(widget, QLineEdit):
                widget.setText(str(value))

        self.restoring = False

    def connect_autosave(self):
        for name, widget in self.preference_widgets().items():
            key = "preferences/" + name

            if isinstance(widget, QComboBox):
                widget.currentTextChanged.connect(
                    lambda value, k=key: self.save_value(k, value)
                )
            elif isinstance(widget, QCheckBox):
                widget.toggled.connect(
                    lambda value, k=key: self.save_value(k, value)
                )
            elif isinstance(widget, QLineEdit):
                widget.textChanged.connect(
                    lambda value, k=key: self.save_value(k, value)
                )

    def save_value(self, key, value):
        if self.restoring:
            return
        self.settings.setValue(key, value)
        self.settings.sync()

    def save_settings(self):
        for name, widget in self.preference_widgets().items():
            key = "preferences/" + name

            if isinstance(widget, QComboBox):
                value = widget.currentText()
            elif isinstance(widget, QCheckBox):
                value = widget.isChecked()
            else:
                value = widget.text()

            self.settings.setValue(key, value)

        self.settings.sync()

    def reset_settings(self):
        answer = QMessageBox.question(
            self,
            "Reset settings",
            "Clear saved preferences? Restart the app to reload defaults.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.settings.clear()
        self.settings.sync()

        QMessageBox.information(
            self, "Settings reset",
            "Saved settings cleared. Restart Scrcpy GUI."
        )

    # --------------------------------------------------------
    # DEVICE DETECTION
    # --------------------------------------------------------

    
    
    def refresh_devices(self):
        if not ADB_PATH.is_file():
            self.status.setText(f"ADB not found:\n{ADB_PATH}")
            return

        previous = self.device_combo.currentData()
        self.device_combo.blockSignals(True)

        try:
            result = subprocess.run(
                [str(ADB_PATH), "devices", "-l"],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                ),
            )

            if result.returncode != 0:
                error = result.stderr.strip() or "ADB command failed."
                self.status.setText(error)
                return

            devices = []
            unauthorized = []
            offline = []

            for line in result.stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) < 2:
                    continue

                serial, state = parts[0], parts[1]
                details = " ".join(parts[2:])

                if state == "device":
                    connection = (
                        "Wireless"
                        if serial.startswith("192.168.")
                        or ":" in serial
                        else "USB / ADB"
                    )
                    label = (
                        f"{serial} — {details} [{connection}]"
                        if details
                        else f"{serial} [{connection}]"
                    )
                    devices.append((label, serial))

                elif state == "unauthorized":
                    unauthorized.append(serial)
                elif state == "offline":
                    offline.append(serial)

            # Update only if the device list actually changed.
            current_items = [
                (
                    self.device_combo.itemText(i),
                    self.device_combo.itemData(i),
                )
                for i in range(self.device_combo.count())
            ]

            new_items = (
                [(label, serial) for label, serial in devices]
                if devices
                else [("No authorized device detected", None)]
            )

            if current_items != new_items:
                self.device_combo.clear()

                for label, serial in new_items:
                    self.device_combo.addItem(label, serial)

                index = self.device_combo.findData(previous)
                if index >= 0:
                    self.device_combo.setCurrentIndex(index)

            
            if self.process is not None and self.process.poll() is None:
                # Keep the active mirroring status visible during auto-refresh.
                pass
            elif devices:
                self.status.setText(
                    f"Connected: {len(devices)} device(s) ready."
                )
            elif unauthorized:
                self.status.setText(
                    "Device unauthorized — allow USB debugging on your phone."
                )
            elif offline:
                self.status.setText(
                    "Device offline — reconnect USB or check Wireless debugging."
                )
            else:
                self.status.setText(
                    "Disconnected — connect your phone using USB or Wireless ADB."
                )


        except subprocess.TimeoutExpired:
            self.status.setText("ADB timed out. Try refreshing again.")
        except Exception as exc:
            self.status.setText(f"Device detection failed: {exc}")
        finally:
            self.device_combo.blockSignals(False)





    
    def connect_wireless_adb(self):
        address, ok = QInputDialog.getText(
            self,
            "Connect Wireless Device",
            "Device IP address and port (example: 192.168.1.10:5555):",
        )

        if not ok or not address.strip():
            return

        address = address.strip()

        if any(char.isspace() for char in address):
            QMessageBox.warning(
                self, "Invalid address",
                "Enter the IP address and port without spaces.",
            )
            return

        try:
            result = subprocess.run(
                [str(ADB_PATH), "connect", address],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15,
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                ),
            )

            output = (result.stdout or "").strip()
            error = (result.stderr or "").strip()
            message = output or error or "No response from ADB."

            if result.returncode == 0 and "connected" in message.lower():
                QMessageBox.information(
                    self, "Wireless ADB", message
                )
                self.refresh_devices()
            else:
                QMessageBox.warning(
                    self, "Wireless ADB", message
                )

        except subprocess.TimeoutExpired:
            QMessageBox.warning(
                self, "Wireless ADB",
                "Connection timed out. Check the IP, port and Wi-Fi.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self, "Wireless ADB", str(exc)
            )




    
    def pair_wireless_adb(self):
        pairing_address, ok = QInputDialog.getText(
            self,
            "Pair Wireless Device",
            "Pairing IP address and port\n"
            "Example: 192.168.1.10:37123",
        )
        if not ok or not pairing_address.strip():
            return

        pairing_address = pairing_address.strip()

        if (
            any(char.isspace() for char in pairing_address)
            or ":" not in pairing_address
        ):
            QMessageBox.warning(
                self,
                "Invalid pairing address",
                "Enter the IP address and pairing port.",
            )
            return

        pairing_code, ok = QInputDialog.getText(
            self,
            "Pair Wireless Device",
            "Enter the 6-digit pairing code:",
        )
        if not ok or not pairing_code.strip():
            return

        pairing_code = pairing_code.strip()

        try:
            paired = subprocess.run(
                [
                    str(ADB_PATH),
                    "pair",
                    pairing_address,
                    pairing_code,
                ],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                ),
            )

            output = (
                (paired.stdout or "").strip()
                or (paired.stderr or "").strip()
                or "No output from ADB."
            )

            if paired.returncode != 0 or "successfully paired" not in output.lower():
                QMessageBox.warning(
                    self,
                    "Pairing Failed",
                    output,
                )
                return

            QMessageBox.information(
                self,
                "Pairing Successful",
                output,
            )

            connection_address, ok = QInputDialog.getText(
                self,
                "Connect Wireless Device",
                "Now enter the IP address and CONNECTION port\n"
                "from the main Wireless debugging screen:",
            )

            if not ok or not connection_address.strip():
                return

            connection_address = connection_address.strip()

            if (
                any(char.isspace() for char in connection_address)
                or ":" not in connection_address
            ):
                QMessageBox.warning(
                    self,
                    "Invalid connection address",
                    "Enter the IP address and connection port.",
                )
                return

            connected = subprocess.run(
                [
                    str(ADB_PATH),
                    "connect",
                    connection_address,
                ],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                ),
            )

            connect_output = (
                (connected.stdout or "").strip()
                or (connected.stderr or "").strip()
                or "No output from ADB."
            )

            if (
                connected.returncode == 0
                and (
                    "connected to" in connect_output.lower()
                    or "already connected" in connect_output.lower()
                )
            ):
                QMessageBox.information(
                    self,
                    "Wireless Connected",
                    connect_output,
                )
            else:
                QMessageBox.warning(
                    self,
                    "Connection Failed",
                    connect_output,
                )

            self.refresh_devices()

        except subprocess.TimeoutExpired:
            QMessageBox.warning(
                self,
                "Wireless ADB",
                "ADB timed out. Check the phone and try again.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Wireless ADB",
                str(exc),
            )





    def disconnect_wireless_adb(self):
        serial = self.device_combo.currentData()

        if not serial:
            QMessageBox.warning(
                self, "No device",
                "Select a connected wireless device first.",
            )
            return

        if not (
            serial.startswith("192.168.")
            or ":" in serial
        ):
            QMessageBox.warning(
                self, "USB device selected",
                "Select a wireless device before disconnecting.",
            )
            return

        result = QMessageBox.question(
            self,
            "Disconnect Wireless Device",
            f"Disconnect {serial}?",
        )

        if result != QMessageBox.StandardButton.Yes:
            return

        try:
            completed = subprocess.run(
                [str(ADB_PATH), "disconnect", serial],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=12,
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                ),
            )

            message = (
                (completed.stdout or "").strip()
                or (completed.stderr or "").strip()
                or "ADB disconnect completed."
            )

            if completed.returncode == 0:
                QMessageBox.information(
                    self, "Wireless ADB", message
                )
            else:
                QMessageBox.warning(
                    self, "Wireless ADB", message
                )

            self.refresh_devices()

        except Exception as exc:
            QMessageBox.critical(
                self, "Wireless ADB", str(exc)
            )


    # --------------------------------------------------------
    # BUILD COMMAND USING ONLY DOCUMENTED OPTIONS
    # --------------------------------------------------------

    def build_arguments(self, serial):
        args = [str(SCRCPY_PATH), "-s", serial]

        def add_value(option, value):
            if value is not None and str(value).strip():
                args.append(f"{option}={str(value).strip()}")

        # Resolution
        value = self.resolution.currentText()
        if value != "Device default":
            add_value("--max-size", value.split()[0])

        # FPS
        value = self.fps.currentText()
        if value != "Device default":
            add_value("--max-fps", value.split()[0])

        # Video bitrate
        bitrate_map = {
            "Low — 2 Mbps": "2M",
            "Balanced — 4 Mbps": "4M",
            "High — 8 Mbps": "8M",
            "Very High — 12 Mbps": "12M",
            "Maximum — 16 Mbps": "16M",
        }
        add_value("--video-bit-rate",
                  bitrate_map[self.bitrate.currentText()])

        # Codec
        codec_map = {
            "H.264": "h264",
            "H.265 / HEVC": "h265",
            "AV1": "av1",
            "VP8": "vp8",
            "VP9": "vp9",
        }
        codec = self.video_codec.currentText()
        if codec in codec_map:
            add_value("--video-codec", codec_map[codec])

        # Hardware decoder
        hw_map = {
            "Disabled (software)": "disabled",
            "Direct3D 11 (Windows)": "d3d11va",
        }
        hw = self.hwdec.currentText()
        if hw in hw_map:
            add_value("--hwdec", hw_map[hw])

        # Video buffer
        if self.video_buffer.currentText() != "Default (0 ms)":
            add_value("--video-buffer",
                      self.video_buffer.currentText().split()[0])

        # Render fit
        render_map = {
            "Preserve proportions": "letterbox",
            "Stretch to fill": "stretched",
            "Pixel size (unscaled)": "unscaled",
        }
        add_value("--render-fit",
                  render_map[self.render_fit.currentText()])

        # Orientation
        orientation_map = {
            "Portrait (0°)": "0",
            "Rotate clockwise (90°)": "90",
            "Upside-down (180°)": "180",
            "Rotate counterclockwise (270°)": "270",
        }
        orientation = self.orientation.currentText()
        if orientation in orientation_map:
            add_value("--orientation", orientation_map[orientation])

        # Window flags
        flags = [
            (self.fullscreen, "--fullscreen"),
            (self.always_on_top, "--always-on-top"),
            (self.borderless, "--window-borderless"),
            (self.no_aspect_lock, "--no-window-aspect-ratio-lock"),
            (self.disable_screensaver, "--disable-screensaver"),
            (self.stay_awake, "--stay-awake"),
            (self.turn_screen_off, "--turn-screen-off"),
            (self.no_power_on, "--no-power-on"),
            (self.power_off_on_close, "--power-off-on-close"),
            (self.keep_active, "--keep-active"),
            (self.show_touches, "--show-touches"),
            (self.no_control, "--no-control"),
            (self.no_key_repeat, "--no-key-repeat"),
            (self.raw_key_events, "--raw-key-events"),
            (self.prefer_text, "--prefer-text"),
            (self.no_mouse_hover, "--no-mouse-hover"),
            (self.no_clipboard, "--no-clipboard-autosync"),
            (self.legacy_paste, "--legacy-paste"),
            (self.audio_dup, "--audio-dup"),
            (self.no_cleanup, "--no-cleanup"),
            (self.no_downsize, "--no-downsize-on-error"),
            (self.no_video, "--no-video"),
            (self.no_window, "--no-window"),
            (self.no_video_playback, "--no-video-playback"),
            (self.no_audio_playback, "--no-audio-playback"),
            (self.no_mipmaps, "--no-mipmaps"),
            (self.flex_display, "--flex-display"),
            (self.require_audio, "--require-audio"),
            (self.print_fps, "--print-fps"),
            (self.force_adb_forward, "--force-adb-forward"),
        ]

        for checkbox, option in flags:
            if checkbox.isChecked():
                args.append(option)

        # Window text/geometry
        add_value("--window-title", self.window_title.text())
        add_value("--window-x", self.window_x.text())
        add_value("--window-y", self.window_y.text())
        add_value("--window-width", self.window_width.text())
        add_value("--window-height", self.window_height.text())
        add_value("--display-id", self.display_id.text())
        add_value("--crop", self.crop.text())

        # Audio
        if self.no_audio.isChecked():
            args.append("--no-audio")
        else:
            audio_codec_map = {
                "Opus": "opus",
                "AAC": "aac",
                "FLAC": "flac",
                "Raw": "raw",
            }
            codec = self.audio_codec.currentText()
            if codec in audio_codec_map:
                add_value("--audio-codec", audio_codec_map[codec])

            source_map = {
                "App playback": "playback",
                "Microphone": "mic",
                "Unprocessed microphone": "mic-unprocessed",
                "Camcorder microphone": "mic-camcorder",
                "Voice recognition microphone": "mic-voice-recognition",
                "Voice communication microphone": "mic-voice-communication",
                "Voice call": "voice-call",
                "Voice call uplink": "voice-call-uplink",
                "Voice call downlink": "voice-call-downlink",
                "Voice performance": "voice-performance",
            }
            source = self.audio_source.currentText()
            if source in source_map:
                add_value("--audio-source", source_map[source])

            if self.audio_bitrate.currentText() != "Default (128 Kbps)":
                add_value(
                    "--audio-bit-rate",
                    self.audio_bitrate.currentText().split()[0] + "K"
                )

            if self.audio_buffer.currentText() != "Default (50 ms)":
                add_value(
                    "--audio-buffer",
                    self.audio_buffer.currentText().split()[0]
                )

        # Recording
        recording = self.recording_path.text().strip()
        if recording:
            add_value("--record", recording)

        format_map = {
            "MKV": "mkv", "MP4": "mp4", "M4A": "m4a",
            "MKA": "mka", "Opus": "opus", "AAC": "aac",
            "FLAC": "flac", "WAV": "wav",
        }
        fmt = self.record_format.currentText()
        if fmt in format_map:
            add_value("--record-format", format_map[fmt])

        # Input modes
        keyboard_map = {
            "Disabled": "disabled",
            "Android SDK": "sdk",
            "Physical keyboard (UHID)": "uhid",
            "AOA keyboard": "aoa",
        }
        keyboard = self.keyboard_mode.currentText()
        if keyboard in keyboard_map:
            add_value("--keyboard", keyboard_map[keyboard])

        mouse_map = {
            "Disabled": "disabled",
            "Android SDK": "sdk",
            "Physical mouse (UHID)": "uhid",
            "AOA mouse": "aoa",
        }
        mouse = self.mouse_mode.currentText()
        if mouse in mouse_map:
            add_value("--mouse", mouse_map[mouse])

        gamepad_map = {
            "Disabled": "disabled",
            "Physical gamepad (UHID)": "uhid",
            "AOA gamepad": "aoa",
        }
        gamepad = self.gamepad_mode.currentText()
        if gamepad in gamepad_map:
            add_value("--gamepad", gamepad_map[gamepad])

        shortcut_map = {
            "Left Alt": "lalt",
            "Left Ctrl": "lctrl",
            "Left Super": "lsuper",
            "Right Super": "rsuper",
            "Left Ctrl or Left Super": "lctrl,lsuper",
        }
        shortcut = self.shortcut_mod.currentText()
        if shortcut in shortcut_map:
            add_value("--shortcut-mod", shortcut_map[shortcut])

        add_value("--start-app", self.start_app.text())
        add_value("--push-target", self.push_target.text())

        # Advanced
        verbosity_map = {
            "Verbose": "verbose",
            "Debug": "debug",
            "Info": "info",
            "Warning": "warn",
            "Error": "error",
        }
        verbosity = self.verbosity.currentText()
        if verbosity in verbosity_map:
            add_value("--verbosity", verbosity_map[verbosity])

        add_value("--time-limit", self.time_limit.text())
        add_value("--screen-off-timeout", self.screen_timeout.text())
        add_value("--background-color", self.background_color.text())
        add_value("--angle", self.angle.text())

        # TCP/IP mode: use scrcpy's own supported connection option.
        tcpip = self.tcpip_address.text().strip()
        if tcpip:
            args = [str(SCRCPY_PATH), f"--tcpip={tcpip}"]

        virtual_display = self.new_display.text().strip()
        if virtual_display:
            add_value("--new-display", virtual_display)

        # Additional arguments are optional; user is responsible for validity.
        extra = self.extra_args.text().strip()
        if extra:
            try:
                args.extend(shlex.split(extra, posix=True))
            except ValueError as exc:
                raise ValueError(
                    f"Cannot parse additional arguments: {exc}"
                ) from exc

        return args

    # --------------------------------------------------------
    # START / STOP
    # --------------------------------------------------------

    def start_mirroring(self):
        if not SCRCPY_PATH.is_file():
            QMessageBox.critical(
                self, "scrcpy not found", str(SCRCPY_PATH)
            )
            return

        serial = self.device_combo.currentData()
        if not serial:
            QMessageBox.warning(
                self, "No device",
                "Refresh devices and select an authorized device."
            )
            return

        if self.process is not None and self.process.poll() is None:
            QMessageBox.information(
                self, "Already running", "Mirroring is already running."
            )
            return

        try:
            self.save_settings()
            api_level = self.sndcpy.get_android_api(serial)

            # Android 10 = API 29
            use_sndcpy = api_level == 29 and not self.no_audio.isChecked()
            if use_sndcpy:
                QMessageBox.information(
                self,
                "Android 10 Audio Tip",
                "Android 10 only:\n\n"
                "To hear audio on your PC without sound coming "
                "from your phone speaker, set your phone's "
                "media volume to 0.\n\n"
                "Keep OmniMirror audio forwarding enabled."
                )

            if api_level < 29 and not self.no_audio.isChecked():
                QMessageBox.information(
                            self,
                "Audio limitation",
                "sndcpy Android 10 বা তার পরের সমর্থিত সংস্করণের জন্য। "
                "এই ডিভাইসে screen mirroring চলবে, তবে audio forwarding নাও চলতে পারে.",
                )
            args = self.build_arguments(serial)
            if use_sndcpy and "--no-audio" not in args:
                args.append("--no-audio")

            self.close_log()
            self.log_handle = LOG_PATH.open(
                "w", encoding="utf-8", errors="replace"
            )
            self.log_handle.write(
                "Command: " + subprocess.list2cmdline(args) + "\n\n"
            )
            self.log_handle.flush()

            self.process = subprocess.Popen(
                args,
                cwd=str(RUNTIME_DIR),
                stdin=subprocess.DEVNULL,
                stdout=self.log_handle,
                stderr=subprocess.STDOUT,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )

            if use_sndcpy:
                try:
                    preferred_vlc = (
                    self.settings.value("preferences/vlc_path", "", type=str)
                    )
                    self.sndcpy.start(serial, preferred_vlc)
                    self.settings.setValue(
                    "preferences/vlc_path",
                    self.sndcpy.vlc_path,
                    )
                except Exception as exc:
                    self.sndcpy.stop()
                    QMessageBox.warning(
                        self,
                        "Android 10 audio unavailable",
                        f"Screen mirroring started, but sndcpy could not start.\n\n{exc}",
                    )

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status.setText(f"Starting mirroring: {serial}")

            self.timer.start()
            QTimer.singleShot(1500, self.check_process)

        except Exception as exc:
            self.close_log()
            QMessageBox.critical(self, "Could not start scrcpy", str(exc))
            self.status.setText(f"Could not start scrcpy: {exc}")

    def check_process(self):
        if self.process is None:
            self.timer.stop()
            return

        code = self.process.poll()
        if code is None:
            return

        self.timer.stop()
        self.process = None
        self.sndcpy.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.close_log()

        try:
            log = LOG_PATH.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            log = ""

        if code == 0:
            self.status.setText("Mirroring session closed.")
        else:
            tail = "\n".join(log.splitlines()[-14:])
            self.status.setText(f"scrcpy exited with code {code}.")
            QMessageBox.warning(
                self, "scrcpy error",
                f"Exit code: {code}\n\nLog: {LOG_PATH}\n\n"
                f"{tail or 'No output captured.'}"
            )

    def stop_mirroring(self):
        process = self.process

        if process is None or process.poll() is not None:
            self.process = None
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.close_log()
            self.status.setText("No active mirroring process.")
            return

        try:
            process.terminate()
            try:
                process.wait(timeout=4)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
            self.status.setText("Mirroring stopped.")
        except Exception as exc:
            QMessageBox.warning(self, "Stop failed", str(exc))
        finally:
            self.sndcpy.stop()
            self.process = None
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.close_log()

    # --------------------------------------------------------
    # UTILITIES
    # --------------------------------------------------------

    def choose_recording_path(self):
        videos = Path.home() / "Videos"
        videos.mkdir(parents=True, exist_ok=True)

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Choose recording file",
            str(videos / "phone-recording.mkv"),
            "MKV video (*.mkv);;MP4 video (*.mp4);;"
            "M4A audio (*.m4a);;All files (*)",
        )
        if path:
            self.recording_path.setText(path)

    def show_scrcpy_help(self):
        try:
            result = subprocess.run(
                [str(SCRCPY_PATH), "--help"],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                timeout=15,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            text = result.stdout or result.stderr or "No help output."

            dialog = QMessageBox(self)
            dialog.setWindowTitle("scrcpy 5.0.1 options")
            dialog.setText(
                "Supported options from the installed scrcpy version:"
            )
            dialog.setDetailedText(text)
            dialog.exec()
        except Exception as exc:
            QMessageBox.warning(self, "Help unavailable", str(exc))

    def run_scrcpy_utility(self, option):
        try:
            result = subprocess.run(
                [str(SCRCPY_PATH), option],
                cwd=str(RUNTIME_DIR),
                capture_output=True,
                text=True,
                timeout=20,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            output = result.stdout or result.stderr or "No output."

            dialog = QMessageBox(self)
            dialog.setWindowTitle(option)
            dialog.setText(output[:3000])
            dialog.setDetailedText(output)
            dialog.exec()
        except Exception as exc:
            QMessageBox.warning(self, "Command failed", str(exc))

    def open_log(self):
        if not LOG_PATH.exists():
            QMessageBox.information(
                self, "No log",
                "Start mirroring first to create a log."
            )
            return
        try:
            os.startfile(str(LOG_PATH))
        except Exception as exc:
            QMessageBox.warning(
                self, "Could not open log",
                f"{exc}\n\n{LOG_PATH}"
            )

    def close_log(self):
        if self.log_handle is not None:
            try:
                self.log_handle.flush()
                self.log_handle.close()
            except Exception:
                pass
            self.log_handle = None

    def closeEvent(self, event):
        self.save_settings()

        if self.process is not None and self.process.poll() is None:
            answer = QMessageBox.question(
                self,
                "Close Scrcpy GUI",
                "Stop mirroring and close the application?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            self.stop_mirroring()

        self.sndcpy.stop()
        self.close_log()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    app.setOrganizationName(ORG_NAME)
    app.setApplicationName(APP_NAME)

    if not RUNTIME_DIR.is_dir():
        QMessageBox.critical(
            None, "Runtime not found",
            f"Runtime folder not found:\n{RUNTIME_DIR}"
        )
        return

    window = ScrcpyGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
