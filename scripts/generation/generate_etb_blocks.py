#!/usr/bin/env python3
"""
Generate ETB block classes and copy textures for Minecraft mod
"""

import os
import shutil
from pathlib import Path
import json

# ETB sets from the view files
ETB_SETS = [
    "black_bolt",
    "breakpoint",
    "brilliant_stars",
    "burning_shadows",
    "cosmic_eclipse",
    "crown_zenith",
    "evolutions",
    "evolving_skies",
    "hidden_fates",
    "phantom_forces",
    "primal_clash",
    "prismatic_evolutions",
    "rebel_clash",
    "shining_fates",
    "shrouded_fable",
    "surging_sparks",
    "team_up",
    "unified_minds",
    "vivid_voltage",
    "white_flare"
]

def to_class_name(set_name):
    """Convert set name to Java class name"""
    return ''.join(word.capitalize() for word in set_name.split('_')) + 'ETBBlock'

def to_display_name(set_name):
    """Convert set name to display name"""
    return ' '.join(word.capitalize() for word in set_name.split('_')) + ' ETB'

def generate_etb_block_class(set_name):
    """Generate a Java class for an ETB block"""
    class_name = to_class_name(set_name)
    
    return f"""package com.example.etbmod.blocks;

/**
 * {to_display_name(set_name)} Block
 * Auto-generated ETB block class
 */
public class {class_name} extends ETBBlock {{
    public {class_name}() {{
        super("etb_{set_name}");
    }}
}}
"""

def generate_registry_file():
    """Generate the registry file for all ETB blocks"""
    
    imports = """package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.blocks.*;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.HashMap;
import java.util.Map;

/**
 * Auto-generated ETB Block Registry
 */
public class GeneratedETBRegistry {
    
    // ETB Blocks
"""
    
    block_registrations = []
    item_registrations = []
    registry_map = []
    
    for set_name in ETB_SETS:
        class_name = to_class_name(set_name)
        const_name = set_name.upper() + "_ETB"
        
        block_registrations.append(
            f'    public static final RegistryObject<Block> {const_name} = ModBlocks.BLOCKS.register("etb_{set_name}", '
            f'{class_name}::new);'
        )
        
        item_registrations.append(
            f'    public static final RegistryObject<Item> {const_name}_ITEM = ModItems.ITEMS.register("etb_{set_name}", '
            f'() -> new BlockItem({const_name}.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));'
        )
        
        registry_map.append(
            f'        ETB_BLOCKS.put("{set_name}", {const_name});'
        )
    
    content = imports
    content += '\n'.join(block_registrations)
    content += '\n\n    // ETB Block Items\n'
    content += '\n'.join(item_registrations)
    content += '\n\n    // Registry map for easy lookup\n'
    content += '    public static final Map<String, RegistryObject<Block>> ETB_BLOCKS = new HashMap<>();\n\n'
    content += '    static {\n'
    content += '\n'.join(registry_map)
    content += '\n    }\n}\n'
    
    return content

def copy_textures():
    """Copy ETB textures to the appropriate Minecraft directories"""
    views_dir = Path("raw_images/etb_views")
    
    # Base texture directory for the mod
    texture_base = Path("src/main/resources/assets/etbmod/textures/block")
    texture_base.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    
    for set_name in ETB_SETS:
        # Source files
        front_src = views_dir / f"{set_name}_etb_front.png"
        side_src = views_dir / f"{set_name}_etb_side.png"
        
        # Destination files
        front_dst = texture_base / f"etb_{set_name}_front.png"
        side_dst = texture_base / f"etb_{set_name}_side.png"
        
        # Copy if source exists
        if front_src.exists():
            shutil.copy2(front_src, front_dst)
            print(f"  Copied: {front_src.name} -> {front_dst.name}")
            copied_count += 1
        else:
            print(f"  WARNING: Missing {front_src.name}")
            
        if side_src.exists():
            shutil.copy2(side_src, side_dst)
            print(f"  Copied: {side_src.name} -> {side_dst.name}")
            copied_count += 1
        else:
            print(f"  WARNING: Missing {side_src.name}")
    
    return copied_count

