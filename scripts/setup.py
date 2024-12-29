#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main():
    print("Setting up ModelGUI environment...")

    # Determine platform-specific settings
    is_windows = platform.system() == "Windows"
    
    # Set up Python command based on platform
    if is_windows:
        python_cmd = "python"  # On Windows, use the default Python
    else:
        python_cmd = "/usr/local/bin/python3.11"  # On Mac, use Python 3.11 specifically
        # Check if Python 3.11 is available
        try:
            subprocess.run([python_cmd, "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Python 3.11 is required but not found.")
            print("Please install Python 3.11 using:")
            print("brew install python@3.11")
            sys.exit(1)

    # Remove existing venv if it exists
    if os.path.exists("venv"):
        print("Removing existing virtual environment...")
        shutil.rmtree("venv")

    # Set up paths based on platform
    venv_path = "venv\\Scripts" if is_windows else "venv/bin"
    python_path = os.path.join(venv_path, "python")
    if is_windows:
        python_path += ".exe"
        pip_path = os.path.join(venv_path, "pip")
        pip_path += ".exe"
    else:
        pip_path = os.path.join(venv_path, "pip3")

    # Create virtual environment
    print("Creating virtual environment...")
    run_command(f"{python_cmd} -m venv venv")

    # Upgrade pip in the virtual environment
    print("Upgrading pip...")
    run_command(f'"{python_path}" -m pip install --upgrade pip')

    # Install requirements
    print("Installing requirements...")
    run_command(f'"{python_path}" -m pip install -r requirements.txt')

    # Run the download script
    print("Downloading YOLO model and sample images...")
    run_command(f'"{python_path}" download_assets.py')

    print("\nSetup complete!")
    print("\nTo run the application:")
    if is_windows:
        print("1. Run: venv\\Scripts\\python main.py")
    else:
        print("1. Run: venv/bin/python main.py")

if __name__ == "__main__":
    main()
