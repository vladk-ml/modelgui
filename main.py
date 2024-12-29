import sys
import os
from datetime import datetime
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QFileDialog, QLabel, QComboBox,
                           QProgressBar, QMessageBox, QHBoxLayout, QFrame,
                           QStyle, QSplitter, QListWidget, QCheckBox, QTextEdit,
                           QGridLayout)
from PyQt5.QtCore import Qt, QSettings, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from ultralytics import YOLO
import glob
from PIL import Image
import subprocess

class ModelGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('ModelGUI', 'YOLO')
        self.last_directory = self.settings.value('last_directory', '')
        self.last_model_directory = self.settings.value('last_model_directory', '')
        
        # Initialize labels as class members
        self.model_name_label = None
        self.model_path_label = None
        self.model_combo = None
        self.file_list = None
        self.status_label = None
        self.progress_bar = None
        self.console_output = None
        self.run_btn = None
        self.auto_open = None
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YOLO Model GUI")
        self.setGeometry(100, 100, 1000, 600)
        
        # Set dark theme
        self.setDarkTheme()
        
        # Set window icon
        icon_path = os.path.join('assets', 'icon.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Top section with model selection
        top_frame = QFrame()
        top_frame.setObjectName("topFrame")
        top_layout = QVBoxLayout(top_frame)
        top_layout.setSpacing(15)
        
        # Model selection with path display
        model_label = QLabel("Model:")
        model_label.setFont(QFont("Segoe UI", 12))
        
        # Large model name display
        self.model_name_label = QLabel()
        self.model_name_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.model_name_label.setAlignment(Qt.AlignCenter)
        self.model_name_label.setObjectName("modelNameLabel")
        
        # Model path display
        self.model_path_label = QLabel()
        self.model_path_label.setObjectName("pathLabel")
        
        model_layout = QHBoxLayout()
        self.model_combo = QComboBox()
        self.updateModelList()  # First populate the combo box
        self.model_combo.currentTextChanged.connect(self.updateModelDisplay)  # Then connect the signal
        
        browse_model_btn = QPushButton()
        browse_model_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogStart))
        browse_model_btn.setText("Browse Model")
        browse_model_btn.setFixedWidth(120)
        browse_model_btn.clicked.connect(self.browseModel)
        browse_model_btn.setObjectName("browseModelBtn")
        
        model_layout.addWidget(self.model_combo, stretch=1)
        model_layout.addWidget(browse_model_btn)
        
        top_layout.addWidget(model_label)
        top_layout.addWidget(self.model_name_label)
        top_layout.addLayout(model_layout)
        top_layout.addWidget(self.model_path_label)
        
        # Initialize the display after all widgets are created
        self.updateModelDisplay()
        
        layout.addWidget(top_frame)
        
        # Middle section with file selection
        file_frame = QFrame()
        file_frame.setObjectName("fileFrame")
        
        file_layout = QVBoxLayout(file_frame)
        file_layout.setContentsMargins(10, 10, 10, 10)
        
        # File selection controls
        file_controls = QHBoxLayout()
        
        # Add Files button with icon
        add_files_btn = QPushButton()
        add_files_btn.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        add_files_btn.setText("Add Files")
        add_files_btn.setFixedWidth(120)
        add_files_btn.clicked.connect(self.browseFiles)
        add_files_btn.setObjectName("addFilesBtn")
        
        # Add Folder button with icon
        add_folder_btn = QPushButton()
        add_folder_btn.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        add_folder_btn.setText("Add Folder")
        add_folder_btn.setFixedWidth(120)
        add_folder_btn.clicked.connect(self.browseFolder)
        add_folder_btn.setObjectName("addFolderBtn")
        
        file_controls.addWidget(add_files_btn)
        file_controls.addWidget(add_folder_btn)
        file_controls.addStretch()
        
        # Clear button with icon
        clear_btn = QPushButton()
        clear_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogDiscardButton))
        clear_btn.setText("Clear")
        clear_btn.setFixedWidth(100)
        clear_btn.clicked.connect(self.clearFileList)
        clear_btn.setObjectName("clearBtn")
        file_controls.addWidget(clear_btn)
        
        file_layout.addLayout(file_controls)
        
        # File list widget
        self.file_list = QListWidget()
        self.file_list.setObjectName("fileList")
        file_layout.addWidget(self.file_list)
        
        layout.addWidget(file_frame)
        
        # Options section
        options_frame = QFrame()
        options_frame.setObjectName("optionsFrame")
        options_layout = QVBoxLayout(options_frame)
        
        options_label = QLabel("Detection Options:")
        options_label.setFont(QFont("Segoe UI", 10))
        options_layout.addWidget(options_label)
        
        # Checkboxes for YOLO options
        options_grid = QGridLayout()
        
        self.save_txt = QCheckBox("Save Labels (txt)")
        self.save_txt.setChecked(True)
        self.save_txt.setToolTip("Save detection results as YOLO format txt files")
        options_grid.addWidget(self.save_txt, 0, 0)
        
        self.save_conf = QCheckBox("Save Confidence")
        self.save_conf.setToolTip("Save confidence scores in labels")
        options_grid.addWidget(self.save_conf, 0, 1)
        
        self.save_crop = QCheckBox("Save Crops")
        self.save_crop.setToolTip("Save cropped images of detections")
        options_grid.addWidget(self.save_crop, 0, 2)
        
        self.save_plots = QCheckBox("Save Plots")
        self.save_plots.setToolTip("Save detection plots (confusion matrix, results.png)")
        options_grid.addWidget(self.save_plots, 1, 0)
        
        self.hide_labels = QCheckBox("Hide Labels")
        self.hide_labels.setToolTip("Hide labels in detection images")
        options_grid.addWidget(self.hide_labels, 1, 1)
        
        self.hide_conf = QCheckBox("Hide Confidence")
        self.hide_conf.setToolTip("Hide confidence scores in detection images")
        options_grid.addWidget(self.hide_conf, 1, 2)
        
        options_layout.addLayout(options_grid)
        layout.addWidget(options_frame)
        
        # Bottom section with status and run button
        bottom_frame = QFrame()
        bottom_frame.setObjectName("bottomFrame")
        bottom_layout = QVBoxLayout(bottom_frame)
        
        # Add console output
        console_label = QLabel("Console Output:")
        console_label.setFont(QFont("Segoe UI", 10))
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setObjectName("consoleOutput")
        self.console_output.setMinimumHeight(100)
        self.console_output.setMaximumHeight(200)
        
        # Progress and status
        progress_layout = QVBoxLayout()
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        
        # Run button and auto-open checkbox
        run_layout = QHBoxLayout()
        
        run_button_layout = QVBoxLayout()
        self.run_btn = QPushButton("Run Detection")
        self.run_btn.setFixedWidth(200)
        self.run_btn.clicked.connect(self.run_detection)
        self.run_btn.setObjectName("runButton")
        
        self.auto_open = QCheckBox("Auto-open Results")
        self.auto_open.setChecked(True)  # On by default
        self.auto_open.setToolTip("Automatically open results folder after detection")
        
        run_button_layout.addWidget(self.run_btn)
        run_button_layout.addWidget(self.auto_open)
        run_button_layout.setAlignment(self.auto_open, Qt.AlignCenter)
        
        run_layout.addStretch()
        run_layout.addLayout(run_button_layout)
        run_layout.addStretch()
        
        bottom_layout.addWidget(console_label)
        bottom_layout.addWidget(self.console_output)
        bottom_layout.addLayout(progress_layout)
        bottom_layout.addLayout(run_layout)
        
        layout.addWidget(bottom_frame)
        
        # Set styles
        self.updateStyleSheet()

    def setDarkTheme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(37, 37, 37))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

    def updateModelList(self):
        self.model_combo.clear()
        # Add models from the default models directory
        models_dir = "models"
        if os.path.exists(models_dir):
            model_files = [os.path.join(models_dir, f) for f in os.listdir(models_dir) if f.endswith('.pt')]
            self.model_combo.addItems(model_files)
        
        # Add last used custom model if it exists
        last_model = self.settings.value('last_model')
        if last_model and os.path.exists(last_model):
            if self.model_combo.findText(last_model) == -1:
                self.model_combo.addItem(last_model)
            self.model_combo.setCurrentText(last_model)

    def updateModelDisplay(self):
        """Update the model name and path displays."""
        if hasattr(self, 'model_combo') and hasattr(self, 'model_name_label') and hasattr(self, 'model_path_label'):
            if self.model_combo.currentText():
                model_path = self.model_combo.currentText()
                model_name = os.path.basename(model_path)
                self.model_name_label.setText(model_name)
                self.model_path_label.setText(f"Path: {model_path}")
                self.settings.setValue('last_model', model_path)
            else:
                self.model_name_label.setText("No model selected")
                self.model_path_label.setText("No model selected")

    def browseModel(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select YOLO Model",
            self.settings.value('last_model_directory', 'models'),
            "YOLO Models (*.pt);;All Files (*.*)"
        )
        if file_name:
            self.settings.setValue('last_model_directory', os.path.dirname(file_name))
            # Add to combo box if not already present
            if self.model_combo.findText(file_name) == -1:
                self.model_combo.addItem(file_name)
            self.model_combo.setCurrentText(file_name)

    def browseFiles(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter("Images (*.jpg *.jpeg *.png *.bmp)")
        dialog.setDirectory(self.settings.value('last_directory', ''))
        
        if dialog.exec_():
            selected_paths = dialog.selectedFiles()
            for path in selected_paths:
                if self.file_list.findItems(path, Qt.MatchExactly) == []:
                    self.file_list.addItem(path)
            
            # Save the last used directory
            self.settings.setValue('last_directory', os.path.dirname(selected_paths[0]))
            self.updateStatus()

    def browseFolder(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setDirectory(self.settings.value('last_directory', ''))
        
        if dialog.exec_():
            folder_path = dialog.selectedFiles()[0]
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
                image_files.extend(glob.glob(os.path.join(folder_path, ext)))
                image_files.extend(glob.glob(os.path.join(folder_path, '**', ext), recursive=True))
            
            # Remove duplicates and sort
            image_files = sorted(set(image_files))
            
            if not image_files:
                QMessageBox.warning(self, "No Images Found", 
                                  f"No image files found in the selected folder:\n{folder_path}")
                return
            
            # Add only files that aren't already in the list
            for path in image_files:
                if self.file_list.findItems(path, Qt.MatchExactly) == []:
                    self.file_list.addItem(path)
            
            # Save the last used directory
            self.settings.setValue('last_directory', folder_path)
            self.updateStatus()

    def clearFileList(self):
        self.file_list.clear()
        self.updateStatus()

    def updateStatus(self):
        total_files = self.file_list.count()
        if total_files > 0:
            self.status_label.setText(f"Ready to process {total_files} image{'s' if total_files > 1 else ''}")
        else:
            self.status_label.setText("Ready")

    def updateStyleSheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QFrame {
                background-color: #252526;
                border-radius: 5px;
            }
            QLabel {
                color: #ffffff;
            }
            #modelNameLabel {
                color: #4CAF50;
                margin: 10px;
            }
            #pathLabel {
                color: #888888;
                font-size: 11px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            /* Standard blue for most buttons */
            #addFilesBtn, #addFolderBtn, #browseModelBtn {
                background-color: #2b5797;
                border-color: #3b67a7;
            }
            #addFilesBtn:hover, #addFolderBtn:hover, #browseModelBtn:hover {
                background-color: #3b67a7;
            }
            /* Red for clear button */
            #clearBtn {
                background-color: #8a2d2d;
                border-color: #9a3d3d;
            }
            #clearBtn:hover {
                background-color: #9a3d3d;
            }
            /* Green for run button */
            #runButton {
                background-color: #1e7145;
                border-color: #2e8155;
                font-weight: bold;
                padding: 8px 16px;
            }
            #runButton:hover {
                background-color: #2e8155;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QListWidget {
                background-color: #252526;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 2px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #2b5797;
                border-radius: 2px;
            }
            #consoleOutput {
                background-color: #252526;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                font-family: 'Segoe UI', sans-serif;
                padding: 5px;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #2b5797;
                border-color: #3b67a7;
            }
            QCheckBox::indicator:hover {
                border-color: #3b67a7;
            }
        """)

    def log_output(self, text):
        self.console_output.append(text)
        # Ensure the latest output is visible
        self.console_output.verticalScrollBar().setValue(
            self.console_output.verticalScrollBar().maximum()
        )
        QApplication.processEvents()

    def run_detection(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "No Files Selected", "Please select image files first.")
            return
        
        try:
            # Load model
            model_name = self.model_combo.currentText()
            if not model_name:
                QMessageBox.warning(self, "No Model Selected", "Please select a model first.")
                return
            
            self.log_output(f"Loading model: {os.path.basename(model_name)}")
            self.status_label.setText(f"Loading model: {os.path.basename(model_name)}")
            self.model = YOLO(model_name)
            
            # Create results directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir = os.path.join("results", f"detection_{timestamp}")
            os.makedirs(results_dir, exist_ok=True)
            
            # Collect all image paths
            image_paths = [self.file_list.item(i).text() for i in range(self.file_list.count())]
            
            # Set detection options
            options = {
                "save": True,  # Always save results
                "save_txt": self.save_txt.isChecked(),
                "save_conf": self.save_conf.isChecked(),
                "save_crop": self.save_crop.isChecked(),
                "hide_labels": self.hide_labels.isChecked(),
                "hide_conf": self.hide_conf.isChecked(),
                "project": "results",
                "name": f"detection_{timestamp}",
                "exist_ok": True  # Overwrite existing results
            }
            
            # Run batch detection
            self.log_output("Starting detection with options:")
            for key, value in options.items():
                if value:  # Only log enabled options
                    self.log_output(f"- {key}: {value}")
            
            # Process files with progress updates
            total_files = len(image_paths)
            self.progress_bar.setMaximum(total_files)
            
            results = self.model.predict(
                source=image_paths,
                **options
            )
            
            # Update progress bar for each processed image
            for i, r in enumerate(results):
                self.progress_bar.setValue(i + 1)
                
                # Log detections for this image
                boxes = r.boxes
                class_counts = {}
                for box in boxes:
                    class_name = r.names[int(box.cls)]
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                
                # Format detection summary
                if class_counts:
                    detections = ", ".join([f"{count} {name}{'s' if count > 1 else ''}" 
                                          for name, count in class_counts.items()])
                    self.log_output(f"Found in {os.path.basename(image_paths[i])}: {detections}")
                
                QApplication.processEvents()
            
            # Generate and save plots if requested
            if self.save_plots.isChecked():
                try:
                    self.log_output("Generating result plots...")
                    plots_dir = os.path.join(results_dir, "plots")
                    os.makedirs(plots_dir, exist_ok=True)
                    
                    # Save confusion matrix if available
                    if hasattr(results[0], 'save_conf_matrix'):
                        results[0].save_conf_matrix(file=os.path.join(plots_dir, "confusion_matrix.png"))
                    
                    # Save results plot
                    try:
                        import pandas as pd
                        import matplotlib.pyplot as plt
                        
                        # Collect detection data
                        data = []
                        for i, r in enumerate(results):
                            for box in r.boxes:
                                confidence = float(box.conf)
                                class_name = r.names[int(box.cls)]
                                data.append({
                                    'Image': os.path.basename(image_paths[i]),
                                    'Class': class_name,
                                    'Confidence': confidence
                                })
                        
                        if data:
                            df = pd.DataFrame(data)
                            
                            # Create confidence distribution plot
                            plt.figure(figsize=(10, 6))
                            plt.hist(df['Confidence'], bins=20, edgecolor='black')
                            plt.title('Detection Confidence Distribution')
                            plt.xlabel('Confidence Score')
                            plt.ylabel('Count')
                            plt.savefig(os.path.join(plots_dir, 'confidence_distribution.png'))
                            plt.close()
                            
                            # Create class distribution plot
                            plt.figure(figsize=(10, 6))
                            df['Class'].value_counts().plot(kind='bar')
                            plt.title('Detected Classes Distribution')
                            plt.xlabel('Class')
                            plt.ylabel('Count')
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            plt.savefig(os.path.join(plots_dir, 'class_distribution.png'))
                            plt.close()
                            
                            self.log_output("Generated distribution plots")
                    except Exception as e:
                        self.log_output(f"Warning: Could not generate distribution plots: {str(e)}")
                        
                except Exception as e:
                    self.log_output(f"Warning: Could not generate some plots: {str(e)}")
            
            completion_msg = f"Detection completed! Results saved in: {results_dir}"
            self.log_output(completion_msg)
            self.status_label.setText("Detection completed!")
            
            # Open results folder if auto-open is checked
            if self.auto_open.isChecked():
                self.log_output("Opening results folder...")
                if sys.platform == 'win32':
                    os.startfile(results_dir)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', results_dir])
                else:
                    subprocess.run(['xdg-open', results_dir])
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.log_output(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            self.status_label.setText("Error during detection")
        finally:
            self.progress_bar.setValue(0)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark theme support
    window = ModelGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
