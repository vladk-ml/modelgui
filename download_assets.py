import os
import requests
from pathlib import Path

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def main():
    # Create directories if they don't exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('sample_images', exist_ok=True)
    
    # Download YOLOv8n model
    model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
    model_path = Path('models/yolov8n.pt')
    
    print(f"Downloading YOLOv8n model to {model_path}...")
    download_file(model_url, model_path)
    print("Model downloaded successfully!")
    
    # Download sample images
    sample_images = [
        "https://ultralytics.com/images/zidane.jpg",
        "https://ultralytics.com/images/bus.jpg"
    ]
    
    for i, url in enumerate(sample_images, 1):
        filename = Path(url).name
        dest_path = Path('sample_images') / filename
        print(f"Downloading sample image {i}/{len(sample_images)}: {filename}")
        download_file(url, dest_path)
    
    print("Sample images downloaded successfully!")

if __name__ == "__main__":
    main()
