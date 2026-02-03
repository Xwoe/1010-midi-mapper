# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect Streamlit data files
streamlit_datas = collect_data_files('streamlit')
streamlit_submodules = collect_submodules('streamlit')

# Collect other necessary data files
altair_datas = collect_data_files('altair')
validators_datas = collect_data_files('validators')

# Your app's data files - add any additional files your app needs
added_files = [
    ('models.py', '.'),
    ('midi_mapper.py', '.'),
    ('mod_source_list.py', '.'),
    ('tenten_zip_utils.py', '.'),
]

block_cipher = None

a = Analysis(
    ['streamlit_midi_mapper.py'],
    pathex=[],
    binaries=[],
    datas=streamlit_datas + altair_datas + validators_datas + added_files,
    hiddenimports=[
        'streamlit',
        'streamlit.web',
        'streamlit.web.cli',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'lxml',
        'lxml.etree',
        'xmltodict',
        'pydantic',
        'pydantic_core',
        'altair',
        'validators',
        'watchdog',
        'tornado',
        'click',
        'tenacity',
        'pillow',
        'pyarrow',
        'pympler',
        'tzdata',
    ] + streamlit_submodules,
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
    [],
    exclude_binaries=True,
    name='MidiMapper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console window for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MidiMapper',
)

# For macOS app bundle (optional)
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='MidiMapper.app',
        icon=None,
        bundle_identifier='com.xwoe.midimapper',
    )
