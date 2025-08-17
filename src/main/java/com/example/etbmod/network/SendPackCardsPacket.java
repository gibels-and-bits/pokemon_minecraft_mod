package com.example.etbmod.network;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.client.screen.MultiPackOpeningScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.network.PacketBuffer;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

public class SendPackCardsPacket {
    private final List<Card> cards;
    
    public SendPackCardsPacket(List<Card> cards) {
        this.cards = cards;
    }
    
    public SendPackCardsPacket(PacketBuffer buf) {
        int cardCount = buf.readInt();
        this.cards = new ArrayList<>();
        
        for (int i = 0; i < cardCount; i++) {
            String id = buf.readUtf();
            String name = buf.readUtf();
            String number = buf.readUtf();
            String setName = buf.readUtf();
            String imagePath = buf.readUtf();
            String rarityStr = buf.readUtf();
            
            CardRarity rarity = CardRarity.COMMON;
            try {
                rarity = CardRarity.valueOf(rarityStr);
            } catch (IllegalArgumentException e) {
                // Debug: Unknown rarity
            }
            
            cards.add(new Card(id, name, number, rarity, setName, imagePath));
        }
    }
    
    public void toBytes(PacketBuffer buf) {
        buf.writeInt(cards.size());
        
        for (Card card : cards) {
            buf.writeUtf(card.getId());
            buf.writeUtf(card.getName());
            buf.writeUtf(card.getNumber());
            buf.writeUtf(card.getSetName());
            buf.writeUtf(card.getImagePath());
            buf.writeUtf(card.getRarity().name());
        }
    }
    
    public void handle(Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            if (ctx.get().getDirection().getReceptionSide().isClient()) {
                // Debug message
                if (Minecraft.getInstance().player != null) {
                    Minecraft.getInstance().player.displayClientMessage(
                        new net.minecraft.util.text.StringTextComponent("§a[ETB] Received SendPackCardsPacket with " + cards.size() + " cards"), false);
                }
                // Send cards to the multi-pack screen
                if (Minecraft.getInstance().screen instanceof MultiPackOpeningScreen) {
                    MultiPackOpeningScreen screen = (MultiPackOpeningScreen) Minecraft.getInstance().screen;
                    screen.setCurrentPackCards(cards);
                    Minecraft.getInstance().player.displayClientMessage(
                        new net.minecraft.util.text.StringTextComponent("§a[ETB] Cards sent to MultiPackOpeningScreen"), false);
                } else {
                    Minecraft.getInstance().player.displayClientMessage(
                        new net.minecraft.util.text.StringTextComponent("§c[ETB] ERROR: Not in MultiPackOpeningScreen!"), false);
                }
            }
        });
        ctx.get().setPacketHandled(true);
    }
}