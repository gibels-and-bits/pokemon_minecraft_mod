package com.example.etbmod.network;

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
            System.out.println("[ETBMod] OpenPackPacket received from player: " + player);
            
            if (player != null) {
                player.displayClientMessage(
                    new StringTextComponent("§b[ETB Server] OpenPackPacket received"), false);
            }
            
            if (player != null && player.containerMenu instanceof GamerTableContainer) {
                GamerTableContainer container = (GamerTableContainer) player.containerMenu;
                System.out.println("[ETBMod] Container found, can open pack: " + container.canOpenPack());
                
                if (container.canOpenPack()) {
                    ItemStack packStack = container.getPackStack();
                    String setName = container.getPackSetName();
                    int packCount = packStack.getCount();
                    
                    player.displayClientMessage(
                        new StringTextComponent("§b[ETB Server] Opening " + packCount + " packs from " + setName + " (initial=" + isInitialOpen + ")"), false);
                    
                    System.out.println("[ETBMod] Opening " + packCount + " packs from set: " + setName);
                    System.out.println("[ETBMod] isInitialOpen: " + isInitialOpen);
                    
                    if (isInitialOpen && packCount > 1) {
                        // For multiple packs, use multi-pack screen
                        System.out.println("[ETBMod] Starting multi-pack session");
                        player.displayClientMessage(
                            new StringTextComponent("§b[ETB Server] Sending StartMultiPackPacket"), false);
                        ModNetworking.sendToPlayer(new StartMultiPackPacket(packCount, setName), player);
                        
                        // ALSO send the first pack of cards immediately
                        player.displayClientMessage(
                            new StringTextComponent("§b[ETB Server] Generating first pack..."), false);
                        List<Card> firstPack = CardDatabase.getInstance().generateBoosterPack(setName);
                        container.consumeOnePack();
                        ModNetworking.sendToPlayer(new SendPackCardsPacket(firstPack), player);
                        return;
                    } else if (isInitialOpen && packCount == 1) {
                        // For single pack, use regular card reveal screen
                        System.out.println("[ETBMod] Opening single pack with regular screen");
                        player.displayClientMessage(
                            new StringTextComponent("§b[ETB Server] Opening single pack with ShowCardsPacket"), false);
                        List<Card> cards = CardDatabase.getInstance().generateBoosterPack(setName);
                        container.consumeOnePack();
                        ModNetworking.sendToPlayer(new ShowCardsPacket(cards), player);
                        return;
                    }
                    
                    if (!isInitialOpen) {
                        // This is a subsequent pack request from the multi-pack screen
                        player.displayClientMessage(
                            new StringTextComponent("§b[ETB Server] Generating next pack..."), false);
                        List<Card> cards = CardDatabase.getInstance().generateBoosterPack(setName);
                        System.out.println("[ETBMod] Generated " + cards.size() + " cards for next pack");
                        
                        // Consume one pack
                        container.consumeOnePack();
                        
                        // Send cards to client
                        ModNetworking.sendToPlayer(new SendPackCardsPacket(cards), player);
                        System.out.println("[ETBMod] Sent cards to multi-pack screen");
                    }
                } else {
                    player.displayClientMessage(
                        new StringTextComponent("§c[ETB Server] No pack found in gamer table!"), false);
                }
            } else {
                if (player != null) {
                    player.displayClientMessage(
                        new StringTextComponent("§c[ETB Server] Not in gamer table container!"), false);
                }
            }
        });
        ctx.get().setPacketHandled(true);
    }
}