package com.example.etbmod.crafting;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.items.CardItem;
import com.example.etbmod.items.CardSlabItem;
import com.example.etbmod.items.GradedSlabItem;
import com.example.etbmod.registry.ModBlocks;
import com.example.etbmod.registry.ModItems;
import net.minecraft.inventory.CraftingInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.item.crafting.IRecipeSerializer;
import net.minecraft.item.crafting.SpecialRecipe;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.util.ResourceLocation;
import net.minecraft.world.World;

import java.util.Random;

public class CardGradingRecipe extends SpecialRecipe {
    private static final Random RANDOM = new Random();
    
    public CardGradingRecipe(ResourceLocation idIn) {
        super(idIn);
    }
    
    @Override
    public boolean matches(CraftingInventory inv, World worldIn) {
        ItemStack cardStack = ItemStack.EMPTY;
        ItemStack slabStack = ItemStack.EMPTY;
        
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack stack = inv.getItem(i);
            if (!stack.isEmpty()) {
                if (stack.getItem() instanceof CardItem) {
                    if (!cardStack.isEmpty()) {
                        return false; // Only one card allowed
                    }
                    cardStack = stack;
                } else if (stack.getItem() instanceof CardSlabItem) {
                    if (!slabStack.isEmpty()) {
                        return false; // Only one slab allowed
                    }
                    slabStack = stack;
                } else {
                    return false; // Unknown item
                }
            }
        }
        
        return !cardStack.isEmpty() && !slabStack.isEmpty();
    }
    
    @Override
    public ItemStack assemble(CraftingInventory inv) {
        ItemStack cardStack = ItemStack.EMPTY;
        
        for (int i = 0; i < inv.getContainerSize(); i++) {
            ItemStack stack = inv.getItem(i);
            if (stack.getItem() instanceof CardItem) {
                cardStack = stack;
                break;
            }
        }
        
        if (cardStack.isEmpty() || !cardStack.hasTag()) {
            return ItemStack.EMPTY;
        }
        
        CompoundNBT cardTag = cardStack.getTag();
        
        // Generate PSA grade based on card rarity (rarer cards tend to grade higher)
        int grade = generateGrade(cardTag);
        
        // Create graded slab item
        ItemStack gradedSlab = new ItemStack(ModBlocks.GRADED_SLAB.get());
        CompoundNBT tag = new CompoundNBT();
        
        // Copy card data to graded slab (using correct NBT tag names)
        tag.putInt("grade", grade);
        tag.putString("cardId", cardTag.getString("card_id"));
        tag.putString("cardName", cardTag.getString("card_name"));
        tag.putString("cardNumber", cardTag.getString("number"));
        tag.putString("cardRarity", cardTag.getString("rarity"));
        tag.putString("cardSet", cardTag.getString("set_name"));
        tag.putString("cardImagePath", cardTag.getString("image_path"));
        
        gradedSlab.setTag(tag);
        return gradedSlab;
    }
    
    private int generateGrade(CompoundNBT cardTag) {
        String rarityStr = cardTag.getString("rarity");
        CardRarity rarity = CardRarity.fromString(rarityStr);
        
        // Base probabilities for each grade
        float roll = RANDOM.nextFloat();
        
        // Adjust probabilities based on rarity
        float rarityBonus = 0.0f;
        switch (rarity) {
            case SPECIAL_ILLUSTRATION_RARE:
            case BLACK_WHITE_RARE:
                rarityBonus = 0.4f;
                break;
            case ULTRA_RARE:
            case ILLUSTRATION_RARE:
                rarityBonus = 0.3f;
                break;
            case DOUBLE_RARE:
                rarityBonus = 0.2f;
                break;
            case RARE:
                rarityBonus = 0.1f;
                break;
            case UNCOMMON:
                rarityBonus = 0.05f;
                break;
            default:
                rarityBonus = 0.0f;
        }
        
        // Apply bonus (capped at 0.95 to prevent guaranteed 10s)
        roll = Math.min(roll + rarityBonus, 0.95f);
        
        // Grade distribution
        if (roll >= 0.95f) {
            return 10; // PSA 10 - Gem Mint (5% base chance)
        } else if (roll >= 0.85f) {
            return 9;  // PSA 9 - Mint (10% base chance)
        } else if (roll >= 0.65f) {
            return 8;  // PSA 8 - Near Mint-Mint (20% base chance)
        } else if (roll >= 0.35f) {
            return 7;  // PSA 7 - Near Mint (30% base chance)
        } else {
            return 6;  // PSA 6 - Excellent-Mint (35% base chance)
        }
    }
    
    @Override
    public boolean canCraftInDimensions(int width, int height) {
        return width >= 2 || height >= 2;
    }
    
    @Override
    public IRecipeSerializer<?> getSerializer() {
        return ModItems.CARD_GRADING_RECIPE.get();
    }
}