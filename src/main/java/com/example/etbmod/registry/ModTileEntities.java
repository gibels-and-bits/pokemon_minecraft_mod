package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.tileentities.GradedSlabTileEntity;
import net.minecraft.tileentity.TileEntityType;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import com.example.etbmod.tileentity.GamerTableTileEntity;

public class ModTileEntities {
    public static final DeferredRegister<TileEntityType<?>> TILE_ENTITIES = 
            DeferredRegister.create(ForgeRegistries.TILE_ENTITIES, ETBMod.MOD_ID);
    
    public static final RegistryObject<TileEntityType<GamerTableTileEntity>> GAMER_TABLE = 
            TILE_ENTITIES.register("gamer_table",
                    () -> TileEntityType.Builder.of(GamerTableTileEntity::new, ModBlocks.GAMER_TABLE.get())
                            .build(null));
    
    public static final RegistryObject<TileEntityType<GradedSlabTileEntity>> GRADED_SLAB = 
            TILE_ENTITIES.register("graded_slab",
                    () -> TileEntityType.Builder.of(GradedSlabTileEntity::new, ModBlocks.GRADED_SLAB.get())
                            .build(null));
}