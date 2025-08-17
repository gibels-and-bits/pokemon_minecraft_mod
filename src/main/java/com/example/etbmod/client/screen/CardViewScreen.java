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
        // Load card texture
        cardTexture = CardTextureManager.getOrLoadCardTexture(card.getImagePath());
    }
    
    @Override
    public void render(MatrixStack matrixStack, int mouseX, int mouseY, float partialTicks) {
        // Dark gradient background
        fillGradient(matrixStack, 0, 0, this.width, this.height, 0xCC000000, 0xCC000000);
        
        // Update scale animation
        if (scale < targetScale) {
            scale = Math.min(scale + 0.02f, targetScale);
        } else if (scale > targetScale) {
            scale = Math.max(scale - 0.02f, targetScale);
        }
        
        // Card dimensions - larger for better viewing
        int cardWidth = 256;  // 128 * 2
        int cardHeight = 512; // 256 * 2
        int x = (this.width - cardWidth) / 2;
        int y = (this.height - cardHeight) / 2;
        
        matrixStack.pushPose();
        
        // Apply scale animation
        float centerX = x + cardWidth / 2.0f;
        float centerY = y + cardHeight / 2.0f;
        matrixStack.translate(centerX, centerY, 0);
        matrixStack.scale(scale, scale, 1.0f);
        matrixStack.translate(-centerX, -centerY, 0);
        
        // Draw card shadow
        fill(matrixStack, x + 6, y + 6, x + cardWidth + 6, y + cardHeight + 6, 0x60000000);
        
        // Draw card
        if (cardTexture != null) {
            RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
            this.minecraft.getTextureManager().bind(cardTexture);
            
            // Draw card from texture (centered in 256x256 texture)
            int textureX = 64;  // Offset in texture where card starts
            int textureY = 0;
            
            // Draw the card
            blit(matrixStack, x, y, cardWidth, cardHeight,
                 textureX, textureY, 128, 256, 256, 256);
        } else {
            // Fallback - draw placeholder
            fill(matrixStack, x, y, x + cardWidth, y + cardHeight, 0xFF404040);
            drawCenteredString(matrixStack, this.font, "Card Loading...", 
                x + cardWidth/2, y + cardHeight/2, 0xFFFFFFFF);
        }
        
        // Draw rarity border glow effect
        if (isRareCard()) {
            int glowColor = getRarityColor(card.getRarity());
            // Draw border
            int borderWidth = 3;
            // Top
            fill(matrixStack, x - borderWidth, y - borderWidth, x + cardWidth + borderWidth, y, glowColor);
            // Bottom
            fill(matrixStack, x - borderWidth, y + cardHeight, x + cardWidth + borderWidth, y + cardHeight + borderWidth, glowColor);
            // Left
            fill(matrixStack, x - borderWidth, y, x, y + cardHeight, glowColor);
            // Right
            fill(matrixStack, x + cardWidth, y, x + cardWidth + borderWidth, y + cardHeight, glowColor);
        }
        
        matrixStack.popPose();
        
        // Draw card info at bottom
        String info = String.format("%s - %s #%s", 
            card.getName(), 
            card.getSetName(), 
            card.getNumber());
        drawCenteredString(matrixStack, this.font, info, 
            this.width / 2, y + cardHeight + 20, 0xFFFFFFFF);
        
        // Draw rarity
        int rarityColor = getRarityTextColor(card.getRarity());
        drawCenteredString(matrixStack, this.font, card.getRarity().getDisplayName(), 
            this.width / 2, y + cardHeight + 35, rarityColor);
        
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