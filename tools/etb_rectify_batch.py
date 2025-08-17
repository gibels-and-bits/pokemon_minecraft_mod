#!/usr/bin/env python3
"""
ETB Image Rectification and Texture Assembly
Converts angled photos to orthographic faces and assembles Minecraft textures
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

class ETBRectifier:
    def __init__(self, input_dir="raw", output_dir="src/main/resources/assets/etbmod/textures/block"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Minecraft texture size (can be 16, 32, 64, or 128)
        self.texture_size = 32
        
        # Face assignments for ETB
        self.face_map = {
            'front': 'etb_front',
            'back': 'etb_back',
            'left': 'etb_left',
            'right': 'etb_right',
            'top': 'etb_top',
            'bottom': 'etb_bottom'
        }

    def process_image(self, image_path, target_size=None):
        """Process a single image - resize and enhance"""
        if target_size is None:
            target_size = self.texture_size
        
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Find the main content area (simple center crop for now)
            width, height = img.size
            
            # Assuming ETB images are roughly rectangular
            # Crop to square from center
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            
            img = img.crop((left, top, right, bottom))
            
            # Resize to target size
            img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Enhance for Minecraft (optional)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)  # Slight contrast boost
            
            return img
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None

    def create_default_texture(self, color=(128, 128, 128), text=None):
        """Create a default texture when image is missing"""
        img = Image.new('RGB', (self.texture_size, self.texture_size), color)
        
        if text:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            # Use default font
            try:
                # Try to draw some text to indicate the face
                text_color = tuple(255 - c for c in color)  # Contrast color
                draw.text((2, 2), text[:1].upper(), fill=text_color)
            except:
                pass
        
        return img

    def rectify_perspective(self, img):
        """
        Simple perspective correction for angled photos
        This is a simplified version - for better results use OpenCV
        """
        # For now, just return the image as-is
        # In a full implementation, you'd detect corners and warp
        return img

    def process_variant(self, variant_dir):
        """Process all images for a single ETB variant"""
        variant_name = variant_dir.name
        output_variant_dir = self.output_dir / variant_name
        output_variant_dir.mkdir(exist_ok=True)
        
        print(f"\nProcessing variant: {variant_name}")
        
        # Load metadata if available
        metadata_file = variant_dir / "metadata.json"
        metadata = {}
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        # Process each face
        textures_created = []
        
        for face_name, texture_name in self.face_map.items():
            face_file = variant_dir / f"{face_name}.jpg"
            alt_face_file = variant_dir / f"{face_name}.png"
            
            texture_path = output_variant_dir / f"{texture_name}.png"
            
            # Try to find the face image
            if face_file.exists():
                img = self.process_image(face_file)
            elif alt_face_file.exists():
                img = self.process_image(alt_face_file)
            else:
                # Try to use any available image for missing faces
                any_image = None
                for img_file in variant_dir.glob("*.jpg"):
                    if img_file.name != "metadata.json":
                        any_image = img_file
                        break
                
                if not any_image:
                    for img_file in variant_dir.glob("*.png"):
                        if img_file.name != "metadata.json":
                            any_image = img_file
                            break
                
                if any_image:
                    print(f"  Using {any_image.name} for {face_name}")
                    img = self.process_image(any_image)
                    
                    # Apply different effects for different faces
                    if img and face_name in ['left', 'right']:
                        # Slightly darken sides
                        enhancer = ImageEnhance.Brightness(img)
                        img = enhancer.enhance(0.8)
                    elif img and face_name == 'bottom':
                        # Darken bottom more
                        enhancer = ImageEnhance.Brightness(img)
                        img = enhancer.enhance(0.6)
                    elif img and face_name == 'top':
                        # Slightly brighten top
                        enhancer = ImageEnhance.Brightness(img)
                        img = enhancer.enhance(1.1)
                else:
                    # Create default texture
                    colors = {
                        'front': (200, 50, 50),
                        'back': (50, 200, 50),
                        'left': (50, 50, 200),
                        'right': (200, 200, 50),
                        'top': (200, 50, 200),
                        'bottom': (50, 200, 200)
                    }
                    img = self.create_default_texture(
                        colors.get(face_name, (128, 128, 128)),
                        face_name
                    )
            
            if img:
                # Apply perspective correction if needed
                img = self.rectify_perspective(img)
                
                # Save texture
                img.save(texture_path, 'PNG')
                textures_created.append(texture_name)
                print(f"  Created: {texture_name}.png")
        
        return {
            'variant': variant_name,
            'textures': textures_created,
            'metadata': metadata
        }

    def process_all(self):
        """Process all ETB variants"""
        print("ETB Image Rectification and Texture Assembly")
        print("=" * 50)
        
        results = []
        
        # Find all variant directories
        variant_dirs = [d for d in self.input_dir.iterdir() if d.is_dir()]
        
        if not variant_dirs:
            print(f"No variant directories found in {self.input_dir}")
            print("Please run the scraper first to download images.")
            return results
        
        for variant_dir in variant_dirs:
            result = self.process_variant(variant_dir)
            results.append(result)
        
        # Save processing summary
        summary_file = self.output_dir / "processing_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "=" * 50)
        print(f"Processing complete! Processed {len(results)} variants")
        print(f"Textures saved to: {self.output_dir.absolute()}")
        
        return results

    def generate_test_textures(self):
        """Generate test textures for development"""
        print("Generating test textures...")
        
        test_variants = [
            "etb_paldea_evolved",
            "etb_obsidian_flames",
            "etb_paradox_rift",
            "etb_scarlet_violet"
        ]
        
        for variant in test_variants:
            variant_dir = self.output_dir / variant
            variant_dir.mkdir(exist_ok=True)
            
            # Create colorful test textures
            colors = {
                'etb_paldea_evolved': (150, 50, 200),  # Purple
                'etb_obsidian_flames': (255, 100, 0),  # Orange
                'etb_paradox_rift': (0, 150, 255),     # Blue
                'etb_scarlet_violet': (255, 50, 150)   # Pink
            }
            
            base_color = colors.get(variant, (128, 128, 128))
            
            for face_name, texture_name in self.face_map.items():
                # Vary the color slightly for each face
                if face_name == 'front':
                    color = base_color
                elif face_name == 'back':
                    color = tuple(int(c * 0.8) for c in base_color)
                elif face_name in ['left', 'right']:
                    color = tuple(int(c * 0.9) for c in base_color)
                elif face_name == 'top':
                    color = tuple(min(255, int(c * 1.2)) for c in base_color)
                else:  # bottom
                    color = tuple(int(c * 0.6) for c in base_color)
                
                img = self.create_default_texture(color, face_name)
                texture_path = variant_dir / f"{texture_name}.png"
                img.save(texture_path, 'PNG')
            
            print(f"  Created test textures for {variant}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Rectify ETB images and create Minecraft textures')
    parser.add_argument('input_dir', nargs='?', default='raw', 
                       help='Input directory with scraped images')
    parser.add_argument('output_dir', nargs='?', 
                       default='src/main/resources/assets/etbmod/textures/block',
                       help='Output directory for textures')
    parser.add_argument('--size', type=int, default=32, 
                       choices=[16, 32, 64, 128],
                       help='Texture size (default: 32)')
    parser.add_argument('--test', action='store_true',
                       help='Generate test textures')
    
    args = parser.parse_args()
    
    rectifier = ETBRectifier(args.input_dir, args.output_dir)
    rectifier.texture_size = args.size
    
    if args.test:
        rectifier.generate_test_textures()
    else:
        rectifier.process_all()

if __name__ == "__main__":
    main()