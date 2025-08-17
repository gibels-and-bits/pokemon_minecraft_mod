package com.example.etbmod.network;

import com.example.etbmod.ETBMod;
import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardDatabase;
import com.example.etbmod.client.screen.MultiPackOpeningScreen;
import com.example.etbmod.container.GamerTableContainer;
import net.minecraft.client.Minecraft;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.network.PacketBuffer;
import net.minecraft.util.text.StringTextComponent;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.List;
import java.util.function.Supplier;

public class OpenPackPacket {
    
    private boolean isInitialOpen;
    
    public OpenPackPacket() {
        this(true);
    }
    
    public OpenPackPacket(boolean isInitialOpen) {
        this.isInitialOpen = isInitialOpen;
    }
    
    public OpenPackPacket(PacketBuffer buf) {
        this.isInitialOpen = buf.readBoolean();
    }
    
    public void toBytes(PacketBuffer buf) {
        buf.writeBoolean(isInitialOpen);
    }
    
    public void handle(Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            ServerPlayerEntity player = ctx.get().getSender();
            // OpenPackPacket received
            
            if (player != null && player.containerMenu instanceof GamerTableContainer) {
                GamerTableContainer container = (GamerTableContainer) player.containerMenu;
                // Container found
                
                if (container.canOpenPack()) {
                    ItemStack packStack = container.getPackStack();
                    String setName = container.getPackSetName();
                    int packCount = packStack.getCount();
                    
                    // Opening packs
                    
                    
                    if (isInitialOpen && packCount > 1) {
                        // For multiple packs, use multi-pack screen
                        // Starting multi-pack session
                        ModNetworking.sendToPlayer(new StartMultiPackPacket(packCount, setName), player);
                        
                        // Send the first pack of cards immediately
                        List<Card> firstPack = CardDatabase.getInstance().generateBoosterPack(setName);
                        container.consumeOnePack();
                        ModNetworking.sendToPlayer(new SendPackCardsPacket(firstPack), player);
                        return;
                    } else if (isInitialOpen && packCount == 1) {
                        // For single pack, use regular card reveal screen
                        // Opening single pack
                        List<Card> cards = CardDatabase.getInstance().generateBoosterPack(setName);
                        container.consumeOnePack();
                        ModNetworking.sendToPlayer(new ShowCardsPacket(cards), player);
                        return;
                    }
                    
                    if (!isInitialOpen) {
                        // This is a subsequent pack request from the multi-pack screen
                        // Generating next pack
                        List<Card> cards = CardDatabase.getInstance().generateBoosterPack(setName);
                        // Generated cards for next pack
                        
                        // Consume one pack
                        container.consumeOnePack();
                        
                        // Send cards to client
                        ModNetworking.sendToPlayer(new SendPackCardsPacket(cards), player);
                        // Sent cards to multi-pack screen
                    }
                } else {
                    ETBMod.LOGGER.warn("Player " + player.getName().getString() + " tried to open pack but no pack found in gamer table");
                }
            } else {
                if (player != null) {
                    ETBMod.LOGGER.warn("Player " + player.getName().getString() + " tried to open pack but not in gamer table container");
                }
            }
        });
        ctx.get().setPacketHandled(true);
    }
}