package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.blocks.ETBBlock;
import com.example.etbmod.blocks.GamerTableBlock;
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
    public static final RegistryObject<Block> ETB_151 = registerETB("etb_151");
    public static final RegistryObject<Block> ETB_BLACK_BOLT = registerETB("etb_black_bolt");
    public static final RegistryObject<Block> ETB_BRILLIANT_STARS = registerETB("etb_brilliant_stars");
    public static final RegistryObject<Block> ETB_CELEBRATIONS = registerETB("etb_celebrations");
    public static final RegistryObject<Block> ETB_DESTINED_RIVALS = registerETB("etb_destined_rivals");
    public static final RegistryObject<Block> ETB_GENERATIONS = registerETB("etb_generations");
    public static final RegistryObject<Block> ETB_GROUDON = registerETB("etb_groudon");
    public static final RegistryObject<Block> ETB_JOURNEY_TOGETHER = registerETB("etb_journey_together");
    public static final RegistryObject<Block> ETB_KYOGRE = registerETB("etb_kyogre");
    public static final RegistryObject<Block> ETB_PRISMATIC_EVOLUTIONS = registerETB("etb_prismatic_evolutions");
    public static final RegistryObject<Block> ETB_SURGING_SPARKS = registerETB("etb_surging_sparks");
    public static final RegistryObject<Block> ETB_WHITE_FLARE = registerETB("etb_white_flare");
    
    // Gamer Table
    public static final RegistryObject<Block> GAMER_TABLE = BLOCKS.register("gamer_table", 
            GamerTableBlock::new);
    
    public static RegistryObject<Block> registerETB(String name) {
        RegistryObject<Block> block = BLOCKS.register(name, () -> new ETBBlock(name));
        ETB_BLOCKS.add(block);
        return block;
    }
}
