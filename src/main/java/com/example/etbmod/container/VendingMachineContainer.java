package com.example.etbmod.container;

import com.example.etbmod.registry.ModContainers;
import com.example.etbmod.tileentity.VendingMachineTileEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.IInventory;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.Slot;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.network.PacketBuffer;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.items.IItemHandler;
import net.minecraftforge.items.SlotItemHandler;
import net.minecraftforge.items.wrapper.InvWrapper;

public class VendingMachineContainer extends Container {
    
    private final VendingMachineTileEntity tileEntity;
    private final PlayerInventory playerInventory;
    
    // Client constructor
    public VendingMachineContainer(int windowId, PlayerInventory playerInventory, PacketBuffer data) {
        this(windowId, playerInventory, getTileEntity(playerInventory, data));
    }
    
    // Server constructor
    public VendingMachineContainer(int windowId, PlayerInventory playerInventory, VendingMachineTileEntity tileEntity) {
        super(ModContainers.VENDING_MACHINE.get(), windowId);
        this.tileEntity = tileEntity;
        this.playerInventory = playerInventory;
        
        // Add vending machine slots
        addVendingMachineSlots();
        
        // Add player inventory slots
        addPlayerInventory(playerInventory);
    }
    
    private void addVendingMachineSlots() {
        // Diamond input slot (slot 0)
        this.addSlot(new DiamondSlot(tileEntity, 0, 26, 35));
        
        // Output slots (slots 1-9) - 3x3 grid
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                int index = 1 + (row * 3) + col;
                int x = 116 + col * 18;
                int y = 17 + row * 18;
                this.addSlot(new OutputSlot(tileEntity, index, x, y));
            }
        }
    }
    
    private void addPlayerInventory(PlayerInventory playerInventory) {
        // Player inventory slots (9-35)
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                int x = 8 + col * 18;
                int y = 84 + row * 18;
                this.addSlot(new Slot(playerInventory, 9 + row * 9 + col, x, y));
            }
        }
        
        // Player hotbar slots (0-8)
        for (int col = 0; col < 9; col++) {
            int x = 8 + col * 18;
            int y = 142;
            this.addSlot(new Slot(playerInventory, col, x, y));
        }
    }
    
    @Override
    public boolean stillValid(PlayerEntity player) {
        return this.tileEntity.stillValid(player);
    }
    
    @Override
    public ItemStack quickMoveStack(PlayerEntity player, int index) {
        ItemStack itemstack = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        
        if (slot != null && slot.hasItem()) {
            ItemStack slotStack = slot.getItem();
            itemstack = slotStack.copy();
            
            // Moving from vending machine to player inventory
            if (index < 10) {
                if (!this.moveItemStackTo(slotStack, 10, this.slots.size(), true)) {
                    return ItemStack.EMPTY;
                }
            }
            // Moving from player inventory to vending machine
            else {
                // Only diamonds can go to input slot
                if (slotStack.getItem() == Items.DIAMOND) {
                    if (!this.moveItemStackTo(slotStack, 0, 1, false)) {
                        return ItemStack.EMPTY;
                    }
                } else {
                    return ItemStack.EMPTY;
                }
            }
            
            if (slotStack.isEmpty()) {
                slot.set(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
        }
        
        return itemstack;
    }
    
    public VendingMachineTileEntity getTileEntity() {
        return this.tileEntity;
    }
    
    private static VendingMachineTileEntity getTileEntity(PlayerInventory playerInventory, PacketBuffer data) {
        BlockPos pos = data.readBlockPos();
        return (VendingMachineTileEntity) playerInventory.player.level.getBlockEntity(pos);
    }
    
    /**
     * Custom slot that only accepts diamonds
     */
    private static class DiamondSlot extends Slot {
        public DiamondSlot(IInventory inventory, int index, int x, int y) {
            super(inventory, index, x, y);
        }
        
        @Override
        public boolean mayPlace(ItemStack stack) {
            return stack.getItem() == Items.DIAMOND;
        }
    }
    
    /**
     * Output slot that doesn't accept items
     */
    private static class OutputSlot extends Slot {
        public OutputSlot(IInventory inventory, int index, int x, int y) {
            super(inventory, index, x, y);
        }
        
        @Override
        public boolean mayPlace(ItemStack stack) {
            return false; // Output only
        }
    }
}