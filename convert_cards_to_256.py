#!/usr/bin/env python3
import os
from PIL import Image
import glob
from pathlib import Path

# Texture size for Minecraft
TEXTURE_SIZE = 256

# Card directories to process
CARD_DIRS = [
    "src/main/resources/assets/etbmod/textures/cards",
    "raw_images/cards",
    "build/resources/main/assets/etbmod/textures/cards"
]

def convert_card_to_256(image_path):
    """Convert a card image to 256x256 while maintaining aspect ratio"""
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get original dimensions
        orig_width, orig_height = img.size
        
        # Calculate scaling to fit within 256x256 while maintaining aspect ratio
        scale = min(TEXTURE_SIZE / orig_width, TEXTURE_SIZE / orig_height)
        
        # Calculate new dimensions
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        # Resize the image with high quality
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a new 256x256 transparent image
        final_img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE), (0, 0, 0, 0))
        
        # Calculate position to center the card
        x_offset = (TEXTURE_SIZE - new_width) // 2
        y_offset = (TEXTURE_SIZE - new_height) // 2
        
        # Paste the resized card onto the transparent background
        final_img.paste(img_resized, (x_offset, y_offset))
        
        return final_img
        
    except Exception as e:
        print(f"  ✗ Error processing {image_path}: {e}")
        return None

def process_directory(directory):
    """Process all card images in a directory and its subdirectories"""
    if not os.path.exists(directory):
        print(f"  ⚠ Directory not found: {directory}")
        return 0
    
    processed_count = 0
    error_count = 0
    
    # Find all PNG files in subdirectories
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            print(f"\n  📁 Processing {subdir}...")
            
            png_files = glob.glob(os.path.join(subdir_path, "*.png"))
            
            for png_file in png_files:
                # Convert the image
                converted_img = convert_card_to_256(png_file)
                
                if converted_img:
                    # Save over the original file
                    converted_img.save(png_file, "PNG", optimize=True)
                    processed_count += 1
                    
                    # Show progress every 50 cards
                    if processed_count % 50 == 0:
                        print(f"    ✓ Processed {processed_count} cards...")
                else:
                    error_count += 1
            
            if png_files:
                print(f"    ✅ Completed {len(png_files)} cards in {subdir}")
    
    return processed_count, error_count

def verify_dimensions(directory):
    """Verify all images are 256x256"""
    if not os.path.exists(directory):
        return
    
    print(f"\n🔍 Verifying dimensions in {directory}...")
    
    non_standard = []
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            png_files = glob.glob(os.path.join(subdir_path, "*.png"))
            
            for png_file in png_files:
                try:
                    img = Image.open(png_file)
                    if img.size != (TEXTURE_SIZE, TEXTURE_SIZE):
                        non_standard.append((png_file, img.size))
                except:
                    pass
    
    if non_standard:
        print(f"  ⚠ Found {len(non_standard)} non-256x256 images")
        for file, size in non_standard[:5]:  # Show first 5
            print(f"    - {os.path.basename(file)}: {size}")
    else:
        print(f"  ✅ All images are 256x256")

def main():
    print("🎴 Pokemon Card Texture Converter")
    print("Converting all cards to 256x256 textures with preserved aspect ratio")
    print("=" * 70)
    
    total_processed = 0
    total_errors = 0
    
    for directory in CARD_DIRS:
        print(f"\n📂 Processing directory: {directory}")
        processed, errors = process_directory(directory)
        total_processed += processed
        total_errors += errors
        
        if processed > 0:
            print(f"  📊 Processed: {processed} cards, Errors: {errors}")
    
    print("\n" + "=" * 70)
    print(f"✨ Conversion complete!")
    print(f"   Total cards processed: {total_processed}")
    print(f"   Total errors: {total_errors}")
    
    # Verify dimensions
    print("\n" + "=" * 70)
    print("Verifying conversions...")
    for directory in CARD_DIRS:
        if os.path.exists(directory):
            verify_dimensions(directory)

if __name__ == "__main__":
    main()