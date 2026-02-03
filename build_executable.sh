#!/bin/bash
# Build script for creating PyInstaller executable

set -e  # Exit on error

echo "=========================================="
echo "Building MidiMapper Executable"
echo "=========================================="

# Check if PyInstaller is installed
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Create the spec file with the launcher
echo "Creating PyInstaller spec file..."
cat > midi_mapper_launcher.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect Streamlit data files
streamlit_datas = collect_data_files('streamlit')
streamlit_submodules = collect_submodules('streamlit')

# Collect other necessary data files
altair_datas = collect_data_files('altair', include_py_files=True)

# Your app's data files
added_files = [
    ('models.py', '.'),
    ('midi_mapper.py', '.'),
    ('mod_source_list.py', '.'),
    ('tenten_zip_utils.py', '.'),
    ('streamlit_midi_mapper.py', '.'),
]

block_cipher = None

a = Analysis(
    ['run_streamlit_app.py'],
    pathex=[],
    binaries=[],
    datas=streamlit_datas + altair_datas + added_files,
    hiddenimports=[
        'streamlit',
        'streamlit.web',
        'streamlit.web.cli',
        'streamlit.web.bootstrap',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.scriptrunner.script_runner',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'xmltodict',
        'pydantic',
        'pydantic_core',
        'altair',
        'validators',
        'watchdog',
        'watchdog.observers',
        'watchdog.observers.polling',
        'tornado',
        'tornado.web',
        'click',
        'tenacity',
        'PIL',
        'PIL.Image',
        'pyarrow',
        'pympler',
        'tzdata',
        'cachetools',
        'packaging',
        'typing_extensions',
    ] + streamlit_submodules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'numpy.distutils'],
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
    console=True,
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

# For macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='MidiMapper.app',
        icon=None,
        bundle_identifier='com.xwoe.midimapper',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
        },
    )
EOF

# Build with PyInstaller
echo "Building executable..."
pyinstaller --clean midi_mapper_launcher.spec

echo "=========================================="
echo "Build Complete!"
echo "=========================================="

if [ "$(uname)" = "Darwin" ]; then
    echo "macOS app bundle: dist/MidiMapper.app"
    echo "To run: open dist/MidiMapper.app"
else
    echo "Executable folder: dist/MidiMapper/"
    echo "To run: ./dist/MidiMapper/MidiMapper"
fi

echo ""
echo "Note: The app will open a browser window automatically."
echo "To distribute, zip the entire dist/MidiMapper folder."
