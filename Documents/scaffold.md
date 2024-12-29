# ModelGUI - AI Model Execution GUI

## Project Overview

ModelGUI is a modern, cross-platform desktop application designed to simplify the execution of AI models, specifically YOLO models, on images or directories of images. It provides an intuitive graphical user interface (GUI) with advanced features for model selection, batch processing, and result analysis. The application aims to make AI model testing and evaluation accessible to users of all technical levels.

## Features Implemented

### Core Features
- Multiple model support (YOLOv8 nano and small)
- Single file and batch processing
- Timestamped results
- Progress tracking
- Detailed logging

### Detection Options
- Save Labels (YOLO format txt)
- Save Confidence scores
- Save Cropped detections
- Generate Analysis Plots
  - Confidence distribution
  - Class distribution
  - Confusion matrix
- Hide/Show Labels
- Hide/Show Confidence

### User Interface
- Modern dark theme
- Color-coded action buttons
  - Blue (#2b5797) for standard actions
  - Red (#8a2d2d) for destructive actions
  - Green (#1e7145) for primary actions
- Integrated console output
- Progress bar with status updates
- Auto-open results option

## Technology Stack

- **Programming Language:** Python 3.8+
- **GUI Framework:** PyQt5
- **AI/ML Library:** Ultralytics YOLO
- **Additional Libraries:**
  - matplotlib (plotting)
  - pandas (data analysis)
  - Pillow (image handling)
  - requests (downloading assets)

## File Structure
```
modelgui/
├── main.py              # Main application and GUI
├── download_assets.py   # Asset downloader
├── requirements.txt     # Dependencies
├── scripts/            
│   ├── setup.py        # Setup script
│   └── yologui.bat     # Windows launcher
├── models/             # YOLO models
├── sample_images/      # Example images
└── results/            # Detection results
    └── detection_YYYYMMDD_HHMMSS/
        ├── labels/     # YOLO format files
        ├── crops/      # Detected objects
        └── plots/      # Analysis plots
```

## Module Descriptions

### `main.py`
- Main application window (ModelGUI class)
- GUI layout and styling
- File handling logic
- Model execution
- Results processing
- Plot generation

### `download_assets.py`
- Downloads YOLO models
  - yolov8n.pt (nano)
  - yolov8s.pt (small)
- Downloads sample images
- Creates necessary directories

### `scripts/setup.py`
- Cross-platform setup
- Virtual environment creation
- Dependency installation
- Asset downloading

### `scripts/yologui.bat`
- Windows launcher script
- Environment activation
- Application startup

## UI Layout

The application follows a vertical layout:
```
+-------------------------------------------+
|              ModelGUI                      |
+-------------------------------------------+
| Model:                                     |
| yolov8s.pt                                |
| [model path textbox          ] [Browse...] |
| Path: models/yolov8s.pt                   |
|                                           |
| [Add Files] [Add Folder]          [Clear] |
| +---------------------------------------+ |
| |           File List                   | |
| |                                       | |
| +---------------------------------------+ |
|                                           |
| Detection Options:                        |
| [✓] Save Labels (txt)  [✓] Save Confidence|
| [✓] Save Plots        [✓] Hide Labels    |
| [✓] Save Crops        [✓] Hide Confidence|
|                                           |
| Console Output:                           |
| +---------------------------------------+ |
| | > Loading model: yolov8s.pt          | |
| | > Processing: image_003.jpg          | |
| +---------------------------------------+ |
|                                           |
| [Progress Bar ===================>] 95%    |
| Ready                                     |
|                                           |
|            [Run Detection]                |
|            [✓] Auto-open Results         |
+-------------------------------------------+
```

## Implementation Details

### Model Management
- Models stored in `models/` directory
- Automatic download during setup
- Model path tracking
- Support for custom models

### File Handling
- Support for multiple image formats
- Recursive directory scanning
- Duplicate prevention
- Clear all functionality

### Results Organization
- Timestamped output folders
- Separate directories for:
  - Labeled images
  - YOLO format txt files
  - Cropped detections
  - Analysis plots

### Error Handling
- Input validation
- Model loading checks
- File access verification
- Graceful error reporting

## Future Enhancements
- Video processing support
- Real-time detection preview
- Custom model training interface
- Result comparison tools
- Export functionality
- Settings persistence