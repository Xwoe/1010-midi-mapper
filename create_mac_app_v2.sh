#!/bin/bash
# macOS app launcher that opens in Terminal

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

# Create the backend script that does the actual work
cat > "$RESOURCES_DIR/run_app.sh" << 'BACKEND_EOF'
#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "         MidiMapper Launcher"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "First launch - setting up environment..."
    echo "This may take 1-2 minutes..."
    echo ""
    
    # Create virtual environment
    python3 -m venv venv
    
    # Install dependencies
    venv/bin/pip install --upgrade pip -q
    venv/bin/pip install -r requirements.txt -q
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
fi

# Use the virtual environment's Streamlit directly
STREAMLIT_BIN="$SCRIPT_DIR/venv/bin/streamlit"

echo "Starting MidiMapper..."
echo "Your browser will open automatically at:"
echo "http://localhost:8501"
echo ""
echo "➡️  Keep this window open while using the app"
echo "➡️  Press Ctrl+C or close this window to stop"
echo ""
echo "=========================================="
echo ""

# Launch Streamlit
"$STREAMLIT_BIN" run streamlit_midi_mapper.py \
    --server.headless=true \
    --server.port=8501 \
    --browser.gatherUsageStats=false

echo ""
echo "MidiMapper stopped."
read -p "Press Enter to close this window..."
BACKEND_EOF

chmod +x "$RESOURCES_DIR/run_app.sh"

# Create the main launcher using AppleScript to open Terminal
cat > "$MACOS_DIR/MidiMapper" << 'LAUNCHER_EOF'
#!/bin/bash

# Get the Resources directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$SCRIPT_DIR/../Resources"

# Use osascript to open Terminal and run the script
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd '$RESOURCES_DIR' && ./run_app.sh"
end tell
EOF
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
    <key>CFBundleDisplayName</key>
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
echo "  2. A Terminal window will open"
echo "  3. Your browser will open automatically"
echo ""
echo "First launch takes 1-2 minutes to install dependencies."
echo "Keep the Terminal window open while using the app!"
echo ""
