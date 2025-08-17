package com.example.etbmod.network;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.items.CardItem;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.network.PacketBuffer;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.text.StringTextComponent;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.function.Supplier;

public class AddCardToInventoryPacket {
    private final String cardId;
    private final String cardName;
    private final String cardNumber;
    private final String rarity;
    private final String setName;
    private final String imagePath;
    
    public AddCardToInventoryPacket(Card card) {
        this.cardId = card.getId();
        this.cardName = card.getName();
        this.cardNumber = card.getNumber();
        this.rarity = card.getRarity().getDisplayName();
        this.setName = card.getSetName();
        this.imagePath = card.getImagePath();
    }
    
    public AddCardToInventoryPacket(PacketBuffer buf) {
        this.cardId = buf.readUtf(32767);
        this.cardName = buf.readUtf(32767);
        this.cardNumber = buf.readUtf(32767);
        this.rarity = buf.readUtf(32767);
        this.setName = buf.readUtf(32767);
        this.imagePath = buf.readUtf(32767);
    }
    
    public void encode(PacketBuffer buf) {
        buf.writeUtf(cardId);
        buf.writeUtf(cardName);
        buf.writeUtf(cardNumber);
        buf.writeUtf(rarity);
        buf.writeUtf(setName);
        buf.writeUtf(imagePath);
    }
    
    public void handle(Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            ServerPlayerEntity player = ctx.get().getSender();
            if (player != null) {
                // Create card from packet data
                CardRarity cardRarity = CardRarity.fromString(rarity);
                Card card = new Card(cardId, cardName, cardNumber, cardRarity, setName, imagePath);
                
                // Create card item
                ItemStack cardStack = CardItem.createCardItem(card);
                
                // Try to add to player inventory
                if (player.inventory.add(cardStack)) {
                    // Success message
                    player.displayClientMessage(
                        new StringTextComponent("§a" + cardName + " has been added to your inventory!"), 
                        false);
                    
                    // Play sound on server
                    player.playSound(SoundEvents.ITEM_PICKUP, 0.5F, 1.0F);
                } else {
                    // Inventory full - drop on ground
                    player.drop(cardStack, false);
                    player.displayClientMessage(
                        new StringTextComponent("§eInventory full! " + cardName + " dropped on ground."), 
                        false);
                }
            }
        });
        ctx.get().setPacketHandled(true);
    }
}