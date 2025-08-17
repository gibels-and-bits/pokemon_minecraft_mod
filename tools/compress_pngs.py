#!/usr/bin/env python3
import os
from PIL import Image
import concurrent.futures

def compress_png(png_path):
    """Compress PNG with better optimization"""
    try:
        with Image.open(png_path) as img:
            # Convert to RGB (remove alpha channel if present)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save with maximum compression
            img.save(png_path, 'PNG', optimize=True, compress_level=9)
        
        return True
    except Exception as e:
        print(f"Error compressing {png_path}: {e}")
        return False

def main():
    base_path = 'src/main/resources/assets/etbmod/textures/cards'
    png_files = []
    
    # Get initial size
    initial_size = 0
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.png'):
                full_path = os.path.join(root, file)
                png_files.append(full_path)
                initial_size += os.path.getsize(full_path)
    
    print(f"Found {len(png_files)} PNG files")
    print(f"Initial total size: {initial_size / 1024 / 1024:.1f} MB")
    
    # Compress in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(compress_png, png_files))
    
    # Get final size
    final_size = 0
    for file_path in png_files:
        if os.path.exists(file_path):
            final_size += os.path.getsize(file_path)
    
    print(f"Final total size: {final_size / 1024 / 1024:.1f} MB")
    print(f"Saved: {(initial_size - final_size) / 1024 / 1024:.1f} MB")

if __name__ == '__main__':
    main()