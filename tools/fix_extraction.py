#!/usr/bin/env python3
"""
Fix the extraction of front and side faces from angled ETB images
"""

import os
from pathlib import Path
from PIL import Image
import json

class FixedExtractor:
    def __init__(self, raw_dir="raw"):
        self.raw_dir = Path(raw_dir)
    
    def extract_front_from_angled(self, image_path):
        """Extract the front face from an angled box image - CORRECTED"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # For angled ETB images, the front face is the LEFT portion
            # But we want most of it, not just 60%
            # The front typically takes up about 75-80% of the width
            front_width = int(width * 0.75)
            
            # Crop to get the front face (left portion)
            front_crop = img.crop((0, 0, front_width, height))
            
            # Now resize to square by taking the center square
            # We want to preserve as much as possible
            min_dim = min(front_crop.size)
            
            # For the front, we want to keep it centered but not lose too much
            # Since ETBs are wider than tall, we'll fit to height
            if front_crop.width > front_crop.height:
                # Resize to make it square, keeping aspect ratio
                new_width = front_crop.height
                left = (front_crop.width - new_width) // 2
                front_crop = front_crop.crop((left, 0, left + new_width, front_crop.height))
            else:
                # Height is larger (unusual), fit to width
                new_height = front_crop.width
                top = (front_crop.height - new_height) // 2
                front_crop = front_crop.crop((0, top, front_crop.width, top + new_height))
            
            return front_crop
        except Exception as e:
            print(f"Error extracting front: {e}")
            return None
    
    def extract_side_from_angled(self, image_path):
        """Extract the side face from an angled box image - CORRECTED"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # The side is the RIGHT portion, about 35% of the image
            # (some overlap with front is fine)
            side_start = int(width * 0.65)
            
            # Crop to get the side face (right portion)
            side_crop = img.crop((side_start, 0, width, height))
            
            # Make it square
            min_dim = min(side_crop.size)
            if side_crop.width > side_crop.height:
                # Fit to height
                new_width = side_crop.height
                # For the side, we want the left part (closer to front)
                side_crop = side_crop.crop((0, 0, new_width, side_crop.height))
            else:
                # Fit to width
                new_height = side_crop.width
                top = (side_crop.height - new_height) // 2
                side_crop = side_crop.crop((0, top, side_crop.width, top + new_height))
            
            return side_crop
        except Exception as e:
            print(f"Error extracting side: {e}")
            return None
    
    def create_black_texture(self, size=256):
        """Create a plain black texture"""
        img = Image.new('RGB', (size, size), (0, 0, 0))
        return img
    
    def process_etb(self, variant_dir):
        """Re-process a single ETB variant"""
        variant_name = variant_dir.name
        print(f"Processing: {variant_name}")
        
        main_image = variant_dir / "main.jpg"
        
        if not main_image.exists():
            print(f"  No main.jpg found, skipping")
            return False
        
        # Extract front and side with corrected logic
        front_img = self.extract_front_from_angled(main_image)
        if front_img:
            front_img.save(variant_dir / "front.jpg", quality=95)
            print(f"  ✓ Fixed front face extraction")
        
        side_img = self.extract_side_from_angled(main_image)
        if side_img:
            # Save as both left and right (mirrored)
            side_img.save(variant_dir / "left.jpg", quality=95)
            side_img_flipped = side_img.transpose(Image.FLIP_LEFT_RIGHT)
            side_img_flipped.save(variant_dir / "right.jpg", quality=95)
            print(f"  ✓ Fixed side face extraction")
        
        # Keep black textures for back, top, bottom
        black = self.create_black_texture(256)
        black.save(variant_dir / "back.jpg", quality=95)
        black.save(variant_dir / "top.jpg", quality=95) 
        black.save(variant_dir / "bottom.jpg", quality=95)
        print(f"  ✓ Created black textures")
        
        return True
    
    def fix_all(self):
        """Fix all ETB extractions"""
        print("Fixing ETB Face Extractions")
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
        print(f"Fixed {fixed_count} ETB variants")
        print("Now re-run the rectification script to update textures")

def main():
    fixer = FixedExtractor()
    fixer.fix_all()

if __name__ == "__main__":
    main()