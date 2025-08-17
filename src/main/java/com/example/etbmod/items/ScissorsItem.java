package com.example.etbmod.items;

import net.minecraft.item.Item;
import com.example.etbmod.ETBMod;

public class ScissorsItem extends Item {
    
    public ScissorsItem() {
        super(new Item.Properties()
                .tab(ETBMod.ITEM_GROUP)
                .durability(238));
    }
}