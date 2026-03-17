# MidiMapper - Standalone App Creation Guide

## ✅ Simple Approach (Recommended)

I've created a **self-contained .app bundle** that's much more reliable than PyInstaller.

### What was created:
- **MidiMapper.app** - Double-clickable macOS application
- **create_windows_launcher.bat** - Windows launcher script

### How it works:
1. First launch: Creates a virtual environment and installs dependencies (1-2 minutes)
2. Future launches: Starts instantly
3. Opens your browser automatically to the Streamlit app
4. App runs in the background

## Running the App

### macOS:
```bash
# Method 1: Double-click MidiMapper.app in Finder

# Method 2: From terminal
open MidiMapper.app

# Method 3: Run directly to see output
./MidiMapper.app/Contents/MacOS/MidiMapper
```

### Windows (when distributed):
1. Copy `create_windows_launcher.bat` and all `.py` files to a folder
2. Copy `requirements.txt` to the same folder  
3. Double-click `create_windows_launcher.bat`

## Debugging

If double-clicking doesn't work, run from terminal to see errors:

```bash
./MidiMapper.app/Contents/MacOS/MidiMapper
```

This will show you any error messages.

## Distribution

### macOS:
```bash
# Create a distributable zip
zip -r MidiMapper.zip MidiMapper.app

# Recipients need:
# - macOS 10.13 or later
# - Python 3.7+ installed
```

### Windows:
Zip these files together:
- `create_windows_launcher.bat`
- `streamlit_midi_mapper.py`
- `midi_mapper.py`
- `models.py`
- `mod_source_list.py`
- `tenten_zip_utils.py`
- `requirements.txt`

Recipients need Python 3.7+ installed.

## Advantages over PyInstaller:

✅ More reliable - no hidden import issues  
✅ Smaller size - reuses system Python  
✅ Easier to debug - can see actual errors  
✅ Easier to update - just replace .py files  
✅ No antivirus false positives  

## Disadvantages:

❌ Requires Python 3 installed on user's system  
❌ First launch is slower (installs dependencies)  
❌ Not a true "standalone" executable  

## True Standalone Alternative (Advanced)

If you need a truly standalone executable without Python requirement, you can:

1. **Use Docker** - Package as a container
2. **Use py2app** - macOS native packaging (complex)
3. **Hire a developer** - Create a native wrapper in Swift/Electron

For most use cases, the simple .app bundle approach works great!
