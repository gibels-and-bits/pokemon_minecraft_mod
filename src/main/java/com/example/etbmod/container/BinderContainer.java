package com.example.etbmod.container;

import com.example.etbmod.items.BinderItem;
import com.example.etbmod.items.CardItem;
import com.example.etbmod.registry.ModContainers;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.IInventory;
import net.minecraft.inventory.Inventory;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.Slot;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.nbt.ListNBT;
import net.minecraft.network.PacketBuffer;
import net.minecraftforge.items.IItemHandler;
import net.minecraftforge.items.ItemStackHandler;
import net.minecraftforge.items.SlotItemHandler;

public class BinderContainer extends Container {
    private static final int CARDS_PER_PAGE = 9;
    private final ItemStack binderStack;
    private final PlayerInventory playerInventory;
    private int currentPage = 0;
    private final ItemStackHandler pageInventory;
    private boolean isBlockContainer = false;
    
    // Client constructor
    public BinderContainer(int windowId, PlayerInventory playerInventory, PacketBuffer buffer) {
        this(windowId, playerInventory, buffer.readItem());
    }
    
    // Server constructor
    public BinderContainer(int windowId, PlayerInventory playerInventory, ItemStack binderStack) {
        super(ModContainers.BINDER_CONTAINER.get(), windowId);
        this.playerInventory = playerInventory;
        this.binderStack = binderStack;
        this.currentPage = BinderItem.getCurrentPage(binderStack);
        
        // Create page inventory handler
        this.pageInventory = new ItemStackHandler(CARDS_PER_PAGE) {
            @Override
            public boolean isItemValid(int slot, ItemStack stack) {
                return stack.getItem() instanceof CardItem;
            }
            
            @Override
            protected void onContentsChanged(int slot) {
                super.onContentsChanged(slot);
                savePageToNBT();
            }
        };
        
        // Load current page from NBT
        loadPageFromNBT();
        
        // Add binder slots (3x3 grid for card display) - matching the visual layout
        // Card size is 80x80 with 10px spacing, starting at x=8, y=20 in the GUI
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                int slotIndex = row * 3 + col;
                // Position slots in the center of each card display area
                int slotX = 8 + col * 90 + 32; // 8 start + col * (80 size + 10 spacing) + center offset
                int slotY = 20 + row * 90 + 32; // 20 start + row * (80 size + 10 spacing) + center offset
                this.addSlot(new SlotItemHandler(pageInventory, slotIndex, slotX, slotY) {
                    @Override
                    public boolean mayPlace(ItemStack stack) {
                        return stack.getItem() instanceof CardItem;
                    }
                    
                    @Override
                    public int getMaxStackSize() {
                        return 1;
                    }
                });
            }
        }
        
        // Add player inventory slots - adjusted for larger GUI (286x330)
        int invStartY = 275; // Moved down to accommodate larger card grid
        for (int row = 0; row < 3; ++row) {
            for (int col = 0; col < 9; ++col) {
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9, 8 + col * 18, invStartY + row * 18));
            }
        }
        
        // Add player hotbar slots
        for (int col = 0; col < 9; ++col) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, invStartY + 58));
        }
    }
    
    private void loadPageFromNBT() {
        ListNBT cards = BinderItem.getCards(binderStack);
        int startIdx = currentPage * CARDS_PER_PAGE;
        
        for (int i = 0; i < CARDS_PER_PAGE; i++) {
            int cardIdx = startIdx + i;
            if (cardIdx < cards.size()) {
                CompoundNBT cardTag = cards.getCompound(cardIdx);
                pageInventory.setStackInSlot(i, ItemStack.of(cardTag));
            } else {
                pageInventory.setStackInSlot(i, ItemStack.EMPTY);
            }
        }
    }
    
    private void savePageToNBT() {
        ListNBT cards = BinderItem.getCards(binderStack);
        int startIdx = currentPage * CARDS_PER_PAGE;
        
        // Ensure list is large enough
        while (cards.size() < startIdx + CARDS_PER_PAGE) {
            cards.add(new CompoundNBT());
        }
        
        // Save current page
        for (int i = 0; i < CARDS_PER_PAGE; i++) {
            ItemStack stack = pageInventory.getStackInSlot(i);
            CompoundNBT cardTag = new CompoundNBT();
            if (!stack.isEmpty()) {
                stack.save(cardTag);
            }
            cards.set(startIdx + i, cardTag);
        }
        
        // Clean up empty slots at the end
        for (int i = cards.size() - 1; i >= 0; i--) {
            CompoundNBT tag = cards.getCompound(i);
            if (tag.isEmpty() || !tag.contains("id")) {
                cards.remove(i);
            } else {
                break;
            }
        }
        
        BinderItem.setCards(binderStack, cards);
    }
    
    public void changePage(int delta) {
        // Save current page
        savePageToNBT();
        
        // Change page
        int maxPage = BinderItem.MAX_PAGES - 1;
        currentPage = Math.max(0, Math.min(currentPage + delta, maxPage));
        BinderItem.setCurrentPage(binderStack, currentPage);
        
        // Load new page
        loadPageFromNBT();
        
        // Update slots
        this.broadcastChanges();
    }
    
    public void setPage(int page) {
        // Save current page
        savePageToNBT();
        
        // Set page
        currentPage = Math.max(0, Math.min(page, BinderItem.MAX_PAGES - 1));
        BinderItem.setCurrentPage(binderStack, currentPage);
        
        // Load new page
        loadPageFromNBT();
        
        // Update slots
        this.broadcastChanges();
    }
    
    public int getCurrentPage() {
        return currentPage;
    }
    
    public int getTotalPages() {
        return BinderItem.MAX_PAGES;
    }
    
    public int getTotalCards() {
        return BinderItem.getCards(binderStack).size();
    }
    
    @Override
    public boolean stillValid(PlayerEntity player) {
        // Always return true for now - proper validation would check if player is near block or has item
        return true;
    }
    
    @Override
    public ItemStack quickMoveStack(PlayerEntity player, int index) {
        ItemStack returnStack = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        
        if (slot != null && slot.hasItem()) {
            ItemStack slotStack = slot.getItem();
            returnStack = slotStack.copy();
            
            // Moving from binder slots to player inventory
            if (index < CARDS_PER_PAGE) {
                if (!this.moveItemStackTo(slotStack, CARDS_PER_PAGE, CARDS_PER_PAGE + 36, true)) {
                    return ItemStack.EMPTY;
                }
            }
            // Moving from player inventory to binder
            else {
                if (slotStack.getItem() instanceof CardItem) {
                    if (!this.moveItemStackTo(slotStack, 0, CARDS_PER_PAGE, false)) {
                        return ItemStack.EMPTY;
                    }
                }
                // Move between inventory and hotbar
                else if (index < CARDS_PER_PAGE + 27) {
                    if (!this.moveItemStackTo(slotStack, CARDS_PER_PAGE + 27, CARDS_PER_PAGE + 36, false)) {
                        return ItemStack.EMPTY;
                    }
                } else {
                    if (!this.moveItemStackTo(slotStack, CARDS_PER_PAGE, CARDS_PER_PAGE + 27, false)) {
                        return ItemStack.EMPTY;
                    }
                }
            }
            
            if (slotStack.isEmpty()) {
                slot.set(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
            
            if (slotStack.getCount() == returnStack.getCount()) {
                return ItemStack.EMPTY;
            }
            
            slot.onTake(player, slotStack);
        }
        
        return returnStack;
    }
    
    @Override
    public void removed(PlayerEntity player) {
        super.removed(player);
        // Save any remaining changes
        savePageToNBT();
    }
}