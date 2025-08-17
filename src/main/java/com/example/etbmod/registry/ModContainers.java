package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.container.GamerTableContainer;
import net.minecraft.inventory.container.ContainerType;
import net.minecraftforge.common.extensions.IForgeContainerType;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

public class ModContainers {
    public static final DeferredRegister<ContainerType<?>> CONTAINERS = 
            DeferredRegister.create(ForgeRegistries.CONTAINERS, ETBMod.MOD_ID);
    
    public static final RegistryObject<ContainerType<GamerTableContainer>> GAMER_TABLE = 
            CONTAINERS.register("gamer_table", 
                () -> IForgeContainerType.create(
                    (windowId, inv, data) -> new GamerTableContainer(windowId, inv)));
}