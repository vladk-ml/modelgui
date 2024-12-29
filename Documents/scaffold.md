# ModelGUI - AI Model Execution GUI

## Project Overview

ModelGUI is a cross-platform desktop application designed to simplify the execution of AI models, specifically YOLO models, on images or directories of images. It provides an intuitive graphical user interface (GUI) for selecting a pre-trained model, selecting an input image or folder, running the model, and viewing the results. This tool aims to replace manual command-line interactions, making it easier and faster to test and evaluate AI models.

## Target Audience

This scaffold is intended for a large language model (LLM) that will generate the code for the ModelGUI application. The LLM should have proficiency in Python, PyQt, and ideally, experience with AI model libraries like Ultralytics YOLO.

## Technology Stack

*   **Programming Language:** Python 3.x
*   **GUI Framework:** PyQt5 (or PySide2 as an alternative)
*   **AI/ML Library:** Ultralytics YOLO (for model handling)
*   **Other Libraries:**
    *   `os`, `subprocess` (for file system operations and running processes)
    *   `configparser` (optional, for saving user settings)
    *   `PIL` or `OpenCV` (optional, for image display if you want that capability later)

## File Structure
Use code with caution.
Markdown
modelgui/
├── main.py # Main application entry point
├── gui/ # GUI-related modules
│ └── gui_app.py # Main GUI application window and logic
├── model/ # AI model management
│ └── model_manager.py # Model loading, execution, and processing logic
├── utils/ # Utility functions (optional)
│ └── file_utils.py # File operations (e.g., selecting output directory)
├── config.ini # Configuration file (optional, for storing settings)
├── outputs/ # Default output directory (created on first run)
└── README.md # Project documentation (this file)

## Module Descriptions

### `main.py`

*   **Purpose:** The entry point of the application.
*   **Responsibilities:**
    *   Initializes the `ModelManager` from `model/model_manager.py`.
    *   Creates an instance of the `QApplication`.
    *   Creates the main application window (`ModelGUIMainWindow`) from `gui/gui_app.py`.
    *   Starts the Qt event loop.

### `gui/gui_app.py`

*   **Purpose:** Defines the main application window and GUI logic.
*   **Class:** `ModelGUIMainWindow` (inherits from `QMainWindow`).
*   **Responsibilities:**
    *   Creates the UI layout (see UI Layout section).
    *   Handles user interactions (button clicks, selections, etc.).
    *   Interacts with `ModelManager` to load and run models.
    *   Updates the UI with progress and status information.
    *   Implements error handling and user feedback.

### `model/model_manager.py`

*   **Purpose:** Handles AI model loading, execution, and result processing.
*   **Class:** `ModelManager`.
*   **Responsibilities:**
    *   Loads YOLO models using the `ultralytics` library.
    *   Manages multiple models (if applicable).
    *   Provides functions to run the selected model on an image or folder of images.
    *   Handles the execution of the YOLO model (either directly through the library's API or via `subprocess` to emulate command-line usage).
    *   Processes the output of the YOLO model.

### `utils/file_utils.py` (Optional)

*   **Purpose:** Provides utility functions for file operations.
*   **Responsibilities:**
    *   Opening the output directory in the file explorer/finder.
    *   Any other file or directory related helper functions you might need.

### `config.ini` (Optional)

*   **Purpose:** Stores user settings persistently.
*   **Format:** Standard INI file format.
*   **Content:**
    *   Selected model
    *   Output directory
    *   Other user-adjustable parameters (if any)

## UI Layout

The UI layout should follow the mockup described below:
Use code with caution.
+-------------------------------------------------------------------+
| ModelGUI - [Model: yolov8n (default)] |
+-------------------------------------------------------------------+
| +-----------------------------------------+ +-------------------+ |
| | Model Selection: | | Input: | |
| | [Dropdown: yolov8n (default) ] v | | [Select Image] | |
| | | | [Select Folder] | |
| +-----------------------------------------+ +-------------------+ |
| |
| Progress: |
| [============================>__________] 60% |
| Processing: image_003.jpg |
| Status: Running inference... |
| |
| +----------------------------------------------------------------+ |
| | [ Run ] | [View Results (disabled)] | |
| +----------------------------------------------------------------+ |
+-------------------------------------------------------------------+

**Widget Choices:**

*   **Main Window:** `QMainWindow`
*   **Model Selection:** `QComboBox`
*   **Input Selection:** `QPushButton` (for "Select Image" and "Select Folder") with `QFileDialog`
*   **Progress Area:** `QProgressBar` and `QLabel` (or `QTextEdit` for detailed logs)
*   **Run/View Results:** `QPushButton`

## Coding Practices

*   **Language:** Python 3.7 or higher.
*   **Style:** Follow PEP 8 guidelines for code style (use a linter like `flake8` or `pylint`).
*   **Comments:** Write clear and concise comments explaining the purpose of functions, classes, and complex logic.
*   **Error Handling:** Implement robust error handling throughout the application. Display informative error messages to the user using `QMessageBox` or the status label.
*   **Modularity:** Maintain a modular design, separating GUI logic, model management, and file operations into different modules.
*   **Asynchronous Execution (Optional but Recommended):** Use Python's `threading` or `asyncio` to run model execution in a separate thread. This will prevent the UI from freezing during processing. Use signals and slots to update the GUI from the worker thread.
*   **Object-Oriented:** Use object-oriented principles, encapsulating data and behavior within classes.
*   **Virtual Environments:** The project should be developed within a virtual environment to manage dependencies cleanly. Provide clear instructions in the README for setting up the environment.

## AI Model Integration (YOLO)

*   The application should be primarily designed to work with YOLO models from the `ultralytics` library.
*   The `ModelManager` should handle the loading of pre-trained YOLO models.
*   The user should be able to select a model from a list of available models (either through the GUI or a configuration file).
*   The application should provide functions to run the selected model on either a single image or a directory of images.
*   The output of the YOLO model (processed images with bounding boxes, etc.) should be saved to an output directory.
*   The user should be able to open the output directory from within the application.

## Additional Features (Optional)

*   **Configuration File:** Implement a `config.ini` file to save and load user settings, including the selected model, output directory, and other parameters.
*   **Progress Reporting:** Provide detailed progress information, including the current image being processed, the number of images processed, and any relevant status messages.
*   **Error Handling:** Implement comprehensive error handling and reporting, catching potential issues such as incorrect file paths, model loading failures, and processing errors. Display informative error messages to the user.
*   **Logging:** Consider adding logging functionality to record important events, errors, and debug information. This can be helpful for troubleshooting and understanding the application's behavior.

## Deployment

*   The application should be packaged as a standalone executable for Windows, macOS, and Linux.
*   Packaging tools like `pyinstaller`, `cx_Freeze`, or `nuitka` can be used.
*   Provide clear instructions in the `README.md` file for building and distributing the application.

## Testing

*   Write unit tests for individual modules (`model_manager.py`, `file_utils.py`, etc.) to ensure their functionality.
*   Perform integration testing to verify that the different parts of the application work together correctly.
*   Test the application on all target platforms (Windows, macOS, Linux) to identify and fix any platform-specific issues.