# PyInstaller Executable Setup for MidiMapper

This folder contains everything needed to create a standalone executable of the MidiMapper Streamlit app.

## Prerequisites

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

## Building the Executable

### On macOS (your current system):

```bash
./build_executable.sh
```

This will create:
- `dist/MidiMapper.app` - Double-clickable macOS app bundle
- Or `dist/MidiMapper/` - Folder with the executable and dependencies

### Manual build (if script doesn't work):

```bash
pyinstaller midi_mapper_launcher.spec
```

### On Windows:

1. Install Python and PyInstaller on Windows
2. Copy your project to Windows
3. Run:
   ```cmd
   python -m PyInstaller midi_mapper_launcher.spec
   ```

This creates `dist\MidiMapper\MidiMapper.exe`

## Running the Executable

### macOS:
- **App Bundle:** `open dist/MidiMapper.app`
- **Or from terminal:** `./dist/MidiMapper/MidiMapper`

### Windows:
- Double-click `dist\MidiMapper\MidiMapper.exe`
- Or run from command prompt

The app will:
1. Start a local Streamlit server
2. Automatically open your default browser to http://localhost:8501
3. Show the console window (useful for debugging)

## Distribution

To share the app:

1. **macOS:** Zip the entire `MidiMapper.app` or `MidiMapper` folder
2. **Windows:** Zip the entire `MidiMapper` folder (includes all DLLs and dependencies)

Recipients just unzip and run the executable.

## File Sizes

Expect the bundled app to be:
- **macOS:** 150-250 MB
- **Windows:** 100-200 MB

This includes Python, Streamlit, and all dependencies.

## Troubleshooting

### Missing modules error:
If you get import errors, add the missing module to `hiddenimports` in the spec file.

### Browser doesn't open:
Manually navigate to http://localhost:8501 in your browser.

### Antivirus warnings:
PyInstaller executables may trigger false positives. You may need to:
- Add an exception in your antivirus
- Code-sign the executable (macOS/Windows)

### Large file size:
To reduce size, you can:
- Use `--onefile` option (slower startup)
- Remove unused dependencies from requirements.txt
- Use `upx` compression (already enabled)

## Notes

- The executable is platform-specific (build on macOS for macOS, Windows for Windows)
- Cross-compilation is very difficult - build on the target platform
- First launch may be slower (10-15 seconds)
- The app still runs a local web server, just bundled
