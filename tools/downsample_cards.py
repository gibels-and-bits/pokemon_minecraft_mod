#!/usr/bin/env python3
"""Downsample card images to reduce mod size."""

import os
from PIL import Image
import json

def downsample_cards():
    base_path = "/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/cards"
    
    total_before = 0
    total_after = 0
    processed = 0
    
    # Target dimensions for cards (maintain aspect ratio)
    # Pokemon cards are 2.5" x 3.5" (ratio 5:7)
    # Reduced for mod size constraints
    max_width = 250  # Small but readable
    max_height = 350  # Maintains 5:7 ratio
    jpeg_quality = 75  # Use JPEG compression
    
    for set_folder in os.listdir(base_path):
        set_path = os.path.join(base_path, set_folder)
        if not os.path.isdir(set_path):
            continue
            
        print(f"Processing set: {set_folder}")
        
        for filename in os.listdir(set_path):
            if filename.endswith('.png'):
                filepath = os.path.join(set_path, filename)
                
                # Get original size
                original_size = os.path.getsize(filepath)
                total_before += original_size
                
                try:
                    # Open and resize image
                    img = Image.open(filepath)
                    
                    # Always resize to ensure consistency and smaller size
                    # Calculate new size maintaining aspect ratio
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # Convert RGBA to RGB if needed (JPEG doesn't support transparency)
                    if img.mode == 'RGBA':
                        # Create white background
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as JPEG with compression
                    jpeg_path = filepath.replace('.png', '.jpg')
                    img.save(jpeg_path, 'JPEG', optimize=True, quality=jpeg_quality)
                    
                    # Remove original PNG
                    if os.path.exists(jpeg_path) and jpeg_path != filepath:
                        os.remove(filepath)
                    
                    processed += 1
                    
                    # Get new size (from JPEG file)
                    new_size = os.path.getsize(jpeg_path)
                    total_after += new_size
                    
                    if processed % 50 == 0:
                        print(f"  Processed {processed} images...")
                        
                except Exception as e:
                    print(f"  Error processing {filename}: {e}")
    
    # Convert bytes to MB
    before_mb = total_before / (1024 * 1024)
    after_mb = total_after / (1024 * 1024)
    reduction = ((total_before - total_after) / total_before) * 100 if total_before > 0 else 0
    
    print(f"\nDownsampling complete!")
    print(f"Processed: {processed} images")
    print(f"Size before: {before_mb:.1f} MB")
    print(f"Size after: {after_mb:.1f} MB")
    print(f"Reduction: {reduction:.1f}%")

if __name__ == "__main__":
    downsample_cards()