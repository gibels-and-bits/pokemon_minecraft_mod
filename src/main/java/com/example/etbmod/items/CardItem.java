package com.example.etbmod.items;

import com.example.etbmod.cards.Card;
import com.example.etbmod.cards.CardRarity;
import com.example.etbmod.registry.ModItems;
import net.minecraft.client.util.ITooltipFlag;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Rarity;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.util.text.TextFormatting;
import net.minecraft.world.World;

import javax.annotation.Nullable;
import java.util.List;

public class CardItem extends Item {
    
    public CardItem() {
        super(new Item.Properties()
                .tab(ItemGroup.TAB_MISC)
                .stacksTo(1)
                .rarity(Rarity.COMMON));
    }
    
    @Override
    public ActionResult<ItemStack> use(World world, PlayerEntity player, Hand hand) {
        ItemStack stack = player.getItemInHand(hand);
        
        if (world.isClientSide) {
            // Open card view screen directly on client
            Card card = getCardFromStack(stack);
            if (card != null) {
                openCardViewScreen(card);
            }
        }
        
        return ActionResult.sidedSuccess(stack, world.isClientSide);
    }
    
    @net.minecraftforge.api.distmarker.OnlyIn(net.minecraftforge.api.distmarker.Dist.CLIENT)
    private void openCardViewScreen(Card card) {
        net.minecraft.client.Minecraft.getInstance().setScreen(
            new com.example.etbmod.client.screen.CardViewScreen(card)
        );
    }
    
    @Override
    public void appendHoverText(ItemStack stack, @Nullable World world, List<ITextComponent> tooltip, ITooltipFlag flag) {
        CompoundNBT tag = stack.getOrCreateTag();
        
        if (tag.contains("card_name")) {
            String cardName = tag.getString("card_name");
            String setName = tag.getString("set_name");
            String number = tag.getString("number");
            String rarityStr = tag.getString("rarity");
            
            // Card name with rarity color
            TextFormatting color = getColorForRarity(rarityStr);
            tooltip.add(new StringTextComponent(cardName).withStyle(color));
            
            // Set and number
            tooltip.add(new StringTextComponent("§7" + setName + " #" + number));
            
            // Rarity
            tooltip.add(new StringTextComponent("§6Rarity: " + rarityStr));
        }
        
        super.appendHoverText(stack, world, tooltip, flag);
    }
    
    @Override
    public ITextComponent getName(ItemStack stack) {
        CompoundNBT tag = stack.getOrCreateTag();
        if (tag.contains("card_name")) {
            String cardName = tag.getString("card_name");
            String rarityStr = tag.getString("rarity");
            TextFormatting color = getColorForRarity(rarityStr);
            return new StringTextComponent(cardName).withStyle(color);
        }
        return super.getName(stack);
    }
    
    @Override
    public boolean isFoil(ItemStack stack) {
        // No enchantment glow for cards
        return false;
    }
    
    @Override
    public Rarity getRarity(ItemStack stack) {
        CompoundNBT tag = stack.getOrCreateTag();
        if (tag.contains("rarity")) {
            String rarity = tag.getString("rarity");
            if (rarity.contains("Ultra") || rarity.contains("Special")) {
                return Rarity.EPIC;
            } else if (rarity.contains("Double") || rarity.contains("Illustration")) {
                return Rarity.RARE;
            } else if (rarity.equals("Rare")) {
                return Rarity.UNCOMMON;
            }
        }
        return Rarity.COMMON;
    }
    
    private TextFormatting getColorForRarity(String rarity) {
        if (rarity.contains("Special") || rarity.contains("Black")) {
            return TextFormatting.LIGHT_PURPLE;
        } else if (rarity.contains("Ultra")) {
            return TextFormatting.GOLD;
        } else if (rarity.contains("Illustration")) {
            return TextFormatting.AQUA;
        } else if (rarity.contains("Double")) {
            return TextFormatting.YELLOW;
        } else if (rarity.equals("Rare")) {
            return TextFormatting.BLUE;
        } else if (rarity.equals("Uncommon")) {
            return TextFormatting.GREEN;
        }
        return TextFormatting.WHITE;
    }
    
    public static ItemStack createCardItem(Card card) {
        ItemStack stack = new ItemStack(ModItems.POKEMON_CARD.get());
        CompoundNBT tag = stack.getOrCreateTag();
        
        tag.putString("card_id", card.getId());
        tag.putString("card_name", card.getName());
        tag.putString("set_name", card.getSetName());
        tag.putString("number", card.getNumber());
        tag.putString("rarity", card.getRarity().getDisplayName());
        tag.putString("image_path", card.getImagePath());
        
        return stack;
    }
    
    public static Card getCardFromStack(ItemStack stack) {
        if (!(stack.getItem() instanceof CardItem)) {
            return null;
        }
        
        CompoundNBT tag = stack.getOrCreateTag();
        if (!tag.contains("card_id")) {
            return null;
        }
        
        String id = tag.getString("card_id");
        String name = tag.getString("card_name");
        String number = tag.getString("number");
        String rarityStr = tag.getString("rarity");
        String setName = tag.getString("set_name");
        String imagePath = tag.getString("image_path");
        
        CardRarity rarity = CardRarity.fromString(rarityStr);
        
        return new Card(id, name, number, rarity, setName, imagePath);
    }
}