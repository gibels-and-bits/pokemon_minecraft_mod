#!/usr/bin/env python3
"""
Unified image processor for Pokemon TCG card and ETB images.
Handles border removal, transparency, resizing, and optimization.
"""

import os
from pathlib import Path
from typing import Tuple, Optional, List
from PIL import Image, ImageOps
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles all image processing operations for the mod."""
    
    def __init__(self):
        self.card_size = (367, 512)  # Standard Pokemon card aspect ratio
        self.etb_texture_size = (64, 64)  # Minecraft texture size
        
    def process_card_image(self, input_path: Path, output_path: Path, 
                          remove_borders: bool = True, 
                          add_transparency: bool = False) -> bool:
        """Process a single card image."""
        try:
            img = Image.open(input_path)
            
            if remove_borders:
                img = self.remove_borders(img)
            
            if add_transparency:
                img = self.add_rounded_corners(img)
            
            # Resize to standard dimensions
            img = img.resize(self.card_size, Image.Resampling.LANCZOS)
            
            # Ensure RGBA format
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Save optimized
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, 'PNG', optimize=True)
            return True
            
        except Exception as e:
            logger.error(f"Failed to process {input_path}: {e}")
            return False
    
    def remove_borders(self, img: Image.Image, threshold: int = 240) -> Image.Image:
        """Remove white borders from card image."""
        # Convert to numpy array
        arr = np.array(img)
        
        # Create mask for non-white pixels
        if len(arr.shape) == 3:
            mask = np.any(arr[:, :, :3] < threshold, axis=2)
        else:
            mask = arr < threshold
        
        # Find bounding box
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not rows.any() or not cols.any():
            return img
        
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        # Add small padding
        padding = 2
        rmin = max(0, rmin - padding)
        rmax = min(arr.shape[0], rmax + padding + 1)
        cmin = max(0, cmin - padding)
        cmax = min(arr.shape[1], cmax + padding + 1)
        
        # Crop image
        return img.crop((cmin, rmin, cmax, rmax))
    
    def add_rounded_corners(self, img: Image.Image, radius: int = 20) -> Image.Image:
        """Add rounded corners with transparency."""
        # Ensure RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create mask for rounded corners
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        
        # Apply mask
        output = Image.new('RGBA', img.size, (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        return output
    
    def process_etb_texture(self, input_path: Path, output_path: Path,
                           face: str = 'front') -> bool:
        """Process ETB box texture for Minecraft."""
        try:
            img = Image.open(input_path)
            
            # Different processing based on face
            if face == 'front':
                # Main box art - higher quality
                img = img.resize((128, 128), Image.Resampling.LANCZOS)
            elif face in ['top', 'bottom']:
                # Top/bottom - can be lower res
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
            else:
                # Sides - standard texture size
                img = img.resize(self.etb_texture_size, Image.Resampling.LANCZOS)
            
            # Optimize for Minecraft
            img = self.optimize_for_minecraft(img)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, 'PNG', optimize=True)
            return True
            
        except Exception as e:
            logger.error(f"Failed to process ETB texture {input_path}: {e}")
            return False
    
    def optimize_for_minecraft(self, img: Image.Image) -> Image.Image:
        """Optimize image for Minecraft rendering."""
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Reduce colors if image is large
        if img.size[0] > 64 or img.size[1] > 64:
            img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT).convert('RGBA')
        
        return img
    
    def create_texture_atlas(self, images: List[Path], output_path: Path,
                           atlas_size: Tuple[int, int] = (512, 512)) -> bool:
        """Create a texture atlas from multiple images."""
        try:
            atlas = Image.new('RGBA', atlas_size, (0, 0, 0, 0))
            
            # Simple grid packing
            grid_size = int(np.sqrt(len(images)))
            tile_width = atlas_size[0] // grid_size
            tile_height = atlas_size[1] // grid_size
            
            for idx, img_path in enumerate(images):
                if not img_path.exists():
                    continue
                
                img = Image.open(img_path)
                img = img.resize((tile_width, tile_height), Image.Resampling.LANCZOS)
                
                x = (idx % grid_size) * tile_width
                y = (idx // grid_size) * tile_height
                
                atlas.paste(img, (x, y))
            
            atlas.save(output_path, 'PNG', optimize=True)
            return True
            
        except Exception as e:
            logger.error(f"Failed to create texture atlas: {e}")
            return False
    
    def batch_process_cards(self, input_dir: Path, output_dir: Path,
                          remove_borders: bool = True) -> dict:
        """Process all card images in a directory."""
        stats = {"success": 0, "failed": 0}
        
        for img_file in input_dir.glob("*.png"):
            output_file = output_dir / img_file.name
            
            if self.process_card_image(img_file, output_file, remove_borders):
                stats["success"] += 1
            else:
                stats["failed"] += 1
        
        logger.info(f"Processed {stats['success']} cards, {stats['failed']} failed")
        return stats
    
    def generate_minecraft_item_texture(self, input_path: Path, output_path: Path) -> bool:
        """Generate a 16x16 item texture for Minecraft."""
        try:
            img = Image.open(input_path)
            
            # Resize to 16x16 for item texture
            img = img.resize((16, 16), Image.Resampling.LANCZOS)
            
            # Enhance contrast for small size
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, 'PNG', optimize=True)
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate item texture: {e}")
            return False


class ETBTextureGenerator:
    """Specialized generator for ETB block textures."""
    
    def __init__(self, processor: ImageProcessor):
        self.processor = processor
        
    def generate_etb_textures(self, set_id: str, input_image: Path, output_dir: Path) -> bool:
        """Generate all required textures for an ETB block."""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Load source image
            img = Image.open(input_image)
            
            # Generate different faces
            faces = {
                'front': (128, 128),
                'back': (128, 128),
                'top': (64, 64),
                'bottom': (64, 64),
                'left': (64, 128),
                'right': (64, 128)
            }
            
            for face, size in faces.items():
                face_img = img.resize(size, Image.Resampling.LANCZOS)
                face_path = output_dir / f"etb_{set_id}_{face}.png"
                face_img.save(face_path, 'PNG', optimize=True)
            
            # Generate item texture (for inventory)
            item_img = img.resize((16, 16), Image.Resampling.LANCZOS)
            item_path = output_dir / f"etb_{set_id}_item.png"
            item_img.save(item_path, 'PNG', optimize=True)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate ETB textures for {set_id}: {e}")
            return False


def main():
    """Main entry point for image processing."""
    import argparse
    from PIL import ImageDraw
    
    parser = argparse.ArgumentParser(description="Pokemon TCG Image Processor")
    parser.add_argument('--input', required=True, help='Input directory or file')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--type', choices=['cards', 'etb', 'atlas'], default='cards',
                       help='Type of processing to perform')
    parser.add_argument('--remove-borders', action='store_true', help='Remove white borders')
    parser.add_argument('--add-transparency', action='store_true', help='Add transparency')
    
    args = parser.parse_args()
    
    processor = ImageProcessor()
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if args.type == 'cards':
        if input_path.is_dir():
            processor.batch_process_cards(input_path, output_path, args.remove_borders)
        else:
            processor.process_card_image(input_path, output_path, 
                                        args.remove_borders, args.add_transparency)
    
    elif args.type == 'etb':
        etb_gen = ETBTextureGenerator(processor)
        set_id = input_path.stem
        etb_gen.generate_etb_textures(set_id, input_path, output_path)


if __name__ == "__main__":
    # Import ImageDraw here to avoid import error if not needed
    from PIL import ImageDraw
    main()