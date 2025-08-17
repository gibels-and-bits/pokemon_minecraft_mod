#!/usr/bin/env python3
import os
from PIL import Image
import concurrent.futures

def resize_to_power_of_2(png_path):
    """Resize PNG to 256x512 (power of 2 dimensions)"""
    try:
        with Image.open(png_path) as img:
            # Target size: 256x512 (maintains rough aspect ratio)
            # Original is 250x349, so we'll scale up slightly
            resized = img.resize((256, 512), Image.LANCZOS)
            resized.save(png_path, 'PNG', optimize=True)
        
        print(f"Resized: {os.path.basename(png_path)}")
        return True
    except Exception as e:
        print(f"Error resizing {png_path}: {e}")
        return False

def main():
    base_path = 'src/main/resources/assets/etbmod/textures/cards'
    png_files = []
    
    # Find all PNG files
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.png'):
                png_files.append(os.path.join(root, file))
    
    print(f"Found {len(png_files)} PNG files to resize to 256x512")
    
    # Resize in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(resize_to_power_of_2, png_files))
    
    success_count = sum(results)
    print(f"\nResized {success_count}/{len(png_files)} files successfully")

if __name__ == '__main__':
    main()