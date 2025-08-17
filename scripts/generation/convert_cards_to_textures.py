#!/usr/bin/env python3
"""
Convert Pokemon cards to power-of-2 textures with transparent padding
Cards are centered horizontally in the transparent background
"""

import shutil
from pathlib import Path
from PIL import Image
import logging
import math

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def next_power_of_2(n):
    """Find the next power of 2 greater than or equal to n"""
    if n <= 0:
        return 1
    # If n is already a power of 2, return it
    if (n & (n - 1)) == 0:
        return n
    # Find the next power of 2
    power = 1
    while power < n:
        power *= 2
    return power

def convert_card_to_texture(source_path, dest_path):
    """Convert a card to power-of-2 texture with transparent padding"""
    try:
        # Open the source image
        img = Image.open(source_path)
        
        # Get current dimensions
        width, height = img.size
        
        # Calculate power-of-2 dimensions
        new_width = next_power_of_2(width)
        new_height = next_power_of_2(height)
        
        # If already power of 2, just copy
        if width == new_width and height == new_height:
            # Ensure RGBA mode for consistency
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img.save(dest_path, 'PNG')
            return True
        
        # Create new image with transparent background
        # Use RGBA for transparency support
        new_img = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        
        # Convert source to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Calculate position to center the card horizontally
        x_offset = (new_width - width) // 2
        y_offset = 0  # No vertical centering needed since height is already 256
        
        # Paste the card onto the transparent background
        new_img.paste(img, (x_offset, y_offset), img)
        
        # Save the result
        new_img.save(dest_path, 'PNG')
        
        return True
        
    except Exception as e:
        logging.error(f"Error converting {source_path.name}: {e}")
        return False

def process_set(set_name, source_dir, dest_dir):
    """Process all cards in a set"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    if not source_path.exists():
        logging.warning(f"Source directory not found: {source_path}")
        return 0
    
    # Create destination directory
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Get all PNG files
    png_files = list(source_path.glob("*.png"))
    
    if not png_files:
        logging.warning(f"No PNG files found in {source_path}")
        return 0
    
    logging.info(f"Processing {set_name}: {len(png_files)} cards")
    
    successful = 0
    for i, png_file in enumerate(png_files, 1):
        dest_file = dest_path / png_file.name
        
        # Skip if already exists
        if dest_file.exists():
            successful += 1
            continue
        
        if convert_card_to_texture(png_file, dest_file):
            successful += 1
        
        # Progress update
        if i % 50 == 0:
            logging.info(f"  Progress: {i}/{len(png_files)} cards")
    
    return successful

def main():
    logging.info("Pokemon Card to Texture Converter")
    logging.info("=" * 60)
    
    # Source and destination directories
    source_base = Path("raw_images/cards")
    dest_base = Path("src/main/resources/assets/etbmod/textures/cards")
    
    # Create destination if it doesn't exist
    dest_base.mkdir(parents=True, exist_ok=True)
    
    # Get all sets from raw_images
    sets = [d for d in source_base.iterdir() if d.is_dir() and list(d.glob("*.png"))]
    
    logging.info(f"Found {len(sets)} sets to process")
    logging.info("")
    
    total_cards = 0
    processed_sets = []
    
    for set_dir in sorted(sets):
        set_name = set_dir.name
        source_dir = source_base / set_name
        dest_dir = dest_base / set_name
        
        count = process_set(set_name, source_dir, dest_dir)
        if count > 0:
            total_cards += count
            processed_sets.append((set_name, count))
            logging.info(f"  ✓ {set_name}: {count} cards")
    
    # Also copy metadata files
    logging.info("\nCopying metadata files...")
    for set_dir in sets:
        set_name = set_dir.name
        source_dir = source_base / set_name
        dest_dir = dest_base / set_name
        
        # Copy any JSON metadata files
        for json_file in source_dir.glob("*.json"):
            dest_json = dest_dir / json_file.name
            if not dest_json.exists():
                shutil.copy2(json_file, dest_json)
                logging.info(f"  Copied {set_name}/{json_file.name}")
    
    # Final summary
    logging.info("\n" + "=" * 60)
    logging.info("CONVERSION COMPLETE")
    logging.info(f"Total sets processed: {len(processed_sets)}")
    logging.info(f"Total cards converted: {total_cards}")
    
    # Check dimensions of a sample output
    if processed_sets:
        sample_set = processed_sets[0][0]
        sample_dir = dest_base / sample_set
        sample_files = list(sample_dir.glob("*.png"))[:1]
        if sample_files:
            img = Image.open(sample_files[0])
            logging.info(f"\nSample output dimensions: {img.width}x{img.height}")
            logging.info(f"Power of 2: Width={bin(img.width).count('1')==1}, Height={bin(img.height).count('1')==1}")
    
    logging.info("=" * 60)

if __name__ == "__main__":
    main()