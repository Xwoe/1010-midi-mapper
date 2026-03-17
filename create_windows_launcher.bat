@echo off
REM Windows launcher for Streamlit MidiMapper

setlocal enabledelayedexpansion

echo ==========================================
echo MidiMapper Launcher
echo ==========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv\" (
    echo First launch - setting up environment...
    echo This may take a minute...
    echo.
    
    REM Create virtual environment
    python -m venv venv
    
    REM Activate and install dependencies
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    echo.
    echo Setup complete!
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Launch Streamlit
echo Starting MidiMapper...
echo Your browser will open automatically.
echo Close this window to stop the application.
echo.

streamlit run streamlit_midi_mapper.py ^
    --server.headless=true ^
    --server.port=8501 ^
    --browser.gatherUsageStats=false

pause
