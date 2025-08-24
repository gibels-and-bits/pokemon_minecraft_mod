package com.example.etbmod.network;

import com.example.etbmod.tileentity.VendingMachineTileEntity;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.network.PacketBuffer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.util.text.TextFormatting;
import net.minecraftforge.fml.network.NetworkEvent;

import java.util.function.Supplier;

public class VendingMachinePurchasePacket {
    
    public enum PurchaseType {
        BOOSTER,
        ETB,
        PREMIUM
    }
    
    private final BlockPos pos;
    private final PurchaseType type;
    private final String itemName;
    
    public VendingMachinePurchasePacket(BlockPos pos, PurchaseType type, String itemName) {
        this.pos = pos;
        this.type = type;
        this.itemName = itemName;
    }
    
    public static void encode(VendingMachinePurchasePacket packet, PacketBuffer buffer) {
        buffer.writeBlockPos(packet.pos);
        buffer.writeEnum(packet.type);
        buffer.writeUtf(packet.itemName);
    }
    
    public static VendingMachinePurchasePacket decode(PacketBuffer buffer) {
        BlockPos pos = buffer.readBlockPos();
        PurchaseType type = buffer.readEnum(PurchaseType.class);
        String itemName = buffer.readUtf();
        return new VendingMachinePurchasePacket(pos, type, itemName);
    }
    
    public static void handle(VendingMachinePurchasePacket packet, Supplier<NetworkEvent.Context> ctx) {
        ctx.get().enqueueWork(() -> {
            ServerPlayerEntity player = ctx.get().getSender();
            if (player != null && player.level != null) {
                TileEntity te = player.level.getBlockEntity(packet.pos);
                if (te instanceof VendingMachineTileEntity) {
                    VendingMachineTileEntity vendingMachine = (VendingMachineTileEntity) te;
                    
                    boolean success = false;
                    String message = "";
                    
                    switch (packet.type) {
                        case BOOSTER:
                            success = vendingMachine.purchaseBoosterPack(packet.itemName);
                            if (success) {
                                message = "Purchased " + formatName(packet.itemName) + " Booster Pack!";
                            } else {
                                message = "Not enough diamonds or inventory full!";
                            }
                            break;
                            
                        case ETB:
                            success = vendingMachine.purchaseETB(packet.itemName);
                            if (success) {
                                message = "Purchased " + formatName(packet.itemName) + " ETB!";
                            } else {
                                message = "Not enough diamonds or inventory full!";
                            }
                            break;
                            
                        case PREMIUM:
                            // Handle premium packs in the future
                            message = "Premium packs coming soon!";
                            break;
                    }
                    
                    // Send feedback to player
                    TextFormatting color = success ? TextFormatting.GREEN : TextFormatting.RED;
                    player.sendMessage(new StringTextComponent(message).withStyle(color), 
                                       player.getUUID());
                }
            }
        });
        ctx.get().setPacketHandled(true);
    }
    
    private static String formatName(String name) {
        String[] words = name.split("_");
        StringBuilder formatted = new StringBuilder();
        for (String word : words) {
            if (formatted.length() > 0) formatted.append(" ");
            formatted.append(word.substring(0, 1).toUpperCase());
            formatted.append(word.substring(1));
        }
        return formatted.toString();
    }
}