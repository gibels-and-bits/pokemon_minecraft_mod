#!/usr/bin/env python3
"""
Fix and finalize ETB Mod v1.4
Expert review and corrections
"""

import json
import os
from pathlib import Path

class V14Fixer:
    def __init__(self):
        self.assets_dir = Path("src/main/resources/assets/etbmod")
        self.data_dir = Path("src/main/resources/data/etbmod")
        self.java_dir = Path("src/main/java/com/example/etbmod")
        
    def fix_loot_tables(self):
        """Ensure all ETB blocks have proper loot tables that drop themselves"""
        loot_dir = self.data_dir / "loot_tables" / "blocks"
        loot_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all ETB variants
        blockstates_dir = self.assets_dir / "blockstates"
        if blockstates_dir.exists():
            for blockstate_file in blockstates_dir.glob("etb_*.json"):
                variant = blockstate_file.stem
                
                # Create loot table for this variant
                loot_table = {
                    "type": "minecraft:block",
                    "pools": [
                        {
                            "rolls": 1,
                            "entries": [
                                {
                                    "type": "minecraft:item",
                                    "name": f"etbmod:{variant}"
                                }
                            ],
                            "conditions": [
                                {
                                    "condition": "minecraft:survives_explosion"
                                }
                            ]
                        }
                    ]
                }
                
                loot_file = loot_dir / f"{variant}.json"
                with open(loot_file, 'w') as f:
                    json.dump(loot_table, f, indent=2)
                
                print(f"  ✓ Fixed loot table for {variant}")
    
    def fix_scissors_item(self):
        """Fix the scissors item implementation"""
        scissors_code = '''package com.example.etbmod.items;

import net.minecraft.item.Item;
import com.example.etbmod.ETBMod;

public class ScissorsItem extends Item {
    
    public ScissorsItem() {
        super(new Item.Properties()
                .tab(ETBMod.ITEM_GROUP)
                .durability(238)
                .stacksTo(1));
    }
}'''
        
        scissors_path = self.java_dir / "items" / "ScissorsItem.java"
        with open(scissors_path, 'w') as f:
            f.write(scissors_code)
        
        print("  ✓ Fixed ScissorsItem.java")
    
    def ensure_all_blockstates_support_rotation(self):
        """Make sure all blockstates have default facing if not already set"""
        blockstates_dir = self.assets_dir / "blockstates"
        
        for blockstate_file in blockstates_dir.glob("etb_*.json"):
            with open(blockstate_file, 'r') as f:
                data = json.load(f)
            
            # Check if it already has facing variants
            if "facing=north" not in data.get("variants", {}):
                # Update to support rotation
                model_ref = f"etbmod:block/{blockstate_file.stem}"
                data = {
                    "variants": {
                        "facing=north": {"model": model_ref},
                        "facing=south": {"model": model_ref, "y": 180},
                        "facing=west": {"model": model_ref, "y": 270},
                        "facing=east": {"model": model_ref, "y": 90}
                    }
                }
                
                with open(blockstate_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"  ✓ Fixed rotation for {blockstate_file.stem}")
    
    def update_mod_info(self):
        """Update mods.toml with v1.4 changes"""
        mods_toml = """modLoader="javafml"
loaderVersion="[36,)"
license="All rights reserved"

[[mods]]
modId="etbmod"
version="${file.jarVersion}"
displayName="Elite Trainer Box Mod"
credits="Pokemon TCG Community"
authors="ETB Mod Team"
description='''Brings Pokemon TCG Elite Trainer Boxes to Minecraft!

Features in v1.4:
- 13 unique ETB designs from real Pokemon TCG sets
- Custom 3D models with accurate proportions  
- Directional placement - rotate your ETBs
- Breaking ETBs drops the block item
- NEW: Scissors tool - craft with iron and sticks
- NEW: Right-click ETBs with scissors to open them
- NEW: Opening ETBs spawns 9 items (diamonds as placeholder)
- Decorative blocks perfect for Pokemon-themed builds
'''

[[dependencies.etbmod]]
    modId="forge"
    mandatory=true
    versionRange="[36,)"
    ordering="NONE"
    side="BOTH"

[[dependencies.etbmod]]
    modId="minecraft"
    mandatory=true
    versionRange="[1.16.5,1.17)"
    ordering="NONE"
    side="BOTH"
"""
        
        mods_path = Path("src/main/resources/META-INF/mods.toml")
        with open(mods_path, 'w') as f:
            f.write(mods_toml)
        
        print("  ✓ Updated mods.toml for v1.4")
    
    def run(self):
        """Run all v1.4 fixes"""
        print("ETB Mod v1.4 - Final Expert Review")
        print("=" * 50)
        
        print("\nFixing loot tables...")
        self.fix_loot_tables()
        
        print("\nFixing scissors item...")
        self.fix_scissors_item()
        
        print("\nEnsuring rotation support...")
        self.ensure_all_blockstates_support_rotation()
        
        print("\nUpdating mod info...")
        self.update_mod_info()
        
        print("\n" + "=" * 50)
        print("✓ All v1.4 fixes complete!")
        print("\nReady to build final version.")

if __name__ == "__main__":
    fixer = V14Fixer()
    fixer.run()