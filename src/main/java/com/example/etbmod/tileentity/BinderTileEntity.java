package com.example.etbmod.tileentity;

import com.example.etbmod.items.BinderItem;
import com.example.etbmod.registry.ModItems;
import com.example.etbmod.registry.ModTileEntities;
import net.minecraft.block.BlockState;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.network.NetworkManager;
import net.minecraft.network.play.server.SUpdateTileEntityPacket;
import net.minecraft.tileentity.TileEntity;

import javax.annotation.Nullable;

public class BinderTileEntity extends TileEntity {
    private ItemStack binderStack = ItemStack.EMPTY;
    
    public BinderTileEntity() {
        super(ModTileEntities.BINDER_TILE_ENTITY.get());
    }
    
    public ItemStack getBinderStack() {
        if (binderStack.isEmpty()) {
            // Create empty binder stack if none exists
            binderStack = new ItemStack(ModItems.BINDER.get());
        }
        return binderStack;
    }
    
    public void setBinderStack(ItemStack stack) {
        this.binderStack = stack.copy();
        this.setChanged();
        if (this.level != null && !this.level.isClientSide) {
            this.level.sendBlockUpdated(this.worldPosition, this.getBlockState(), this.getBlockState(), 3);
        }
    }
    
    @Override
    public CompoundNBT save(CompoundNBT compound) {
        super.save(compound);
        if (!binderStack.isEmpty()) {
            CompoundNBT binderTag = new CompoundNBT();
            binderStack.save(binderTag);
            compound.put("BinderStack", binderTag);
        }
        return compound;
    }
    
    @Override
    public void load(BlockState state, CompoundNBT compound) {
        super.load(state, compound);
        if (compound.contains("BinderStack")) {
            this.binderStack = ItemStack.of(compound.getCompound("BinderStack"));
        } else {
            this.binderStack = ItemStack.EMPTY;
        }
    }
    
    @Nullable
    @Override
    public SUpdateTileEntityPacket getUpdatePacket() {
        return new SUpdateTileEntityPacket(this.worldPosition, -1, this.getUpdateTag());
    }
    
    @Override
    public void onDataPacket(NetworkManager net, SUpdateTileEntityPacket pkt) {
        this.load(this.getBlockState(), pkt.getTag());
    }
    
    @Override
    public CompoundNBT getUpdateTag() {
        return this.save(new CompoundNBT());
    }
    
    @Override
    public void handleUpdateTag(BlockState state, CompoundNBT tag) {
        this.load(state, tag);
    }
}