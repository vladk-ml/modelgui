#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("Updating ModelGUI environment...")

    # Determine platform-specific settings
    is_windows = platform.system() == "Windows"
    
    # Set up paths
    project_root = os.path.dirname(os.path.dirname(__file__))
    venv_dir = os.path.join(project_root, "venv")
    venv_path = os.path.join(venv_dir, "Scripts" if is_windows else "bin")
    python_path = os.path.join(venv_path, "python" + (".exe" if is_windows else ""))
    pip_path = os.path.join(venv_path, "pip" + (".exe" if is_windows else ""))

    if not os.path.exists(venv_dir):
        print("Error: Virtual environment not found. Please run setup.py first.")
        sys.exit(1)

    # Upgrade pip first
    print("\nUpgrading pip...")
    if not run_command(f'"{python_path}" -m pip install --upgrade pip'):
        sys.exit(1)

    # Upgrade all packages to their latest versions
    print("\nUpgrading packages...")
    requirements_path = os.path.join(project_root, "requirements.txt")
    if not run_command(f'"{pip_path}" install --upgrade -r "{requirements_path}"'):
        sys.exit(1)

    print("\nChecking ultralytics version...")
    try:
        from ultralytics import __version__ as ultralytics_version
        print(f"Installed ultralytics version: {ultralytics_version}")
    except ImportError:
        print("Warning: Could not determine ultralytics version")

    print("\nUpdate complete! Your environment is now up to date.")
    print("\nIf you encounter any issues, you can:")
    print("1. Delete the 'venv' folder")
    print("2. Run setup.py again to create a fresh environment")

if __name__ == "__main__":
    main()
