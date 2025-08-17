package com.example.etbmod.client.texture;

import com.example.etbmod.ETBMod;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.client.renderer.texture.NativeImage;
import net.minecraft.resources.IResourceManager;
import net.minecraft.util.ResourceLocation;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public class CardTextureManager {
    private static final Map<String, ResourceLocation> loadedTextures = new HashMap<>();
    
    public static ResourceLocation getOrLoadCardTexture(String cardPath) {
        // Check if already loaded
        if (loadedTextures.containsKey(cardPath)) {
            return loadedTextures.get(cardPath);
        }
        
        try {
            // Try to load the image from resources (no leading slash for getResourceAsStream)
            String resourcePath = "assets/etbmod/textures/" + cardPath;
            InputStream stream = CardTextureManager.class.getClassLoader().getResourceAsStream(resourcePath);
            
            if (stream == null) {
                // Card texture not found - this is expected for some cards
                return null;
            }
            
            // Load as NativeImage with proper resource management
            NativeImage originalImage;
            try {
                originalImage = NativeImage.read(stream);
            } finally {
                stream.close();
            }
            
            // Create a 256x256 canvas and center the card image WITHOUT stretching
            NativeImage canvasImage = new NativeImage(256, 256, true);
            
            // Fill with transparent
            for (int x = 0; x < 256; x++) {
                for (int y = 0; y < 256; y++) {
                    canvasImage.setPixelRGBA(x, y, 0);
                }
            }
            
            // Get original card dimensions
            int cardWidth = originalImage.getWidth();
            int cardHeight = originalImage.getHeight();
            
            // DO NOT SCALE - just center the original image in the canvas
            // Calculate position to center the card
            int xOffset = (256 - cardWidth) / 2;
            int yOffset = (256 - cardHeight) / 2;
            
            // Ensure we don't go out of bounds
            xOffset = Math.max(0, xOffset);
            yOffset = Math.max(0, yOffset);
            
            // Copy pixels from original to canvas WITHOUT scaling
            int copyWidth = Math.min(cardWidth, 256);
            int copyHeight = Math.min(cardHeight, 256);
            
            for (int x = 0; x < copyWidth; x++) {
                for (int y = 0; y < copyHeight; y++) {
                    int pixel = originalImage.getPixelRGBA(x, y);
                    if (xOffset + x < 256 && yOffset + y < 256) {
                        canvasImage.setPixelRGBA(xOffset + x, yOffset + y, pixel);
                    }
                }
            }
            
            originalImage.close();
            
            // Create DynamicTexture from the canvas
            DynamicTexture dynamicTexture = new DynamicTexture(canvasImage);
            
            // Register with texture manager
            String textureName = "etbmod_card_" + cardPath.replace("/", "_").replace(".png", "");
            ResourceLocation textureLocation = Minecraft.getInstance().getTextureManager()
                .register(textureName, dynamicTexture);
            
            // Cache it
            loadedTextures.put(cardPath, textureLocation);
            
            // Successfully loaded card texture
            return textureLocation;
            
        } catch (IOException e) {
            // Failed to load card texture
            ETBMod.LOGGER.error("Failed to load card texture: " + cardPath, e);
            return null;
        } catch (Exception e) {
            // Unexpected error loading texture
            ETBMod.LOGGER.error("Unexpected error loading texture: " + cardPath, e);
            return null;
        }
    }
    
    public static void clearCache() {
        loadedTextures.clear();
    }
}