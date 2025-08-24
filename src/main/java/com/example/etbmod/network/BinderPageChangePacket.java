package com.example.etbmod.network;

import com.example.etbmod.container.BinderContainer;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.network.PacketBuffer;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.function.Supplier;

public class BinderPageChangePacket {
    private final int pageDelta;
    
    public BinderPageChangePacket(int pageDelta) {
        this.pageDelta = pageDelta;
    }
    
    public static void encode(BinderPageChangePacket packet, PacketBuffer buffer) {
        buffer.writeInt(packet.pageDelta);
    }
    
    public static BinderPageChangePacket decode(PacketBuffer buffer) {
        return new BinderPageChangePacket(buffer.readInt());
    }
    
    public static void handle(BinderPageChangePacket packet, Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            ServerPlayerEntity player = ctx.get().getSender();
            if (player != null && player.containerMenu instanceof BinderContainer) {
                BinderContainer container = (BinderContainer) player.containerMenu;
                container.changePage(packet.pageDelta);
            }
        });
        ctx.get().setPacketHandled(true);
    }
}