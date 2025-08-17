package com.example.etbmod.config;

/**
 * Configuration constants for the ETB Mod
 * These values can be externalized to a config file in the future
 */
public class ETBConfig {
    
    // Pack Generation Settings
    public static final int BOOSTER_PACK_COUNT = 9;
    public static final int CARDS_PER_PACK = 10;
    public static final int COMMON_CARDS_PER_PACK = 9;
    
    // Card Rarity Chances for 10th card
    public static final float CHANCE_SPECIAL_ILLUSTRATION_RARE = 0.005f;
    public static final float CHANCE_ULTRA_RARE = 0.02f;
    public static final float CHANCE_ILLUSTRATION_RARE = 0.05f;
    public static final float CHANCE_DOUBLE_RARE = 0.10f;
    public static final float CHANCE_RARE = 0.825f; // Remainder
    
    // Common/Uncommon ratio for first 9 cards
    public static final float COMMON_CARD_CHANCE = 0.75f;
    
    // Texture Settings
    public static final int CARD_TEXTURE_WIDTH = 256;
    public static final int CARD_TEXTURE_HEIGHT = 256;
    public static final int CARD_DISPLAY_WIDTH = 128;
    public static final int CARD_DISPLAY_HEIGHT = 256;
    
    // GUI Settings
    public static final int CARD_REVEAL_WIDTH = 192;  // 128 * 1.5
    public static final int CARD_REVEAL_HEIGHT = 384; // 256 * 1.5
    
    // Animation Settings
    public static final float CARD_SCALE_SPEED = 0.05f;
    public static final float GLOW_EFFECT_SPEED = 0.02f;
    public static final float GLOW_EFFECT_MIN = 0.3f;
    public static final float GLOW_EFFECT_MAX = 1.0f;
    
    // Item Stack Settings
    public static final int MAX_BOOSTER_PACK_STACK = 64;
    public static final int MAX_CARD_STACK = 1;
    
    // Debug Settings
    public static final boolean ENABLE_DEBUG_MESSAGES = false;
    public static final boolean ENABLE_TEXTURE_DEBUG = false;
    
    // Performance Settings
    public static final int MAX_CACHED_TEXTURES = 100;
    public static final long TEXTURE_CACHE_TTL = 300000; // 5 minutes in ms
}