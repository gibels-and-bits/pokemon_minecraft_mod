#!/usr/bin/env python3
"""
Booster Pack Pipeline for Pokemon ETB Minecraft Mod
====================================================

This script processes booster pack images from various formats into game-ready textures.

Usage:
    python booster_pack_pipeline.py <set_name> <input_image_path>
    
Example:
    python booster_pack_pipeline.py stellar_crown raw_images/stellar_crown_booster.png
    python booster_pack_pipeline.py stellar_crown raw_images/stellar_crown_booster.webp

The script will:
1. Process the input image (supports PNG, JPG, WEBP)
2. Remove white borders
3. Create a 128x128 booster pack texture
4. Create a 64x64 ETB block texture
5. Register the set in the mod if needed
6. Provide instructions for final integration
"""

import sys
import os
from PIL import Image, ImageOps
import numpy as np
from pathlib import Path
import json

class BoosterPackPipeline:
    def __init__(self, mod_path="/Users/gibels_and_bits/Development/etb-mod"):
        self.mod_path = Path(mod_path)
        self.textures_path = self.mod_path / "src/main/resources/assets/etbmod/textures"
        self.item_textures_path = self.textures_path / "item"
        self.block_textures_path = self.textures_path / "block"
        
        # Ensure directories exist
        self.item_textures_path.mkdir(parents=True, exist_ok=True)
        self.block_textures_path.mkdir(parents=True, exist_ok=True)
    
    def remove_white_border(self, img, threshold=240):
        """Remove white/light border from image."""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Convert to numpy array
        data = np.array(img)
        
        # Create mask of non-white pixels
        mask = np.any(data[:, :, :3] < threshold, axis=2)
        
        # Find bounding box
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            print("Warning: No non-white pixels found, returning original image")
            return img
        
        # Get the bounds
        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]
        
        # Add small padding
        padding = 5
        top = max(0, top - padding)
        bottom = min(data.shape[0], bottom + padding + 1)
        left = max(0, left - padding)
        right = min(data.shape[1], right + padding + 1)
        
        # Crop the image
        return img.crop((left, top, right, bottom))
    
    def create_booster_texture(self, img, set_name):
        """Create a 128x128 booster pack texture."""
        # Remove white border
        img = self.remove_white_border(img)
        print(f"  After border removal: {img.size}")
        
        # Create a new 128x128 image with transparent background
        final_img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        
        # Calculate size to fit in 128x128 while maintaining aspect ratio
        # Leave some padding like the other boosters
        max_size = 120  # Leave 4 pixels padding on each side
        
        # Calculate the scaling needed
        scale = min(max_size / img.width, max_size / img.height)
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        
        # Resize the image
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center the image in the 128x128 canvas
        x_offset = (128 - new_width) // 2
        y_offset = (128 - new_height) // 2
        
        # Paste the resized image onto the canvas
        final_img.paste(img_resized, (x_offset, y_offset), img_resized)
        
        # Save the booster texture
        output_path = self.item_textures_path / f"etb_{set_name}_booster.png"
        final_img.save(output_path, 'PNG')
        print(f"  Saved booster texture: {output_path}")
        
        return final_img
    
    def create_etb_texture(self, img, set_name):
        """Create a 64x64 ETB block texture atlas."""
        # ETB textures are 64x64 with different faces
        etb_img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        
        # Create a 16x16 version for each face
        face_img = img.resize((16, 16), Image.Resampling.LANCZOS)
        
        # Layout for Minecraft block texture:
        # Top face (0, 0)
        etb_img.paste(face_img, (0, 0))
        # Bottom face (16, 0)
        etb_img.paste(face_img, (16, 0))
        # Front face (32, 0)
        etb_img.paste(face_img, (32, 0))
        # Back face (48, 0)
        etb_img.paste(face_img, (48, 0))
        # Left face (0, 16)
        etb_img.paste(face_img, (0, 16))
        # Right face (16, 16)
        etb_img.paste(face_img, (16, 16))
        
        # Save the ETB texture
        output_path = self.block_textures_path / f"etb_{set_name}.png"
        etb_img.save(output_path, 'PNG')
        print(f"  Saved ETB block texture: {output_path}")
        
        return etb_img
    
    def process_booster_pack(self, set_name, input_path):
        """Main processing function."""
        print(f"\n{'='*60}")
        print(f"Processing booster pack for set: {set_name}")
        print(f"{'='*60}")
        
        # Validate input
        input_file = Path(input_path)
        if not input_file.exists():
            print(f"Error: Input file not found: {input_path}")
            return False
        
        # Normalize set name (lowercase, underscores)
        set_name = set_name.lower().replace(' ', '_').replace('-', '_')
        print(f"Normalized set name: {set_name}")
        
        try:
            # Load the image
            print(f"\nLoading image: {input_path}")
            img = Image.open(input_path)
            print(f"  Original size: {img.size}")
            print(f"  Mode: {img.mode}")
            
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                print("  Converted to RGBA")
            
            # Create booster pack texture (128x128)
            print("\nCreating booster pack texture (128x128)...")
            booster_img = self.create_booster_texture(img, set_name)
            
            # Create ETB block texture (64x64)
            print("\nCreating ETB block texture (64x64)...")
            self.create_etb_texture(booster_img, set_name)
            
            # Generate integration instructions
            self.print_integration_instructions(set_name)
            
            return True
            
        except Exception as e:
            print(f"\nError processing image: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def print_integration_instructions(self, set_name):
        """Print instructions for integrating the new set into the mod."""
        print(f"\n{'='*60}")
        print("INTEGRATION INSTRUCTIONS")
        print(f"{'='*60}")
        print(f"\nTo complete the integration of '{set_name}' into the mod:\n")
        
        print("1. TEXTURES CREATED:")
        print(f"   ✓ Booster pack: etb_{set_name}_booster.png")
        print(f"   ✓ ETB block: etb_{set_name}.png")
        
        print("\n2. NEXT STEPS (if this is a new set):")
        print(f"   a) Add to ModBlocks.java:")
        print(f'      public static final RegistryObject<Block> ETB_{set_name.upper()} = ')
        print(f'          registerBlock("etb_{set_name}", ')
        print(f'              () -> new ETBBlock("etb_{set_name}"));')
        
        print(f"\n   b) Add to ModItems.java:")
        print(f'      BOOSTER_PACKS.put("{set_name}", ITEMS.register(')
        print(f'          "etb_{set_name}_booster", ')
        print(f'          () -> new BoosterPackItem("{set_name}")));')
        
        print(f"\n   c) Create card metadata file:")
        print(f"      src/main/resources/assets/etbmod/textures/cards/{set_name}/cards_metadata.json")
        
        print(f"\n   d) Add card images to:")
        print(f"      src/main/resources/assets/etbmod/textures/cards/{set_name}/")
        
        print(f"\n   e) Create lang entries in en_us.json:")
        print(f'      "block.etbmod.etb_{set_name}": "{set_name.replace("_", " ").title()} ETB",')
        print(f'      "item.etbmod.etb_{set_name}_booster": "{set_name.replace("_", " ").title()} Booster Pack",')
        
        print("\n3. REBUILD THE MOD:")
        print("   ./gradlew clean build")
        
        print(f"\n{'='*60}\n")

def main():
    """Main entry point."""
    # Check command line arguments
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    set_name = sys.argv[1]
    input_path = sys.argv[2]
    
    # Create pipeline instance
    pipeline = BoosterPackPipeline()
    
    # Process the booster pack
    success = pipeline.process_booster_pack(set_name, input_path)
    
    if success:
        print("✅ Pipeline completed successfully!")
    else:
        print("❌ Pipeline failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()