# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('assets', 'assets'),
    ('../scrcpy-runtime', 'scrcpy-runtime'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
    'tkinter',
    'matplotlib',
    'pandas',
    'PyQt5',
    'PyQt6',
    'PySide6.QtQuick',
    'PySide6.QtQml',
    'PySide6.QtPdf',
    'PySide6.QtOpenGL',
    'PySide6.QtOpenGLWidgets',
    'PySide6.QtPdfWidgets',
    'PySide6.QtPdfQuick',
    'PySide6.QtQuickWidgets',
    'PySide6.QtVirtualKeyboard',
    ],
    noarchive=False,
    optimize=0,
)

# Remove Qt translation files to reduce distribution size.
a.datas = [
    item for item in a.datas
    if not (
        len(item) > 0
        and 'translations' in str(item[0]).lower()
    )
]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OmniMirror-Lite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/omnimirror.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OmniMirror-Lite-Optimized',
)
