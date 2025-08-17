package com.example.etbmod.network;

import net.minecraft.network.PacketBuffer;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.function.Supplier;

public class RequestNextPackPacket {
    
    public RequestNextPackPacket() {}
    
    public RequestNextPackPacket(PacketBuffer buf) {}
    
    public void toBytes(PacketBuffer buf) {}
    
    public void handle(Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            // Delegate to OpenPackPacket with isInitialOpen = false
            OpenPackPacket openPackPacket = new OpenPackPacket(false);
            openPackPacket.handle(ctx);
        });
        ctx.get().setPacketHandled(true);
    }
}