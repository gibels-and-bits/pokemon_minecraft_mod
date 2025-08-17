#!/usr/bin/env python3
"""
CORRECTED extraction of front and side faces from angled ETB images
The FRONT is the main artwork (right/larger portion)
The SIDE is the thin edge (left portion)
"""

import os
from pathlib import Path
from PIL import Image
import json

class CorrectExtractor:
    def __init__(self, raw_dir="raw"):
        self.raw_dir = Path(raw_dir)
    
    def extract_front_from_angled(self, image_path):
        """Extract the FRONT face (main artwork) from an angled box image"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # The FRONT is the main portion on the RIGHT
            # Skip the thin side strip on the left (about 15-20% of width)
            side_width = int(width * 0.18)  # The thin side strip
            
            # Crop to get the front face (right portion, main artwork)
            front_crop = img.crop((side_width, 0, width, height))
            
            # Now make it square by fitting to the shorter dimension
            # We want to preserve the main artwork
            if front_crop.width > front_crop.height:
                # Width is larger, fit to height and center horizontally
                new_width = front_crop.height
                left = (front_crop.width - new_width) // 2
                front_crop = front_crop.crop((left, 0, left + new_width, front_crop.height))
            else:
                # Height is larger, fit to width and center vertically
                new_height = front_crop.width
                top = (front_crop.height - new_height) // 2
                front_crop = front_crop.crop((0, top, front_crop.width, top + new_height))
            
            return front_crop
        except Exception as e:
            print(f"Error extracting front: {e}")
            return None
    
    def extract_side_from_angled(self, image_path):
        """Extract the SIDE face (thin strip with Pokemon logo) from an angled box image"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # The SIDE is the thin strip on the LEFT (about 15-20% of width)
            side_width = int(width * 0.20)
            
            # Crop to get the side face (left thin strip)
            side_crop = img.crop((0, 0, side_width, height))
            
            # The side is very thin, so we'll need to stretch it to make it square
            # Or we can tile it / repeat it
            # For now, let's just resize it to square (it will be stretched)
            side_square = side_crop.resize((256, 256), Image.Resampling.LANCZOS)
            
            return side_square
        except Exception as e:
            print(f"Error extracting side: {e}")
            return None
    
    def create_black_texture(self, size=256):
        """Create a plain black texture"""
        img = Image.new('RGB', (size, size), (0, 0, 0))
        return img
    
    def process_etb(self, variant_dir):
        """Re-process a single ETB variant with correct extraction"""
        variant_name = variant_dir.name
        print(f"Processing: {variant_name}")
        
        main_image = variant_dir / "main.jpg"
        
        if not main_image.exists():
            print(f"  No main.jpg found, skipping")
            return False
        
        # Extract front (main artwork) and side (thin strip) correctly
        front_img = self.extract_front_from_angled(main_image)
        if front_img:
            front_img.save(variant_dir / "front.jpg", quality=95)
            print(f"  ✓ Extracted front face (main artwork)")
        
        side_img = self.extract_side_from_angled(main_image)
        if side_img:
            # Save as both left and right
            side_img.save(variant_dir / "left.jpg", quality=95)
            side_img.save(variant_dir / "right.jpg", quality=95)
            print(f"  ✓ Extracted side faces (Pokemon logo strip)")
        
        # Keep black textures for back, top, bottom
        black = self.create_black_texture(256)
        black.save(variant_dir / "back.jpg", quality=95)
        black.save(variant_dir / "top.jpg", quality=95) 
        black.save(variant_dir / "bottom.jpg", quality=95)
        print(f"  ✓ Created black textures for other faces")
        
        return True
    
    def fix_all(self):
        """Fix all ETB extractions with correct orientation"""
        print("Correcting ETB Face Extractions")
        print("=" * 50)
        print("Front = Main artwork (Snorlax, etc.)")
        print("Side = Thin strip with Pokemon logo")
        print("=" * 50)
        
        # Process all variant directories
        variant_dirs = [d for d in self.raw_dir.iterdir() if d.is_dir()]
        
        if not variant_dirs:
            print("No variant directories found!")
            return
        
        fixed_count = 0
        for variant_dir in variant_dirs:
            if self.process_etb(variant_dir):
                fixed_count += 1
        
        print("\n" + "=" * 50)
        print(f"Corrected {fixed_count} ETB variants")
        print("Now re-run the rectification script to update textures")

def main():
    fixer = CorrectExtractor()
    fixer.fix_all()

if __name__ == "__main__":
    main()