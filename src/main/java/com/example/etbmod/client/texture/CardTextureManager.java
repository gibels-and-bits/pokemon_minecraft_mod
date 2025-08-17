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
                // Debug: Card texture not found
                // Send debug message
                if (Minecraft.getInstance().player != null) {
                    Minecraft.getInstance().player.displayClientMessage(
                        new net.minecraft.util.text.StringTextComponent("§c[ETB] Texture not found: " + cardPath), true);
                }
                return null;
            }
            
            // Load as NativeImage
            NativeImage originalImage = NativeImage.read(stream);
            stream.close();
            
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
            
            // Debug message
            if (Minecraft.getInstance().player != null) {
                Minecraft.getInstance().player.displayClientMessage(
                    new net.minecraft.util.text.StringTextComponent("§a[ETB] Texture loaded: " + textureName), true);
            }
            
            // Debug: Successfully loaded card texture
            return textureLocation;
            
        } catch (IOException e) {
            // Debug: Failed to load card texture
            e.printStackTrace();
            if (Minecraft.getInstance().player != null) {
                Minecraft.getInstance().player.displayClientMessage(
                    new net.minecraft.util.text.StringTextComponent("§c[ETB] Load error: " + e.getMessage()), true);
            }
            return null;
        } catch (Exception e) {
            // Debug: Unexpected error loading texture
            e.printStackTrace();
            if (Minecraft.getInstance().player != null) {
                Minecraft.getInstance().player.displayClientMessage(
                    new net.minecraft.util.text.StringTextComponent("§c[ETB] Unexpected error: " + e.getClass().getSimpleName()), true);
            }
            return null;
        }
    }
    
    public static void clearCache() {
        loadedTextures.clear();
    }
}