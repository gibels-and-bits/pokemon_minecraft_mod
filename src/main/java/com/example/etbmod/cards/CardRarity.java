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
        for (CardRarity r : values()) {
            if (r.displayName.equalsIgnoreCase(rarity)) {
                return r;
            }
        }
        // Handle special cases
        if (rarity.contains("Illustration Rare") && rarity.contains("Special")) {
            return SPECIAL_ILLUSTRATION_RARE;
        }
        if (rarity.contains("Illustration Rare")) {
            return ILLUSTRATION_RARE;
        }
        return COMMON; // Default
    }
}