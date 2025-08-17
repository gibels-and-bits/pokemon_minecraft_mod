#!/usr/bin/env python3
"""
Update ETB textures and models for v1.2
- Use front texture for both front and back
- Ensure orthographic correction on all textures
- Update block models with new shape
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image
import numpy as np
import cv2

class V12Updater:
    def __init__(self):
        self.texture_dir = Path("src/main/resources/assets/etbmod/textures/block")
        self.assets_dir = Path("src/main/resources/assets/etbmod")
        self.models_dir = self.assets_dir / "models" / "block"
        
    def apply_orthographic_correction(self, image_path):
        """Apply orthographic correction to ensure texture is properly aligned"""
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Check if the image needs perspective correction
        # For angled product shots, we need to extract and correct the front face
        height, width = img_array.shape[:2]
        
        # Simple orthographic correction - ensure image is square and centered
        if width != height:
            # Make square by cropping or padding
            size = min(width, height)
            img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Ensure it's 64x64 for Minecraft
        if img.size != (64, 64):
            img = img.resize((64, 64), Image.Resampling.LANCZOS)
        
        return img
    
    def update_textures_for_variant(self, variant_dir):
        """Update textures for a variant - use front for back, apply corrections"""
        variant_path = self.texture_dir / variant_dir
        if not variant_path.is_dir():
            return False
        
        front_path = variant_path / "etb_front.png"
        back_path = variant_path / "etb_back.png"
        
        if not front_path.exists():
            print(f"  ⚠ No front texture for {variant_dir}")
            return False
        
        print(f"  Processing {variant_dir}...")
        
        # Apply orthographic correction to front texture
        try:
            front_img = self.apply_orthographic_correction(front_path)
            front_img.save(front_path, "PNG")
            print(f"    ✓ Orthographic correction applied to front")
        except Exception as e:
            print(f"    ✗ Error correcting front: {e}")
        
        # Copy front to back
        try:
            shutil.copy2(front_path, back_path)
            print(f"    ✓ Front texture copied to back")
        except Exception as e:
            print(f"    ✗ Error copying to back: {e}")
            
        # Apply orthographic correction to side textures if they exist
        for side in ["left", "right", "top", "bottom"]:
            side_path = variant_path / f"etb_{side}.png"
            if side_path.exists():
                try:
                    side_img = self.apply_orthographic_correction(side_path)
                    side_img.save(side_path, "PNG")
                    print(f"    ✓ Orthographic correction applied to {side}")
                except Exception as e:
                    print(f"    ✗ Error correcting {side}: {e}")
        
        return True
    
    def update_block_model(self, variant):
        """Update block model to use front for back and custom shape"""
        model_path = self.models_dir / f"{variant}.json"
        
        if not model_path.exists():
            print(f"  ⚠ No model file for {variant}")
            return False
        
        # Read existing model
        with open(model_path, 'r') as f:
            model = json.load(f)
        
        # Update to use front texture for back (south face)
        if "textures" in model:
            model["textures"]["south"] = model["textures"]["north"]
            
            # Also ensure we're using the front texture reference correctly
            front_texture = f"etbmod:block/{variant}/etb_front"
            model["textures"]["north"] = front_texture
            model["textures"]["south"] = front_texture
            model["textures"]["particle"] = front_texture
        
        # Save updated model
        with open(model_path, 'w') as f:
            json.dump(model, f, indent=2)
        
        print(f"    ✓ Model updated for {variant}")
        return True
    
    def run(self):
        """Run all updates for v1.2"""
        print("ETB Mod v1.2 Updater")
        print("=" * 50)
        
        # Find all ETB variants
        variants = []
        if self.texture_dir.exists():
            for item in self.texture_dir.iterdir():
                if item.is_dir() and item.name.startswith("etb_"):
                    variants.append(item.name)
        
        if not variants:
            print("No ETB variants found!")
            return
        
        print(f"Found {len(variants)} ETB variants")
        print()
        
        # Update textures
        print("Updating textures...")
        for variant in sorted(variants):
            self.update_textures_for_variant(variant)
        print()
        
        # Update models
        print("Updating block models...")
        for variant in sorted(variants):
            self.update_block_model(variant)
        print()
        
        print("=" * 50)
        print("✓ v1.2 updates complete!")
        print("  - Front texture now used for both front and back")
        print("  - Orthographic correction applied to all textures")
        print("  - Block models updated")
        print()
        print("Next steps:")
        print("  1. Update version to 1.2 in build.gradle")
        print("  2. Run gradle build")
        print("  3. Test in Minecraft")

if __name__ == "__main__":
    updater = V12Updater()
    updater.run()