import sys
import os
from datetime import datetime
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QFileDialog, QLabel, QComboBox,
                           QProgressBar, QMessageBox, QHBoxLayout, QFrame,
                           QStyle, QSplitter, QListWidget, QCheckBox)
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
        
        model_layout = QHBoxLayout()
        self.model_combo = QComboBox()
        self.updateModelList()
        
        browse_model_btn = QPushButton("Browse")
        browse_model_btn.setFixedWidth(100)
        browse_model_btn.clicked.connect(self.browseModel)
        
        model_layout.addWidget(self.model_combo, stretch=1)
        model_layout.addWidget(browse_model_btn)
        
        # Model path display
        self.model_path_label = QLabel()
        self.model_path_label.setObjectName("pathLabel")
        self.updateModelPath()
        
        top_layout.addWidget(model_label)
        top_layout.addLayout(model_layout)
        top_layout.addWidget(self.model_path_label)
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
        
        # Bottom section with status and run button
        bottom_frame = QFrame()
        bottom_frame.setObjectName("bottomFrame")
        bottom_layout = QVBoxLayout(bottom_frame)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        
        run_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Detection")
        self.run_btn.setFixedWidth(200)
        self.run_btn.clicked.connect(self.run_detection)
        run_layout.addStretch()
        run_layout.addWidget(self.run_btn)
        run_layout.addStretch()
        
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addWidget(self.progress_bar)
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

    def updateModelPath(self):
        if self.model_combo.currentText():
            model_path = self.model_combo.currentText()
            self.model_path_label.setText(f"Path: {model_path}")
            self.settings.setValue('last_model', model_path)
        else:
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
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            #addFilesBtn {
                background-color: #2d5a27;
            }
            #addFilesBtn:hover {
                background-color: #3d6a37;
            }
            #addFolderBtn {
                background-color: #2d4a8a;
            }
            #addFolderBtn:hover {
                background-color: #3d5a9a;
            }
            #clearBtn {
                background-color: #8a2d2d;
            }
            #clearBtn:hover {
                background-color: #9a3d3d;
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
                background-color: #2196F3;
                border-radius: 2px;
            }
        """)

    def run_detection(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "No Files Selected", "Please select image files first.")
            return
        
        try:
            # Load model
            model_name = self.model_combo.currentText()
            self.status_label.setText(f"Loading model: {os.path.basename(model_name)}")
            self.model = YOLO(model_name)
            
            # Create results directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir = os.path.join("results", f"detection_{timestamp}")
            os.makedirs(results_dir, exist_ok=True)
            
            # Process all files
            total_files = self.file_list.count()
            self.progress_bar.setMaximum(total_files)
            self.progress_bar.setValue(0)
            
            for i in range(total_files):
                image_path = self.file_list.item(i).text()
                self.status_label.setText(f"Processing {i+1}/{total_files}: {os.path.basename(image_path)}")
                
                # Run detection
                results = self.model(image_path)
                
                # Save results
                for r in results:
                    im_array = r.plot()
                    im = Image.fromarray(im_array[..., ::-1])
                    output_path = os.path.join(results_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_detected.jpg")
                    im.save(output_path)
                
                self.progress_bar.setValue(i + 1)
                QApplication.processEvents()
            
            self.status_label.setText("Detection completed!")
            
            # Open results folder
            if sys.platform == 'win32':
                os.startfile(results_dir)
            elif sys.platform == 'darwin':
                subprocess.run(['open', results_dir])
            else:
                subprocess.run(['xdg-open', results_dir])
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
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
