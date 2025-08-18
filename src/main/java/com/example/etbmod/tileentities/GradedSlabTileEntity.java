package com.example.etbmod.tileentities;

import com.example.etbmod.registry.ModTileEntities;
import net.minecraft.block.BlockState;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.network.NetworkManager;
import net.minecraft.network.play.server.SUpdateTileEntityPacket;
import net.minecraft.tileentity.TileEntity;

import javax.annotation.Nullable;

public class GradedSlabTileEntity extends TileEntity {
    private int grade = 10;
    private String cardId = "";
    private String cardName = "";
    private String cardNumber = "";
    private String cardRarity = "";
    private String cardSet = "";
    private String cardImagePath = "";
    
    public GradedSlabTileEntity() {
        super(ModTileEntities.GRADED_SLAB.get());
    }
    
    public void setCardData(int grade, String cardId, String cardName, String cardNumber, 
                           String cardRarity, String cardSet, String cardImagePath) {
        this.grade = grade;
        this.cardId = cardId;
        this.cardName = cardName;
        this.cardNumber = cardNumber;
        this.cardRarity = cardRarity;
        this.cardSet = cardSet;
        this.cardImagePath = cardImagePath;
        
        setChanged();
        if (level != null && !level.isClientSide) {
            level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), 3);
        }
    }
    
    @Override
    public CompoundNBT save(CompoundNBT compound) {
        super.save(compound);
        compound.putInt("grade", grade);
        compound.putString("cardId", cardId);
        compound.putString("cardName", cardName);
        compound.putString("cardNumber", cardNumber);
        compound.putString("cardRarity", cardRarity);
        compound.putString("cardSet", cardSet);
        compound.putString("cardImagePath", cardImagePath);
        return compound;
    }
    
    @Override
    public void load(BlockState state, CompoundNBT nbt) {
        super.load(state, nbt);
        grade = nbt.getInt("grade");
        cardId = nbt.getString("cardId");
        cardName = nbt.getString("cardName");
        cardNumber = nbt.getString("cardNumber");
        cardRarity = nbt.getString("cardRarity");
        cardSet = nbt.getString("cardSet");
        cardImagePath = nbt.getString("cardImagePath");
    }
    
    @Nullable
    @Override
    public SUpdateTileEntityPacket getUpdatePacket() {
        return new SUpdateTileEntityPacket(worldPosition, 0, getUpdateTag());
    }
    
    @Override
    public CompoundNBT getUpdateTag() {
        return save(new CompoundNBT());
    }
    
    @Override
    public void onDataPacket(NetworkManager net, SUpdateTileEntityPacket pkt) {
        load(getBlockState(), pkt.getTag());
    }
    
    // Getters
    public int getGrade() { return grade; }
    public String getCardId() { return cardId; }
    public String getCardName() { return cardName; }
    public String getCardNumber() { return cardNumber; }
    public String getCardRarity() { return cardRarity; }
    public String getCardSet() { return cardSet; }
    public String getCardImagePath() { return cardImagePath; }
}