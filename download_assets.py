import os
import requests
from pathlib import Path

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    current_size = 0
    
    print(f"Downloading {os.path.basename(dest_path)}...")
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=block_size):
            f.write(chunk)
            current_size += len(chunk)
            if total_size:
                progress = (current_size / total_size) * 100
                print(f"Progress: {progress:.1f}%", end='\r')
    print()

def main():
    # Create directories if they don't exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('sample_images', exist_ok=True)
    
    # Download YOLOv8n model (nano - smallest)
    model_urls = {
        "yolov8n.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt",
        "yolov8s.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt"  # small model
    }
    
    for model_name, url in model_urls.items():
        model_path = Path('models') / model_name
        print(f"\nDownloading {model_name}...")
        download_file(url, model_path)
        print(f"{model_name} downloaded successfully!")
    
    # Download sample images
    sample_images = [
        "https://ultralytics.com/images/zidane.jpg",
        "https://ultralytics.com/images/bus.jpg"
    ]
    
    for i, url in enumerate(sample_images, 1):
        filename = Path(url).name
        dest_path = Path('sample_images') / filename
        print(f"\nDownloading sample image {i}/{len(sample_images)}: {filename}")
        download_file(url, dest_path)
    
    print("\nAll assets downloaded successfully!")

if __name__ == "__main__":
    main()
