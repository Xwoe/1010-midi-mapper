# ✅ MidiMapper Standalone App - WORKING!

## Quick Start

### Running on macOS:

**Option 1: Double-click (easiest)**
```
Double-click MidiMapper.app in Finder
```
Note: First launch takes 1-2 minutes to install dependencies.

**Option 2: From terminal (to see output)**
```bash
open MidiMapper.app
```

**Option 3: Direct run (for debugging)**
```bash
./MidiMapper.app/Contents/MacOS/MidiMapper
```

### Your browser should open automatically to http://localhost:8501

If it doesn't, manually open that URL in your browser.

## Rebuilding the App

If you make changes to the Python code:

```bash
./create_mac_app.sh
```

This will create a fresh MidiMapper.app with your updated code.

## Distribution

### For macOS users:

1. Zip the app:
   ```bash
   zip -r MidiMapper.zip MidiMapper.app
   ```

2. Send `MidiMapper.zip` to users

3. Users need:
   - macOS 10.13 or later
   - Python 3.7+ installed (most Macs have this)

### For Windows users:

1. Send them these files in a zip:
   - `create_windows_launcher.bat`
   - All `.py` files
   - `requirements.txt`

2. Users double-click `create_windows_launcher.bat`

3. Users need:
   - Windows 10 or later  
   - Python 3.7+ installed

## Stopping the App

- Close the terminal window that appears
- Or press Ctrl+C in the terminal
- Or kill the process: `lsof -ti:8501 | xargs kill -9`

## Troubleshooting

### Port already in use?
```bash
lsof -ti:8501 | xargs kill -9
```

### App won't start?
Run from terminal to see errors:
```bash
./MidiMapper.app/Contents/MacOS/MidiMapper
```

### Need to reinstall dependencies?
```bash
rm -rf MidiMapper.app/Contents/Resources/venv
open MidiMapper.app  # Will reinstall on launch
```

## Files

- `MidiMapper.app` - The standalone Mac app (WORKING!)
- `create_mac_app.sh` - Script to rebuild the app
- `create_windows_launcher.bat` - Windows launcher
- `APP_CREATION_GUIDE.md` - Detailed documentation

---

**Status: ✅ WORKING** - The app successfully launches and runs Streamlit!
