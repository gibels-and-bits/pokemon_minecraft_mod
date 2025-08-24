package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.blocks.*;
import com.example.etbmod.items.GradedSlabItem;
import net.minecraft.block.Block;
import net.minecraft.item.Item;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ModBlocks {
    public static final DeferredRegister<Block> BLOCKS = 
            DeferredRegister.create(ForgeRegistries.BLOCKS, ETBMod.MOD_ID);
    
    public static final List<RegistryObject<Block>> ETB_BLOCKS = new ArrayList<>();
    public static final Map<String, RegistryObject<Block>> ETB_BLOCKS_BY_NAME = new HashMap<>();
    
    // Register all ETB blocks using the factory pattern
    static {
        // Main sets
        registerETB("black_bolt");
        registerETB("breakpoint");
        registerETB("brilliant_stars");
        registerETB("burning_shadows");
        registerETB("cosmic_eclipse");
        registerETB("crown_zenith");
        registerETB("evolutions");
        registerETB("evolving_skies");
        registerETB("hidden_fates");
        registerETB("phantom_forces");
        registerETB("primal_clash");
        registerETB("prismatic_evolutions");
        registerETB("rebel_clash");
        registerETB("shining_fates");
        registerETB("shrouded_fable");
        registerETB("surging_sparks");
        registerETB("team_up");
        registerETB("unified_minds");
        registerETB("vivid_voltage");
        registerETB("white_flare");
    }
    
    // Gamer Table
    public static final RegistryObject<Block> GAMER_TABLE = BLOCKS.register("gamer_table", 
            GamerTableBlock::new);
    
    // Graded slab block for displaying graded cards
    public static final RegistryObject<Block> GRADED_SLAB = BLOCKS.register("graded_slab",
            GradedSlabBlock::new);
    
    // Register the item for the graded slab block
    public static final RegistryObject<Item> GRADED_SLAB_ITEM = ModItems.ITEMS.register("graded_slab",
            () -> new GradedSlabItem(GRADED_SLAB.get()));
    
    // Binder block for storing and displaying cards
    public static final RegistryObject<Block> BINDER_BLOCK = BLOCKS.register("binder",
            BinderBlock::new);
    
    // Vending machine block for purchasing packs and ETBs
    public static final RegistryObject<Block> VENDING_MACHINE = BLOCKS.register("vending_machine",
            VendingMachineBlock::new);
    
    /**
     * Register an ETB block using the factory pattern
     */
    private static RegistryObject<Block> registerETB(String name) {
        String fullName = "etb_" + name;
        RegistryObject<Block> block = BLOCKS.register(fullName, 
            () -> ETBBlockFactory.create(fullName));
        ETB_BLOCKS.add(block);
        ETB_BLOCKS_BY_NAME.put(name, block);
        return block;
    }
    
    /**
     * Get an ETB block by its name (without the etb_ prefix)
     */
    public static RegistryObject<Block> getETBBlock(String name) {
        return ETB_BLOCKS_BY_NAME.get(name);
    }
    
    /**
     * Get all registered ETB block names
     */
    public static List<String> getAllETBNames() {
        return new ArrayList<>(ETB_BLOCKS_BY_NAME.keySet());
    }
}