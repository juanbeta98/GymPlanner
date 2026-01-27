# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gym_planner_app.py'],
    pathex=[],
    binaries=[],
    datas=[('config.py', '.'), ('workouts.py', '.'), ('credentials.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GymPlanner',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GymPlanner',
)
app = BUNDLE(
    coll,
    name='GymPlanner.app',
    icon=None,
    bundle_identifier=None,
)
