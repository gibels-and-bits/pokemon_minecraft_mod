package com.example.etbmod.blocks;

import java.util.HashMap;
import java.util.Map;

/**
 * Factory class for creating ETB blocks efficiently without needing individual classes
 */
public class ETBBlockFactory {
    
    private static final Map<String, ETBMetadata> ETB_METADATA = new HashMap<>();
    
    static {
        // Initialize ETB metadata - could be loaded from JSON in the future
        registerETB("black_bolt", "Black Bolt", "swsh12pt5");
        registerETB("breakpoint", "Breakpoint", "xy9");
        registerETB("brilliant_stars", "Brilliant Stars", "swsh45");
        registerETB("burning_shadows", "Burning Shadows", "sm3");
        registerETB("cosmic_eclipse", "Cosmic Eclipse", "sm12");
        registerETB("crown_zenith", "Crown Zenith", "swsh12");
        registerETB("evolutions", "Evolutions", "xy12");
        registerETB("evolving_skies", "Evolving Skies", "swsh7");
        registerETB("hidden_fates", "Hidden Fates", "sm115");
        registerETB("phantom_forces", "Phantom Forces", "xy4");
        registerETB("primal_clash", "Primal Clash", "xy5");
        registerETB("prismatic_evolutions", "Prismatic Evolutions", "sv8");
        registerETB("rebel_clash", "Rebel Clash", "swsh2");
        registerETB("shining_fates", "Shining Fates", "swsh45sv");
        registerETB("shrouded_fable", "Shrouded Fable", "sv6pt5");
        registerETB("surging_sparks", "Surging Sparks", "sv7");
        registerETB("team_up", "Team Up", "sm9");
        registerETB("unified_minds", "Unified Minds", "sm11");
        registerETB("vivid_voltage", "Vivid Voltage", "swsh4");
        registerETB("white_flare", "White Flare", "sv6");
        
        // Legacy sets
        registerETB("151", "151", "sv3pt5");
        registerETB("celebrations", "Celebrations", "cel25");
        registerETB("destined_rivals", "Destined Rivals", "sv5");
        registerETB("generations", "Generations", "g1");
        registerETB("groudon", "Groudon Collection", "ex14");
        registerETB("journey_together", "Journey Together", "sv9");
        registerETB("kyogre", "Kyogre Collection", "ex13");
    }
    
    private static void registerETB(String id, String displayName, String setCode) {
        ETB_METADATA.put(id, new ETBMetadata(id, displayName, setCode));
    }
    
    /**
     * Create an ETB block with the given variant ID
     */
    public static ETBBlock create(String variantId) {
        String cleanId = variantId.replace("etb_", "");
        ETBMetadata metadata = ETB_METADATA.get(cleanId);
        
        if (metadata != null) {
            return new ETBBlock("etb_" + cleanId) {
                @Override
                public String getSetCode() {
                    return metadata.setCode;
                }
                
                @Override
                public String getDisplayName() {
                    return metadata.displayName;
                }
            };
        }
        
        // Fallback for unknown sets
        return new ETBBlock("etb_" + cleanId);
    }
    
    /**
     * Metadata for ETB sets
     */
    private static class ETBMetadata {
        final String id;
        final String displayName;
        final String setCode;
        
        ETBMetadata(String id, String displayName, String setCode) {
            this.id = id;
            this.displayName = displayName;
            this.setCode = setCode;
        }
    }
    
    /**
     * Get all registered ETB IDs
     */
    public static String[] getAllETBIds() {
        return ETB_METADATA.keySet().toArray(new String[0]);
    }
}