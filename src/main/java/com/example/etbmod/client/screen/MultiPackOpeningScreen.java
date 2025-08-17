package com.example.etbmod.client.screen;

import com.example.etbmod.ETBMod;
import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.client.texture.CardTextureManager;
import com.example.etbmod.network.ModNetworking;
import com.example.etbmod.network.OpenPackPacket;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.text.StringTextComponent;
import org.lwjgl.glfw.GLFW;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MultiPackOpeningScreen extends Screen {
    private int totalPacks;
    private int currentPackIndex = 0;
    private int remainingPacks;
    private List<Card> currentCards;
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
    
    // Pack opening state
    private boolean waitingForPack = false;
    private boolean isDragging = false;
    private int dragStartX, dragStartY;
    
    // UI positions
    private static final int PACK_STACK_X = 50;
    private static final int PACK_STACK_Y = 100;
    private static final int OPEN_ZONE_X = 300;
    private static final int OPEN_ZONE_Y = 100;
    private static final int OPEN_ZONE_SIZE = 60;
    
    private String setName;
    
    public MultiPackOpeningScreen(int totalPacks, String setName) {
        super(new StringTextComponent("Opening Booster Packs"));
        this.totalPacks = totalPacks;
        this.remainingPacks = totalPacks - 1; // One pack will be opened immediately
        this.setName = setName;
        this.currentCards = new ArrayList<>();
        this.waitingForPack = false; // We'll receive cards immediately
    }
    
    public void setCurrentPackCards(List<Card> cards) {
        this.currentCards = cards;
        this.currentCardIndex = 0;
        this.revealed = new boolean[cards.size()];
        this.revealed[0] = true;
        this.celebrationPlayed = false;
        this.waitingForPack = false;
        
        // Send debug message
        if (minecraft != null && minecraft.player != null) {
            minecraft.player.displayClientMessage(
                new StringTextComponent("§a[ETB] Received " + cards.size() + " cards from server"), false);
        }
        
        // Preload textures
        for (int i = 0; i < cards.size(); i++) {
            Card card = cards.get(i);
            minecraft.player.displayClientMessage(
                new StringTextComponent("§e[ETB] Loading card " + (i+1) + ": " + card.getName() + " - " + card.getImagePath()), false);
            loadCardTexture(card);
        }
        
        minecraft.player.displayClientMessage(
            new StringTextComponent("§a[ETB] All textures loaded, screen ready"), false);
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
        // Dark gradient background
        fillGradient(matrixStack, 0, 0, this.width, this.height, 0xFF0F0F1F, 0xFF1A1A3A);
        
        // Draw UI title
        drawCenteredString(matrixStack, this.font, 
            String.format("Opening %s Packs - Pack %d of %d", setName, currentPackIndex + 1, totalPacks),
            this.width / 2, 20, 0xFFFFD700);
        
        if (waitingForPack) {
            if (minecraft != null && minecraft.player != null) {
                minecraft.player.displayClientMessage(
                    new StringTextComponent("§e[ETB] Screen state: WAITING FOR PACK"), true);
            }
            // Draw pack stack
            drawPackStack(matrixStack);
            
            // Draw open zone
            drawOpenZone(matrixStack);
            
            // Draw instructions
            drawCenteredString(matrixStack, this.font, 
                "Drag a pack to the opening zone", 
                this.width / 2, this.height - 40, 0xFFFFFFFF);
            
            // Handle dragging
            if (isDragging) {
                drawDraggedPack(matrixStack, mouseX, mouseY);
            }
        } else if (!currentCards.isEmpty()) {
            // Draw current card (similar to CardRevealScreen)
            if (minecraft != null && minecraft.player != null) {
                minecraft.player.displayClientMessage(
                    new StringTextComponent("§b[ETB] Rendering card " + (currentCardIndex+1) + "/" + currentCards.size()), true);
            }
            renderCurrentCard(matrixStack);
            
            // Draw navigation
            drawCardNavigation(matrixStack);
            
            // Draw progress
            drawCardProgress(matrixStack);
        } else {
            // No cards and not waiting - this shouldn't happen
            if (minecraft != null && minecraft.player != null) {
                minecraft.player.displayClientMessage(
                    new StringTextComponent("§c[ETB] ERROR: No cards loaded yet! Cards=" + currentCards.size() + " waiting=" + waitingForPack), true);
            }
            drawCenteredString(matrixStack, this.font, 
                "Loading cards...", 
                this.width / 2, this.height / 2, 0xFFFFFF00);
        }
        
        super.render(matrixStack, mouseX, mouseY, partialTicks);
    }
    
    private void drawPackStack(MatrixStack matrixStack) {
        // Draw remaining pack stack
        for (int i = 0; i < Math.min(remainingPacks, 5); i++) {
            int x = PACK_STACK_X + i * 2;
            int y = PACK_STACK_Y + i * 2;
            
            // Pack background
            fill(matrixStack, x, y, x + 50, y + 70, 0xFF4A4A6A);
            // Pack border
            fill(matrixStack, x, y, x + 50, y + 2, 0xFF8080FF);
            fill(matrixStack, x, y + 68, x + 50, y + 70, 0xFF8080FF);
            fill(matrixStack, x, y, x + 2, y + 70, 0xFF8080FF);
            fill(matrixStack, x + 48, y, x + 50, y + 70, 0xFF8080FF);
            
            // Pack label
            drawCenteredString(matrixStack, this.font, "PACK", x + 25, y + 30, 0xFFFFFFFF);
        }
        
        // Draw count
        drawString(matrixStack, this.font, 
            remainingPacks + " packs", 
            PACK_STACK_X, PACK_STACK_Y + 80, 0xFFFFFFFF);
    }
    
    private void drawOpenZone(MatrixStack matrixStack) {
        // Draw the zone where packs should be dragged
        int color = isDraggingOverZone(minecraft.mouseHandler.xpos(), minecraft.mouseHandler.ypos()) 
            ? 0xFF00FF00 : 0xFF808080;
        
        // Dashed border effect
        for (int i = 0; i < OPEN_ZONE_SIZE; i += 4) {
            // Top
            fill(matrixStack, OPEN_ZONE_X + i, OPEN_ZONE_Y, 
                 OPEN_ZONE_X + i + 2, OPEN_ZONE_Y + 2, color);
            // Bottom
            fill(matrixStack, OPEN_ZONE_X + i, OPEN_ZONE_Y + OPEN_ZONE_SIZE - 2, 
                 OPEN_ZONE_X + i + 2, OPEN_ZONE_Y + OPEN_ZONE_SIZE, color);
            // Left
            fill(matrixStack, OPEN_ZONE_X, OPEN_ZONE_Y + i, 
                 OPEN_ZONE_X + 2, OPEN_ZONE_Y + i + 2, color);
            // Right
            fill(matrixStack, OPEN_ZONE_X + OPEN_ZONE_SIZE - 2, OPEN_ZONE_Y + i, 
                 OPEN_ZONE_X + OPEN_ZONE_SIZE, OPEN_ZONE_Y + i + 2, color);
        }
        
        // Label
        drawCenteredString(matrixStack, this.font, "DROP", 
            OPEN_ZONE_X + OPEN_ZONE_SIZE/2, OPEN_ZONE_Y + OPEN_ZONE_SIZE/2 - 10, color);
        drawCenteredString(matrixStack, this.font, "HERE", 
            OPEN_ZONE_X + OPEN_ZONE_SIZE/2, OPEN_ZONE_Y + OPEN_ZONE_SIZE/2 + 2, color);
    }
    
    private void drawDraggedPack(MatrixStack matrixStack, int mouseX, int mouseY) {
        // Draw pack following mouse
        int x = mouseX - 25;
        int y = mouseY - 35;
        
        fill(matrixStack, x, y, x + 50, y + 70, 0xFF6A6A8A);
        fill(matrixStack, x, y, x + 50, y + 2, 0xFFAAAAFF);
        fill(matrixStack, x, y + 68, x + 50, y + 70, 0xFFAAAAFF);
        fill(matrixStack, x, y, x + 2, y + 70, 0xFFAAAAFF);
        fill(matrixStack, x + 48, y, x + 50, y + 70, 0xFFAAAAFF);
        
        drawCenteredString(matrixStack, this.font, "PACK", x + 25, y + 30, 0xFFFFFFFF);
    }
    
    private void renderCurrentCard(MatrixStack matrixStack) {
        if (currentCardIndex >= currentCards.size()) {
            if (minecraft != null && minecraft.player != null) {
                minecraft.player.displayClientMessage(
                    new StringTextComponent("§c[ETB] No card to render (index out of bounds)"), true);
            }
            return;
        }
        
        Card currentCard = currentCards.get(currentCardIndex);
        
        // Update animations
        if (cardScale < targetScale) {
            cardScale = Math.min(cardScale + 0.05f, targetScale);
        } else if (cardScale > targetScale) {
            cardScale = Math.max(cardScale - 0.05f, targetScale);
        }
        
        // Card dimensions - match actual card texture size (128x256)
        // Scale up slightly for better visibility
        int cardWidth = 192;  // 128 * 1.5
        int cardHeight = 384; // 256 * 1.5
        int x = (this.width - cardWidth) / 2;
        int y = (this.height - cardHeight) / 2 - 20;
        
        matrixStack.pushPose();
        
        // Apply scale
        float centerX = x + cardWidth / 2.0f;
        float centerY = y + cardHeight / 2.0f;
        matrixStack.translate(centerX, centerY, 0);
        matrixStack.scale(cardScale, cardScale, 1.0f);
        matrixStack.translate(-centerX, -centerY, 0);
        
        // Draw card shadow
        fill(matrixStack, x + 4, y + 4, x + cardWidth + 4, y + cardHeight + 4, 0x80000000);
        
        if (revealed[currentCardIndex]) {
            // Draw card image
            ResourceLocation texture = cardTextures.get(currentCard.getImagePath());
            if (texture != null) {
                minecraft.player.displayClientMessage(
                    new StringTextComponent("§a[ETB] Found texture for: " + currentCard.getName()), true);
                RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
                this.minecraft.getTextureManager().bind(texture);
                // The card image is centered in a 256x256 texture
                // Cards are 128x256, centered at (64, 0) in the texture
                int textureX = 64;  // Offset in texture where card starts (256-128)/2
                int textureY = 0;   // No vertical offset
                // Draw the entire 128x256 card from the 256x256 texture
                blit(matrixStack, x, y, textureX, textureY, 128, 256, 256, 256);
            } else {
                minecraft.player.displayClientMessage(
                    new StringTextComponent("§c[ETB] No texture for: " + currentCard.getName() + " path: " + currentCard.getImagePath()), true);
                // Placeholder
                fill(matrixStack, x, y, x + cardWidth, y + cardHeight, 0xFF2A2A3E);
                drawCenteredString(matrixStack, this.font, currentCard.getName(), 
                    x + cardWidth / 2, y + cardHeight / 2, 0xFFFFFF);
            }
        } else {
            // Card back
            fillGradient(matrixStack, x, y, x + cardWidth, y + cardHeight, 0xFF1E3A8A, 0xFF312E81);
            drawCenteredString(matrixStack, this.font, "POKEMON", 
                x + cardWidth / 2, y + cardHeight / 2 - 10, 0xFFFFD700);
        }
        
        matrixStack.popPose();
        
        // Check for rare last card celebration
        if (currentCardIndex == currentCards.size() - 1 && !celebrationPlayed && isRareCard(currentCard)) {
            if (this.minecraft.player != null) {
                this.minecraft.player.playSound(SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, 1.0F, 1.0F);
                celebrationPlayed = true;
            }
        }
    }
    
    private void drawCardNavigation(MatrixStack matrixStack) {
        // Show left/right arrows
        if (currentCardIndex > 0) {
            drawString(matrixStack, this.font, "< PREV", 50, this.height / 2, 0xFFFFD700);
        }
        
        if (currentCardIndex < currentCards.size() - 1) {
            drawString(matrixStack, this.font, "NEXT >", this.width - 80, this.height / 2, 0xFFFFD700);
        } else if (remainingPacks > 0) {
            // Show option to open next pack
            drawCenteredString(matrixStack, this.font, 
                "Press SPACE to open next pack", 
                this.width / 2, this.height - 60, 0xFF00FF00);
        }
    }
    
    private void drawCardProgress(MatrixStack matrixStack) {
        String progress = String.format("Card %d of %d", currentCardIndex + 1, currentCards.size());
        drawCenteredString(matrixStack, this.font, progress, this.width / 2, this.height - 80, 0xFFFFFFFF);
    }
    
    private boolean isDraggingOverZone(double mouseX, double mouseY) {
        double scaledX = mouseX * this.width / minecraft.getWindow().getScreenWidth();
        double scaledY = mouseY * this.height / minecraft.getWindow().getScreenHeight();
        
        return scaledX >= OPEN_ZONE_X && scaledX <= OPEN_ZONE_X + OPEN_ZONE_SIZE &&
               scaledY >= OPEN_ZONE_Y && scaledY <= OPEN_ZONE_Y + OPEN_ZONE_SIZE;
    }
    
    private boolean isOverPackStack(double mouseX, double mouseY) {
        return mouseX >= PACK_STACK_X && mouseX <= PACK_STACK_X + 50 &&
               mouseY >= PACK_STACK_Y && mouseY <= PACK_STACK_Y + 70;
    }
    
    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (waitingForPack && button == 0 && remainingPacks > 0) {
            if (isOverPackStack(mouseX, mouseY)) {
                isDragging = true;
                dragStartX = (int)mouseX;
                dragStartY = (int)mouseY;
                return true;
            }
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }
    
    @Override
    public boolean mouseReleased(double mouseX, double mouseY, int button) {
        if (isDragging && button == 0) {
            isDragging = false;
            
            // Check if dropped in zone
            if (isDraggingOverZone(minecraft.mouseHandler.xpos(), minecraft.mouseHandler.ypos())) {
                // Send debug message to chat
                if (this.minecraft.player != null) {
                    this.minecraft.player.displayClientMessage(
                        new StringTextComponent("§e[ETB] Requesting pack opening..."), false);
                }
                
                // Request pack opening from server - use OpenPackPacket directly
                remainingPacks--;
                currentPackIndex++;
                ModNetworking.sendToServer(new OpenPackPacket(false));
                
                // Play sound
                if (this.minecraft.player != null) {
                    this.minecraft.player.playSound(SoundEvents.UI_BUTTON_CLICK, 0.5F, 1.0F);
                }
            } else {
                if (this.minecraft.player != null) {
                    this.minecraft.player.displayClientMessage(
                        new StringTextComponent("§c[ETB] Pack not dropped in zone"), false);
                }
            }
            return true;
        }
        return super.mouseReleased(mouseX, mouseY, button);
    }
    
    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (waitingForPack) {
            return super.keyPressed(keyCode, scanCode, modifiers);
        }
        
        long currentTime = System.currentTimeMillis();
        if (currentTime - lastKeyPress < 200) {
            return true;
        }
        lastKeyPress = currentTime;
        
        if (keyCode == GLFW.GLFW_KEY_RIGHT) {
            if (currentCardIndex < currentCards.size() - 1) {
                currentCardIndex++;
                revealed[currentCardIndex] = true;
                targetScale = 0.9f;
                cardScale = 1.1f;
                if (this.minecraft.player != null) {
                    this.minecraft.player.playSound(SoundEvents.UI_BUTTON_CLICK, 0.5F, 1.0F);
                }
                return true;
            }
        } else if (keyCode == GLFW.GLFW_KEY_LEFT) {
            if (currentCardIndex > 0) {
                currentCardIndex--;
                targetScale = 1.0f;
                cardScale = 0.9f;
                if (this.minecraft.player != null) {
                    this.minecraft.player.playSound(SoundEvents.UI_BUTTON_CLICK, 0.5F, 0.8F);
                }
                return true;
            }
        } else if (keyCode == GLFW.GLFW_KEY_SPACE) {
            if (currentCardIndex == currentCards.size() - 1 && remainingPacks > 0) {
                // Move to next pack
                waitingForPack = true;
                currentCards.clear();
                return true;
            }
        }
        
        return super.keyPressed(keyCode, scanCode, modifiers);
    }
    
    private boolean isRareCard(Card card) {
        CardRarity rarity = card.getRarity();
        return rarity == CardRarity.DOUBLE_RARE || 
               rarity == CardRarity.ULTRA_RARE || 
               rarity == CardRarity.ILLUSTRATION_RARE || 
               rarity == CardRarity.SPECIAL_ILLUSTRATION_RARE ||
               rarity == CardRarity.BLACK_WHITE_RARE;
    }
    
    @Override
    public boolean isPauseScreen() {
        return false;
    }
}