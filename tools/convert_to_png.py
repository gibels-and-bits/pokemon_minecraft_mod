#!/usr/bin/env python3
import os
from PIL import Image
import concurrent.futures

def convert_jpg_to_png(jpg_path):
    """Convert a single JPG to PNG"""
    png_path = jpg_path.replace('.jpg', '.png')
    
    try:
        with Image.open(jpg_path) as img:
            # Convert RGBA to RGB if needed (PNG supports transparency but we don't need it)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as PNG with compression
            img.save(png_path, 'PNG', optimize=True)
        
        # Delete the original JPG
        os.remove(jpg_path)
        print(f"Converted: {os.path.basename(jpg_path)} -> {os.path.basename(png_path)}")
        return True
    except Exception as e:
        print(f"Error converting {jpg_path}: {e}")
        return False

def main():
    base_path = 'src/main/resources/assets/etbmod/textures/cards'
    jpg_files = []
    
    # Find all JPG files
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.jpg'):
                jpg_files.append(os.path.join(root, file))
    
    print(f"Found {len(jpg_files)} JPG files to convert")
    
    # Convert in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(convert_jpg_to_png, jpg_files))
    
    success_count = sum(results)
    print(f"\nConverted {success_count}/{len(jpg_files)} files successfully")

if __name__ == '__main__':
    main()