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
                System.err.println("[ETBMod] Card texture not found: " + resourcePath);
                // Send debug message
                if (Minecraft.getInstance().player != null) {
                    Minecraft.getInstance().player.displayClientMessage(
                        new net.minecraft.util.text.StringTextComponent("§c[ETB] Texture not found: " + cardPath), true);
                }
                return null;
            }
            
            // Load as NativeImage
            NativeImage image = NativeImage.read(stream);
            stream.close();
            
            // Create DynamicTexture
            DynamicTexture dynamicTexture = new DynamicTexture(image);
            
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
            
            System.out.println("[ETBMod] Successfully loaded card texture: " + cardPath);
            return textureLocation;
            
        } catch (IOException e) {
            System.err.println("[ETBMod] Failed to load card texture: " + cardPath);
            e.printStackTrace();
            if (Minecraft.getInstance().player != null) {
                Minecraft.getInstance().player.displayClientMessage(
                    new net.minecraft.util.text.StringTextComponent("§c[ETB] Load error: " + e.getMessage()), true);
            }
            return null;
        } catch (Exception e) {
            System.err.println("[ETBMod] Unexpected error loading texture: " + cardPath);
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