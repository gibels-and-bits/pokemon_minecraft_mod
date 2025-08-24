package com.example.etbmod.registry;

import com.example.etbmod.ETBMod;
import com.example.etbmod.container.BinderContainer;
import com.example.etbmod.container.GamerTableContainer;
import com.example.etbmod.container.VendingMachineContainer;
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
    
    public static final RegistryObject<ContainerType<BinderContainer>> BINDER_CONTAINER = 
            CONTAINERS.register("binder", 
                () -> IForgeContainerType.create(BinderContainer::new));
    
    public static final RegistryObject<ContainerType<VendingMachineContainer>> VENDING_MACHINE = 
            CONTAINERS.register("vending_machine", 
                () -> IForgeContainerType.create(VendingMachineContainer::new));
}