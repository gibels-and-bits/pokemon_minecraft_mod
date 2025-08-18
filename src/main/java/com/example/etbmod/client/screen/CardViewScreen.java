package com.example.etbmod.client.screen;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.client.texture.CardTextureManager;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.text.StringTextComponent;
import org.lwjgl.glfw.GLFW;

public class CardViewScreen extends Screen {
    private final Card card;
    private ResourceLocation cardTexture;
    private float scale = 1.0f;
    private float targetScale = 1.0f;
    
    public CardViewScreen(Card card) {
        super(new StringTextComponent(card.getName()));
        this.card = card;
    }
    
    @Override
    protected void init() {
        super.init();
        // Load card texture with debug logging
        String imagePath = card.getImagePath();
        if (minecraft != null && minecraft.player != null) {
            minecraft.player.displayClientMessage(
                new StringTextComponent("§e[ETB] Loading card view for: " + card.getName() + " - Path: " + imagePath), false);
        }
        cardTexture = CardTextureManager.getOrLoadCardTexture(imagePath);
        if (cardTexture == null && minecraft != null && minecraft.player != null) {
            minecraft.player.displayClientMessage(
                new StringTextComponent("§c[ETB] Failed to load texture for: " + imagePath), false);
        }
    }
    
    @Override
    public void render(MatrixStack matrixStack, int mouseX, int mouseY, float partialTicks) {
        // Try to load texture if it failed during init
        if (cardTexture == null) {
            cardTexture = CardTextureManager.getOrLoadCardTexture(card.getImagePath());
        }
        
        // Dark gradient background with subtle pattern
        fillGradient(matrixStack, 0, 0, this.width, this.height, 0xDD000000, 0xDD111111);
        
        // Add subtle vignette effect
        fillGradient(matrixStack, 0, 0, this.width, 50, 0x44000000, 0x00000000);
        fillGradient(matrixStack, 0, this.height - 50, this.width, this.height, 0x00000000, 0x44000000);
        
        // Update scale animation
        if (scale < targetScale) {
            scale = Math.min(scale + 0.02f, targetScale);
        } else if (scale > targetScale) {
            scale = Math.max(scale - 0.02f, targetScale);
        }
        
        // Card dimensions - maintain proper aspect ratio
        // Cards are stored in 256x256 textures with the card image centered inside
        // Display at a good size that fits the screen
        int maxHeight = Math.min(400, this.height - 120); // Leave room for UI text
        int maxWidth = Math.min(400, this.width - 80);
        
        // Use the smaller constraint to maintain square aspect ratio
        int cardSize = Math.min(maxHeight, maxWidth);
        
        // For better visibility, use at least 256 pixels if space allows
        cardSize = Math.max(cardSize, Math.min(256, Math.min(this.height - 120, this.width - 80)));
        
        int x = (this.width - cardSize) / 2;
        int y = (this.height - cardSize) / 2 - 10; // Slight upward shift for balance
        
        matrixStack.pushPose();
        
        // Apply scale animation
        float centerX = x + cardSize / 2.0f;
        float centerY = y + cardSize / 2.0f;
        matrixStack.translate(centerX, centerY, 0);
        matrixStack.scale(scale, scale, 1.0f);
        matrixStack.translate(-centerX, -centerY, 0);
        
        // Draw card shadow
        fill(matrixStack, x + 6, y + 6, x + cardSize + 6, y + cardSize + 6, 0x60000000);
        
        // Draw card
        if (cardTexture != null) {
            RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
            RenderSystem.enableBlend();
            RenderSystem.defaultBlendFunc();
            this.minecraft.getTextureManager().bind(cardTexture);
            
            // The card fills the entire 256x256 texture with transparent borders
            // Draw the full texture at native resolution
            blit(matrixStack, 
                 x, y,                      // Screen position
                 cardSize, cardSize,        // Screen size (square)
                 0.0f, 0.0f,               // UV start - full texture from top-left
                 256, 256,                  // UV size - entire texture
                 256, 256);                 // Total texture size
        } else {
            // Fallback - draw nicer placeholder with card info
            fillGradient(matrixStack, x, y, x + cardSize, y + cardSize, 0xFF2A2A3E, 0xFF1E1E2E);
            
            // Draw border
            int borderColor = getRarityColor(card.getRarity());
            fill(matrixStack, x, y, x + cardSize, y + 2, borderColor);
            fill(matrixStack, x, y + cardSize - 2, x + cardSize, y + cardSize, borderColor);
            fill(matrixStack, x, y, x + 2, y + cardSize, borderColor);
            fill(matrixStack, x + cardSize - 2, y, x + cardSize, y + cardSize, borderColor);
            
            // Draw card name in center
            drawCenteredString(matrixStack, this.font, card.getName(), 
                x + cardSize/2, y + cardSize/2 - 20, 0xFFFFFFFF);
            
            // Draw set name
            drawCenteredString(matrixStack, this.font, card.getSetName(), 
                x + cardSize/2, y + cardSize/2, 0xFFAAAAAA);
            
            // Draw card number
            drawCenteredString(matrixStack, this.font, "#" + card.getNumber(), 
                x + cardSize/2, y + cardSize/2 + 20, 0xFF888888);
            
            // Draw "Image Not Available" message
            drawCenteredString(matrixStack, this.font, "Image Not Available", 
                x + cardSize/2, y + cardSize - 30, 0xFFFF6666);
        }
        
        // Draw rarity border glow effect
        if (isRareCard()) {
            int glowColor = getRarityColor(card.getRarity());
            // Draw border
            int borderWidth = 3;
            // Top
            fill(matrixStack, x - borderWidth, y - borderWidth, x + cardSize + borderWidth, y, glowColor);
            // Bottom
            fill(matrixStack, x - borderWidth, y + cardSize, x + cardSize + borderWidth, y + cardSize + borderWidth, glowColor);
            // Left
            fill(matrixStack, x - borderWidth, y, x, y + cardSize, glowColor);
            // Right
            fill(matrixStack, x + cardSize, y, x + cardSize + borderWidth, y + cardSize, glowColor);
        }
        
        matrixStack.popPose();
        
        // Draw card info at bottom
        String info = String.format("%s - %s #%s", 
            card.getName(), 
            card.getSetName(), 
            card.getNumber());
        drawCenteredString(matrixStack, this.font, info, 
            this.width / 2, y + cardSize + 20, 0xFFFFFFFF);
        
        // Draw rarity
        int rarityColor = getRarityTextColor(card.getRarity());
        drawCenteredString(matrixStack, this.font, card.getRarity().getDisplayName(), 
            this.width / 2, y + cardSize + 35, rarityColor);
        
        // Draw instruction
        drawCenteredString(matrixStack, this.font, "Press ESC or Right-Click to close", 
            this.width / 2, this.height - 20, 0xFF808080);
        
        super.render(matrixStack, mouseX, mouseY, partialTicks);
    }
    
    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_RIGHT) {
            this.onClose();
            return true;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }
    
    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == GLFW.GLFW_KEY_ESCAPE) {
            this.onClose();
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }
    
    @Override
    public boolean isPauseScreen() {
        return false;
    }
    
    private boolean isRareCard() {
        CardRarity rarity = card.getRarity();
        return rarity != CardRarity.COMMON && rarity != CardRarity.UNCOMMON;
    }
    
    private int getRarityColor(CardRarity rarity) {
        switch (rarity) {
            case RARE: return 0xFF4169E1;
            case DOUBLE_RARE: return 0xFFFFD700;
            case ULTRA_RARE: return 0xFFFF00FF;
            case ILLUSTRATION_RARE: return 0xFF00FFFF;
            case SPECIAL_ILLUSTRATION_RARE: return 0xFFFF1493;
            case BLACK_WHITE_RARE: return 0xFFE0E0E0;
            default: return 0xFF808080;
        }
    }
    
    private int getRarityTextColor(CardRarity rarity) {
        switch (rarity) {
            case COMMON: return 0xFF808080;
            case UNCOMMON: return 0xFF40FF40;
            case RARE: return 0xFF4169E1;
            case DOUBLE_RARE: return 0xFFFFD700;
            case ULTRA_RARE: return 0xFFFF00FF;
            case ILLUSTRATION_RARE: return 0xFF00FFFF;
            case SPECIAL_ILLUSTRATION_RARE: return 0xFFFF1493;
            case BLACK_WHITE_RARE: return 0xFFFFFFFF;
            default: return 0xFFFFFFFF;
        }
    }
}