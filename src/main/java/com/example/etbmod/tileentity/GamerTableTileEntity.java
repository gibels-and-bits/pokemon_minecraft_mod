package com.example.etbmod.tileentity;

import com.example.etbmod.container.GamerTableContainer;
import com.example.etbmod.registry.ModTileEntities;
import net.minecraft.block.BlockState;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.IInventory;
import net.minecraft.inventory.ItemStackHelper;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.INamedContainerProvider;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.NonNullList;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TranslationTextComponent;

import javax.annotation.Nullable;

public class GamerTableTileEntity extends TileEntity implements IInventory, INamedContainerProvider {
    
    private NonNullList<ItemStack> items = NonNullList.withSize(1, ItemStack.EMPTY);
    
    public GamerTableTileEntity() {
        super(ModTileEntities.GAMER_TABLE.get());
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
        return 1;
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
            return player.distanceToSqr((double)this.worldPosition.getX() + 0.5D, 
                                        (double)this.worldPosition.getY() + 0.5D, 
                                        (double)this.worldPosition.getZ() + 0.5D) <= 64.0D;
        }
    }
    
    @Override
    public void clearContent() {
        this.items.clear();
    }
    
    @Override
    public ITextComponent getDisplayName() {
        return new TranslationTextComponent("container.etbmod.gamer_table");
    }
    
    @Nullable
    @Override
    public Container createMenu(int id, PlayerInventory playerInventory, PlayerEntity player) {
        return new GamerTableContainer(id, playerInventory, this);
    }
}