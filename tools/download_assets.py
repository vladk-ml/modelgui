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
    # Get the project root directory (parent of scripts directory)
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Create directories if they don't exist
    models_dir = os.path.join(project_root, 'models')
    sample_images_dir = os.path.join(project_root, 'sample_images')
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(sample_images_dir, exist_ok=True)
    
    # Download YOLOv8n model (nano - smallest)
    model_urls = {
        "yolov8n.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt",
        "yolov8s.pt": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt"  # small model
    }
    
    for model_name, url in model_urls.items():
        model_path = os.path.join(models_dir, model_name)
        if not os.path.exists(model_path):
            print(f"\nDownloading {model_name}...")
            download_file(url, model_path)
            print(f"{model_name} downloaded successfully!")
        else:
            print(f"Model {model_name} already exists, skipping download.")
    
    # Download sample images if they don't exist
    sample_image_urls = [
        "https://ultralytics.com/images/zidane.jpg",
        "https://ultralytics.com/images/bus.jpg"
    ]
    
    for i, url in enumerate(sample_image_urls, 1):
        filename = os.path.basename(url)
        image_path = os.path.join(sample_images_dir, filename)
        if not os.path.exists(image_path):
            print(f"\nDownloading sample image {i}/{len(sample_image_urls)}: {filename}")
            download_file(url, image_path)
        else:
            print(f"Sample image {filename} already exists, skipping download.")
    
    print("\nAll assets downloaded successfully!")

if __name__ == "__main__":
    main()
