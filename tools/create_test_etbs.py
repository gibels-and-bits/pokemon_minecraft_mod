#!/usr/bin/env python3
"""
Create test ETB images for development
"""

import os
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class TestETBCreator:
    def __init__(self, output_dir="raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Popular ETB sets
        self.etb_sets = [
            {"name": "Paldea Evolved", "color": (147, 51, 234)},  # Purple
            {"name": "Obsidian Flames", "color": (249, 115, 22)},  # Orange
            {"name": "Paradox Rift", "color": (59, 130, 246)},   # Blue
            {"name": "Temporal Forces", "color": (34, 197, 94)},  # Green
            {"name": "Twilight Masquerade", "color": (168, 85, 247)}, # Purple-pink
            {"name": "Shrouded Fable", "color": (99, 102, 241)},  # Indigo
            {"name": "Stellar Crown", "color": (251, 191, 36)},   # Yellow
            {"name": "Surging Sparks", "color": (239, 68, 68)},   # Red
            {"name": "Scarlet Violet", "color": (220, 38, 127)},  # Pink
            {"name": "Crown Zenith", "color": (236, 72, 153)},    # Pink
            {"name": "Silver Tempest", "color": (148, 163, 184)}, # Silver
            {"name": "Lost Origin", "color": (107, 114, 128)},    # Gray
            {"name": "Astral Radiance", "color": (14, 165, 233)}, # Sky blue
            {"name": "Brilliant Stars", "color": (251, 146, 60)}, # Amber
            {"name": "Fusion Strike", "color": (217, 70, 239)},   # Magenta
            {"name": "Evolving Skies", "color": (125, 211, 252)}, # Light blue
            {"name": "Chilling Reign", "color": (56, 189, 248)},  # Cyan
            {"name": "Battle Styles", "color": (239, 68, 68)},    # Red
            {"name": "Vivid Voltage", "color": (252, 211, 77)},   # Yellow
            {"name": "Darkness Ablaze", "color": (239, 68, 68)},  # Dark red
        ]

    def create_etb_face(self, base_color, face_name, text=""):
        """Create a single face texture for an ETB"""
        img = Image.new('RGB', (256, 256), base_color)
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        for i in range(128):
            alpha = i / 128
            if face_name == "front":
                color = tuple(int(c * (1 + alpha * 0.2)) for c in base_color)
            elif face_name == "back":
                color = tuple(int(c * (1 - alpha * 0.2)) for c in base_color)
            elif face_name in ["left", "right"]:
                color = tuple(int(c * (1 - alpha * 0.1)) for c in base_color)
            elif face_name == "top":
                color = tuple(int(c * (1 + alpha * 0.3)) for c in base_color)
            else:  # bottom
                color = tuple(int(c * (1 - alpha * 0.3)) for c in base_color)
            
            # Clamp colors to valid range
            color = tuple(min(255, max(0, c)) for c in color)
            
            if face_name in ["front", "back"]:
                draw.rectangle([0, i*2, 256, i*2+2], fill=color)
            elif face_name in ["left", "right"]:
                draw.rectangle([i*2, 0, i*2+2, 256], fill=color)
        
        # Add Pokemon-style border
        border_color = tuple(int(c * 0.7) for c in base_color)
        draw.rectangle([0, 0, 256, 10], fill=border_color)
        draw.rectangle([0, 246, 256, 256], fill=border_color)
        draw.rectangle([0, 0, 10, 256], fill=border_color)
        draw.rectangle([246, 0, 256, 256], fill=border_color)
        
        # Add text if provided
        if text:
            # Try to use a basic font
            try:
                from PIL import ImageFont
                font = ImageFont.load_default()
            except:
                font = None
            
            text_color = (255, 255, 255) if sum(base_color) < 384 else (0, 0, 0)
            
            # Draw text multiple times for bold effect
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    draw.text((128 + dx, 128 + dy), text, fill=text_color, anchor="mm")
        
        # Add some texture pattern
        for x in range(20, 236, 40):
            for y in range(20, 236, 40):
                circle_color = tuple(int(c * 0.9) for c in base_color)
                draw.ellipse([x, y, x+20, y+20], outline=circle_color, width=2)
        
        return img

    def create_etb_set(self, name, base_color):
        """Create all 6 faces for an ETB set"""
        # Sanitize name for folder
        folder_name = name.lower().replace(' ', '_')
        folder_name = f"etb_{folder_name}"
        
        variant_dir = self.output_dir / folder_name
        variant_dir.mkdir(exist_ok=True)
        
        print(f"Creating ETB: {name}")
        
        # Create each face
        faces = {
            "front": name,
            "back": "TRAINER BOX",
            "left": "ELITE",
            "right": "POKEMON",
            "top": "TCG",
            "bottom": ""
        }
        
        for face_name, face_text in faces.items():
            img = self.create_etb_face(base_color, face_name, face_text)
            img.save(variant_dir / f"{face_name}.jpg", quality=95)
            print(f"  Created: {face_name}.jpg")
        
        # Create metadata
        metadata = {
            "title": f"Pokemon {name} Elite Trainer Box",
            "variant_name": folder_name,
            "test_data": True,
            "base_color": base_color
        }
        
        with open(variant_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return folder_name

    def create_all(self):
        """Create test images for all ETB sets"""
        print("Creating Test ETB Images")
        print("=" * 50)
        
        created_variants = []
        
        for etb in self.etb_sets[:10]:  # Create first 10 for testing
            variant = self.create_etb_set(etb["name"], etb["color"])
            created_variants.append(variant)
        
        print("\n" + "=" * 50)
        print(f"Created {len(created_variants)} test ETB sets")
        print(f"Images saved to: {self.output_dir.absolute()}")
        
        return created_variants

def main():
    creator = TestETBCreator()
    creator.create_all()

if __name__ == "__main__":
    main()