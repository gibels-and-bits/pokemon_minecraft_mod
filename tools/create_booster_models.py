#!/usr/bin/env python3
"""
Generate item model JSON files for booster packs
"""

import json
from pathlib import Path

def create_item_model(name):
    """Create item model JSON for a booster pack"""
    return {
        "parent": "item/generated",
        "textures": {
            "layer0": f"etbmod:item/{name}"
        }
    }

def main():
    print("Creating Booster Pack Model Files")
    print("=" * 60)
    
    models_dir = Path("src/main/resources/assets/etbmod/models/item")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # List of booster pack variants
    variants = [
        "151", "black_bolt", "brilliant_stars", "celebrations",
        "destined_rivals", "generations", "groudon", "journey_together",
        "kyogre", "prismatic_evolutions", "surging_sparks", "white_flare"
    ]
    
    count = 0
    for variant in variants:
        filename = f"etb_{variant}_booster"
        model_data = create_item_model(filename)
        
        output_file = models_dir / f"{filename}.json"
        with open(output_file, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        print(f"✓ Created: {output_file.name}")
        count += 1
    
    print(f"\n✓ Created {count} booster pack model files")

if __name__ == "__main__":
    main()