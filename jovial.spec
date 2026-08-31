# -*- mode: python ; coding: utf-8 -*-

"""Shared PyInstaller definition for the Windows and Linux executables."""


analysis = Analysis(
    ["src/Jovial_Assembler.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        (
            "src/fonts/hdad-dotrice-1.001/dotrice-condensed.ttf",
            "fonts/hdad-dotrice-1.001",
        )
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(analysis.pure)

executable = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="jovial",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
