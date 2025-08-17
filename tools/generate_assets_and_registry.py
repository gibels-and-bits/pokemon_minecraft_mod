#!/usr/bin/env python3
"""
Asset and Registry Generator for ETB Mod
Generates JSON assets and Java registry code based on available textures
"""

import os
import json
from pathlib import Path
import re

class AssetGenerator:
    def __init__(self, texture_dir="src/main/resources/assets/etbmod/textures/block",
                 assets_dir="src/main/resources/assets/etbmod",
                 data_dir="src/main/resources/data/etbmod",
                 java_dir="src/main/java/com/example/etbmod/registry"):
        
        self.texture_dir = Path(texture_dir)
        self.assets_dir = Path(assets_dir)
        self.data_dir = Path(data_dir)
        self.java_dir = Path(java_dir)
        
        # Ensure directories exist
        (self.assets_dir / "blockstates").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "models" / "block").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "models" / "item").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "lang").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "loot_tables" / "blocks").mkdir(parents=True, exist_ok=True)

    def find_etb_variants(self):
        """Find all ETB variants based on texture folders"""
        variants = []
        
        if not self.texture_dir.exists():
            print(f"Texture directory not found: {self.texture_dir}")
            return variants
        
        # Look for directories containing ETB textures
        for variant_dir in self.texture_dir.iterdir():
            if variant_dir.is_dir():
                # Check if it has the required face textures
                required_faces = ['etb_front.png', 'etb_back.png']
                if all((variant_dir / face).exists() for face in required_faces):
                    variants.append(variant_dir.name)
        
        return sorted(variants)

    def variant_to_display_name(self, variant):
        """Convert variant ID to display name"""
        # Remove etb_ prefix if present
        name = variant.replace('etb_', '')
        
        # Convert underscores to spaces and capitalize
        name = name.replace('_', ' ')
        words = name.split()
        
        # Capitalize each word
        capitalized = []
        for word in words:
            if word.lower() in ['etb', 'tcg']:
                capitalized.append(word.upper())
            else:
                capitalized.append(word.capitalize())
        
        return f"Elite Trainer Box - {' '.join(capitalized)}"

    def generate_blockstate(self, variant):
        """Generate blockstate JSON for a variant"""
        blockstate = {
            "variants": {
                "": {
                    "model": f"etbmod:block/{variant}"
                }
            }
        }
        
        output_file = self.assets_dir / "blockstates" / f"{variant}.json"
        with open(output_file, 'w') as f:
            json.dump(blockstate, f, indent=2)
        
        return output_file

    def generate_block_model(self, variant):
        """Generate block model JSON for a variant"""
        model = {
            "parent": "block/cube",
            "textures": {
                "north": f"etbmod:block/{variant}/etb_front",
                "south": f"etbmod:block/{variant}/etb_back",
                "east": f"etbmod:block/{variant}/etb_right",
                "west": f"etbmod:block/{variant}/etb_left",
                "up": f"etbmod:block/{variant}/etb_top",
                "down": f"etbmod:block/{variant}/etb_bottom",
                "particle": f"etbmod:block/{variant}/etb_front"
            }
        }
        
        # Check which textures actually exist and use defaults for missing ones
        variant_dir = self.texture_dir / variant
        if not (variant_dir / "etb_left.png").exists():
            model["textures"]["west"] = model["textures"]["north"]
        if not (variant_dir / "etb_right.png").exists():
            model["textures"]["east"] = model["textures"]["north"]
        if not (variant_dir / "etb_top.png").exists():
            model["textures"]["up"] = model["textures"]["north"]
        if not (variant_dir / "etb_bottom.png").exists():
            model["textures"]["down"] = model["textures"]["south"]
        
        output_file = self.assets_dir / "models" / "block" / f"{variant}.json"
        with open(output_file, 'w') as f:
            json.dump(model, f, indent=2)
        
        return output_file

    def generate_item_model(self, variant):
        """Generate item model JSON for a variant"""
        model = {
            "parent": f"etbmod:block/{variant}"
        }
        
        output_file = self.assets_dir / "models" / "item" / f"{variant}.json"
        with open(output_file, 'w') as f:
            json.dump(model, f, indent=2)
        
        return output_file

    def generate_loot_table(self, variant):
        """Generate loot table JSON for a variant"""
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
                    ]
                }
            ]
        }
        
        output_file = self.data_dir / "loot_tables" / "blocks" / f"{variant}.json"
        with open(output_file, 'w') as f:
            json.dump(loot_table, f, indent=2)
        
        return output_file

    def update_lang_file(self, variants):
        """Update language file with all variants"""
        lang_file = self.assets_dir / "lang" / "en_us.json"
        
        # Load existing translations
        if lang_file.exists():
            with open(lang_file, 'r') as f:
                lang_data = json.load(f)
        else:
            lang_data = {}
        
        # Add item group if not present
        lang_data["itemGroup.etbmod"] = "Elite Trainer Boxes"
        
        # Add all variants
        for variant in variants:
            key = f"block.etbmod.{variant}"
            lang_data[key] = self.variant_to_display_name(variant)
        
        # Sort keys for consistency
        sorted_lang = dict(sorted(lang_data.items()))
        
        with open(lang_file, 'w') as f:
            json.dump(sorted_lang, f, indent=2)
        
        return lang_file

    def generate_java_registry(self, variants):
        """Generate Java registry code for all variants"""
        
        # Generate the registry file
        java_code = '''package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.blocks.ETBBlock;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraftforge.fml.RegistryObject;

/**
 * Auto-generated ETB registry
 * Generated by generate_assets_and_registry.py
 */
public class GeneratedETBRegistry {
    
    public static void registerETBs() {
'''
        
        # Add registration calls for each variant
        for variant in variants:
            java_code += f'        ModBlocks.registerETB("{variant}");\n'
        
        java_code += '''    }
    
    public static void registerETBItems() {
        // Items are automatically registered via ModItems static block
    }
}
'''
        
        output_file = self.java_dir / "GeneratedETBRegistry.java"
        with open(output_file, 'w') as f:
            f.write(java_code)
        
        # Update ModBlocks.java to call the generated registry
        self.update_mod_blocks(variants)
        
        return output_file

    def update_mod_blocks(self, variants):
        """Update ModBlocks.java to include all variants"""
        mod_blocks_file = self.java_dir / "ModBlocks.java"
        
        java_code = '''package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.blocks.ETBBlock;
import net.minecraft.block.Block;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.ArrayList;
import java.util.List;

public class ModBlocks {
    public static final DeferredRegister<Block> BLOCKS = 
            DeferredRegister.create(ForgeRegistries.BLOCKS, ETBMod.MOD_ID);
    
    public static final List<RegistryObject<Block>> ETB_BLOCKS = new ArrayList<>();
    
    // Individual block references for easy access
'''
        
        # Add individual block references
        for variant in variants:
            var_name = variant.upper()
            java_code += f'    public static final RegistryObject<Block> {var_name} = registerETB("{variant}");\n'
        
        java_code += '''    
    public static RegistryObject<Block> registerETB(String name) {
        RegistryObject<Block> block = BLOCKS.register(name, ETBBlock::new);
        ETB_BLOCKS.add(block);
        return block;
    }
}
'''
        
        with open(mod_blocks_file, 'w') as f:
            f.write(java_code)
        
        return mod_blocks_file

    def generate_all(self):
        """Generate all assets and registry code"""
        print("ETB Asset and Registry Generator")
        print("=" * 50)
        
        # Find all ETB variants
        variants = self.find_etb_variants()
        
        if not variants:
            print("No ETB variants found!")
            print("Please run the rectification script first to create textures.")
            return
        
        print(f"Found {len(variants)} ETB variants:")
        for variant in variants:
            print(f"  - {variant}")
        
        print("\nGenerating assets...")
        
        # Generate assets for each variant
        for variant in variants:
            print(f"\nProcessing {variant}:")
            
            # Generate JSON files
            self.generate_blockstate(variant)
            print(f"  ✓ Blockstate")
            
            self.generate_block_model(variant)
            print(f"  ✓ Block model")
            
            self.generate_item_model(variant)
            print(f"  ✓ Item model")
            
            self.generate_loot_table(variant)
            print(f"  ✓ Loot table")
        
        # Update language file
        self.update_lang_file(variants)
        print(f"\n✓ Language file updated")
        
        # Generate Java registry
        self.generate_java_registry(variants)
        print(f"✓ Java registry generated")
        
        print("\n" + "=" * 50)
        print(f"Generation complete!")
        print(f"Generated assets for {len(variants)} ETB variants")
        print("\nNext steps:")
        print("1. Run './gradlew build' to compile the mod")
        print("2. Test with './gradlew runClient'")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate ETB mod assets and registry')
    parser.add_argument('--texture-dir', default='src/main/resources/assets/etbmod/textures/block',
                       help='Directory containing ETB textures')
    parser.add_argument('--assets-dir', default='src/main/resources/assets/etbmod',
                       help='Assets output directory')
    parser.add_argument('--data-dir', default='src/main/resources/data/etbmod',
                       help='Data output directory')
    parser.add_argument('--java-dir', default='src/main/java/com/example/etbmod/registry',
                       help='Java output directory')
    
    args = parser.parse_args()
    
    generator = AssetGenerator(
        texture_dir=args.texture_dir,
        assets_dir=args.assets_dir,
        data_dir=args.data_dir,
        java_dir=args.java_dir
    )
    
    generator.generate_all()

if __name__ == "__main__":
    main()