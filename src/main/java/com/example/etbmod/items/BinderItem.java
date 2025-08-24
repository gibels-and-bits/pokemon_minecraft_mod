package com.example.etbmod.items;

import com.example.etbmod.ETBMod;
import com.example.etbmod.blocks.BinderBlock;
import com.example.etbmod.container.BinderContainer;
import com.example.etbmod.registry.ModBlocks;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.INamedContainerProvider;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemUseContext;
import net.minecraft.item.Rarity;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.nbt.ListNBT;
import net.minecraft.util.ActionResult;
import net.minecraft.util.ActionResultType;
import net.minecraft.util.Hand;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.world.World;
import net.minecraftforge.fml.network.NetworkHooks;

import javax.annotation.Nullable;

public class BinderItem extends BlockItem {
    public static final int CARDS_PER_PAGE = 9;
    public static final int MAX_PAGES = 20;
    
    public BinderItem() {
        super(ModBlocks.BINDER_BLOCK.get(), new Item.Properties()
                .tab(ItemGroup.TAB_MISC)
                .stacksTo(1)
                .rarity(Rarity.UNCOMMON));
    }
    
    @Override
    public ActionResult<ItemStack> use(World world, PlayerEntity player, Hand hand) {
        ItemStack stack = player.getItemInHand(hand);
        
        if (!world.isClientSide) {
            ServerPlayerEntity serverPlayer = (ServerPlayerEntity) player;
            ETBMod.LOGGER.info("Opening binder GUI for player: " + player.getName().getString());
            NetworkHooks.openGui(serverPlayer, new INamedContainerProvider() {
                @Override
                public ITextComponent getDisplayName() {
                    return new StringTextComponent("Binder");
                }
                
                @Override
                @Nullable
                public Container createMenu(int windowId, PlayerInventory playerInventory, PlayerEntity player) {
                    return new BinderContainer(windowId, playerInventory, stack);
                }
            }, buffer -> {
                buffer.writeItem(stack);
            });
        }
        
        return ActionResult.sidedSuccess(stack, world.isClientSide);
    }
    
    @Override
    public ActionResultType useOn(ItemUseContext context) {
        // Check if sneaking to place as block, otherwise open GUI
        if (context.getPlayer() != null && context.getPlayer().isCrouching()) {
            return super.useOn(context);
        }
        // Don't place block when not sneaking - let use() handle opening
        return ActionResultType.PASS;
    }
    
    public static CompoundNBT getOrCreateBinderData(ItemStack stack) {
        CompoundNBT tag = stack.getOrCreateTag();
        if (!tag.contains("BinderData")) {
            CompoundNBT binderData = new CompoundNBT();
            binderData.put("Cards", new ListNBT());
            binderData.putInt("CurrentPage", 0);
            tag.put("BinderData", binderData);
        }
        return tag.getCompound("BinderData");
    }
    
    public static ListNBT getCards(ItemStack stack) {
        CompoundNBT binderData = getOrCreateBinderData(stack);
        return binderData.getList("Cards", 10); // 10 = CompoundNBT type
    }
    
    public static void setCards(ItemStack stack, ListNBT cards) {
        CompoundNBT binderData = getOrCreateBinderData(stack);
        binderData.put("Cards", cards);
    }
    
    public static int getCurrentPage(ItemStack stack) {
        CompoundNBT binderData = getOrCreateBinderData(stack);
        return binderData.getInt("CurrentPage");
    }
    
    public static void setCurrentPage(ItemStack stack, int page) {
        CompoundNBT binderData = getOrCreateBinderData(stack);
        binderData.putInt("CurrentPage", Math.max(0, Math.min(page, MAX_PAGES - 1)));
    }
    
    @Override
    public ITextComponent getName(ItemStack stack) {
        int cardCount = getCards(stack).size();
        if (cardCount > 0) {
            return new StringTextComponent("Binder (" + cardCount + " cards)");
        }
        return super.getName(stack);
    }
}