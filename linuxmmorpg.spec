# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
from PyQt6 import QtCore

block_cipher = None

# Find Qt6 plugins directory
qt_plugins_path = Path(QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.PluginsPath))

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[
        # Include Qt platform plugins (critical for GUI rendering)
        (str(qt_plugins_path / 'platforms'), 'PyQt6/Qt6/plugins/platforms'),
        (str(qt_plugins_path / 'platformthemes'), 'PyQt6/Qt6/plugins/platformthemes'),
    ],
    datas=[
        ('install_game_helper.sh', '.'),
        ('install_knight_myko.sh', '.'),
        ('install_silkroad_origin.sh', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='linuxmmorpg',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
