#!/usr/bin/env python3
import os
from PIL import Image
import concurrent.futures

def resize_to_smaller(png_path):
    """Resize PNG to 128x256 (smaller power of 2)"""
    try:
        with Image.open(png_path) as img:
            # Target size: 128x256 (half the current size)
            resized = img.resize((128, 256), Image.LANCZOS)
            
            # Save with optimization
            resized.save(png_path, 'PNG', optimize=True, compress_level=9)
        
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
    
    print(f"Found {len(png_files)} PNG files to resize to 128x256")
    
    # Resize in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(resize_to_smaller, png_files))
    
    success_count = sum(results)
    print(f"Resized {success_count}/{len(png_files)} files successfully")

if __name__ == '__main__':
    main()