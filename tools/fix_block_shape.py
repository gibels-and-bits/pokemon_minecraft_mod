#!/usr/bin/env python3
"""
Fix block models to use custom shape instead of full cube
ETB dimensions: 13x7x12 pixels (width x depth x height)
Positioned at: x=1.5-14.5, y=0-12, z=4.5-11.5
"""

import json
from pathlib import Path

def create_custom_model(variant):
    """Create a custom model with ETB box shape"""
    # The shape from ETBBlock.java: Block.box(1.5D, 0.0D, 4.5D, 14.5D, 12.0D, 11.5D)
    # This translates to: from (1.5, 0, 4.5) to (14.5, 12, 11.5) in block coordinates
    
    model = {
        "parent": "block/block",
        "textures": {
            "north": f"etbmod:block/{variant}/etb_front",
            "south": f"etbmod:block/{variant}/etb_front",  # Using front for back
            "east": f"etbmod:block/{variant}/etb_right",
            "west": f"etbmod:block/{variant}/etb_left", 
            "up": f"etbmod:block/{variant}/etb_top",
            "down": f"etbmod:block/{variant}/etb_bottom",
            "particle": f"etbmod:block/{variant}/etb_front"
        },
        "elements": [
            {
                "from": [1.5, 0, 4.5],
                "to": [14.5, 12, 11.5],
                "faces": {
                    "north": {"uv": [0, 0, 16, 16], "texture": "#north"},
                    "south": {"uv": [0, 0, 16, 16], "texture": "#south"},
                    "east": {"uv": [0, 0, 16, 16], "texture": "#east"},
                    "west": {"uv": [0, 0, 16, 16], "texture": "#west"},
                    "up": {"uv": [0, 0, 16, 16], "texture": "#up"},
                    "down": {"uv": [0, 0, 16, 16], "texture": "#down"}
                }
            }
        ]
    }
    
    return model

def main():
    models_dir = Path("src/main/resources/assets/etbmod/models/block")
    
    if not models_dir.exists():
        print(f"Models directory not found: {models_dir}")
        return
    
    # Find all ETB model files
    model_files = list(models_dir.glob("etb_*.json"))
    
    print(f"Fixing {len(model_files)} block models to use custom shape...")
    print("=" * 50)
    
    for model_file in model_files:
        variant = model_file.stem
        print(f"  Updating {variant}...")
        
        # Create custom model with proper shape
        model = create_custom_model(variant)
        
        # Write the updated model
        with open(model_file, 'w') as f:
            json.dump(model, f, indent=2)
        
        print(f"    ✓ Model updated with custom shape")
    
    # Also update the base model if it exists
    base_model = models_dir / "etb_base.json"
    if base_model.exists():
        print(f"  Updating etb_base...")
        model = create_custom_model("etb_base")
        with open(base_model, 'w') as f:
            json.dump(model, f, indent=2)
        print(f"    ✓ Base model updated")
    
    print("=" * 50)
    print("✓ All models updated with custom ETB shape!")
    print("  Shape: 13x12x7 pixels (81.25% x 75% x 43.75% of a block)")
    print("  Position: Centered on X and Z axes")

if __name__ == "__main__":
    main()