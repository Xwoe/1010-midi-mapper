#!/bin/bash
# Create a macOS .app bundle for the Streamlit MidiMapper

set -e

APP_NAME="MidiMapper"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

echo "=========================================="
echo "Creating ${APP_NAME}.app bundle"
echo "=========================================="

# Clean up old app if exists
if [ -d "$APP_DIR" ]; then
    echo "Removing old ${APP_DIR}..."
    rm -rf "$APP_DIR"
fi

# Create app bundle structure
echo "Creating app bundle structure..."
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Copy all Python files to Resources
echo "Copying application files..."
cp streamlit_midi_mapper.py "$RESOURCES_DIR/"
cp midi_mapper.py "$RESOURCES_DIR/"
cp models.py "$RESOURCES_DIR/"
cp mod_source_list.py "$RESOURCES_DIR/"
cp tenten_zip_utils.py "$RESOURCES_DIR/"
cp requirements.txt "$RESOURCES_DIR/"

# Create the launcher script
echo "Creating launcher script..."
cat > "$MACOS_DIR/MidiMapper" << 'LAUNCHER_EOF'
#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$SCRIPT_DIR/../Resources"

# Change to resources directory
cd "$RESOURCES_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "First launch - setting up environment..."
    echo "This may take a minute..."
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "Setup complete!"
fi

# Use the virtual environment's Python and Streamlit directly
PYTHON_BIN="$RESOURCES_DIR/venv/bin/python3"
STREAMLIT_BIN="$RESOURCES_DIR/venv/bin/streamlit"

# Launch Streamlit
echo "Starting MidiMapper..."
echo "Your browser will open automatically."
echo "Close this window to stop the application."

"$STREAMLIT_BIN" run streamlit_midi_mapper.py \
    --server.headless=true \
    --server.port=8501 \
    --browser.gatherUsageStats=false
LAUNCHER_EOF

# Make launcher executable
chmod +x "$MACOS_DIR/MidiMapper"

# Create Info.plist
echo "Creating Info.plist..."
cat > "$CONTENTS_DIR/Info.plist" << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MidiMapper</string>
    <key>CFBundleIdentifier</key>
    <string>com.xwoe.midimapper</string>
    <key>CFBundleName</key>
    <string>MidiMapper</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
PLIST_EOF

echo ""
echo "=========================================="
echo "✅ ${APP_NAME}.app created successfully!"
echo "=========================================="
echo ""
echo "To run:"
echo "  1. Double-click ${APP_NAME}.app"
echo "  2. Or from terminal: open ${APP_NAME}.app"
echo ""
echo "First launch will take 1-2 minutes to install dependencies."
echo "Subsequent launches will be much faster."
echo ""
echo "To distribute:"
echo "  - Zip the entire ${APP_NAME}.app folder"
echo "  - Recipients will need Python 3 installed on macOS"
echo ""
