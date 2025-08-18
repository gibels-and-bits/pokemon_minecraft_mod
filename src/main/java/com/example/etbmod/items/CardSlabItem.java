package com.example.etbmod.items;

import net.minecraft.client.util.ITooltipFlag;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.util.text.TextFormatting;
import net.minecraft.world.World;

import javax.annotation.Nullable;
import java.util.List;

public class CardSlabItem extends Item {
    public CardSlabItem() {
        super(new Item.Properties()
                .tab(ItemGroup.TAB_MISC)
                .stacksTo(64));
    }
    
    @Override
    public void appendHoverText(ItemStack stack, @Nullable World worldIn, List<ITextComponent> tooltip, ITooltipFlag flagIn) {
        tooltip.add(new StringTextComponent("Empty Card Slab").withStyle(TextFormatting.GRAY));
        tooltip.add(new StringTextComponent("Combine with a card to grade it").withStyle(TextFormatting.DARK_GRAY, TextFormatting.ITALIC));
        super.appendHoverText(stack, worldIn, tooltip, flagIn);
    }
}