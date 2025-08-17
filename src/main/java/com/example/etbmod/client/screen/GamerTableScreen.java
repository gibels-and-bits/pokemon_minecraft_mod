package com.example.etbmod.client.screen;

import com.example.etbmod.ETBMod;
import com.example.etbmod.container.GamerTableContainer;
import com.example.etbmod.network.ModNetworking;
import com.example.etbmod.network.OpenPackPacket;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.screen.inventory.ContainerScreen;
import net.minecraft.client.gui.widget.button.Button;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;

public class GamerTableScreen extends ContainerScreen<GamerTableContainer> {
    
    private static final ResourceLocation TEXTURE = new ResourceLocation(ETBMod.MOD_ID, 
            "textures/gui/gamer_table_v2.png");
    private Button openButton;
    
    public GamerTableScreen(GamerTableContainer container, PlayerInventory playerInventory, ITextComponent title) {
        super(container, playerInventory, title);
        // Standard chest-like size for simplicity
        this.imageWidth = 176;
        this.imageHeight = 166;
    }
    
    @Override
    protected void init() {
        super.init();
        
        // Position the Open button below the pack slot
        int buttonX = this.leftPos + 65;
        int buttonY = this.topPos + 45;
        this.openButton = this.addButton(new Button(buttonX, buttonY, 46, 20, 
            new StringTextComponent("OPEN"), 
            (button) -> {
                if (this.menu.canOpenPack()) {
                    // Send debug message
                    if (this.minecraft.player != null) {
                        this.minecraft.player.displayClientMessage(
                            new net.minecraft.util.text.StringTextComponent("§6[ETB] Sending open pack request..."), false);
                    }
                    // Send packet to server to open pack
                    ModNetworking.sendToServer(new OpenPackPacket());
                }
            }));
    }
    
    @Override
    public void tick() {
        super.tick();
        // Enable/disable button based on whether there's a pack
        if (this.openButton != null) {
            this.openButton.active = this.menu.canOpenPack();
        }
    }
    
    @Override
    public void render(MatrixStack matrixStack, int mouseX, int mouseY, float partialTicks) {
        this.renderBackground(matrixStack);
        super.render(matrixStack, mouseX, mouseY, partialTicks);
        this.renderTooltip(matrixStack, mouseX, mouseY);
    }
    
    @Override
    protected void renderBg(MatrixStack matrixStack, float partialTicks, int mouseX, int mouseY) {
        RenderSystem.color4f(1.0F, 1.0F, 1.0F, 1.0F);
        this.minecraft.getTextureManager().bind(TEXTURE);
        int x = (this.width - this.imageWidth) / 2;
        int y = (this.height - this.imageHeight) / 2;
        this.blit(matrixStack, x, y, 0, 0, this.imageWidth, this.imageHeight);
    }
    
    @Override
    protected void renderLabels(MatrixStack matrixStack, int mouseX, int mouseY) {
        // Title at top
        this.font.draw(matrixStack, this.title, 8.0F, 6.0F, 0x404040);
        
        // Inventory label at bottom
        this.font.draw(matrixStack, this.inventory.getDisplayName(), 8.0F, 
                (float)(this.imageHeight - 96 + 2), 0x404040);
    }
}