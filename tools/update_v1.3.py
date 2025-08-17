#!/usr/bin/env python3
"""
ETB Mod v1.3 - Expert Review and Fixes
- Fix UV mapping for non-square faces
- Add proper rotation support
- Optimize rendering
- Improve block properties
"""

import json
import os
from pathlib import Path

class V13Expert:
    def __init__(self):
        self.assets_dir = Path("src/main/resources/assets/etbmod")
        self.java_dir = Path("src/main/java/com/example/etbmod")
        self.models_dir = self.assets_dir / "models" / "block"
        
    def fix_block_model_uvs(self, variant):
        """Fix UV mapping for proper texture display on non-cubic shape"""
        model_path = self.models_dir / f"{variant}.json"
        
        if not model_path.exists():
            return False
            
        # Proper UV mapping for ETB shape
        # The box is 13 wide, 7 deep, 12 tall
        model = {
            "parent": "block/block",
            "display": {
                "gui": {
                    "rotation": [30, 45, 0],
                    "translation": [0, 0, 0],
                    "scale": [0.625, 0.625, 0.625]
                },
                "ground": {
                    "rotation": [0, 0, 0],
                    "translation": [0, 3, 0],
                    "scale": [0.25, 0.25, 0.25]
                },
                "fixed": {
                    "rotation": [0, 0, 0],
                    "translation": [0, 0, 0],
                    "scale": [0.5, 0.5, 0.5]
                },
                "thirdperson_righthand": {
                    "rotation": [75, 45, 0],
                    "translation": [0, 2.5, 0],
                    "scale": [0.375, 0.375, 0.375]
                },
                "firstperson_righthand": {
                    "rotation": [0, 45, 0],
                    "translation": [0, 4, 0],
                    "scale": [0.40, 0.40, 0.40]
                },
                "firstperson_lefthand": {
                    "rotation": [0, 225, 0],
                    "translation": [0, 4, 0],
                    "scale": [0.40, 0.40, 0.40]
                }
            },
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
                    "name": "etb_box",
                    "from": [1.5, 0, 4.5],
                    "to": [14.5, 12, 11.5],
                    "faces": {
                        "north": {
                            "uv": [0, 2, 16, 16],  # Adjusted for 13x12 face
                            "texture": "#north",
                            "cullface": "north"
                        },
                        "south": {
                            "uv": [0, 2, 16, 16],  # Same as front
                            "texture": "#south",
                            "cullface": "south"
                        },
                        "east": {
                            "uv": [0, 2, 11, 16],  # Adjusted for 7x12 face
                            "texture": "#east",
                            "cullface": "east"
                        },
                        "west": {
                            "uv": [5, 2, 16, 16],  # Adjusted for 7x12 face
                            "texture": "#west",
                            "cullface": "west"
                        },
                        "up": {
                            "uv": [1, 4, 15, 12],  # Adjusted for 13x7 face
                            "texture": "#up",
                            "cullface": "up"
                        },
                        "down": {
                            "uv": [1, 4, 15, 12],  # Adjusted for 13x7 face
                            "texture": "#down",
                            "cullface": "down"
                        }
                    }
                }
            ]
        }
        
        with open(model_path, 'w') as f:
            json.dump(model, f, indent=2)
        
        return True
    
    def update_blockstates_with_rotation(self, variant):
        """Add rotation support to blockstates"""
        blockstate_path = self.assets_dir / "blockstates" / f"{variant}.json"
        
        if not blockstate_path.exists():
            return False
        
        # Support for directional placement
        blockstate = {
            "variants": {
                "facing=north": {"model": f"etbmod:block/{variant}"},
                "facing=south": {"model": f"etbmod:block/{variant}", "y": 180},
                "facing=west": {"model": f"etbmod:block/{variant}", "y": 270},
                "facing=east": {"model": f"etbmod:block/{variant}", "y": 90}
            }
        }
        
        with open(blockstate_path, 'w') as f:
            json.dump(blockstate, f, indent=2)
        
        return True
    
    def create_improved_etb_block(self):
        """Create an improved ETBBlock with rotation support"""
        block_code = '''package com.example.etbmod.blocks;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.HorizontalBlock;
import net.minecraft.block.SoundType;
import net.minecraft.block.material.Material;
import net.minecraft.item.BlockItemUseContext;
import net.minecraft.state.DirectionProperty;
import net.minecraft.state.StateContainer;
import net.minecraft.util.Direction;
import net.minecraft.util.Mirror;
import net.minecraft.util.Rotation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.shapes.ISelectionContext;
import net.minecraft.util.math.shapes.VoxelShape;
import net.minecraft.util.math.shapes.VoxelShapes;
import net.minecraft.world.IBlockReader;
import net.minecraftforge.common.ToolType;

public class ETBBlock extends Block {
    
    public static final DirectionProperty FACING = HorizontalBlock.FACING;
    
    // ETB dimensions: 6.5" x 3.43" x 7.36" (width x depth x height)
    // Scaled to Minecraft: 13x7x12 pixels
    private static final VoxelShape SHAPE_NS = Block.box(1.5D, 0.0D, 4.5D, 14.5D, 12.0D, 11.5D);
    private static final VoxelShape SHAPE_EW = Block.box(4.5D, 0.0D, 1.5D, 11.5D, 12.0D, 14.5D);
    
    public ETBBlock() {
        super(Properties.of(Material.WOOD)
                .strength(2.0F, 3.0F)
                .sound(SoundType.WOOD)
                .harvestTool(ToolType.AXE)
                .harvestLevel(0)
                .noOcclusion()
                .lightLevel((state) -> 0));
        this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.NORTH));
    }
    
    @Override
    public VoxelShape getShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        Direction direction = state.getValue(FACING);
        return (direction == Direction.NORTH || direction == Direction.SOUTH) ? SHAPE_NS : SHAPE_EW;
    }
    
    @Override
    public VoxelShape getCollisionShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        return getShape(state, worldIn, pos, context);
    }
    
    @Override
    public BlockState getStateForPlacement(BlockItemUseContext context) {
        return this.defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }
    
    @Override
    public BlockState rotate(BlockState state, Rotation rot) {
        return state.setValue(FACING, rot.rotate(state.getValue(FACING)));
    }
    
    @Override
    public BlockState mirror(BlockState state, Mirror mirrorIn) {
        return state.rotate(mirrorIn.getRotation(state.getValue(FACING)));
    }
    
    @Override
    protected void createBlockStateDefinition(StateContainer.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }
    
    @Override
    public boolean useShapeForLightOcclusion(BlockState state) {
        return true;
    }
}'''
        
        block_path = self.java_dir / "blocks" / "ETBBlock.java"
        with open(block_path, 'w') as f:
            f.write(block_code)
        
        return True
    
    def update_mod_metadata(self):
        """Update mods.toml with better metadata"""
        mods_toml = """modLoader="javafml"
loaderVersion="[36,)"
license="All rights reserved"
issueTrackerURL="https://github.com/yourname/etbmod/issues"
logoFile="etbmod_logo.png"

[[mods]]
modId="etbmod"
version="${file.jarVersion}"
displayName="Elite Trainer Box Mod"
credits="Pokemon TCG Community"
authors="ETB Mod Team"
description='''Brings Pokemon TCG Elite Trainer Boxes to Minecraft!

Features:
- 13 unique ETB designs from real Pokemon TCG sets
- Custom 3D models with accurate proportions
- Directional placement - rotate your ETBs
- Decorative blocks perfect for Pokemon-themed builds
- Collectible items to display in your world

Version 1.3:
- Fixed UV mapping for proper texture display
- Added rotation support for placement direction
- Optimized rendering and display angles
- Improved block properties and interactions
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
        
        return True
    
    def run(self):
        """Run all v1.3 improvements"""
        print("ETB Mod v1.3 - Expert Review & Improvements")
        print("=" * 50)
        
        # Find all variants
        variants = []
        if self.models_dir.exists():
            for model_file in self.models_dir.glob("etb_*.json"):
                variants.append(model_file.stem)
        
        print(f"Found {len(variants)} ETB variants to update")
        print()
        
        # Update ETBBlock with rotation support
        print("Updating ETBBlock.java with rotation support...")
        if self.create_improved_etb_block():
            print("  ✓ ETBBlock updated with directional placement")
        print()
        
        # Fix all models
        print("Fixing block models with proper UV mapping...")
        for variant in sorted(variants):
            if self.fix_block_model_uvs(variant):
                print(f"  ✓ Fixed {variant}")
        print()
        
        # Update blockstates
        print("Updating blockstates with rotation support...")
        for variant in sorted(variants):
            if self.update_blockstates_with_rotation(variant):
                print(f"  ✓ Updated {variant}")
        print()
        
        # Update mod metadata
        print("Updating mod metadata...")
        if self.update_mod_metadata():
            print("  ✓ Updated mods.toml")
        print()
        
        print("=" * 50)
        print("✓ v1.3 Expert Review Complete!")
        print()
        print("Improvements made:")
        print("  • Fixed UV mapping for all faces")
        print("  • Added directional placement with rotation")
        print("  • Optimized display angles for inventory/hand")
        print("  • Improved block properties")
        print("  • Updated mod metadata")

if __name__ == "__main__":
    expert = V13Expert()
    expert.run()