package com.example.etbmod.items;

import com.example.etbmod.blocks.GradedSlabBlock;
import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import net.minecraft.block.Block;
import net.minecraft.client.util.ITooltipFlag;
import net.minecraft.item.BlockItem;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemUseContext;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.util.ActionResultType;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.util.text.TextFormatting;
import net.minecraft.world.World;

import javax.annotation.Nullable;
import java.util.List;

public class GradedSlabItem extends BlockItem {
    
    public GradedSlabItem(Block block) {
        super(block, new Properties()
                .tab(ItemGroup.TAB_DECORATIONS)
                .stacksTo(1));
    }
    
    @Override
    public ActionResultType useOn(ItemUseContext context) {
        ActionResultType result = super.useOn(context);
        
        // Transfer NBT data to the placed block
        if (result == ActionResultType.SUCCESS || result == ActionResultType.CONSUME) {
            ItemStack stack = context.getItemInHand();
            if (stack.hasTag()) {
                // The block will read the NBT data from the item
                // This happens automatically through the BlockItem placement
            }
        }
        
        return result;
    }
    
    @Override
    public void appendHoverText(ItemStack stack, @Nullable World worldIn, List<ITextComponent> tooltip, ITooltipFlag flagIn) {
        if (stack.hasTag()) {
            CompoundNBT tag = stack.getTag();
            
            // Show PSA grade
            if (tag.contains("grade")) {
                int grade = tag.getInt("grade");
                TextFormatting gradeColor = getGradeColor(grade);
                tooltip.add(new StringTextComponent("PSA " + grade)
                        .withStyle(gradeColor, TextFormatting.BOLD));
            }
            
            // Show card name
            if (tag.contains("cardName")) {
                String cardName = tag.getString("cardName");
                tooltip.add(new StringTextComponent(cardName)
                        .withStyle(TextFormatting.WHITE));
            }
            
            // Show card set and number
            if (tag.contains("cardSet") && tag.contains("cardNumber")) {
                String cardSet = tag.getString("cardSet");
                String cardNumber = tag.getString("cardNumber");
                tooltip.add(new StringTextComponent(cardSet + " #" + cardNumber)
                        .withStyle(TextFormatting.GRAY));
            }
            
            // Show rarity
            if (tag.contains("cardRarity")) {
                String rarityStr = tag.getString("cardRarity");
                CardRarity rarity = CardRarity.fromString(rarityStr);
                TextFormatting rarityColor = getRarityColor(rarity);
                tooltip.add(new StringTextComponent(rarity.getDisplayName())
                        .withStyle(rarityColor, TextFormatting.ITALIC));
            }
            
            tooltip.add(new StringTextComponent("")); // Empty line
            tooltip.add(new StringTextComponent("Place to display")
                    .withStyle(TextFormatting.DARK_GRAY, TextFormatting.ITALIC));
        }
        
        super.appendHoverText(stack, worldIn, tooltip, flagIn);
    }
    
    private TextFormatting getGradeColor(int grade) {
        switch (grade) {
            case 10: return TextFormatting.GOLD;
            case 9: return TextFormatting.YELLOW;
            case 8: return TextFormatting.GREEN;
            case 7: return TextFormatting.AQUA;
            default: return TextFormatting.GRAY;
        }
    }
    
    private TextFormatting getRarityColor(CardRarity rarity) {
        switch (rarity) {
            case COMMON: return TextFormatting.GRAY;
            case UNCOMMON: return TextFormatting.GREEN;
            case RARE: return TextFormatting.BLUE;
            case DOUBLE_RARE: return TextFormatting.GOLD;
            case ULTRA_RARE: return TextFormatting.LIGHT_PURPLE;
            case ILLUSTRATION_RARE: return TextFormatting.AQUA;
            case SPECIAL_ILLUSTRATION_RARE: return TextFormatting.RED;
            case BLACK_WHITE_RARE: return TextFormatting.WHITE;
            default: return TextFormatting.WHITE;
        }
    }
    
    @Override
    public ITextComponent getName(ItemStack stack) {
        if (stack.hasTag()) {
            CompoundNBT tag = stack.getTag();
            if (tag.contains("grade") && tag.contains("cardName")) {
                int grade = tag.getInt("grade");
                String cardName = tag.getString("cardName");
                return new StringTextComponent("PSA " + grade + " " + cardName);
            }
        }
        return super.getName(stack);
    }
    
    // Static method to create a graded slab item from a card
    public static ItemStack createGradedSlab(Card card, int grade, Block gradedSlabBlock) {
        ItemStack stack = new ItemStack(gradedSlabBlock.asItem());
        CompoundNBT tag = new CompoundNBT();
        
        tag.putInt("grade", grade);
        tag.putString("cardId", card.getId());
        tag.putString("cardName", card.getName());
        tag.putString("cardNumber", card.getNumber());
        tag.putString("cardRarity", card.getRarity().toString());
        tag.putString("cardSet", card.getSetName());
        tag.putString("cardImagePath", card.getImagePath());
        
        stack.setTag(tag);
        return stack;
    }
}