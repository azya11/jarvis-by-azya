#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR=$(pwd)
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
# We use -m src.main to run it as a module
MAIN_CMD="-m src.main"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/jarvis.desktop"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found. Please run 'python3 -m venv venv' and install requirements first."
    exit 1
fi

# Create autostart directory if it doesn't exist
mkdir -p "$AUTOSTART_DIR"

# Create the .desktop file
cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Type=Application
Name=Jarvis Voice Assistant
Comment=AI Voice Assistant
Exec=$PROJECT_DIR/run.sh
Path=$PROJECT_DIR
Terminal=false
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOL

echo "Autostart entry created at $DESKTOP_FILE"
echo "The assistant will now start automatically when you log in."
