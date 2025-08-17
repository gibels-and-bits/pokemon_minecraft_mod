package com.example.etbmod.cards;

public enum CardRarity {
    COMMON("Common", 0.70f),
    UNCOMMON("Uncommon", 0.20f),
    RARE("Rare", 0.07f),
    DOUBLE_RARE("Double Rare", 0.015f),
    ULTRA_RARE("Ultra Rare", 0.01f),
    ILLUSTRATION_RARE("Illustration Rare", 0.004f),
    SPECIAL_ILLUSTRATION_RARE("Special Illustration Rare", 0.001f),
    BLACK_WHITE_RARE("Black White Rare", 0.0005f);
    
    private final String displayName;
    private final float pullRate;
    
    CardRarity(String displayName, float pullRate) {
        this.displayName = displayName;
        this.pullRate = pullRate;
    }
    
    public String getDisplayName() {
        return displayName;
    }
    
    public float getPullRate() {
        return pullRate;
    }
    
    public static CardRarity fromString(String rarity) {
        // Normalize the input - handle underscores, hyphens, and case
        String normalized = rarity.toLowerCase()
            .replace("_", " ")
            .replace("-", " ")
            .trim();
        
        // Direct string mappings for common formats
        switch (normalized) {
            case "common":
                return COMMON;
            case "uncommon":
                return UNCOMMON;
            case "rare":
            case "rare holo":
                return RARE;
            case "double rare":
            case "double_rare":
                return DOUBLE_RARE;
            case "ultra rare":
            case "ultra_rare":
                return ULTRA_RARE;
            case "illustration rare":
            case "illustration_rare":
                return ILLUSTRATION_RARE;
            case "special illustration rare":
            case "special_illustration_rare":
                return SPECIAL_ILLUSTRATION_RARE;
            case "black white rare":
            case "black_white_rare":
                return BLACK_WHITE_RARE;
        }
        
        // Check against display names (case-insensitive)
        for (CardRarity r : values()) {
            if (r.displayName.equalsIgnoreCase(rarity)) {
                return r;
            }
        }
        
        // Handle special cases with partial matches
        String lowerRarity = rarity.toLowerCase();
        if (lowerRarity.contains("special") && lowerRarity.contains("illustration")) {
            return SPECIAL_ILLUSTRATION_RARE;
        }
        if (lowerRarity.contains("illustration") && lowerRarity.contains("rare")) {
            return ILLUSTRATION_RARE;
        }
        if (lowerRarity.contains("ultra") && lowerRarity.contains("rare")) {
            return ULTRA_RARE;
        }
        if (lowerRarity.contains("double") && lowerRarity.contains("rare")) {
            return DOUBLE_RARE;
        }
        if (lowerRarity.contains("black") && lowerRarity.contains("white")) {
            return BLACK_WHITE_RARE;
        }
        if (lowerRarity.contains("rare")) {
            return RARE;
        }
        if (lowerRarity.contains("uncommon")) {
            return UNCOMMON;
        }
        
        return COMMON; // Default
    }
}