package com.example.etbmod.network;

import com.example.etbmod.ETBMod;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.fml.network.NetworkDirection;
import net.minecraftforge.fml.network.NetworkRegistry;
import net.minecraftforge.fml.network.PacketDistributor;
import net.minecraftforge.fml.network.simple.SimpleChannel;

public class ModNetworking {
    private static SimpleChannel INSTANCE;
    private static int packetId = 0;
    
    private static int id() {
        return packetId++;
    }
    
    public static void register() {
        SimpleChannel net = NetworkRegistry.ChannelBuilder
                .named(new ResourceLocation(ETBMod.MOD_ID, "messages"))
                .networkProtocolVersion(() -> "1.0")
                .clientAcceptedVersions(s -> true)
                .serverAcceptedVersions(s -> true)
                .simpleChannel();
        
        INSTANCE = net;
        
        net.messageBuilder(OpenPackPacket.class, id(), NetworkDirection.PLAY_TO_SERVER)
                .decoder(OpenPackPacket::new)
                .encoder(OpenPackPacket::toBytes)
                .consumer(OpenPackPacket::handle)
                .add();
        
        net.messageBuilder(ShowCardsPacket.class, id(), NetworkDirection.PLAY_TO_CLIENT)
                .decoder(ShowCardsPacket::new)
                .encoder(ShowCardsPacket::toBytes)
                .consumer(ShowCardsPacket::handle)
                .add();
        
        net.messageBuilder(StartMultiPackPacket.class, id(), NetworkDirection.PLAY_TO_CLIENT)
                .decoder(StartMultiPackPacket::new)
                .encoder(StartMultiPackPacket::toBytes)
                .consumer(StartMultiPackPacket::handle)
                .add();
        
        net.messageBuilder(SendPackCardsPacket.class, id(), NetworkDirection.PLAY_TO_CLIENT)
                .decoder(SendPackCardsPacket::new)
                .encoder(SendPackCardsPacket::toBytes)
                .consumer(SendPackCardsPacket::handle)
                .add();
        
        net.messageBuilder(RequestNextPackPacket.class, id(), NetworkDirection.PLAY_TO_SERVER)
                .decoder(RequestNextPackPacket::new)
                .encoder(RequestNextPackPacket::toBytes)
                .consumer(RequestNextPackPacket::handle)
                .add();
    }
    
    public static <MSG> void sendToServer(MSG message) {
        INSTANCE.sendToServer(message);
    }
    
    public static <MSG> void sendToPlayer(MSG message, ServerPlayerEntity player) {
        INSTANCE.send(PacketDistributor.PLAYER.with(() -> player), message);
    }
}