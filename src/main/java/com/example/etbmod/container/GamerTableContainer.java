package com.example.etbmod.container;

import com.example.etbmod.items.BoosterPackItem;
import com.example.etbmod.registry.ModContainers;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.inventory.IInventory;
import net.minecraft.inventory.Inventory;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.Slot;
import net.minecraft.item.ItemStack;
import net.minecraft.util.IWorldPosCallable;

public class GamerTableContainer extends Container {
    
    private final IInventory tableInventory;
    private final IWorldPosCallable access;
    private final PlayerEntity player;
    
    public GamerTableContainer(int id, PlayerInventory playerInventory) {
        this(id, playerInventory, new Inventory(1));
    }
    
    public GamerTableContainer(int id, PlayerInventory playerInventory, IInventory tableInventory) {
        super(ModContainers.GAMER_TABLE.get(), id);
        this.tableInventory = tableInventory;
        this.access = IWorldPosCallable.NULL;
        this.player = playerInventory.player;
        
        tableInventory.startOpen(playerInventory.player);
        
        // Add gamer table slot - accepts only booster packs (now supports stacks)
        // Standard position like a chest
        this.addSlot(new Slot(tableInventory, 0, 80, 20) {
            @Override
            public boolean mayPlace(ItemStack stack) {
                return stack.getItem() instanceof BoosterPackItem;
            }
            
            @Override
            public int getMaxStackSize() {
                return 64; // Allow full stack of booster packs
            }
        });
        
        // Add player inventory slots - standard chest positions
        for (int row = 0; row < 3; ++row) {
            for (int col = 0; col < 9; ++col) {
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9, 8 + col * 18, 84 + row * 18));
            }
        }
        
        // Add player hotbar slots
        for (int col = 0; col < 9; ++col) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, 142));
        }
    }
    
    @Override
    public boolean stillValid(PlayerEntity player) {
        return this.tableInventory.stillValid(player);
    }
    
    @Override
    public ItemStack quickMoveStack(PlayerEntity player, int index) {
        ItemStack itemstack = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        
        if (slot != null && slot.hasItem()) {
            ItemStack slotStack = slot.getItem();
            itemstack = slotStack.copy();
            
            // Moving from table slot to player inventory
            if (index == 0) {
                if (!this.moveItemStackTo(slotStack, 1, 37, true)) {
                    return ItemStack.EMPTY;
                }
            }
            // Moving from player inventory to table slot
            else {
                // Check if it's a booster pack
                if (slotStack.getItem() instanceof BoosterPackItem) {
                    if (!this.moveItemStackTo(slotStack, 0, 1, false)) {
                        return ItemStack.EMPTY;
                    }
                }
                // Move between inventory and hotbar
                else if (index < 28) {
                    if (!this.moveItemStackTo(slotStack, 28, 37, false)) {
                        return ItemStack.EMPTY;
                    }
                } else if (index < 37) {
                    if (!this.moveItemStackTo(slotStack, 1, 28, false)) {
                        return ItemStack.EMPTY;
                    }
                }
            }
            
            if (slotStack.isEmpty()) {
                slot.set(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
            
            if (slotStack.getCount() == itemstack.getCount()) {
                return ItemStack.EMPTY;
            }
            
            slot.onTake(player, slotStack);
        }
        
        return itemstack;
    }
    
    @Override
    public void removed(PlayerEntity player) {
        super.removed(player);
        this.tableInventory.stopOpen(player);
    }
    
    public boolean canOpenPack() {
        ItemStack stack = this.tableInventory.getItem(0);
        return !stack.isEmpty() && stack.getItem() instanceof BoosterPackItem;
    }
    
    public String getPackSetName() {
        ItemStack stack = this.tableInventory.getItem(0);
        if (!stack.isEmpty() && stack.getItem() instanceof BoosterPackItem) {
            return ((BoosterPackItem) stack.getItem()).getSetName();
        }
        return null;
    }
    
    public void consumePack() {
        this.tableInventory.removeItem(0, 1);
    }
    
    public void consumeOnePack() {
        ItemStack stack = this.tableInventory.getItem(0);
        if (!stack.isEmpty()) {
            stack.shrink(1);
            this.tableInventory.setItem(0, stack);
        }
    }
    
    public ItemStack getPackStack() {
        return this.tableInventory.getItem(0);
    }
}