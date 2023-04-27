# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['./app/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('./app/assets/images', './assets/images'),
        ('./app/assets/music', './assets/music'),
    ],
    hiddenimports=[],
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
    name='CursedMage',
    icon='./app/assets/images/team_logo.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
