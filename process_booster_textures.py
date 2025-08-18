#!/usr/bin/env python3
import os
from PIL import Image
import glob

# Input and output directories
RAW_DIR = "raw_images/booster_packs"
OUTPUT_DIR = "src/main/resources/assets/etbmod/textures/item"

# Minecraft texture size - using 32x48 for portrait orientation (2:3 ratio like real packs)
TEXTURE_WIDTH = 32
TEXTURE_HEIGHT = 48

# Mapping of raw file names to booster pack names
BOOSTER_MAPPINGS = {
    "black_bolt_booster": "etb_black_bolt_booster",
    "breakpoint_booster_pack": "etb_breakpoint_booster",
    "brilliant_stars_booster": "etb_brilliant_stars_booster",
    "burning_shadows_booster_pack": "etb_burning_shadows_booster",
    "cosmic_eclipse_booster_pack": "etb_cosmic_eclipse_booster",
    "crown_zenith_booster_pack": "etb_crown_zenith_booster",
    "destined_rivals": "etb_destined_rivals_booster",
    "evolutions_booster_pack": "etb_evolutions_booster",
    "evolving_skies_booster_pack": "etb_evolving_skies_booster",
    "generations_booster": "etb_generations_booster",
    "hidden_fates_booster_pack": "etb_hidden_fates_booster",
    "journey_together_booster": "etb_journey_together_booster",
    "phantom_forces_booster_pack": "etb_phantom_forces_booster",
    "primal_clash_booster": "etb_primal_clash_booster",
    "primal_clash_booster_pack": "etb_primal_clash_booster",
    "prismatic_evolutions_booster": "etb_prismatic_evolutions_booster",
    "rebel_clash_booster_pack": "etb_rebel_clash_booster",
    "shining_fates_booster_pack": "etb_shining_fates_booster",
    "surging_sparks_booster": "etb_surging_sparks_booster",
    "team_up_booster_pack": "etb_team_up_booster",
    "unified_minds_booster_pack": "etb_unified_minds_booster",
    "vivid_voltage_booster": "etb_vivid_voltage_booster",
    "white_flair_booster": "etb_white_flare_booster"
}

def remove_white_background(img, threshold=240):
    """Remove white background from image and make it transparent"""
    img = img.convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # Check if pixel is white-ish
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            # Make it transparent
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    return img

def auto_crop(img):
    """Auto-crop the image to remove transparent/white borders"""
    # Get the bounding box of non-transparent pixels
    bbox = img.getbbox()
    if bbox:
        return img.crop(bbox)
    return img

def process_booster_image(input_path, output_name):
    """Process a booster pack image to Minecraft texture format"""
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Remove white background
        img = remove_white_background(img)
        
        # Auto-crop to remove excess transparent/white space
        img = auto_crop(img)
        
        # Calculate aspect ratio after cropping
        width, height = img.size
        aspect_ratio = width / height
        
        # Resize to fit the portrait format while maintaining aspect ratio
        if aspect_ratio > (TEXTURE_WIDTH / TEXTURE_HEIGHT):
            # Image is wider than target ratio, fit by height
            new_height = TEXTURE_HEIGHT
            new_width = int(new_height * aspect_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Crop horizontally to center
            left = (new_width - TEXTURE_WIDTH) // 2
            img = img.crop((left, 0, left + TEXTURE_WIDTH, TEXTURE_HEIGHT))
        else:
            # Image is taller than target ratio, fit by width
            new_width = TEXTURE_WIDTH
            new_height = int(new_width / aspect_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Crop vertically to center
            top = (new_height - TEXTURE_HEIGHT) // 2
            img = img.crop((0, top, TEXTURE_WIDTH, top + TEXTURE_HEIGHT))
        
        # Ensure exact dimensions
        if img.size != (TEXTURE_WIDTH, TEXTURE_HEIGHT):
            img = img.resize((TEXTURE_WIDTH, TEXTURE_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save the texture
        output_path = os.path.join(OUTPUT_DIR, f"{output_name}.png")
        img.save(output_path, "PNG", optimize=True)
        print(f"✓ Processed {os.path.basename(input_path)} -> {output_name}.png")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return False

def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Process all booster pack images
    processed_count = 0
    error_count = 0
    
    # Get all image files in raw directory
    image_files = glob.glob(os.path.join(RAW_DIR, "*"))
    
    for file_path in image_files:
        if not os.path.isfile(file_path):
            continue
            
        # Get base name without extension
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Find matching mapping
        output_name = None
        for raw_name, texture_name in BOOSTER_MAPPINGS.items():
            if raw_name in base_name:
                output_name = texture_name
                break
        
        if output_name:
            if process_booster_image(file_path, output_name):
                processed_count += 1
            else:
                error_count += 1
        else:
            print(f"⚠ No mapping found for {base_name}")
    
    print(f"\n✅ Processing complete: {processed_count} textures created, {error_count} errors")

if __name__ == "__main__":
    main()