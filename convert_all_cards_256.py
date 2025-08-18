#!/usr/bin/env python3
import os
import shutil
from PIL import Image
import glob
from pathlib import Path

# Texture size for Minecraft
TEXTURE_SIZE = 256

# All directories containing card images
CARD_DIRECTORIES = [
    "src/main/resources/assets/etbmod/textures/cards",
    "raw_images/cards",
    "build/resources/main/assets/etbmod/textures/cards",
    "cards"  # The newly downloaded cards
]

def clean_build_directory():
    """Clean the build directory"""
    build_dir = "build/resources/main/assets/etbmod/textures/cards"
    if os.path.exists(build_dir):
        print(f"🧹 Cleaning build directory: {build_dir}")
        shutil.rmtree(build_dir)
        os.makedirs(build_dir, exist_ok=True)
        print(f"  ✓ Build directory cleaned")
        return True
    return False

def convert_card_to_256_with_padding(image_path):
    """Convert a card image to 256x256 with transparent padding to preserve aspect ratio"""
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGBA for transparency support
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Skip if already 256x256
        if img.size == (TEXTURE_SIZE, TEXTURE_SIZE):
            return img
        
        # Get original dimensions
        orig_width, orig_height = img.size
        
        # Calculate scale to fit within 256x256 while maintaining aspect ratio
        # We want the card to fill most of the space but leave some padding
        scale = min((TEXTURE_SIZE - 10) / orig_width, (TEXTURE_SIZE - 10) / orig_height)
        
        # Calculate new dimensions
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        # Resize the image with high quality antialiasing
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a new 256x256 image with transparent background
        final_img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE), (0, 0, 0, 0))
        
        # Calculate position to center the card
        x_offset = (TEXTURE_SIZE - new_width) // 2
        y_offset = (TEXTURE_SIZE - new_height) // 2
        
        # Paste the resized card onto the transparent background
        final_img.paste(img_resized, (x_offset, y_offset), img_resized)
        
        return final_img
        
    except Exception as e:
        print(f"    ✗ Error processing {os.path.basename(image_path)}: {e}")
        return None

def process_card_set(set_path):
    """Process all cards in a set directory"""
    set_name = os.path.basename(set_path)
    png_files = glob.glob(os.path.join(set_path, "*.png"))
    
    if not png_files:
        return 0, 0
    
    print(f"  📁 Processing {set_name}: {len(png_files)} cards")
    
    success_count = 0
    error_count = 0
    
    for i, png_file in enumerate(png_files, 1):
        # Convert the image
        converted_img = convert_card_to_256_with_padding(png_file)
        
        if converted_img:
            # Save over the original file
            converted_img.save(png_file, "PNG", optimize=True)
            success_count += 1
            
            # Show progress
            if i % 50 == 0:
                print(f"    ... processed {i}/{len(png_files)} cards")
        else:
            error_count += 1
    
    print(f"    ✓ Completed: {success_count} success, {error_count} errors")
    return success_count, error_count

def sync_cards_to_build():
    """Copy all processed cards to the build directory"""
    src_dir = "src/main/resources/assets/etbmod/textures/cards"
    build_dir = "build/resources/main/assets/etbmod/textures/cards"
    
    if not os.path.exists(src_dir):
        return
    
    print(f"\n📋 Syncing cards to build directory...")
    os.makedirs(build_dir, exist_ok=True)
    
    for set_name in os.listdir(src_dir):
        set_src = os.path.join(src_dir, set_name)
        if os.path.isdir(set_src):
            set_dest = os.path.join(build_dir, set_name)
            
            # Copy entire directory
            if os.path.exists(set_dest):
                shutil.rmtree(set_dest)
            shutil.copytree(set_src, set_dest)
            
            card_count = len(glob.glob(os.path.join(set_dest, "*.png")))
            print(f"  ✓ Copied {set_name}: {card_count} cards")

def verify_all_cards():
    """Verify all cards are 256x256"""
    print(f"\n🔍 Verifying all cards are 256x256...")
    
    all_directories = [
        "src/main/resources/assets/etbmod/textures/cards",
        "raw_images/cards",
        "build/resources/main/assets/etbmod/textures/cards"
    ]
    
    total_cards = 0
    non_standard = []
    
    for directory in all_directories:
        if not os.path.exists(directory):
            continue
            
        for set_name in os.listdir(directory):
            set_path = os.path.join(directory, set_name)
            if os.path.isdir(set_path):
                png_files = glob.glob(os.path.join(set_path, "*.png"))
                
                for png_file in png_files:
                    total_cards += 1
                    try:
                        img = Image.open(png_file)
                        if img.size != (TEXTURE_SIZE, TEXTURE_SIZE):
                            non_standard.append((png_file, img.size))
                    except Exception as e:
                        non_standard.append((png_file, f"Error: {e}"))
    
    if non_standard:
        print(f"  ⚠ Found {len(non_standard)} non-standard images out of {total_cards} total")
        for file, info in non_standard[:10]:  # Show first 10
            rel_path = '/'.join(file.split('/')[-3:])
            print(f"    - {rel_path}: {info}")
    else:
        print(f"  ✅ All {total_cards} cards are 256x256 with proper formatting")
    
    return total_cards, len(non_standard)

def main():
    print("🎴 Pokemon Card Texture Converter - Full Processing")
    print("Converting ALL cards to 256x256 with transparent padding")
    print("=" * 70)
    
    # Step 1: Clean build directory
    clean_build_directory()
    
    # Step 2: Process all card directories
    print(f"\n📂 Processing all card directories...")
    
    total_processed = 0
    total_errors = 0
    
    # Process main source directory
    src_cards = "src/main/resources/assets/etbmod/textures/cards"
    if os.path.exists(src_cards):
        print(f"\n🎯 Processing main card directory: {src_cards}")
        for set_name in sorted(os.listdir(src_cards)):
            set_path = os.path.join(src_cards, set_name)
            if os.path.isdir(set_path):
                success, errors = process_card_set(set_path)
                total_processed += success
                total_errors += errors
    
    # Process raw_images directory
    raw_cards = "raw_images/cards"
    if os.path.exists(raw_cards):
        print(f"\n🎯 Processing raw cards directory: {raw_cards}")
        for set_name in sorted(os.listdir(raw_cards)):
            set_path = os.path.join(raw_cards, set_name)
            if os.path.isdir(set_path):
                success, errors = process_card_set(set_path)
                total_processed += success
                total_errors += errors
    
    # Process newly downloaded cards
    new_cards = "cards"
    if os.path.exists(new_cards):
        print(f"\n🎯 Processing newly downloaded cards: {new_cards}")
        for set_name in sorted(os.listdir(new_cards)):
            set_path = os.path.join(new_cards, set_name)
            if os.path.isdir(set_path):
                success, errors = process_card_set(set_path)
                total_processed += success
                total_errors += errors
    
    # Step 3: Sync to build directory
    sync_cards_to_build()
    
    # Step 4: Verify all cards
    total_cards, non_standard = verify_all_cards()
    
    # Final report
    print("\n" + "=" * 70)
    print(f"✨ Processing Complete!")
    print(f"   Total cards processed: {total_processed}")
    print(f"   Total errors: {total_errors}")
    print(f"   Total cards verified: {total_cards}")
    print(f"   Non-standard cards: {non_standard}")
    
    if non_standard == 0:
        print(f"\n✅ All cards are now 256x256 with transparent padding!")
    else:
        print(f"\n⚠ Some cards may need manual attention")

if __name__ == "__main__":
    main()