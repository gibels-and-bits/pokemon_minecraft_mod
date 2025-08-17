package com.example.etbmod.cards;

import com.example.etbmod.ETBMod;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.util.ResourceLocation;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.*;

public class CardDatabase {
    private static CardDatabase INSTANCE;
    private final Map<String, List<Card>> setCards = new HashMap<>();
    private final Map<String, Map<CardRarity, List<Card>>> setRarityCards = new HashMap<>();
    private final Random random = new Random();
    
    private CardDatabase() {
        loadCards();
    }
    
    public static synchronized CardDatabase getInstance() {
        if (INSTANCE == null) {
            INSTANCE = new CardDatabase();
        }
        return INSTANCE;
    }
    
    private void loadCards() {
        // Map booster pack names to card set folders
        // Only include sets that have actual card textures in textures/cards/
        Map<String, String> setMappings = new HashMap<>();
        setMappings.put("black_bolt", "black_bolt");
        setMappings.put("breakpoint", "breakpoint");
        setMappings.put("brilliant_stars", "brilliant_stars");
        setMappings.put("burning_shadows", "burning_shadows");
        setMappings.put("cosmic_eclipse", "cosmic_eclipse");
        setMappings.put("crown_zenith", "crown_zenith");
        setMappings.put("destined_rivals", "destined_rivals");
        setMappings.put("evolutions", "evolutions");
        setMappings.put("evolving_skies", "evolving_skies");
        setMappings.put("generations", "generations");
        setMappings.put("hidden_fates", "hidden_fates");
        setMappings.put("journey_together", "journey_together");
        setMappings.put("phantom_forces", "phantom_forces");
        setMappings.put("primal_clash", "primal_clash");
        setMappings.put("prismatic_evolutions", "prismatic_evolutions");
        setMappings.put("rebel_clash", "rebel_clash");
        setMappings.put("shining_fates", "shining_fates");
        setMappings.put("shrouded_fable", "shrouded_fable");
        setMappings.put("surging_sparks", "surging_sparks");
        setMappings.put("team_up", "team_up");
        setMappings.put("unified_minds", "unified_minds");
        setMappings.put("vivid_voltage", "vivid_voltage");
        setMappings.put("white_flare", "white_flare");
        
        for (Map.Entry<String, String> entry : setMappings.entrySet()) {
            String setName = entry.getKey();
            String folderName = entry.getValue();
            loadSetCards(setName, folderName);
        }
    }
    
    private void loadSetCards(String setName, String folderName) {
        try {
            // Load from JAR resources - cards are in textures/cards folder
            String resourcePath = "/assets/etbmod/textures/cards/" + folderName + "/cards_metadata.json";
            InputStream stream = CardDatabase.class.getResourceAsStream(resourcePath);
            
            if (stream == null) {
                // Debug: Card metadata not found in JAR for set
                return;
            }
            
            BufferedReader reader = new BufferedReader(new InputStreamReader(stream));
            JsonParser parser = new JsonParser();
            JsonObject metadata = parser.parse(reader).getAsJsonObject();
            JsonArray cards = metadata.getAsJsonArray("cards");
            
            List<Card> cardList = new ArrayList<>();
            Map<CardRarity, List<Card>> rarityMap = new HashMap<>();
            
            for (JsonElement element : cards) {
                JsonObject cardObj = element.getAsJsonObject();
                
                String id = cardObj.get("id").getAsString();
                String name = cardObj.get("name").getAsString();
                String number = cardObj.get("number").getAsString();
                String rarityStr = cardObj.get("rarity").getAsString();
                CardRarity rarity = CardRarity.fromString(rarityStr);
                
                // Build resource path for image (now using .png)
                // Format matches actual file names: 001_common_snivy.png (all lowercase)
                // Normalize: lowercase, remove apostrophes, underscores for spaces/special chars
                String cleanName = name.toLowerCase()
                    .replace("'", "")
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace(".", "_")
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("à", "a");
                String imagePath = "cards/" + folderName + "/" + 
                    String.format("%03d_%s_%s.png", 
                        Integer.parseInt(number.replaceAll("[^0-9]", "")),
                        rarityStr.toLowerCase().replace(" ", "_"),
                        cleanName);
                
                Card card = new Card(id, name, number, rarity, setName, imagePath);
                cardList.add(card);
                
                rarityMap.computeIfAbsent(rarity, k -> new ArrayList<>()).add(card);
            }
            
            setCards.put(setName, cardList);
            setRarityCards.put(setName, rarityMap);
            
            // Successfully loaded cards for set
            reader.close();
            
        } catch (Exception e) {
            // Error loading cards - log and continue
            ETBMod.LOGGER.error("Failed to load cards for set: " + setName, e);
        }
    }
    
