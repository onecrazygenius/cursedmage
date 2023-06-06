# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(['app/main.py'],
             pathex=[os.getcwd()],
             datas=[
                ('./app', 'app'),
             ],
             hiddenimports=['configparser', 'pygame'])

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          console=False,
          uac_admin=True,
          name='CursedMage',
          icon='app/assets/images/team_logo.ico')