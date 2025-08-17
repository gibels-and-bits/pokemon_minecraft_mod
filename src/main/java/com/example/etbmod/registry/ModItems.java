package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.items.ScissorsItem;
import com.example.etbmod.items.BoosterPackItem;
import com.example.etbmod.items.CardItem;
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
    
    // Pokemon card item
    public static final RegistryObject<Item> POKEMON_CARD = ITEMS.register("pokemon_card",
            () -> new CardItem());
    
    // Booster pack items
    public static final Map<String, RegistryObject<Item>> BOOSTER_PACKS = new HashMap<>();
    
    // ETB Block Items - All 27 ETBs
    // 20 new ETBs with orthographic textures
    public static final RegistryObject<Item> ETB_BLACK_BOLT_ITEM = ITEMS.register("etb_black_bolt",
            () -> new BlockItem(ModBlocks.ETB_BLACK_BOLT.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_BREAKPOINT_ITEM = ITEMS.register("etb_breakpoint",
            () -> new BlockItem(ModBlocks.ETB_BREAKPOINT.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_BRILLIANT_STARS_ITEM = ITEMS.register("etb_brilliant_stars",
            () -> new BlockItem(ModBlocks.ETB_BRILLIANT_STARS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_BURNING_SHADOWS_ITEM = ITEMS.register("etb_burning_shadows",
            () -> new BlockItem(ModBlocks.ETB_BURNING_SHADOWS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_COSMIC_ECLIPSE_ITEM = ITEMS.register("etb_cosmic_eclipse",
            () -> new BlockItem(ModBlocks.ETB_COSMIC_ECLIPSE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_CROWN_ZENITH_ITEM = ITEMS.register("etb_crown_zenith",
            () -> new BlockItem(ModBlocks.ETB_CROWN_ZENITH.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_EVOLUTIONS_ITEM = ITEMS.register("etb_evolutions",
            () -> new BlockItem(ModBlocks.ETB_EVOLUTIONS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_EVOLVING_SKIES_ITEM = ITEMS.register("etb_evolving_skies",
            () -> new BlockItem(ModBlocks.ETB_EVOLVING_SKIES.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_HIDDEN_FATES_ITEM = ITEMS.register("etb_hidden_fates",
            () -> new BlockItem(ModBlocks.ETB_HIDDEN_FATES.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_PHANTOM_FORCES_ITEM = ITEMS.register("etb_phantom_forces",
            () -> new BlockItem(ModBlocks.ETB_PHANTOM_FORCES.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_PRIMAL_CLASH_ITEM = ITEMS.register("etb_primal_clash",
            () -> new BlockItem(ModBlocks.ETB_PRIMAL_CLASH.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_PRISMATIC_EVOLUTIONS_ITEM = ITEMS.register("etb_prismatic_evolutions",
            () -> new BlockItem(ModBlocks.ETB_PRISMATIC_EVOLUTIONS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_REBEL_CLASH_ITEM = ITEMS.register("etb_rebel_clash",
            () -> new BlockItem(ModBlocks.ETB_REBEL_CLASH.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_SHINING_FATES_ITEM = ITEMS.register("etb_shining_fates",
            () -> new BlockItem(ModBlocks.ETB_SHINING_FATES.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_SHROUDED_FABLE_ITEM = ITEMS.register("etb_shrouded_fable",
            () -> new BlockItem(ModBlocks.ETB_SHROUDED_FABLE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_SURGING_SPARKS_ITEM = ITEMS.register("etb_surging_sparks",
            () -> new BlockItem(ModBlocks.ETB_SURGING_SPARKS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_TEAM_UP_ITEM = ITEMS.register("etb_team_up",
            () -> new BlockItem(ModBlocks.ETB_TEAM_UP.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_UNIFIED_MINDS_ITEM = ITEMS.register("etb_unified_minds",
            () -> new BlockItem(ModBlocks.ETB_UNIFIED_MINDS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_VIVID_VOLTAGE_ITEM = ITEMS.register("etb_vivid_voltage",
            () -> new BlockItem(ModBlocks.ETB_VIVID_VOLTAGE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_WHITE_FLARE_ITEM = ITEMS.register("etb_white_flare",
            () -> new BlockItem(ModBlocks.ETB_WHITE_FLARE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    
    // 7 legacy ETBs
    public static final RegistryObject<Item> ETB_151_ITEM = ITEMS.register("etb_151",
            () -> new BlockItem(ModBlocks.ETB_151.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_CELEBRATIONS_ITEM = ITEMS.register("etb_celebrations",
            () -> new BlockItem(ModBlocks.ETB_CELEBRATIONS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_DESTINED_RIVALS_ITEM = ITEMS.register("etb_destined_rivals",
            () -> new BlockItem(ModBlocks.ETB_DESTINED_RIVALS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_GENERATIONS_ITEM = ITEMS.register("etb_generations",
            () -> new BlockItem(ModBlocks.ETB_GENERATIONS.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_GROUDON_ITEM = ITEMS.register("etb_groudon",
            () -> new BlockItem(ModBlocks.ETB_GROUDON.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_JOURNEY_TOGETHER_ITEM = ITEMS.register("etb_journey_together",
            () -> new BlockItem(ModBlocks.ETB_JOURNEY_TOGETHER.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    public static final RegistryObject<Item> ETB_KYOGRE_ITEM = ITEMS.register("etb_kyogre",
            () -> new BlockItem(ModBlocks.ETB_KYOGRE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    
    // Gamer table item
    public static final RegistryObject<Item> GAMER_TABLE_ITEM = ITEMS.register("gamer_table",
            () -> new BlockItem(ModBlocks.GAMER_TABLE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    
    static {
        // Register booster packs for all ETB variants
        String[] etbVariants = {
            "151", "black_bolt", "breakpoint", "brilliant_stars", "burning_shadows",
            "celebrations", "cosmic_eclipse", "crown_zenith", "destined_rivals", 
            "evolutions", "evolving_skies", "flashfire", "generations", "groudon", 
            "hidden_fates", "journey_together", "kyogre", "phantom_forces", "primal_clash",
            "prismatic_evolutions", "rebel_clash", "shining_fates", "shrouded_fable",
            "surging_sparks", "team_up", "unified_minds", "vivid_voltage", "white_flare",
            "xy2", "xy5", "xy9", "xy12"
        };
        
        for (String variant : etbVariants) {
            BOOSTER_PACKS.put(variant, ITEMS.register("etb_" + variant + "_booster",
                () -> new BoosterPackItem(variant)));
        }
    }
}