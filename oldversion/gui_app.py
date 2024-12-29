import tkinter as tk
from tkinter import filedialog, messagebox
from file_processor import read_file_contents

class FileAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Analyzer GUI")
        self.root.geometry("600x400")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and pack widgets
        self.create_widgets()
        
    def create_widgets(self):
        # File selection button
        self.select_button = tk.Button(
            self.main_frame,
            text="Select File",
            command=self.select_file,
            width=20
        )
        self.select_button.pack(pady=10)
        
        # Label to show selected file
        self.file_label = tk.Label(
            self.main_frame,
            text="No file selected",
            wraplength=500
        )
        self.file_label.pack(pady=10)
        
        # Text area for displaying contents
        self.text_area = tk.Text(
            self.main_frame,
            height=15,
            width=60,
            wrap=tk.WORD
        )
        self.text_area.pack(pady=10)
        
        # Scrollbar for text area
        scrollbar = tk.Scrollbar(self.main_frame, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_label.config(text=f"Selected file: {file_path}")
            try:
                content = read_file_contents(file_path)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")

def main():
    root = tk.Tk()
    app = FileAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
