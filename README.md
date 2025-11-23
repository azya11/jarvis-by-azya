# AI Voice Assistant (Jarvis)

This is a Python-based AI voice assistant designed to run on Ubuntu.

## Prerequisites

You need to install some system dependencies for audio handling.

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv portaudio19-dev espeak
```

## Installation

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the assistant manually:
```bash
source venv/bin/activate
python src/main.py
```

## Autostart on Ubuntu

To make the assistant start automatically when you log in, run the setup script:

```bash
chmod +x setup_autostart.sh
./setup_autostart.sh
```

This will create a `.desktop` entry in `~/.config/autostart/`.
