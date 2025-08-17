package com.example.etbmod.network;

import com.example.etbmod.client.screen.MultiPackOpeningScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.network.PacketBuffer;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.function.Supplier;

public class StartMultiPackPacket {
    private final int packCount;
    private final String setName;
    
    public StartMultiPackPacket(int packCount, String setName) {
        this.packCount = packCount;
        this.setName = setName;
    }
    
    public StartMultiPackPacket(PacketBuffer buf) {
        this.packCount = buf.readInt();
        this.setName = buf.readUtf();
    }
    
    public void toBytes(PacketBuffer buf) {
        buf.writeInt(packCount);
        buf.writeUtf(setName);
    }
    
    public void handle(Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            if (ctx.get().getDirection().getReceptionSide().isClient()) {
                // Debug message
                if (Minecraft.getInstance().player != null) {
                    Minecraft.getInstance().player.displayClientMessage(
                        new net.minecraft.util.text.StringTextComponent("§d[ETB] Opening multi-pack screen for " + packCount + " packs"), false);
                }
                // Open the multi-pack screen
                Minecraft.getInstance().setScreen(new MultiPackOpeningScreen(packCount, setName));
            }
        });
        ctx.get().setPacketHandled(true);
    }
}