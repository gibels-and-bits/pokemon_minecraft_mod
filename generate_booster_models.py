#!/usr/bin/env python3
import os
import json
import glob

# Directories
TEXTURE_DIR = "src/main/resources/assets/etbmod/textures/item"
MODEL_DIR = "src/main/resources/assets/etbmod/models/item"

def create_booster_model(booster_name):
    """Create a model file for a booster pack"""
    model_data = {
        "parent": "etbmod:item/booster_pack_base",
        "textures": {
            "layer0": f"etbmod:item/{booster_name}"
        }
    }
    
    model_path = os.path.join(MODEL_DIR, f"{booster_name}.json")
    with open(model_path, 'w') as f:
        json.dump(model_data, f, indent=2)
    print(f"✓ Created model for {booster_name}")

def main():
    # Get all booster pack textures
    texture_files = glob.glob(os.path.join(TEXTURE_DIR, "etb_*_booster.png"))
    
    created_count = 0
    for texture_path in texture_files:
        # Extract the booster name without extension
        booster_name = os.path.splitext(os.path.basename(texture_path))[0]
        create_booster_model(booster_name)
        created_count += 1
    
    # Also check for any special boosters that might exist
    special_boosters = ["etb_celebrations_booster", "etb_shrouded_fable_booster"]
    for booster in special_boosters:
        texture_path = os.path.join(TEXTURE_DIR, f"{booster}.png")
        if not os.path.exists(texture_path):
            print(f"⚠ No texture found for {booster}, skipping model")
        else:
            create_booster_model(booster)
            created_count += 1
    
    print(f"\n✅ Created {created_count} booster pack models")

if __name__ == "__main__":
    main()