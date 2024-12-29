#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main():
    print("Setting up ModelGUI environment...")

    # Determine platform-specific virtual environment path
    is_windows = platform.system() == "Windows"
    venv_path = "venv\\Scripts" if is_windows else "venv/bin"
    activate_command = f"call {venv_path}\\activate" if is_windows else f"source {venv_path}/activate"

    # Create virtual environment
    print("Creating virtual environment...")
    run_command(f"python -m venv venv")

    # Install requirements
    print("Installing requirements...")
    pip_path = os.path.join(venv_path, "pip")
    if is_windows:
        pip_path += ".exe"
    run_command(f'"{pip_path}" install -r requirements.txt')

    # Run the download script
    print("Downloading YOLO model and sample images...")
    python_path = os.path.join(venv_path, "python")
    if is_windows:
        python_path += ".exe"
    run_command(f'"{python_path}" download_assets.py')

    print("\nSetup complete!")
    print("\nTo run the application:")
    if is_windows:
        print("1. Run: venv\\Scripts\\python main.py")
    else:
        print("1. Run: venv/bin/python main.py")

if __name__ == "__main__":
    main()
