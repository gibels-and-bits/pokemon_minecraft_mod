package com.example.etbmod.client.screen;

import com.example.etbmod.ETBMod;
import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.client.texture.CardTextureManager;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.text.StringTextComponent;
import org.lwjgl.glfw.GLFW;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CardRevealScreen extends Screen {
    private final List<Card> cards;
    private int currentCardIndex = 0;
    private final Map<String, ResourceLocation> cardTextures = new HashMap<>();
    private boolean[] revealed;
    private long lastKeyPress = 0;
    private boolean celebrationPlayed = false;
    
    // Animation
    private float cardScale = 1.0f;
    private float targetScale = 1.0f;
    private float glowEffect = 0.0f;
    private boolean glowIncreasing = true;
    
    public CardRevealScreen(List<Card> cards) {
        super(new StringTextComponent("Card Pack Opening"));
        this.cards = cards;
        this.revealed = new boolean[cards.size()];
        this.revealed[0] = true; // First card starts revealed
    }
    
    @Override
    protected void init() {
        super.init();
        // Preload card textures from resources
        for (Card card : cards) {
            loadCardTexture(card);
        }
    }
    
    private void loadCardTexture(Card card) {
        String path = card.getImagePath();
        if (cardTextures.containsKey(path)) {
            return;
        }
        
        // Use the new CardTextureManager to load textures dynamically
        ResourceLocation textureLocation = CardTextureManager.getOrLoadCardTexture(path);
        
        if (textureLocation != null) {
            cardTextures.put(path, textureLocation);
        }
    }
    
    @Override
    public void render(MatrixStack matrixStack, int mouseX, int mouseY, float partialTicks) {
        // Beautiful gradient background
        fillGradient(matrixStack, 0, 0, this.width, this.height, 0xFF0F0F1F, 0xFF1A1A3A);
        
        // Add subtle animated stars/particles in background
        for (int i = 0; i < 20; i++) {
            int x = (int)(Math.sin(System.currentTimeMillis() / 1000.0 + i * 0.5) * 100 + this.width / 2);
            int y = (int)(Math.cos(System.currentTimeMillis() / 800.0 + i * 0.7) * 80 + this.height / 2);
            fill(matrixStack, x, y, x + 2, y + 2, 0x40FFFFFF);
        }
        
        // Update animations
        if (cardScale < targetScale) {
            cardScale = Math.min(cardScale + 0.05f, targetScale);
        } else if (cardScale > targetScale) {
            cardScale = Math.max(cardScale - 0.05f, targetScale);
        }
        
        // Update glow effect for rare cards
        if (currentCardIndex == cards.size() - 1 && isRareCard(cards.get(currentCardIndex))) {
            if (glowIncreasing) {
                glowEffect += 0.02f;
                if (glowEffect >= 1.0f) {
                    glowEffect = 1.0f;
                    glowIncreasing = false;
                }
            } else {
                glowEffect -= 0.02f;
                if (glowEffect <= 0.3f) {
                    glowEffect = 0.3f;
                    glowIncreasing = true;
                }
            }
        }
        
        // Draw current card
        Card currentCard = cards.get(currentCardIndex);
        
        // Card dimensions - proper Pokemon TCG aspect ratio (approximately 5:7)
        // Texture is 256x256 (power of 2), but we only use 180x252 of it (maintains 5:7 ratio)
        int cardWidth = 180;
        int cardHeight = 252;
        int x = (this.width - cardWidth) / 2;
        int y = (this.height - cardHeight) / 2 - 30;
        
        matrixStack.pushPose();
        
        // Apply scale animation
        float centerX = x + cardWidth / 2.0f;
        float centerY = y + cardHeight / 2.0f;
        matrixStack.translate(centerX, centerY, 0);
        matrixStack.scale(cardScale, cardScale, 1.0f);
        matrixStack.translate(-centerX, -centerY, 0);
        
        // Draw glow effect for rare cards
        if (currentCardIndex == cards.size() - 1 && isRareCard(currentCard)) {
            int glowColor = getRarityColor(currentCard.getRarity());
            int alpha = (int)(glowEffect * 100);
            // Draw expanding glow rectangles
            for (int i = 0; i < 5; i++) {
                int offset = i * 4;
                int glowAlpha = alpha / (i + 1);
                fill(matrixStack, x - offset, y - offset, x + cardWidth + offset, y + cardHeight + offset, 
                     (glowAlpha << 24) | (glowColor & 0x00FFFFFF));
            }
        }
        
        // Draw card shadow
        fill(matrixStack, x + 4, y + 4, x + cardWidth + 4, y + cardHeight + 4, 0x80000000);
        
        if (revealed[currentCardIndex]) {
            // Draw card image from resources
            ResourceLocation texture = cardTextures.get(currentCard.getImagePath());
            if (texture != null) {
                try {
                    RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
                    this.minecraft.getTextureManager().bind(texture);
                    
                    // Texture is ready to render
                    // Card textures are stored in 256x256 power-of-2 textures
                    // But actual card image only uses 180x252 (5:7 ratio) of that space
                    // This ensures proper aspect ratio while maintaining power-of-2 texture size
                    
                    // Render the card portion of the texture (180x252 out of 256x256)
                    blit(matrixStack, x, y, 0, 0, cardWidth, cardHeight, 256, 256);
                } catch (Exception e) {
                    // If texture loading fails, use placeholder
                    // Debug: Failed to render texture
                    texture = null;
                }
            }
            
            if (texture == null) {
                // Fallback: draw styled placeholder
                fill(matrixStack, x, y, x + cardWidth, y + cardHeight, 0xFF2A2A3E);
                fill(matrixStack, x + 2, y + 2, x + cardWidth - 2, y + cardHeight - 2, 0xFF35354A);
                
                // Draw card info
                drawCenteredString(matrixStack, this.font, currentCard.getName(), 
                    x + cardWidth / 2, y + cardHeight / 2 - 30, 0xFFFFFF);
                    
                // Draw rarity with special styling
                int rarityColor = getRarityColor(currentCard.getRarity());
                drawCenteredString(matrixStack, this.font, "★ " + currentCard.getRarity().getDisplayName() + " ★", 
                    x + cardWidth / 2, y + cardHeight / 2, rarityColor);
                    
                // Draw set name
                drawCenteredString(matrixStack, this.font, currentCard.getSetName().toUpperCase(), 
                    x + cardWidth / 2, y + cardHeight / 2 + 30, 0xFF888888);
            }
            
            // Draw card border based on rarity
            int borderColor = getRarityColor(currentCard.getRarity());
            // Top border
            fill(matrixStack, x, y, x + cardWidth, y + 2, borderColor);
            // Bottom border
            fill(matrixStack, x, y + cardHeight - 2, x + cardWidth, y + cardHeight, borderColor);
            // Left border
            fill(matrixStack, x, y, x + 2, y + cardHeight, borderColor);
            // Right border
            fill(matrixStack, x + cardWidth - 2, y, x + cardWidth, y + cardHeight, borderColor);
        } else {
            // Draw elegant card back
            fillGradient(matrixStack, x, y, x + cardWidth, y + cardHeight, 0xFF1E3A8A, 0xFF312E81);
            // Inner pattern
            fill(matrixStack, x + 10, y + 10, x + cardWidth - 10, y + cardHeight - 10, 0xFF1E1B4B);
            // Pokeball silhouette
            int centerCardX = x + cardWidth / 2;
            int centerCardY = y + cardHeight / 2;
            fill(matrixStack, centerCardX - 30, centerCardY - 2, centerCardX + 30, centerCardY + 2, 0xFF4C1D95);
            drawCenteredString(matrixStack, this.font, "POKEMON", 
                centerCardX, centerCardY - 20, 0xFFFFD700);
            drawCenteredString(matrixStack, this.font, "TRADING CARD GAME", 
                centerCardX, centerCardY + 20, 0xFFA78BFA);
        }
        
        matrixStack.popPose();
        
        // Draw navigation arrows (only when applicable)
        drawNavigationArrows(matrixStack);
        
        // Draw progress bar at bottom
        drawProgressBar(matrixStack);
        
        // Draw card counter
        String progress = String.format("Card %d of %d", currentCardIndex + 1, cards.size());
        drawCenteredString(matrixStack, this.font, progress, this.width / 2, y + cardHeight + 40, 0xFFFFFFFF);
        
        // Draw instructions
        String instruction;
        if (currentCardIndex == 0 && !revealed[0]) {
            instruction = "Press SPACE to reveal";
        } else if (currentCardIndex < cards.size() - 1) {
            instruction = "Use arrow keys to navigate";
        } else {
            if (isRareCard(currentCard)) {
                instruction = "★ AMAZING PULL! ★ Press ESC to close";
            } else {
                instruction = "Press ESC to close";
            }
        }
        drawCenteredString(matrixStack, this.font, instruction, 
            this.width / 2, y + cardHeight + 60, 0xFFFFD700);
        
        // Draw card stack visualization on left
        drawCardStack(matrixStack);
        
        // Play celebration sound for rare last card (client-side only)
        if (currentCardIndex == cards.size() - 1 && !celebrationPlayed && isRareCard(currentCard)) {
            if (this.minecraft.player != null) {
                this.minecraft.player.playSound(SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, 1.0F, 1.0F);
                celebrationPlayed = true;
            }
        }
        
        super.render(matrixStack, mouseX, mouseY, partialTicks);
    }
    
    private void drawNavigationArrows(MatrixStack matrixStack) {
        int centerY = this.height / 2;
        
        // Left arrow (if not on first card)
        if (currentCardIndex > 0) {
            int leftX = 50;
            // Draw arrow shape
            for (int i = 0; i < 20; i++) {
                int width = i;
                fill(matrixStack, leftX + i, centerY - width/2, leftX + i + 2, centerY + width/2 + 1, 0xFFFFD700);
            }
            drawString(matrixStack, this.font, "PREV", leftX - 5, centerY + 25, 0xFFFFD700);
        }
        
        // Right arrow (if not on last card)
        if (currentCardIndex < cards.size() - 1) {
            int rightX = this.width - 70;
            // Draw arrow shape
            for (int i = 0; i < 20; i++) {
                int width = 20 - i;
                fill(matrixStack, rightX + i, centerY - width/2, rightX + i + 2, centerY + width/2 + 1, 0xFFFFD700);
            }
            drawString(matrixStack, this.font, "NEXT", rightX - 5, centerY + 25, 0xFFFFD700);
        }
    }
    
    private void drawProgressBar(MatrixStack matrixStack) {
        int barWidth = 200;
        int barHeight = 6;
        int barX = (this.width - barWidth) / 2;
        int barY = this.height - 40;
        
        // Background
        fill(matrixStack, barX, barY, barX + barWidth, barY + barHeight, 0xFF333333);
        
        // Progress
        int progress = (int)((float)(currentCardIndex + 1) / cards.size() * barWidth);
        fill(matrixStack, barX, barY, barX + progress, barY + barHeight, 0xFFFFD700);
        
        // Border
        fill(matrixStack, barX - 1, barY - 1, barX + barWidth + 1, barY, 0xFF666666);
        fill(matrixStack, barX - 1, barY + barHeight, barX + barWidth + 1, barY + barHeight + 1, 0xFF666666);
        fill(matrixStack, barX - 1, barY, barX, barY + barHeight, 0xFF666666);
        fill(matrixStack, barX + barWidth, barY, barX + barWidth + 1, barY + barHeight, 0xFF666666);
    }
    
    private void drawCardStack(MatrixStack matrixStack) {
        int stackX = 20;
        int stackY = this.height / 2 - 60;
        
        // Title
        drawString(matrixStack, this.font, "PACK", stackX, stackY - 15, 0xFFFFD700);
        
        for (int i = 0; i < cards.size(); i++) {
            int offsetY = i * 5;
            int color;
            
            if (i == currentCardIndex) {
                // Current card - animated glow
                color = 0xFFFFD700;
                // Glow effect
                int glowSize = (int)(Math.sin(System.currentTimeMillis() / 200.0) * 2 + 3);
                fill(matrixStack, stackX - glowSize, stackY + offsetY - glowSize, 
                     stackX + 35 + glowSize, stackY + offsetY + 45 + glowSize, 0x40FFD700);
            } else if (revealed[i]) {
                // Revealed cards
                color = 0xFF606080;
            } else {
                // Unrevealed cards
                color = 0xFF303040;
            }
            
            // Card rectangle
            fill(matrixStack, stackX, stackY + offsetY, stackX + 35, stackY + offsetY + 45, color);
            
            // Rarity indicator for revealed cards
            if (revealed[i] && i < cards.size()) {
                int rarityColor = getRarityColor(cards.get(i).getRarity());
                fill(matrixStack, stackX + 30, stackY + offsetY, stackX + 35, stackY + offsetY + 45, rarityColor);
            }
        }
    }
    
    private boolean isRareCard(Card card) {
        CardRarity rarity = card.getRarity();
        // Only cards rarer than RARE (not including RARE itself)
        return rarity == CardRarity.DOUBLE_RARE || 
               rarity == CardRarity.ULTRA_RARE || 
               rarity == CardRarity.ILLUSTRATION_RARE || 
               rarity == CardRarity.SPECIAL_ILLUSTRATION_RARE ||
               rarity == CardRarity.BLACK_WHITE_RARE;
    }
    
    private int getRarityColor(com.example.etbmod.cards.CardRarity rarity) {
        switch (rarity) {
            case COMMON: return 0xFF808080;
            case UNCOMMON: return 0xFF40FF40;
            case RARE: return 0xFFFFD700;
            case DOUBLE_RARE: return 0xFFFF69B4;
            case ULTRA_RARE: return 0xFFFF00FF;
            case ILLUSTRATION_RARE: return 0xFF00FFFF;
            case SPECIAL_ILLUSTRATION_RARE: return 0xFFFF0080;
            case BLACK_WHITE_RARE: return 0xFFFFFFFF;
            default: return 0xFFFFFFFF;
        }
    }
    
    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        long currentTime = System.currentTimeMillis();
        if (currentTime - lastKeyPress < 200) {
            return true; // Debounce
        }
        lastKeyPress = currentTime;
        
        if (keyCode == GLFW.GLFW_KEY_RIGHT) {
            // Move to next card
            if (currentCardIndex < cards.size() - 1) {
                currentCardIndex++;
                revealed[currentCardIndex] = true;
                targetScale = 0.9f;
                cardScale = 1.1f; // Start slightly larger for animation
                // Play card flip sound
                if (this.minecraft.player != null) {
                    this.minecraft.player.playSound(SoundEvents.UI_BUTTON_CLICK, 0.5F, 1.0F);
                }
                return true;
            }
        } else if (keyCode == GLFW.GLFW_KEY_LEFT) {
            // Move to previous card
            if (currentCardIndex > 0) {
                currentCardIndex--;
                targetScale = 1.0f;
                cardScale = 0.9f;
                // Play card flip sound
                if (this.minecraft.player != null) {
                    this.minecraft.player.playSound(SoundEvents.UI_BUTTON_CLICK, 0.5F, 0.8F);
                }
                return true;
            }
        } else if (keyCode == GLFW.GLFW_KEY_SPACE) {
            // Reveal current card
            if (!revealed[currentCardIndex]) {
                revealed[currentCardIndex] = true;
                targetScale = 1.1f;
                cardScale = 0.9f;
                if (this.minecraft.player != null) {
                    this.minecraft.player.playSound(SoundEvents.UI_BUTTON_CLICK, 0.5F, 1.2F);
                }
                return true;
            }
        }
        
        return super.keyPressed(keyCode, scanCode, modifiers);
    }
    
    @Override
    public boolean isPauseScreen() {
        return false;
    }
}