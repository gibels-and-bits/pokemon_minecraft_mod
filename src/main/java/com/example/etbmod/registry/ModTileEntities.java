package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.tileentities.GradedSlabTileEntity;
import com.example.etbmod.tileentity.BinderTileEntity;
import com.example.etbmod.tileentity.VendingMachineTileEntity;
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
    
    public static final RegistryObject<TileEntityType<BinderTileEntity>> BINDER_TILE_ENTITY = 
            TILE_ENTITIES.register("binder",
                    () -> TileEntityType.Builder.of(BinderTileEntity::new, ModBlocks.BINDER_BLOCK.get())
                            .build(null));
    
    public static final RegistryObject<TileEntityType<VendingMachineTileEntity>> VENDING_MACHINE = 
            TILE_ENTITIES.register("vending_machine",
                    () -> TileEntityType.Builder.of(VendingMachineTileEntity::new, ModBlocks.VENDING_MACHINE.get())
                            .build(null));
}