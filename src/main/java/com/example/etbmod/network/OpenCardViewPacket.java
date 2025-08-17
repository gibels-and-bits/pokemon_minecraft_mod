package com.example.etbmod.network;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.client.screen.CardViewScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.network.PacketBuffer;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.function.Supplier;

public class OpenCardViewPacket {
    private final String cardId;
    private final String cardName;
    private final String cardNumber;
    private final String rarity;
    private final String setName;
    private final String imagePath;
    
    public OpenCardViewPacket(Card card) {
        this.cardId = card.getId();
        this.cardName = card.getName();
        this.cardNumber = card.getNumber();
        this.rarity = card.getRarity().getDisplayName();
        this.setName = card.getSetName();
        this.imagePath = card.getImagePath();
    }
    
    public OpenCardViewPacket(PacketBuffer buf) {
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
            // This should run on client side
            openCardView();
        });
        ctx.get().setPacketHandled(true);
    }
    
    @OnlyIn(Dist.CLIENT)
    private void openCardView() {
        // Create card from packet data
        CardRarity cardRarity = CardRarity.fromString(rarity);
        Card card = new Card(cardId, cardName, cardNumber, cardRarity, setName, imagePath);
        
        // Open the card view screen
        Minecraft.getInstance().setScreen(new CardViewScreen(card));
    }
}