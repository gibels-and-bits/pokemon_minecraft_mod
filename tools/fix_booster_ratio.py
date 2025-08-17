#!/usr/bin/env python3
"""
Fix booster pack images to have the correct aspect ratio
Real Pokemon booster packs are 2.6" wide x 4.6" tall
Aspect ratio: 2.6:4.6 = 0.565 (width/height)
"""

from PIL import Image
import numpy as np
from pathlib import Path
import shutil

def auto_crop_white(img):
    """Remove white/near-white borders from image"""
    # Convert to numpy array
    data = np.array(img)
    
    # Create mask for non-white pixels
    if img.mode == 'RGBA':
        # Check RGB channels for non-white and alpha for non-transparent
        rgb_sum = np.sum(data[:, :, :3], axis=2)
        not_white = (rgb_sum < 740) | (data[:, :, 3] < 250)  # Not near-white or transparent
    else:
        # For RGB images
        rgb_sum = np.sum(data[:, :, :3], axis=2)
        not_white = rgb_sum < 740  # Not near-white (3*247)
    
    # Find bounding box
    rows = np.any(not_white, axis=1)
    cols = np.any(not_white, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        return img  # All white, return as-is
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # Add tiny padding (1 pixel)
    padding = 1
    rmin = max(0, rmin - padding)
    rmax = min(data.shape[0], rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(data.shape[1], cmax + padding)
    
    # Crop the image
    return img.crop((cmin, rmin, cmax, rmax))

def fix_booster_ratio(input_path, output_path, target_ratio=0.565):
    """
    First remove white borders, then crop to match Pokemon booster pack aspect ratio
    Target ratio is width/height = 2.6/4.6 = 0.565
    """
    img = Image.open(input_path)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Step 1: Remove white borders
    img = auto_crop_white(img)
    
    current_width, current_height = img.size
    current_ratio = current_width / current_height
    
    if abs(current_ratio - target_ratio) < 0.01:
        # Already close to correct ratio
        img.save(output_path, 'PNG', optimize=True)
        return "already correct"
    
    # Calculate new dimensions maintaining the target ratio
    if current_ratio > target_ratio:
        # Image is too wide, crop width
        new_width = int(current_height * target_ratio)
        new_height = current_height
        # Center crop horizontally
        left = (current_width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = current_height
    else:
        # Image is too tall, crop height
        new_width = current_width
        new_height = int(current_width / target_ratio)
        # Crop from top (usually has less important info at bottom)
        left = 0
        top = 0
        right = current_width
        bottom = new_height
    
    # Crop the image
    cropped = img.crop((left, top, right, bottom))
    
    # Save with optimization
    cropped.save(output_path, 'PNG', optimize=True)
    
    return f"{current_width}x{current_height} -> {new_width}x{new_height}"

def main():
    print("Fixing Booster Pack Aspect Ratios")
    print("=" * 60)
    print("Target ratio: 2.6:4.6 (width:height)")
    print()
    
    # Create backup first
    input_dir = Path("raw_images/booster_packs_clean")
    backup_dir = Path("raw_images/booster_packs_clean_backup")
    output_dir = Path("raw_images/booster_packs_fixed")
    
    # Backup existing files
    if input_dir.exists() and not backup_dir.exists():
        shutil.copytree(input_dir, backup_dir)
        print(f"✓ Created backup in {backup_dir}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all booster pack images
    count = 0
    for booster_file in input_dir.glob("etb_*_booster.png"):
        output_file = output_dir / booster_file.name
        
        result = fix_booster_ratio(booster_file, output_file)
        
        if result == "already correct":
            print(f"✓ {booster_file.name}: Already correct ratio")
        else:
            print(f"✓ {booster_file.name}: Fixed ratio ({result})")
        
        count += 1
    
    print(f"\n✓ Processed {count} booster pack images")
    print(f"  Output: {output_dir}")
    
    # Show final dimensions
    print("\nFinal dimensions:")
    for output_file in sorted(output_dir.glob("*.png")):
        img = Image.open(output_file)
        ratio = img.width / img.height
        print(f"  • {output_file.name}: {img.width}x{img.height} (ratio: {ratio:.3f})")

if __name__ == "__main__":
    main()