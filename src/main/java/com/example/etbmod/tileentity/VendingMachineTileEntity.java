package com.example.etbmod.tileentity;

import com.example.etbmod.container.VendingMachineContainer;
import com.example.etbmod.items.BoosterPackItem;
import com.example.etbmod.registry.ModItems;
import com.example.etbmod.registry.ModTileEntities;
import net.minecraft.block.BlockState;
import net.minecraft.entity.item.ItemEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.IInventory;
import net.minecraft.inventory.ItemStackHelper;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.INamedContainerProvider;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.network.NetworkManager;
import net.minecraft.network.play.server.SUpdateTileEntityPacket;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.NonNullList;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TranslationTextComponent;
import net.minecraft.world.World;

import javax.annotation.Nullable;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class VendingMachineTileEntity extends TileEntity implements IInventory, INamedContainerProvider {
    
    // Inventory slots: 0 = diamond input, 1-9 = output slots for dispensed items
    private NonNullList<ItemStack> items = NonNullList.withSize(10, ItemStack.EMPTY);
    private static final int DIAMOND_SLOT = 0;
    private static final int OUTPUT_START = 1;
    private static final int OUTPUT_END = 9;
    
    // Prices in diamonds
    public static final int BOOSTER_PACK_PRICE = 1;
    public static final int ETB_PRICE = 5;
    public static final int PREMIUM_PACK_PRICE = 3;
    
    private Random random = new Random();
    
    public VendingMachineTileEntity() {
        super(ModTileEntities.VENDING_MACHINE.get());
    }
    
    @Override
    public void load(BlockState state, CompoundNBT nbt) {
        super.load(state, nbt);
        this.items = NonNullList.withSize(this.getContainerSize(), ItemStack.EMPTY);
        ItemStackHelper.loadAllItems(nbt, this.items);
    }
    
    @Override
    public CompoundNBT save(CompoundNBT compound) {
        super.save(compound);
        ItemStackHelper.saveAllItems(compound, this.items);
        return compound;
    }
    
    @Override
    public int getContainerSize() {
        return items.size();
    }
    
    @Override
    public boolean isEmpty() {
        for (ItemStack stack : this.items) {
            if (!stack.isEmpty()) {
                return false;
            }
        }
        return true;
    }
    
    @Override
    public ItemStack getItem(int index) {
        return this.items.get(index);
    }
    
    @Override
    public ItemStack removeItem(int index, int count) {
        ItemStack stack = ItemStackHelper.removeItem(this.items, index, count);
        if (!stack.isEmpty()) {
            this.setChanged();
        }
        return stack;
    }
    
    @Override
    public ItemStack removeItemNoUpdate(int index) {
        return ItemStackHelper.takeItem(this.items, index);
    }
    
    @Override
    public void setItem(int index, ItemStack stack) {
        this.items.set(index, stack);
        if (stack.getCount() > this.getMaxStackSize()) {
            stack.setCount(this.getMaxStackSize());
        }
        this.setChanged();
    }
    
    @Override
    public boolean stillValid(PlayerEntity player) {
        if (this.level.getBlockEntity(this.worldPosition) != this) {
            return false;
        } else {
            return player.distanceToSqr(
                    (double)this.worldPosition.getX() + 0.5D,
                    (double)this.worldPosition.getY() + 0.5D,
                    (double)this.worldPosition.getZ() + 0.5D) <= 64.0D;
        }
    }
    
    @Override
    public void clearContent() {
        this.items.clear();
        this.setChanged();
    }
    
    @Override
    public ITextComponent getDisplayName() {
        return new TranslationTextComponent("container.etbmod.vending_machine");
    }
    
    @Nullable
    @Override
    public Container createMenu(int windowId, PlayerInventory playerInventory, PlayerEntity player) {
        return new VendingMachineContainer(windowId, playerInventory, this);
    }
    
    /**
     * Attempt to purchase a booster pack
     */
    public boolean purchaseBoosterPack(String packType) {
        if (canAfford(BOOSTER_PACK_PRICE)) {
            ItemStack diamondStack = items.get(DIAMOND_SLOT);
            diamondStack.shrink(BOOSTER_PACK_PRICE);
            
            // Get the booster pack item from registry
            ItemStack boosterPack = getBoosterPackItem(packType);
            
            if (boosterPack != null && addToOutput(boosterPack)) {
                this.setChanged();
                return true;
            } else {
                // Refund if no space or item not found
                diamondStack.grow(BOOSTER_PACK_PRICE);
            }
        }
        return false;
    }
    
    /**
     * Attempt to purchase an ETB
     */
    public boolean purchaseETB(String etbType) {
        if (canAfford(ETB_PRICE)) {
            ItemStack diamondStack = items.get(DIAMOND_SLOT);
            diamondStack.shrink(ETB_PRICE);
            
            // Get the ETB item from registry
            ItemStack etbItem = getETBItem(etbType);
            
            if (etbItem != null && addToOutput(etbItem)) {
                this.setChanged();
                return true;
            } else {
                // Refund if no space or item not found
                diamondStack.grow(ETB_PRICE);
            }
        }
        return false;
    }
    
    /**
     * Check if player has enough diamonds
     */
    public boolean canAfford(int price) {
        ItemStack diamondStack = items.get(DIAMOND_SLOT);
        return diamondStack.getItem() == Items.DIAMOND && diamondStack.getCount() >= price;
    }
    
    /**
     * Get current diamond count
     */
    public int getDiamondCount() {
        ItemStack diamondStack = items.get(DIAMOND_SLOT);
        if (diamondStack.getItem() == Items.DIAMOND) {
            return diamondStack.getCount();
        }
        return 0;
    }
    
    /**
     * Add item to output slots
     */
    private boolean addToOutput(ItemStack stack) {
        for (int i = OUTPUT_START; i <= OUTPUT_END; i++) {
            ItemStack slotStack = items.get(i);
            if (slotStack.isEmpty()) {
                items.set(i, stack.copy());
                return true;
            } else if (ItemStack.isSame(slotStack, stack) && 
                       slotStack.getCount() + stack.getCount() <= slotStack.getMaxStackSize()) {
                slotStack.grow(stack.getCount());
                return true;
            }
        }
        return false;
    }
    
    /**
     * Get ETB item by type
     */
    private ItemStack getETBItem(String etbType) {
        if (ModItems.ETB_ITEMS.containsKey(etbType)) {
            return new ItemStack(ModItems.ETB_ITEMS.get(etbType).get());
        }
        return null;
    }
    
    /**
     * Get booster pack item by type
     */
    private ItemStack getBoosterPackItem(String packType) {
        if (ModItems.BOOSTER_PACKS.containsKey(packType)) {
            return new ItemStack(ModItems.BOOSTER_PACKS.get(packType).get());
        }
        return null;
    }
    
    /**
     * Get list of available pack types
     */
    public List<String> getAvailablePackTypes() {
        List<String> packTypes = new ArrayList<>();
        packTypes.add("black_bolt");
        packTypes.add("white_flare");
        packTypes.add("brilliant_stars");
        packTypes.add("evolving_skies");
        packTypes.add("crown_zenith");
        // Add more pack types as needed
        return packTypes;
    }
    
    /**
     * Get list of available ETB types
     */
    public List<String> getAvailableETBTypes() {
        return new ArrayList<>(ModItems.ETB_ITEMS.keySet());
    }
    
    /**
     * Drop contents when block is broken
     */
    public void dropContents(World world, BlockPos pos) {
        for (ItemStack stack : items) {
            if (!stack.isEmpty()) {
                ItemEntity itemEntity = new ItemEntity(world, pos.getX() + 0.5, pos.getY() + 0.5, 
                                                       pos.getZ() + 0.5, stack);
                world.addFreshEntity(itemEntity);
            }
        }
        clearContent();
    }
    
    @Override
    public CompoundNBT getUpdateTag() {
        CompoundNBT tag = super.getUpdateTag();
        return this.save(tag);
    }
    
    @Override
    public void handleUpdateTag(BlockState state, CompoundNBT tag) {
        this.load(state, tag);
    }
    
    @Nullable
    @Override
    public SUpdateTileEntityPacket getUpdatePacket() {
        return new SUpdateTileEntityPacket(this.worldPosition, -1, this.getUpdateTag());
    }
    
    @Override
    public void onDataPacket(NetworkManager net, SUpdateTileEntityPacket pkt) {
        this.handleUpdateTag(this.getBlockState(), pkt.getTag());
    }
}