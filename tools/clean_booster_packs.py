#!/usr/bin/env python3
"""
Clean up and standardize booster pack images
- Convert all to PNG
- Auto-crop to remove white borders
- Resize to consistent dimensions
- Apply proper naming convention
"""

from PIL import Image
import numpy as np
from pathlib import Path
import os

def auto_crop_image(img):
    """Auto-crop image to remove white/transparent borders"""
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get image as numpy array
    data = np.array(img)
    
    # Find non-transparent/non-white pixels
    # Check for both alpha channel and white pixels
    if data.shape[2] == 4:  # Has alpha channel
        non_empty = (data[:, :, 3] > 10)  # Alpha > 10
    else:
        # Convert to grayscale for white detection
        gray = np.mean(data[:, :, :3], axis=2)
        non_empty = gray < 250  # Not white
    
    # Also check for near-white pixels in RGB
    if data.shape[2] >= 3:
        rgb_sum = np.sum(data[:, :, :3], axis=2)
        not_white = rgb_sum < 740  # Not near-white (3*247)
        non_empty = non_empty | not_white
    
    # Find bounding box
    rows = np.any(non_empty, axis=1)
    cols = np.any(non_empty, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        # Image is all white/transparent, return as-is
        return img
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # Add small padding (2 pixels)
    padding = 2
    rmin = max(0, rmin - padding)
    rmax = min(data.shape[0], rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(data.shape[1], cmax + padding)
    
    # Crop the image
    return img.crop((cmin, rmin, cmax, rmax))

def process_booster_pack(input_path, output_path, target_height=512):
    """Process a single booster pack image"""
    try:
        # Open image
        img = Image.open(input_path)
        
        # Auto-crop to remove borders
        img = auto_crop_image(img)
        
        # Calculate new dimensions maintaining aspect ratio
        aspect_ratio = img.width / img.height
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
        
        # Resize image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGBA for consistency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Save as PNG
        img.save(output_path, 'PNG', optimize=True)
        
        return True, f"✓ Processed: {input_path.name} -> {output_path.name} ({new_width}x{new_height})"
        
    except Exception as e:
        return False, f"✗ Error processing {input_path.name}: {e}"

def main():
    """Process all booster pack images"""
    print("Cleaning and Standardizing Booster Pack Images")
    print("=" * 60)
    
    # Directories
    input_dir = Path("raw_images/booster_packs")
    output_dir = Path("raw_images/booster_packs_clean")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Mapping of filenames to ETB names
    filename_mapping = {
        "151_booster": "etb_151",
        "black_bolt_booster": "etb_black_bolt",
        "brilliant_stars_booster": "etb_brilliant_stars",
        "celebration_booster": "etb_celebrations",
        "destined_rivals": "etb_destined_rivals",
        "generations_booster": "etb_generations",
        "journey_together_booster": "etb_journey_together",
        "primal_clash_booster": "etb_groudon",  # Assuming Groudon variant
        "prismatic_evolutions_booster": "etb_prismatic_evolutions",
        "surging_sparks_booster": "etb_surging_sparks",
        "white_flair_booster": "etb_white_flare"
    }
    
    # Process each file
    processed = 0
    failed = 0
    
    for file_path in input_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
            # Get base name without extension
            base_name = file_path.stem
            
            # Find matching ETB name
            etb_name = None
            for key, value in filename_mapping.items():
                if key in base_name or key.replace('_', '') in base_name.replace('_', ''):
                    etb_name = value
                    break
            
            if not etb_name:
                print(f"⚠ Could not match: {file_path.name}")
                continue
            
            # Process the image
            output_path = output_dir / f"{etb_name}_booster.png"
            success, message = process_booster_pack(file_path, output_path)
            print(message)
            
            if success:
                processed += 1
            else:
                failed += 1
    
    # Also create a copy for Kyogre (same as Groudon for Primal Clash)
    groudon_path = output_dir / "etb_groudon_booster.png"
    if groudon_path.exists():
        kyogre_path = output_dir / "etb_kyogre_booster.png"
        img = Image.open(groudon_path)
        img.save(kyogre_path, 'PNG')
        print(f"✓ Created Kyogre variant from Primal Clash")
        processed += 1
    
    print("\n" + "=" * 60)
    print(f"Processing Complete!")
    print(f"  ✓ Processed: {processed} images")
    print(f"  ✗ Failed: {failed} images")
    print(f"  Output directory: {output_dir}")
    
    # List all output files
    print("\nGenerated booster pack images:")
    for output_file in sorted(output_dir.glob("*.png")):
        size = os.path.getsize(output_file)
        img = Image.open(output_file)
        print(f"  • {output_file.name}: {img.width}x{img.height} ({size//1024}KB)")

if __name__ == "__main__":
    main()