# ModelGUI

A simple GUI application for running YOLO object detection models on images or folders.

## Features
- Select and run YOLO models through an intuitive interface
- Process single images or entire folders
- View results with automatic folder opening
- Timestamped results for easy tracking

## Requirements
- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/modelgui.git
   cd modelgui
   ```

2. Run the setup script:
   ```bash
   python scripts/setup.py
   ```

   This will:
   - Create a virtual environment
   - Install required packages
   - Download the YOLO model
   - Download sample images

3. Run the application:

   **Windows:**
   ```bash
   venv\Scripts\python main.py
   ```

   **macOS/Linux:**
   ```bash
   venv/bin/python main.py
   ```

## Usage
1. Select a model from the dropdown menu
2. Choose an image or folder using the respective buttons
3. Click "Run Detection" to process
4. Results will be saved in the `results` folder with timestamps
5. The results folder will open automatically when complete

## Project Structure
```
modelgui/
├── main.py              # Main application
├── download_assets.py   # Downloads models and sample images
├── requirements.txt     # Python dependencies
├── scripts/            # Setup scripts
│   └── setup.py        # Cross-platform setup script
├── models/             # YOLO model storage
├── sample_images/      # Example images
└── results/            # Detection results (timestamped)
```

## Notes
- Results are saved in timestamped folders for easy tracking
- Models and sample images are downloaded during setup
- The virtual environment isolates dependencies

## Contributing
Feel free to open issues or submit pull requests for improvements!
