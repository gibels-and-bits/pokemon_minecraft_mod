#!/usr/bin/env python3
"""
Process Black Bolt and White Flare cards from backup
"""

import shutil
from pathlib import Path
from PIL import Image
import logging
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def normalize_filename(filename):
    """Normalize the filename format"""
    # Already in correct format from backup
    # Just need to make lowercase and replace spaces with underscores
    name = filename.replace(' ', '_').lower()
    # Remove any special characters except underscores
    name = re.sub(r'[^\w\.]', '_', name)
    # Clean up multiple underscores
    name = re.sub(r'_+', '_', name)
    return name

def process_card(source_path, dest_dir):
    """Process a single card - resize and save"""
    try:
        filename = normalize_filename(source_path.name)
        dest_path = dest_dir / filename
        
        if dest_path.exists():
            logging.debug(f"  Skipping {filename} - already exists")
            return True
        
        # Open and resize image
        with Image.open(source_path) as img:
            # Calculate new size (256px height)
            aspect = img.width / img.height
            new_h = 256
            new_w = int(new_h * aspect)
            
            # Resize
            img_resized = img.resize((new_w, new_h), Image.LANCZOS)
            
            # Save as PNG
            if img_resized.mode in ('RGBA', 'LA', 'P'):
                img_resized.save(dest_path, 'PNG')
            else:
                img_resized.convert('RGB').save(dest_path, 'PNG')
        
        logging.debug(f"  ✓ Processed: {filename}")
        return True
        
    except Exception as e:
        logging.error(f"  Error processing {source_path.name}: {e}")
        return False

def process_set(set_name, source_folder, dest_folder):
    """Process an entire set"""
    source_dir = Path(source_folder)
    dest_dir = Path(dest_folder)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"\n{'='*60}")
    logging.info(f"Processing {set_name}")
    logging.info(f"{'='*60}")
    
    # Get all PNG files
    png_files = list(source_dir.glob("*.png"))
    logging.info(f"Found {len(png_files)} cards to process")
    
    successful = 0
    failed = []
    
    for i, png_file in enumerate(png_files, 1):
        if process_card(png_file, dest_dir):
            successful += 1
        else:
            failed.append(png_file.name)
        
        # Progress update
        if i % 20 == 0:
            logging.info(f"Progress: {i}/{len(png_files)} cards processed")
    
    # Final report
    logging.info(f"\n✓ Complete: {successful} cards successfully processed")
    if failed:
        logging.warning(f"Failed: {len(failed)} cards")
        for name in failed[:5]:
            logging.warning(f"  - {name}")
        if len(failed) > 5:
            logging.warning(f"  ... and {len(failed)-5} more")
    
    return successful

def main():
    logging.info("Black Bolt & White Flare Card Processor")
    logging.info("=" * 60)
    
    # Process Black Bolt
    black_bolt_count = process_set(
        "Black Bolt",
        "cards_backup/black_bolt",
        "raw_images/cards/black_bolt"
    )
    
    # Process White Flare  
    white_flare_count = process_set(
        "White Flare",
        "cards_backup/white_flare",
        "raw_images/cards/white_flare"
    )
    
    # Final summary
    logging.info("\n" + "=" * 60)
    logging.info("PROCESSING COMPLETE")
    logging.info(f"Black Bolt: {black_bolt_count} cards")
    logging.info(f"White Flare: {white_flare_count} cards")
    logging.info(f"Total: {black_bolt_count + white_flare_count} cards")
    logging.info("=" * 60)

if __name__ == "__main__":
    main()