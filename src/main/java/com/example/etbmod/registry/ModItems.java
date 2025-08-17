package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.items.ScissorsItem;
import com.example.etbmod.items.BoosterPackItem;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.HashMap;
import java.util.Map;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS = 
            DeferredRegister.create(ForgeRegistries.ITEMS, ETBMod.MOD_ID);
    
    // Register the scissors item
    public static final RegistryObject<Item> SCISSORS = ITEMS.register("scissors",
            () -> new ScissorsItem());
    
    // Booster pack items
    public static final Map<String, RegistryObject<Item>> BOOSTER_PACKS = new HashMap<>();
    
    static {
        // Register booster packs for each ETB variant
        String[] etbVariants = {
            "151", "black_bolt", "brilliant_stars", "celebrations",
            "destined_rivals", "generations", "groudon", "journey_together",
            "kyogre", "prismatic_evolutions", "surging_sparks", "white_flare"
        };
        
        for (String variant : etbVariants) {
            BOOSTER_PACKS.put(variant, ITEMS.register("etb_" + variant + "_booster",
                () -> new BoosterPackItem(variant)));
        }
        
        // Register block items
        ModBlocks.ETB_BLOCKS.forEach(blockReg -> {
            ITEMS.register(blockReg.getId().getPath(), 
                () -> new BlockItem(blockReg.get(), 
                    new Item.Properties().tab(ETBMod.ITEM_GROUP)));
        });
        
        // Register gamer table item
        ITEMS.register("gamer_table", 
            () -> new BlockItem(ModBlocks.GAMER_TABLE.get(), 
                new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    }
}