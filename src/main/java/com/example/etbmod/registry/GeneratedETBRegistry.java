package com.example.etbmod.registry;

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
    public static final RegistryObject<Block> BLACK_BOLT_ETB = ModBlocks.BLOCKS.register("etb_black_bolt", BlackBoltETBBlock::new);
    public static final RegistryObject<Block> BREAKPOINT_ETB = ModBlocks.BLOCKS.register("etb_breakpoint", BreakpointETBBlock::new);
    public static final RegistryObject<Block> BRILLIANT_STARS_ETB = ModBlocks.BLOCKS.register("etb_brilliant_stars", BrilliantStarsETBBlock::new);
    public static final RegistryObject<Block> BURNING_SHADOWS_ETB = ModBlocks.BLOCKS.register("etb_burning_shadows", BurningShadowsETBBlock::new);
    public static final RegistryObject<Block> COSMIC_ECLIPSE_ETB = ModBlocks.BLOCKS.register("etb_cosmic_eclipse", CosmicEclipseETBBlock::new);
    public static final RegistryObject<Block> CROWN_ZENITH_ETB = ModBlocks.BLOCKS.register("etb_crown_zenith", CrownZenithETBBlock::new);
    public static final RegistryObject<Block> EVOLUTIONS_ETB = ModBlocks.BLOCKS.register("etb_evolutions", EvolutionsETBBlock::new);
    public static final RegistryObject<Block> EVOLVING_SKIES_ETB = ModBlocks.BLOCKS.register("etb_evolving_skies", EvolvingSkiesETBBlock::new);
    public static final RegistryObject<Block> HIDDEN_FATES_ETB = ModBlocks.BLOCKS.register("etb_hidden_fates", HiddenFatesETBBlock::new);
    public static final RegistryObject<Block> PHANTOM_FORCES_ETB = ModBlocks.BLOCKS.register("etb_phantom_forces", PhantomForcesETBBlock::new);
    public static final RegistryObject<Block> PRIMAL_CLASH_ETB = ModBlocks.BLOCKS.register("etb_primal_clash", PrimalClashETBBlock::new);
    public static final RegistryObject<Block> PRISMATIC_EVOLUTIONS_ETB = ModBlocks.BLOCKS.register("etb_prismatic_evolutions", PrismaticEvolutionsETBBlock::new);
    public static final RegistryObject<Block> REBEL_CLASH_ETB = ModBlocks.BLOCKS.register("etb_rebel_clash", RebelClashETBBlock::new);
    public static final RegistryObject<Block> SHINING_FATES_ETB = ModBlocks.BLOCKS.register("etb_shining_fates", ShiningFatesETBBlock::new);
    public static final RegistryObject<Block> SHROUDED_FABLE_ETB = ModBlocks.BLOCKS.register("etb_shrouded_fable", ShroudedFableETBBlock::new);
    public static final RegistryObject<Block> SURGING_SPARKS_ETB = ModBlocks.BLOCKS.register("etb_surging_sparks", SurgingSparksETBBlock::new);
    public static final RegistryObject<Block> TEAM_UP_ETB = ModBlocks.BLOCKS.register("etb_team_up", TeamUpETBBlock::new);
    public static final RegistryObject<Block> UNIFIED_MINDS_ETB = ModBlocks.BLOCKS.register("etb_unified_minds", UnifiedMindsETBBlock::new);
    public static final RegistryObject<Block> VIVID_VOLTAGE_ETB = ModBlocks.BLOCKS.register("etb_vivid_voltage", VividVoltageETBBlock::new);
    public static final RegistryObject<Block> WHITE_FLARE_ETB = ModBlocks.BLOCKS.register("etb_white_flare", WhiteFlareETBBlock::new);

    // ETB Block Items
    public static final RegistryObject<Item> BLACK_BOLT_ETB_ITEM = ModItems.ITEMS.register("etb_black_bolt", () -> new BlockItem(BLACK_BOLT_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> BREAKPOINT_ETB_ITEM = ModItems.ITEMS.register("etb_breakpoint", () -> new BlockItem(BREAKPOINT_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> BRILLIANT_STARS_ETB_ITEM = ModItems.ITEMS.register("etb_brilliant_stars", () -> new BlockItem(BRILLIANT_STARS_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> BURNING_SHADOWS_ETB_ITEM = ModItems.ITEMS.register("etb_burning_shadows", () -> new BlockItem(BURNING_SHADOWS_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> COSMIC_ECLIPSE_ETB_ITEM = ModItems.ITEMS.register("etb_cosmic_eclipse", () -> new BlockItem(COSMIC_ECLIPSE_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> CROWN_ZENITH_ETB_ITEM = ModItems.ITEMS.register("etb_crown_zenith", () -> new BlockItem(CROWN_ZENITH_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> EVOLUTIONS_ETB_ITEM = ModItems.ITEMS.register("etb_evolutions", () -> new BlockItem(EVOLUTIONS_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> EVOLVING_SKIES_ETB_ITEM = ModItems.ITEMS.register("etb_evolving_skies", () -> new BlockItem(EVOLVING_SKIES_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> HIDDEN_FATES_ETB_ITEM = ModItems.ITEMS.register("etb_hidden_fates", () -> new BlockItem(HIDDEN_FATES_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> PHANTOM_FORCES_ETB_ITEM = ModItems.ITEMS.register("etb_phantom_forces", () -> new BlockItem(PHANTOM_FORCES_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> PRIMAL_CLASH_ETB_ITEM = ModItems.ITEMS.register("etb_primal_clash", () -> new BlockItem(PRIMAL_CLASH_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> PRISMATIC_EVOLUTIONS_ETB_ITEM = ModItems.ITEMS.register("etb_prismatic_evolutions", () -> new BlockItem(PRISMATIC_EVOLUTIONS_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> REBEL_CLASH_ETB_ITEM = ModItems.ITEMS.register("etb_rebel_clash", () -> new BlockItem(REBEL_CLASH_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> SHINING_FATES_ETB_ITEM = ModItems.ITEMS.register("etb_shining_fates", () -> new BlockItem(SHINING_FATES_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> SHROUDED_FABLE_ETB_ITEM = ModItems.ITEMS.register("etb_shrouded_fable", () -> new BlockItem(SHROUDED_FABLE_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> SURGING_SPARKS_ETB_ITEM = ModItems.ITEMS.register("etb_surging_sparks", () -> new BlockItem(SURGING_SPARKS_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> TEAM_UP_ETB_ITEM = ModItems.ITEMS.register("etb_team_up", () -> new BlockItem(TEAM_UP_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> UNIFIED_MINDS_ETB_ITEM = ModItems.ITEMS.register("etb_unified_minds", () -> new BlockItem(UNIFIED_MINDS_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> VIVID_VOLTAGE_ETB_ITEM = ModItems.ITEMS.register("etb_vivid_voltage", () -> new BlockItem(VIVID_VOLTAGE_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));
    public static final RegistryObject<Item> WHITE_FLARE_ETB_ITEM = ModItems.ITEMS.register("etb_white_flare", () -> new BlockItem(WHITE_FLARE_ETB.get(), new Item.Properties().tab(ItemGroup.TAB_DECORATIONS)));

    // Registry map for easy lookup
    public static final Map<String, RegistryObject<Block>> ETB_BLOCKS = new HashMap<>();

    static {
        ETB_BLOCKS.put("black_bolt", BLACK_BOLT_ETB);
        ETB_BLOCKS.put("breakpoint", BREAKPOINT_ETB);
        ETB_BLOCKS.put("brilliant_stars", BRILLIANT_STARS_ETB);
        ETB_BLOCKS.put("burning_shadows", BURNING_SHADOWS_ETB);
        ETB_BLOCKS.put("cosmic_eclipse", COSMIC_ECLIPSE_ETB);
        ETB_BLOCKS.put("crown_zenith", CROWN_ZENITH_ETB);
        ETB_BLOCKS.put("evolutions", EVOLUTIONS_ETB);
        ETB_BLOCKS.put("evolving_skies", EVOLVING_SKIES_ETB);
        ETB_BLOCKS.put("hidden_fates", HIDDEN_FATES_ETB);
        ETB_BLOCKS.put("phantom_forces", PHANTOM_FORCES_ETB);
        ETB_BLOCKS.put("primal_clash", PRIMAL_CLASH_ETB);
        ETB_BLOCKS.put("prismatic_evolutions", PRISMATIC_EVOLUTIONS_ETB);
        ETB_BLOCKS.put("rebel_clash", REBEL_CLASH_ETB);
        ETB_BLOCKS.put("shining_fates", SHINING_FATES_ETB);
        ETB_BLOCKS.put("shrouded_fable", SHROUDED_FABLE_ETB);
        ETB_BLOCKS.put("surging_sparks", SURGING_SPARKS_ETB);
        ETB_BLOCKS.put("team_up", TEAM_UP_ETB);
        ETB_BLOCKS.put("unified_minds", UNIFIED_MINDS_ETB);
        ETB_BLOCKS.put("vivid_voltage", VIVID_VOLTAGE_ETB);
        ETB_BLOCKS.put("white_flare", WHITE_FLARE_ETB);
    }
}
