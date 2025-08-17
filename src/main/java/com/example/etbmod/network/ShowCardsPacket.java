package com.example.etbmod.network;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.client.screen.CardRevealScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.network.PacketBuffer;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

public class ShowCardsPacket {
    private final List<Card> cards;
    
    public ShowCardsPacket(List<Card> cards) {
        this.cards = cards;
    }
    
    public ShowCardsPacket(PacketBuffer buf) {
        int size = buf.readInt();
        cards = new ArrayList<>();
        
        for (int i = 0; i < size; i++) {
            String id = buf.readUtf();
            String name = buf.readUtf();
            String number = buf.readUtf();
            CardRarity rarity = CardRarity.values()[buf.readInt()];
            String setName = buf.readUtf();
            String imagePath = buf.readUtf();
            
            cards.add(new Card(id, name, number, rarity, setName, imagePath));
        }
    }
    
    public void toBytes(PacketBuffer buf) {
        buf.writeInt(cards.size());
        
        for (Card card : cards) {
            buf.writeUtf(card.getId());
            buf.writeUtf(card.getName());
            buf.writeUtf(card.getNumber());
            buf.writeInt(card.getRarity().ordinal());
            buf.writeUtf(card.getSetName());
            buf.writeUtf(card.getImagePath());
        }
    }
    
    public void handle(Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            // Make sure we're on the client side
            if (ctx.get().getDirection().getReceptionSide().isClient()) {
                // Open the card reveal screen on the client
                if (cards != null && !cards.isEmpty()) {
                    Minecraft.getInstance().setScreen(new CardRevealScreen(cards));
                }
            }
        });
        ctx.get().setPacketHandled(true);
    }
}