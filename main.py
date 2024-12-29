import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QFileDialog, QLabel, QComboBox,
                           QProgressBar, QMessageBox, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ultralytics import YOLO

class ModelGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO Model GUI")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 120px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 200px;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Model selection
        model_frame = QFrame()
        model_layout = QVBoxLayout(model_frame)
        model_layout.setSpacing(10)
        
        model_label = QLabel("Select Model:")
        model_label.setFont(QFont("Arial", 12))
        self.model_combo = QComboBox()
        self.model_combo.addItem("yolov8n.pt")  # Default model
        
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        layout.addWidget(model_frame)
        
        # Input selection buttons
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.select_image_btn = QPushButton("Select Image")
        self.select_folder_btn = QPushButton("Select Folder")
        self.select_image_btn.clicked.connect(self.select_image)
        self.select_folder_btn.clicked.connect(self.select_folder)
        
        buttons_layout.addWidget(self.select_image_btn)
        buttons_layout.addWidget(self.select_folder_btn)
        layout.addWidget(buttons_frame)
        
        # Status and progress
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(10)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        layout.addWidget(status_frame)
        
        # Run button
        run_frame = QFrame()
        run_layout = QHBoxLayout(run_frame)
        run_layout.setAlignment(Qt.AlignCenter)
        
        self.run_btn = QPushButton("Run Detection")
        self.run_btn.clicked.connect(self.run_detection)
        self.run_btn.setFixedWidth(200)  # Wider run button
        
        run_layout.addWidget(self.run_btn)
        layout.addWidget(run_frame)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Initialize variables
        self.input_path = None
        self.model = None

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "sample_images",  # Start in sample_images directory
            "Images (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.input_path = file_name
            self.status_label.setText(f"Selected: {os.path.basename(file_name)}")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "sample_images")
        if folder:
            self.input_path = folder
            self.status_label.setText(f"Selected: {os.path.basename(folder)}")

    def run_detection(self):
        if not self.input_path:
            QMessageBox.warning(self, "Warning", "Please select an image or folder first")
            return
        
        try:
            # Load model from models directory
            model_name = os.path.join("models", self.model_combo.currentText())
            self.status_label.setText(f"Loading model: {os.path.basename(model_name)}")
            self.model = YOLO(model_name)
            
            # Create results directory with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir = os.path.join("results", timestamp)
            os.makedirs(results_dir, exist_ok=True)
            
            # Run detection and save to results directory
            self.status_label.setText("Running detection...")
            
            # Convert relative paths to absolute paths
            abs_input_path = os.path.abspath(self.input_path)
            abs_results_dir = os.path.abspath(results_dir)
            
            results = self.model.predict(
                source=abs_input_path,
                save=True,  # Explicitly save the results
                save_txt=True,  # Save labels
                save_conf=True,  # Save confidences
                project=abs_results_dir,
                name="",
                exist_ok=True
            )
            
            # Wait a moment for files to be written
            import time
            time.sleep(1)
            
            # Check if results were generated
            result_files = os.listdir(results_dir)
            if not result_files:
                raise Exception("No output files were generated. Check if the input image/folder is valid.")
                
            self.status_label.setText(f"Found {len(result_files)} result files")
            
            # Show completion message with output location and files
            message = (
                f"Detection complete!\n"
                f"Results saved in: {results_dir}\n"
                f"Files generated: {', '.join(result_files)}\n\n"
                f"Input path: {abs_input_path}"
            )
            QMessageBox.information(self, "Complete", message)
            self.status_label.setText("Ready")
            
            # Open results folder
            os.startfile(results_dir)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.status_label.setText("Error occurred")

def main():
    print("Starting application...")
    app = QApplication(sys.argv)
    print("Created QApplication")
    window = ModelGUI()
    print("Created main window")
    window.show()
    print("Showing window")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
