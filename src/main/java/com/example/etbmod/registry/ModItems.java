package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.items.ScissorsItem;
import com.example.etbmod.items.BoosterPackItem;
import com.example.etbmod.items.CardItem;
import com.example.etbmod.items.CardSlabItem;
import com.example.etbmod.items.GradedSlabItem;
import com.example.etbmod.crafting.CardGradingRecipe;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.crafting.IRecipeSerializer;
import net.minecraft.item.crafting.SpecialRecipeSerializer;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.HashMap;
import java.util.Map;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS = 
            DeferredRegister.create(ForgeRegistries.ITEMS, ETBMod.MOD_ID);
    
    public static final DeferredRegister<IRecipeSerializer<?>> RECIPE_SERIALIZERS = 
            DeferredRegister.create(ForgeRegistries.RECIPE_SERIALIZERS, ETBMod.MOD_ID);
    
    // Register the scissors item
    public static final RegistryObject<Item> SCISSORS = ITEMS.register("scissors",
            () -> new ScissorsItem());
    
    // Pokemon card item
    public static final RegistryObject<Item> POKEMON_CARD = ITEMS.register("pokemon_card",
            () -> new CardItem());
    
    // Booster pack items
    public static final Map<String, RegistryObject<Item>> BOOSTER_PACKS = new HashMap<>();
    
    // ETB Block Items - dynamically registered
    public static final Map<String, RegistryObject<Item>> ETB_ITEMS = new HashMap<>();
    
    // Gamer table item
    public static final RegistryObject<Item> GAMER_TABLE_ITEM = ITEMS.register("gamer_table",
            () -> new BlockItem(ModBlocks.GAMER_TABLE.get(), new Item.Properties().tab(ETBMod.ITEM_GROUP)));
    
    // Card slab item (empty slab for grading)
    public static final RegistryObject<Item> CARD_SLAB = ITEMS.register("card_slab",
            () -> new CardSlabItem());
    
    // Graded slab block item (handled by block registration)
    // The GradedSlabItem is created automatically when the block is registered
    
    // Recipe serializer for card grading
    public static final RegistryObject<SpecialRecipeSerializer<CardGradingRecipe>> CARD_GRADING_RECIPE = 
            RECIPE_SERIALIZERS.register("card_grading",
                    () -> new SpecialRecipeSerializer<>(CardGradingRecipe::new));
    
    static {
        // Only register booster packs for sets that have actual card data
        String[] etbVariants = {
            "black_bolt", "breakpoint", "brilliant_stars", "burning_shadows",
            "cosmic_eclipse", "crown_zenith", "destined_rivals", "evolutions", 
            "evolving_skies", "generations", "hidden_fates", "journey_together", 
            "phantom_forces", "primal_clash", "prismatic_evolutions", "rebel_clash", 
            "shining_fates", "shrouded_fable", "surging_sparks", "team_up", 
            "unified_minds", "vivid_voltage", "white_flare"
        };
        
        for (String variant : etbVariants) {
            BOOSTER_PACKS.put(variant, ITEMS.register("etb_" + variant + "_booster",
                    () -> new BoosterPackItem(variant)));
        }
    }
    
    // Initialize ETB items after ModBlocks is initialized
    public static void initETBItems() {
        for (String etbName : ModBlocks.getAllETBNames()) {
            String fullName = "etb_" + etbName;
            ETB_ITEMS.put(etbName, ITEMS.register(fullName,
                    () -> new BlockItem(ModBlocks.getETBBlock(etbName).get(), 
                            new Item.Properties().tab(ETBMod.ITEM_GROUP))));
        }
    }
}