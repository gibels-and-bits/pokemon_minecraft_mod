package com.example.etbmod;

import com.example.etbmod.client.renderer.GradedSlabRenderer;
import com.example.etbmod.client.screen.GamerTableScreen;
import com.example.etbmod.registry.ModBlocks;
import com.example.etbmod.registry.ModContainers;
import com.example.etbmod.registry.ModItems;
import com.example.etbmod.registry.ModTileEntities;
import net.minecraft.block.Blocks;
import net.minecraft.client.gui.ScreenManager;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.RenderTypeLookup;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@Mod(ETBMod.MOD_ID)
public class ETBMod {
    public static final String MOD_ID = "etbmod";
    public static final Logger LOGGER = LogManager.getLogger();

    public static final ItemGroup ITEM_GROUP = new ItemGroup(MOD_ID) {
        @Override
        public ItemStack makeIcon() {
            return new ItemStack(ModBlocks.ETB_BLOCKS.isEmpty() ? 
                Blocks.CHEST : 
                ModBlocks.ETB_BLOCKS.get(0).get());
        }
    };

    public ETBMod() {
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        
        ModBlocks.BLOCKS.register(modEventBus);
        ModItems.ITEMS.register(modEventBus);
        ModItems.initETBItems(); // Initialize ETB items after blocks are registered
        ModItems.RECIPE_SERIALIZERS.register(modEventBus);
        ModTileEntities.TILE_ENTITIES.register(modEventBus);
        ModContainers.CONTAINERS.register(modEventBus);
        
        modEventBus.addListener(this::setup);
        modEventBus.addListener(this::doClientStuff);
        
        MinecraftForge.EVENT_BUS.register(this);
    }

    private void setup(final FMLCommonSetupEvent event) {
        com.example.etbmod.network.ModNetworking.register();
        LOGGER.info("ETB Mod Setup Complete!");
    }

    private void doClientStuff(final FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ScreenManager.register(ModContainers.GAMER_TABLE.get(), GamerTableScreen::new);
            net.minecraftforge.fml.client.registry.ClientRegistry.bindTileEntityRenderer(
                    ModTileEntities.GRADED_SLAB.get(), GradedSlabRenderer::new);
            
            // Set the graded slab block to use translucent rendering
            RenderTypeLookup.setRenderLayer(ModBlocks.GRADED_SLAB.get(), RenderType.translucent());
        });
        LOGGER.info("ETB Mod Client Setup Complete!");
    }
}