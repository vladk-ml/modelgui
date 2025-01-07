# Windows Installation Guide for ModelGUI

This guide will help you get started with ModelGUI on Windows.

## Method 1: Direct Executable (Recommended)

1. Download `ModelGUI.exe` from the releases page
2. Place it in a directory of your choice
3. Double-click to run the application

## Method 2: Building from Source

If you want to build from source or contribute to development, follow these steps:

### Prerequisites

1. Install Python 3.12 or later from [python.org](https://www.python.org/downloads/)
2. Install Git from [git-scm.com](https://git-scm.com/download/win)

### Installation Steps

Open PowerShell and run the following commands:

```powershell
# Clone the repository
git clone https://github.com/yourusername/modelgui.git
cd modelgui

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Run the application
python main.py
```

### Building the Executable

To create your own executable:

```powershell
# Install PyInstaller
python -m pip install pyinstaller

# Build the executable
pyinstaller modelgui.spec
```

The executable will be created in the `dist` folder.

## Usage

1. Launch ModelGUI
2. Click "Select Model" to choose your YOLO model file (*.pt)
3. Click "Select Files" to choose images or a folder for detection
4. Use the checkboxes to show/hide labels and confidence scores
5. Click "Run Detection" to process the images

## Troubleshooting

1. If you get a Windows Defender warning, click "More Info" and then "Run Anyway"
2. Make sure your YOLO model file is accessible and not corrupted
3. Ensure you have sufficient disk space for the application

## System Requirements

- Windows 10 or later (64-bit)
- 4GB RAM minimum (8GB recommended)
- DirectX 11 capable graphics card
- 500MB free disk space

For issues or questions, please visit our GitHub repository.
