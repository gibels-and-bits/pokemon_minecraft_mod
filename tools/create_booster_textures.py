#!/usr/bin/env python3
"""
Convert booster pack images to Minecraft item textures
"""

from PIL import Image
from pathlib import Path

def create_minecraft_texture(input_path, output_path, size=128):
    """Convert booster pack image to Minecraft item texture, preserving full image"""
    img = Image.open(input_path)
    
    # Convert to RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create a square transparent canvas
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Calculate scaling to fit the entire image within the square
    width, height = img.size
    scale = min(size / width, size / height)
    
    # Scale the image to fit
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Calculate position to center the image on the canvas
    x = (size - new_width) // 2
    y = (size - new_height) // 2
    
    # Paste the resized image onto the canvas
    canvas.paste(img_resized, (x, y), img_resized)
    
    # Save
    canvas.save(output_path, 'PNG', optimize=True)
    return True

def main():
    print("Creating Minecraft Booster Pack Textures")
    print("=" * 60)
    
    input_dir = Path("raw_images/booster_packs_fixed")
    output_dir = Path("src/main/resources/assets/etbmod/textures/item")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all booster pack images
    count = 0
    for booster_file in input_dir.glob("etb_*_booster.png"):
        # Get the base name (e.g., "etb_151_booster")
        base_name = booster_file.stem
        
        # Create 128x128 texture - highest quality for items in Minecraft
        # Minecraft supports up to 512x512 for resource packs, but 128x128 is optimal for items
        output_file = output_dir / f"{base_name}.png"
        
        if create_minecraft_texture(booster_file, output_file, size=128):
            print(f"✓ Created: {output_file.name} (128x128)")
            count += 1
    
    print(f"\n✓ Created {count} booster pack textures")
    print(f"  Location: {output_dir}")

if __name__ == "__main__":
    main()