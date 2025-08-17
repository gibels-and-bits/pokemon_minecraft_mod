#!/usr/bin/env python3
"""
Fix texture dimensions - ensure all 183x256 raw cards become 256x256 textures
"""

from pathlib import Path
from PIL import Image
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def fix_texture(texture_path):
    """Fix a texture to be 256x256 if needed"""
    img = Image.open(texture_path)
    
    # If already 256x256, skip
    if img.width == 256 and img.height == 256:
        return False
    
    # If 128x256, need to re-pad to 256x256
    if img.width == 128 and img.height == 256:
        # Create new 256x256 transparent image
        new_img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        
        # Center the 128x256 image
        x_offset = (256 - 128) // 2
        new_img.paste(img, (x_offset, 0), img if img.mode == 'RGBA' else None)
        
        # Save back
        new_img.save(texture_path, 'PNG')
        return True
    
    return False

def main():
    texture_base = Path("src/main/resources/assets/etbmod/textures/cards")
    
    # Sets that should have 256x256 textures (from raw 183x256)
    sets_to_fix = [
        'surging_sparks',
        'groudon',
        'kyogre',
    ]
    
    logging.info("Fixing texture dimensions to 256x256")
    logging.info("=" * 60)
    
    for set_name in sets_to_fix:
        set_dir = texture_base / set_name
        if not set_dir.exists():
            logging.warning(f"Set not found: {set_name}")
            continue
        
        fixed = 0
        cards = list(set_dir.glob("*.png"))
        
        for card_path in cards:
            if fix_texture(card_path):
                fixed += 1
        
        if fixed > 0:
            logging.info(f"✓ {set_name}: Fixed {fixed}/{len(cards)} cards to 256x256")
        else:
            # Check if already correct
            if cards:
                img = Image.open(cards[0])
                logging.info(f"  {set_name}: Already {img.width}x{img.height}")
    
    logging.info("=" * 60)

if __name__ == "__main__":
    main()