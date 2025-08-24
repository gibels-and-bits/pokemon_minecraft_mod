package com.example.etbmod.client.screen;

import com.example.etbmod.ETBMod;
import com.example.etbmod.cards.Card;
import com.example.etbmod.client.texture.CardTextureManager;
import com.example.etbmod.container.BinderContainer;
import com.example.etbmod.items.CardItem;
import com.example.etbmod.network.BinderPageChangePacket;
import com.example.etbmod.network.ModNetworking;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.screen.inventory.ContainerScreen;
import net.minecraft.inventory.container.Slot;
import net.minecraft.client.gui.widget.button.Button;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;

public class BinderScreen extends ContainerScreen<BinderContainer> {
    private static final ResourceLocation TEXTURE = new ResourceLocation(ETBMod.MOD_ID, "textures/gui/binder_background.png");
    private Button prevPageButton;
    private Button nextPageButton;
    private Button[] pageButtons = new Button[5];
    
    // Card display configuration
    private static final int CARD_SIZE = 80; // Size of each card display
    private static final int CARD_SPACING = 10; // Spacing between cards
    private static final int GRID_START_X = 8; // Start position for card grid
    private static final int GRID_START_Y = 20; // Start position for card grid
    
    public BinderScreen(BinderContainer container, PlayerInventory playerInventory, ITextComponent title) {
        super(container, playerInventory, title);
        // Larger GUI to accommodate bigger card displays
        this.imageWidth = 286; // Wider to fit 3 cards with spacing
        this.imageHeight = 330; // Taller to fit 3 rows of cards plus inventory
        this.inventoryLabelY = this.imageHeight - 94;
    }
    
    @Override
    protected void init() {
        super.init();
        
        // Previous page button - positioned on left side
        this.prevPageButton = this.addButton(new Button(
            this.leftPos - 22, 
            this.topPos + 140, 
            20, 
            20, 
            new StringTextComponent("<"),
            button -> {
                ModNetworking.CHANNEL.sendToServer(new BinderPageChangePacket(-1));
                this.menu.changePage(-1);
            }
        ));
        
        // Next page button - positioned on right side
        this.nextPageButton = this.addButton(new Button(
            this.leftPos + this.imageWidth + 2, 
            this.topPos + 140, 
            20, 
            20, 
            new StringTextComponent(">"),
            button -> {
                ModNetworking.CHANNEL.sendToServer(new BinderPageChangePacket(1));
                this.menu.changePage(1);
            }
        ));
        
        // Page number buttons at the bottom
        int buttonStartX = this.leftPos + (this.imageWidth - (5 * 30)) / 2;
        for (int i = 0; i < 5; i++) {
            final int pageNum = i;
            this.pageButtons[i] = this.addButton(new Button(
                buttonStartX + (i * 32), 
                this.topPos + this.imageHeight - 110, 
                28, 
                16, 
                new StringTextComponent(String.valueOf(i + 1)),
                button -> {
                    ModNetworking.CHANNEL.sendToServer(new BinderPageChangePacket(pageNum - this.menu.getCurrentPage()));
                    this.menu.setPage(pageNum);
                }
            ));
        }
    }
    
