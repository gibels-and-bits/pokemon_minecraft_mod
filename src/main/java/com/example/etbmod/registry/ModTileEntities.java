package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.tileentity.GamerTableTileEntity;
import net.minecraft.tileentity.TileEntityType;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

public class ModTileEntities {
    public static final DeferredRegister<TileEntityType<?>> TILE_ENTITIES = 
            DeferredRegister.create(ForgeRegistries.TILE_ENTITIES, ETBMod.MOD_ID);
    
    public static final RegistryObject<TileEntityType<GamerTableTileEntity>> GAMER_TABLE = 
            TILE_ENTITIES.register("gamer_table", 
                () -> TileEntityType.Builder.of(GamerTableTileEntity::new, 
                    ModBlocks.GAMER_TABLE.get()).build(null));
}