    public List<Card> generateBoosterPack(String setName) {
        List<Card> pack = new ArrayList<>();
        Map<CardRarity, List<Card>> rarityMap = setRarityCards.get(setName);
        
        if (rarityMap == null) {
            // No cards found for set - log warning and return empty list
            ETBMod.LOGGER.warn("No cards found for set: " + setName);
            return pack;
        }
        
        // First 9 cards: mostly commons, some uncommons
        for (int i = 0; i < 9; i++) {
            Card cardToAdd = null;
            if (random.nextFloat() < 0.75f) {
                // 75% chance for common
                List<Card> commons = rarityMap.getOrDefault(CardRarity.COMMON, new ArrayList<>());
                if (!commons.isEmpty()) {
                    cardToAdd = commons.get(random.nextInt(commons.size()));
                }
            }
            
            // If no common found or we rolled uncommon
            if (cardToAdd == null) {
                List<Card> uncommons = rarityMap.getOrDefault(CardRarity.UNCOMMON, new ArrayList<>());
                if (!uncommons.isEmpty()) {
                    cardToAdd = uncommons.get(random.nextInt(uncommons.size()));
                } else {
                    // Fallback to any available card
                    for (List<Card> cards : rarityMap.values()) {
                        if (!cards.isEmpty()) {
                            cardToAdd = cards.get(random.nextInt(cards.size()));
                            break;
                        }
                    }
                }
            }
            
            if (cardToAdd != null) {
                pack.add(cardToAdd);
            }
        }
        
        // 10th card: guaranteed rare or better
        float roll = random.nextFloat();
        Card rareCard = null;
        
        if (roll < 0.005f) {
            // 0.5% chance for Special Illustration Rare
            List<Card> cards = rarityMap.get(CardRarity.SPECIAL_ILLUSTRATION_RARE);
            if (cards != null && !cards.isEmpty()) {
                rareCard = cards.get(random.nextInt(cards.size()));
            }
        } else if (roll < 0.02f) {
            // 1.5% chance for Ultra Rare
            List<Card> cards = rarityMap.get(CardRarity.ULTRA_RARE);
            if (cards != null && !cards.isEmpty()) {
                rareCard = cards.get(random.nextInt(cards.size()));
            }
        } else if (roll < 0.05f) {
            // 3% chance for Double Rare
            List<Card> cards = rarityMap.get(CardRarity.DOUBLE_RARE);
            if (cards != null && !cards.isEmpty()) {
                rareCard = cards.get(random.nextInt(cards.size()));
            }
        } else if (roll < 0.15f) {
            // 10% chance for Illustration Rare
            List<Card> cards = rarityMap.get(CardRarity.ILLUSTRATION_RARE);
            if (cards != null && !cards.isEmpty()) {
                rareCard = cards.get(random.nextInt(cards.size()));
            }
        }
        
        // Default to regular rare
        if (rareCard == null) {
            List<Card> rares = rarityMap.get(CardRarity.RARE);
            if (rares != null && !rares.isEmpty()) {
                rareCard = rares.get(random.nextInt(rares.size()));
            } else {
                // Fallback to uncommon if no rares
                List<Card> uncommons = rarityMap.get(CardRarity.UNCOMMON);
                if (uncommons != null && !uncommons.isEmpty()) {
                    rareCard = uncommons.get(random.nextInt(uncommons.size()));
                }
            }
        }
        
        if (rareCard != null) {
            pack.add(rareCard);
        }
        
        // Debug: Pack generated successfully
        return pack;
    }
}