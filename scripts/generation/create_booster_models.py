#!/usr/bin/env python3
"""
Create model JSON files for all booster packs
"""

import json
from pathlib import Path

# Paths
models_dir = Path("src/main/resources/assets/etbmod/models/item")
textures_dir = Path("src/main/resources/assets/etbmod/textures/item")

# Get all booster pack textures
booster_textures = [f.stem for f in textures_dir.glob("etb_*_booster.png")]

# Create model files
created = []
already_exists = []

for booster_name in sorted(booster_textures):
    model_file = models_dir / f"{booster_name}.json"
    
    if model_file.exists():
        already_exists.append(booster_name)
    else:
        # Create the model JSON
        model_data = {
            "parent": "item/generated",
            "textures": {
                "layer0": f"etbmod:item/{booster_name}"
            }
        }
        
        with open(model_file, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        created.append(booster_name)

print("Booster Pack Model Creation")
print("=" * 60)
print(f"Created {len(created)} new booster pack models:")
for name in created:
    print(f"  • {name}")

print(f"\nAlready existed: {len(already_exists)}")
print("=" * 60)