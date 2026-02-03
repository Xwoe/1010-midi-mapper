"""
Launcher script for the bundled Streamlit app.
This is the entry point for the PyInstaller executable.
"""
import sys
import os
from streamlit.web import cli as stcli

def main():
    # Get the directory of the executable
    if getattr(sys, 'frozen', False):
        # Running as compiled
        application_path = sys._MEIPASS
    else:
        # Running in normal Python
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the application directory
    os.chdir(application_path)
    
    # Path to your streamlit app
    streamlit_script = os.path.join(application_path, 'streamlit_midi_mapper.py')
    
    # Run streamlit
    sys.argv = [
        "streamlit",
        "run",
        streamlit_script,
        "--server.headless=true",
        "--server.port=8501",
        "--browser.serverAddress=localhost",
    ]
    
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()