    @Override
    public void render(MatrixStack matrixStack, int mouseX, int mouseY, float partialTicks) {
        this.renderBackground(matrixStack);
        
        // Render the background first
        RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
        
        // Draw custom background
        fill(matrixStack, this.leftPos, this.topPos, this.leftPos + this.imageWidth, this.topPos + this.imageHeight, 0xFF2C2C2C);
        fill(matrixStack, this.leftPos + 2, this.topPos + 2, this.leftPos + this.imageWidth - 2, this.topPos + this.imageHeight - 2, 0xFF3C3C3C);
        
        // Draw card slots background (3x3 grid)
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                int x = this.leftPos + GRID_START_X + col * (CARD_SIZE + CARD_SPACING);
                int y = this.topPos + GRID_START_Y + row * (CARD_SIZE + CARD_SPACING);
                
                // Draw slot background
                fill(matrixStack, x - 2, y - 2, x + CARD_SIZE + 2, y + CARD_SIZE + 2, 0xFF1A1A1A);
                fill(matrixStack, x, y, x + CARD_SIZE, y + CARD_SIZE, 0xFF000000);
            }
        }
        
        // Render cards in the grid
        renderCards(matrixStack);
        
        // Draw inventory background area
        int invY = this.topPos + 270;
        fill(matrixStack, this.leftPos + 2, invY - 5, this.leftPos + this.imageWidth - 2, this.topPos + this.imageHeight - 2, 0xFF1A1A1A);
        
        // Call super to handle slot interaction and dragging
        // But we'll override the visual rendering
        this.minecraft.getTextureManager().bind(INVENTORY_LOCATION);
        super.render(matrixStack, mouseX, mouseY, partialTicks);
        
        // Update button states
        this.prevPageButton.active = this.menu.getCurrentPage() > 0;
        this.nextPageButton.active = this.menu.getCurrentPage() < this.menu.getTotalPages() - 1;
        
        // Highlight current page button
        for (int i = 0; i < 5; i++) {
            if (i < this.menu.getTotalPages()) {
                this.pageButtons[i].visible = true;
                this.pageButtons[i].active = (i != this.menu.getCurrentPage());
            } else {
                this.pageButtons[i].visible = false;
            }
        }
        
    }
    
    private void renderCards(MatrixStack matrixStack) {
        // Render the actual card images in the 3x3 grid
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                int slotIndex = row * 3 + col;
                ItemStack stack = this.menu.slots.get(slotIndex).getItem();
                
                if (!stack.isEmpty() && stack.getItem() instanceof CardItem) {
                    Card card = CardItem.getCardFromStack(stack);
                    if (card != null) {
                        int x = this.leftPos + GRID_START_X + col * (CARD_SIZE + CARD_SPACING);
                        int y = this.topPos + GRID_START_Y + row * (CARD_SIZE + CARD_SPACING);
                        
                        // Load and render card texture
                        ResourceLocation cardTexture = CardTextureManager.getOrLoadCardTexture(card.getImagePath());
                        if (cardTexture != null) {
                            RenderSystem.pushMatrix();
                            RenderSystem.enableBlend();
                            RenderSystem.defaultBlendFunc();
                            RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
                            
                            this.minecraft.getTextureManager().bind(cardTexture);
                            
                            // Draw the card texture scaled to fit the slot
                            blit(matrixStack, 
                                x, y,                      // Screen position
                                CARD_SIZE, CARD_SIZE,      // Screen size
                                0.0f, 0.0f,               // UV start
                                256, 256,                 // UV size (full texture)
                                256, 256);                // Texture size
                            
                            RenderSystem.disableBlend();
                            RenderSystem.popMatrix();
                        } else {
                            // Draw placeholder for missing texture
                            fill(matrixStack, x, y, x + CARD_SIZE, y + CARD_SIZE, 0xFF444444);
                            drawCenteredString(matrixStack, this.font, "?", x + CARD_SIZE/2, y + CARD_SIZE/2 - 4, 0xFFFFFF);
                        }
                        
                        // Draw card name below the image
                        String cardName = card.getName();
                        if (cardName.length() > 12) {
                            cardName = cardName.substring(0, 11) + "...";
                        }
                        drawCenteredString(matrixStack, this.font, cardName, 
                            x + CARD_SIZE/2, y + CARD_SIZE + 2, 0xFFFFFF);
                    }
                }
            }
        }
    }
    
    @Override
    protected void renderBg(MatrixStack matrixStack, float partialTicks, int mouseX, int mouseY) {
        // Background rendering is handled in render() method
    }
    
    @Override
    protected void renderLabels(MatrixStack matrixStack, int mouseX, int mouseY) {
        // Draw title
        drawCenteredString(matrixStack, this.font, "Card Binder", this.imageWidth / 2, 6, 0xFFFFFF);
        
        // Draw page info
        String pageInfo = String.format("Page %d of %d", 
            this.menu.getCurrentPage() + 1, 
            this.menu.getTotalPages());
        drawCenteredString(matrixStack, this.font, pageInfo, this.imageWidth / 2, this.imageHeight - 120, 0xAAAAAA);
        
        // Draw card count
        String cardCount = String.format("Total: %d cards", this.menu.getTotalCards());
        drawCenteredString(matrixStack, this.font, cardCount, this.imageWidth / 2, this.imageHeight - 108, 0xAAAAAA);
        
        // Draw inventory label
        this.font.draw(matrixStack, "Inventory", 8, this.imageHeight - 93, 0xAAAAAA);
    }
    
    @Override
    protected boolean isHovering(int x, int y, int width, int height, double mouseX, double mouseY) {
        // Override to handle custom slot positions
        return mouseX >= x && mouseY >= y && mouseX < x + width && mouseY < y + height;
    }
    
}