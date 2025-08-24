package com.example.etbmod.gui;

import com.example.etbmod.ETBMod;
import com.example.etbmod.container.VendingMachineContainer;
import com.example.etbmod.network.ModNetworking;
import com.example.etbmod.network.VendingMachinePurchasePacket;
import com.example.etbmod.tileentity.VendingMachineTileEntity;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.screen.inventory.ContainerScreen;
import net.minecraft.client.gui.widget.button.Button;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.util.text.TranslationTextComponent;

import java.util.ArrayList;
import java.util.List;

public class VendingMachineScreen extends ContainerScreen<VendingMachineContainer> {
    
    private static final ResourceLocation TEXTURE = new ResourceLocation(ETBMod.MOD_ID, 
            "textures/gui/vending_machine.png");
    
    private final VendingMachineTileEntity tileEntity;
    private List<Button> packButtons = new ArrayList<>();
    private List<Button> etbButtons = new ArrayList<>();
    private Button categoryBoosterButton;
    private Button categoryETBButton;
    private boolean showingBoosters = true;
    
    public VendingMachineScreen(VendingMachineContainer container, PlayerInventory playerInventory, 
                                ITextComponent title) {
        super(container, playerInventory, title);
        this.tileEntity = container.getTileEntity();
        this.imageWidth = 176;
        this.imageHeight = 166;
        this.inventoryLabelY = this.imageHeight - 94; // Adjust inventory label position
    }
    
    @Override
    protected void init() {
        super.init();
        
        // Category buttons
        categoryBoosterButton = this.addButton(new Button(
                this.leftPos + 7, this.topPos + 7, 50, 20,
                new TranslationTextComponent("gui.etbmod.boosters"),
                button -> switchToBoosterView()
        ));
        
        categoryETBButton = this.addButton(new Button(
                this.leftPos + 60, this.topPos + 7, 50, 20,
                new TranslationTextComponent("gui.etbmod.etbs"),
                button -> switchToETBView()
        ));
        
        // Initialize with booster view
        switchToBoosterView();
    }
    
    private void switchToBoosterView() {
        showingBoosters = true;
        clearProductButtons();
        
        // Create booster pack buttons
        List<String> packTypes = tileEntity.getAvailablePackTypes();
        int buttonY = this.topPos + 30;
        int buttonIndex = 0;
        
        for (String packType : packTypes) {
            if (buttonIndex >= 4) break; // Max 4 buttons shown
            
            Button packButton = this.addButton(new Button(
                    this.leftPos + 7, buttonY,
                    100, 20,
                    new StringTextComponent(formatPackName(packType) + " (1◆)"),
                    button -> purchaseBoosterPack(packType)
            ));
            packButtons.add(packButton);
            buttonY += 22;
            buttonIndex++;
        }
        
        updateButtonStates();
    }
    
    private void switchToETBView() {
        showingBoosters = false;
        clearProductButtons();
        
        // Create ETB buttons
        List<String> etbTypes = tileEntity.getAvailableETBTypes();
        int buttonY = this.topPos + 30;
        int buttonIndex = 0;
        
        for (String etbType : etbTypes) {
            if (buttonIndex >= 4) break; // Max 4 buttons shown
            
            Button etbButton = this.addButton(new Button(
                    this.leftPos + 7, buttonY,
                    100, 20,
                    new StringTextComponent(formatPackName(etbType) + " (5◆)"),
                    button -> purchaseETB(etbType)
            ));
            etbButtons.add(etbButton);
            buttonY += 22;
            buttonIndex++;
        }
        
        updateButtonStates();
    }
    
    private void clearProductButtons() {
        // Remove old buttons
        for (Button button : packButtons) {
            this.buttons.remove(button);
            this.children.remove(button);
        }
        packButtons.clear();
        
        for (Button button : etbButtons) {
            this.buttons.remove(button);
            this.children.remove(button);
        }
        etbButtons.clear();
    }
    
    private void purchaseBoosterPack(String packType) {
        // Send packet to server
        ModNetworking.sendToServer(new VendingMachinePurchasePacket(
                tileEntity.getBlockPos(), 
                VendingMachinePurchasePacket.PurchaseType.BOOSTER,
                packType
        ));
    }
    
    private void purchaseETB(String etbType) {
        // Send packet to server
        ModNetworking.sendToServer(new VendingMachinePurchasePacket(
                tileEntity.getBlockPos(),
                VendingMachinePurchasePacket.PurchaseType.ETB,
                etbType
        ));
    }
    
    private String formatPackName(String packType) {
        // Convert pack_name to Pack Name
        String[] words = packType.split("_");
        StringBuilder formatted = new StringBuilder();
        for (String word : words) {
            if (formatted.length() > 0) formatted.append(" ");
            formatted.append(word.substring(0, 1).toUpperCase());
            formatted.append(word.substring(1));
        }
        return formatted.toString();
    }
    
    private void updateButtonStates() {
        int diamonds = tileEntity.getDiamondCount();
        
        // Update booster buttons
        for (Button button : packButtons) {
            button.active = diamonds >= VendingMachineTileEntity.BOOSTER_PACK_PRICE;
        }
        
        // Update ETB buttons
        for (Button button : etbButtons) {
            button.active = diamonds >= VendingMachineTileEntity.ETB_PRICE;
        }
        
        // Update category button appearance
        categoryBoosterButton.active = !showingBoosters;
        categoryETBButton.active = showingBoosters;
    }
    
    @Override
    public void tick() {
        super.tick();
        updateButtonStates();
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
        // Title
        this.font.draw(matrixStack, this.title, 8.0F, 6.0F, 4210752);
        
        // Diamond count display
        int diamonds = tileEntity.getDiamondCount();
        String diamondText = "Diamonds: " + diamonds;
        this.font.draw(matrixStack, diamondText, 26.0F, 55.0F, 4210752);
        
        // Player inventory label
        this.font.draw(matrixStack, this.inventory.getDisplayName(), 8.0F, 
                      this.imageHeight - 96 + 2, 4210752);
    }
    
    @Override
    public void render(MatrixStack matrixStack, int mouseX, int mouseY, float partialTicks) {
        this.renderBackground(matrixStack);
        super.render(matrixStack, mouseX, mouseY, partialTicks);
        this.renderTooltip(matrixStack, mouseX, mouseY);
    }
}