#!/usr/bin/env python3
"""
Generate metadata for sets that are missing it
"""

import json
import shutil
from pathlib import Path
import re
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def parse_card_filename(filename):
    """Parse card information from filename"""
    # Format: 001_common_pikachu.png or TG01_trainer_gallery_pikachu.png
    name = filename.stem
    parts = name.split('_')
    
    if len(parts) < 3:
        return None
    
    # Extract number, rarity, and name
    number = parts[0]
    rarity = parts[1]
    
    # Handle multi-word rarities
    if len(parts) > 3 and parts[1] in ['rare', 'trainer', 'illustration', 'special', 'ultra', 'double', 'hyper', 'ace']:
        # Could be "rare_holo", "trainer_gallery", etc.
        rarity_parts = []
        idx = 1
        while idx < len(parts) and parts[idx] in ['rare', 'holo', 'trainer', 'gallery', 'illustration', 
                                                    'special', 'ultra', 'double', 'hyper', 'v', 'vmax', 
                                                    'vstar', 'ex', 'gx', 'secret', 'spec', 'ace']:
            rarity_parts.append(parts[idx])
            idx += 1
        rarity = '_'.join(rarity_parts)
        card_name = '_'.join(parts[idx:])
    else:
        card_name = '_'.join(parts[2:])
    
    # Clean up card name
    card_name = card_name.replace('_', ' ').title()
    rarity = rarity.replace('_', ' ').title()
    
    return {
        'number': number,
        'name': card_name,
        'rarity': rarity,
        'filename': filename.name
    }

def generate_metadata_for_set(set_dir):
    """Generate metadata for a set"""
    png_files = sorted(set_dir.glob('*.png'))
    
    if not png_files:
        return None
    
    cards = []
    for png_file in png_files:
        card_info = parse_card_filename(png_file)
        if card_info:
            cards.append(card_info)
    
    metadata = {
        'set_name': set_dir.name.replace('_', ' ').title(),
        'folder_name': set_dir.name,
        'total_cards': len(cards),
        'cards': cards,
        'source': 'generated_from_filenames'
    }
    
    return metadata

def copy_backup_metadata(backup_path, dest_path):
    """Copy metadata from backup folder"""
    try:
        if backup_path.exists():
            shutil.copy2(backup_path, dest_path)
            logging.info(f"  ✓ Copied metadata from backup")
            return True
    except Exception as e:
        logging.error(f"  Error copying metadata: {e}")
    return False

def main():
    cards_dir = Path('raw_images/cards')
    backup_dir = Path('cards_backup')
    
    logging.info("Generating Missing Metadata")
    logging.info("=" * 60)
    
    # Sets that need metadata
    missing_metadata = [
        'black_bolt',
        'crown_zenith', 
        'shining_fates',
        'shrouded_fable',
        'white_flare',
        'xy2'
    ]
    
    for set_name in missing_metadata:
        set_dir = cards_dir / set_name
        if not set_dir.exists():
            logging.warning(f"Set directory not found: {set_name}")
            continue
        
        logging.info(f"\nProcessing: {set_name}")
        
        # Check if backup metadata exists
        backup_metadata = backup_dir / set_name / 'cards_metadata.json'
        dest_metadata = set_dir / 'cards_metadata.json'
        
        if backup_metadata.exists():
            # Copy from backup
            if copy_backup_metadata(backup_metadata, dest_metadata):
                # Also copy energy metadata if exists
                backup_energy = backup_dir / set_name / 'energy_cards_metadata.json'
                if backup_energy.exists():
                    dest_energy = set_dir / 'energy_cards_metadata.json'
                    shutil.copy2(backup_energy, dest_energy)
                    logging.info(f"  ✓ Also copied energy metadata")
            continue
        
        # Generate metadata from filenames
        logging.info(f"  Generating metadata from filenames...")
        metadata = generate_metadata_for_set(set_dir)
        
        if metadata:
            # Save metadata
            metadata_path = set_dir / 'cards_metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logging.info(f"  ✓ Generated metadata for {metadata['total_cards']} cards")
        else:
            logging.warning(f"  Could not generate metadata")
    
    # Final check
    logging.info("\n" + "=" * 60)
    logging.info("FINAL STATUS:")
    
    all_good = True
    for set_dir in sorted(cards_dir.glob('*')):
        if set_dir.is_dir():
            png_count = len(list(set_dir.glob('*.png')))
            json_count = len(list(set_dir.glob('*.json')))
            
            if png_count > 0 and json_count == 0:
                logging.warning(f"  {set_dir.name}: Still missing metadata")
                all_good = False
    
    if all_good:
        logging.info("  ✓ All sets have metadata!")
    
    logging.info("=" * 60)

if __name__ == "__main__":
    main()