def generate_blockstate_json(set_name):
    """Generate blockstate JSON for an ETB block"""
    return {
        "variants": {
            "facing=north": {"model": f"etbmod:block/etb_{set_name}"},
            "facing=south": {"model": f"etbmod:block/etb_{set_name}", "y": 180},
            "facing=west": {"model": f"etbmod:block/etb_{set_name}", "y": 270},
            "facing=east": {"model": f"etbmod:block/etb_{set_name}", "y": 90}
        }
    }

def generate_block_model_json(set_name):
    """Generate block model JSON for an ETB block"""
    return {
        "parent": "block/orientable",
        "textures": {
            "top": f"etbmod:block/etb_{set_name}_side",
            "bottom": f"etbmod:block/etb_{set_name}_side",
            "front": f"etbmod:block/etb_{set_name}_front",
            "back": f"etbmod:block/etb_{set_name}_front",
            "side": f"etbmod:block/etb_{set_name}_side"
        }
    }

def generate_item_model_json(set_name):
    """Generate item model JSON for an ETB block"""
    return {
        "parent": f"etbmod:block/etb_{set_name}"
    }

def main():
    print("ETB Block Generator")
    print("=" * 50)
    
    # Create directories
    blocks_dir = Path("src/main/java/com/example/etbmod/blocks")
    registry_dir = Path("src/main/java/com/example/etbmod/registry")
    blockstates_dir = Path("src/main/resources/assets/etbmod/blockstates")
    models_block_dir = Path("src/main/resources/assets/etbmod/models/block")
    models_item_dir = Path("src/main/resources/assets/etbmod/models/item")
    
    blocks_dir.mkdir(parents=True, exist_ok=True)
    registry_dir.mkdir(parents=True, exist_ok=True)
    blockstates_dir.mkdir(parents=True, exist_ok=True)
    models_block_dir.mkdir(parents=True, exist_ok=True)
    models_item_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate ETB block classes
    print("\n1. Generating ETB Block Classes...")
    for set_name in ETB_SETS:
        class_name = to_class_name(set_name)
        class_file = blocks_dir / f"{class_name}.java"
        
        with open(class_file, 'w') as f:
            f.write(generate_etb_block_class(set_name))
        
        print(f"  Created: {class_name}.java")
    
    # Generate registry file
    print("\n2. Generating Registry File...")
    registry_file = registry_dir / "GeneratedETBRegistry.java"
    with open(registry_file, 'w') as f:
        f.write(generate_registry_file())
    print(f"  Created: GeneratedETBRegistry.java")
    
    # Copy textures
    print("\n3. Copying Textures...")
    texture_count = copy_textures()
    print(f"  Copied {texture_count} texture files")
    
    # Generate JSON files
    print("\n4. Generating JSON Files...")
    for set_name in ETB_SETS:
        # Blockstate JSON
        blockstate_file = blockstates_dir / f"etb_{set_name}.json"
        with open(blockstate_file, 'w') as f:
            json.dump(generate_blockstate_json(set_name), f, indent=2)
        
        # Block model JSON
        block_model_file = models_block_dir / f"etb_{set_name}.json"
        with open(block_model_file, 'w') as f:
            json.dump(generate_block_model_json(set_name), f, indent=2)
        
        # Item model JSON
        item_model_file = models_item_dir / f"etb_{set_name}.json"
        with open(item_model_file, 'w') as f:
            json.dump(generate_item_model_json(set_name), f, indent=2)
        
        print(f"  Generated JSONs for: etb_{set_name}")
    
    # Clean up old blocks that don't match
    print("\n5. Cleaning Up Old Blocks...")
    # List all existing ETB block files
    existing_blocks = list(blocks_dir.glob("*ETBBlock.java"))
    valid_blocks = {to_class_name(s) + ".java" for s in ETB_SETS}
    valid_blocks.add("ETBBlock.java")  # Keep the base class
    
    removed_count = 0
    for block_file in existing_blocks:
        if block_file.name not in valid_blocks:
            print(f"  Removing outdated: {block_file.name}")
            block_file.unlink()
            removed_count += 1
    
    if removed_count == 0:
        print("  No outdated blocks to remove")
    else:
        print(f"  Removed {removed_count} outdated block files")
    
    print("\n" + "=" * 50)
    print("ETB Block Generation Complete!")
    print(f"  Generated {len(ETB_SETS)} ETB blocks")
    print(f"  Copied {texture_count} textures")
    print(f"  Created {len(ETB_SETS) * 3} JSON files")

if __name__ == "__main__":
    main()