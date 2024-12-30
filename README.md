# ModelGUI

A modern, feature-rich GUI application for running YOLO object detection models on images or folders.

## Features
- **Model Management**
  - Support for multiple YOLO models (nano and small included)
  - Large model name display
  - Easy model browsing and selection
  - Model path tracking

- **File Handling**
  - Add individual files or entire folders
  - Support for multiple image formats (jpg, jpeg, png, bmp)
  - Recursive folder scanning
  - Duplicate file prevention
  - Clear file list option

- **Detection Options**
  - Save Labels (txt files with detections)
  - Save Confidence scores
  - Save Cropped detections
  - Generate analysis plots
  - Hide/Show labels and confidence scores
  - Auto-open results option

- **Results & Analysis**
  - Timestamped results folders
  - Detection visualization
  - Confidence distribution plots
  - Class distribution charts
  - Confusion matrices
  - Detailed console output

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
   cd tools
   python setup.py
   ```

   This will:
   - Create a virtual environment
   - Install required packages
   - Download YOLO models (nano and small)
   - Download sample images

3. Run the application:
   ```bash
   yologui.bat    # Ignore for now
   ```
   or manually:
   ```bash
   venv/bin/python main.py    # macOS/Linux/Windows
   ```

## Usage
1. Select a model from the dropdown menu
2. Add images using either:
   - "Add Files" button for individual images
   - "Add Folder" button for entire directories
3. Configure detection options:
   - Choose what to save (labels, crops, plots)
   - Set visualization preferences
   - Enable/disable auto-open results
4. Click "Run Detection" to process
5. View results in the automatically created timestamped folder

## Project Structure
```
modelgui/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── tools/            
│   ├── setup.py        # Cross-platform setup script
│   ├── download_assets.py   # Downloads models and sample images
│   └── yologui.bat     # Windows launcher
├── models/             # YOLO model storage
├── sample_images/      # Example images
└── results/            # Detection results (timestamped)
    └── detection_YYYYMMDD_HHMMSS/
        ├── labels/     # YOLO format detection files
        ├── crops/      # Cropped detections
        └── plots/      # Analysis visualizations
```

## Features in Detail

### Detection Options
- **Save Labels**: Generate YOLO format txt files with detection coordinates
- **Save Confidence**: Include confidence scores in labels
- **Save Crops**: Save individual crops of detected objects
- **Save Plots**: Generate analysis plots
  - Confidence distribution
  - Class distribution
  - Confusion matrix
- **Hide Labels/Confidence**: Control visualization style

### User Interface
- Modern dark theme
- Color-coded buttons for different actions
- Integrated console output
- Progress tracking
- Detailed status updates

## Contributing
Feel free to open issues or submit pull requests for improvements!
