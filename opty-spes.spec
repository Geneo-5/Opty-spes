import os

os.chdir("src")

block_cipher = None

a = Analysis(['__init__.py'],
     pathex=[os.getcwd()],
     binaries=None,
     datas=[(os.getcwd()+'/clt', '/clt')],
     hiddenimports=[],
     hookspath=None,
     runtime_hooks=None,
     excludes=None,
     cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='opty-spes',
          icon='build/icon.png',
          debug=False,
          strip=False,
          upx=True,
          console=False)

app = BUNDLE(exe,
         name='opty-spes.app',
         icon='build/appicon.icns',
         bundle_identifier=None)