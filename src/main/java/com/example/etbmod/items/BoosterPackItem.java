package com.example.etbmod.items;

import net.minecraft.client.util.ITooltipFlag;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Rarity;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TextFormatting;
import net.minecraft.util.text.TranslationTextComponent;
import net.minecraft.world.World;
import com.example.etbmod.ETBMod;

import javax.annotation.Nullable;
import java.util.List;

public class BoosterPackItem extends Item {
    private final String setName;
    private static final int CARDS_PER_PACK = 10;
    
    public BoosterPackItem(String setName) {
        super(new Item.Properties()
                .tab(ETBMod.ITEM_GROUP)
                .stacksTo(64)
                .rarity(Rarity.UNCOMMON));
        this.setName = setName;
    }
    
    @Override
    public void appendHoverText(ItemStack stack, @Nullable World world, List<ITextComponent> tooltip, ITooltipFlag flag) {
        tooltip.add(new TranslationTextComponent("tooltip.etbmod.booster_pack")
                .withStyle(TextFormatting.GRAY));
        tooltip.add(new TranslationTextComponent("tooltip.etbmod.card_count", CARDS_PER_PACK)
                .withStyle(TextFormatting.GOLD));
        
        if (flag.isAdvanced()) {
            tooltip.add(new TranslationTextComponent("tooltip.etbmod.set_name", getFormattedSetName())
                    .withStyle(TextFormatting.DARK_GRAY));
        }
    }
    
    public String getSetName() {
        return setName;
    }
    
    private String getFormattedSetName() {
        return setName.replace("_", " ")
                .substring(0, 1).toUpperCase() + 
                setName.replace("_", " ").substring(1);
    }
}