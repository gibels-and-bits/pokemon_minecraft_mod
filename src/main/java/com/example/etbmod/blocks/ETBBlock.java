package com.example.etbmod.blocks;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.HorizontalBlock;
import net.minecraft.block.SoundType;
import net.minecraft.block.material.Material;
import net.minecraft.entity.item.ItemEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.BlockItemUseContext;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.item.Item;
import net.minecraft.loot.LootContext;
import net.minecraft.loot.LootParameters;
import net.minecraft.state.DirectionProperty;
import net.minecraft.state.StateContainer;
import net.minecraft.util.*;
import net.minecraft.util.SoundCategory;
import net.minecraft.util.SoundEvents;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.BlockRayTraceResult;
import net.minecraft.util.math.shapes.ISelectionContext;
import net.minecraft.util.math.shapes.VoxelShape;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.World;
import net.minecraftforge.common.ToolType;
import com.example.etbmod.config.ETBConfig;
import com.example.etbmod.registry.ModItems;

import java.util.Collections;
import java.util.List;
import java.util.Random;

public class ETBBlock extends Block {
    private final String variant;
    
    public static final DirectionProperty FACING = HorizontalBlock.FACING;
    private static final String VARIANT_PREFIX = "etb_";
    
    // ETB dimensions: 6.5" x 3.43" x 7.36" (width x depth x height)
    // Scaled to Minecraft: 13x7x12 pixels
    private static final VoxelShape SHAPE_NS = Block.box(1.5D, 0.0D, 4.5D, 14.5D, 12.0D, 11.5D);
    private static final VoxelShape SHAPE_EW = Block.box(4.5D, 0.0D, 1.5D, 11.5D, 12.0D, 14.5D);
    
    public ETBBlock(String variant) {
        super(Properties.of(Material.WOOD)  // Back to WOOD material
                .strength(0.0F, 0.0F)  // Instant break (like tall grass)
                .sound(SoundType.WOOD)
                .noOcclusion()
                .harvestLevel(0)  // Can be harvested with any tool or hand
                .lightLevel((state) -> 0));
        this.variant = variant;
        this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.NORTH));
    }
    
    @Override
    public VoxelShape getShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        Direction direction = state.getValue(FACING);
        return (direction == Direction.NORTH || direction == Direction.SOUTH) ? SHAPE_NS : SHAPE_EW;
    }
    
    @Override
    public VoxelShape getCollisionShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        return getShape(state, worldIn, pos, context);
    }
    
    @Override
    public BlockState getStateForPlacement(BlockItemUseContext context) {
        return this.defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }
    
    @Override
    public BlockState rotate(BlockState state, Rotation rot) {
        return state.setValue(FACING, rot.rotate(state.getValue(FACING)));
    }
    
    @Override
    public BlockState mirror(BlockState state, Mirror mirrorIn) {
        return state.rotate(mirrorIn.getRotation(state.getValue(FACING)));
    }
    
    @Override
    protected void createBlockStateDefinition(StateContainer.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }
    
    @Override
    public boolean useShapeForLightOcclusion(BlockState state) {
        return true;
    }
    
    // Override the use method to handle scissors interaction
    @Override
    public ActionResultType use(BlockState state, World worldIn, BlockPos pos, PlayerEntity player, 
                                Hand hand, BlockRayTraceResult hit) {
        ItemStack heldItem = player.getItemInHand(hand);
        
        // Check if player is holding scissors
        if (heldItem.getItem() == ModItems.SCISSORS.get()) {
            if (!worldIn.isClientSide) {
                // Get the appropriate booster pack item based on ETB variant
                String variantName = variant.startsWith(VARIANT_PREFIX) ? 
                    variant.substring(VARIANT_PREFIX.length()) : variant;
                Item boosterPack = ModItems.BOOSTER_PACKS.containsKey(variantName) ?
                    ModItems.BOOSTER_PACKS.get(variantName).get() : Items.PAPER;
                
                // Spawn booster packs with optimized random distribution
                Random random = worldIn.getRandom();
                for (int i = 0; i < ETBConfig.BOOSTER_PACK_COUNT; i++) {
                    double offsetX = (random.nextDouble() - 0.5) * 0.5;
                    double offsetY = random.nextDouble() * 0.3 + 0.1;
                    double offsetZ = (random.nextDouble() - 0.5) * 0.5;
                    
                    ItemEntity itemEntity = new ItemEntity(worldIn,
                        pos.getX() + 0.5 + offsetX,
                        pos.getY() + 0.5 + offsetY,
                        pos.getZ() + 0.5 + offsetZ,
                        new ItemStack(boosterPack, 1));
                    
                    itemEntity.setDeltaMovement(
                        offsetX * 0.1,
                        0.1 + offsetY * 0.05,
                        offsetZ * 0.1
                    );
                    
                    worldIn.addFreshEntity(itemEntity);
                }
                
                // Damage the scissors
                heldItem.hurtAndBreak(1, player, (p) -> {
                    p.broadcastBreakEvent(hand);
                });
                
                // Play opening sound effect
                worldIn.playSound(null, pos, SoundEvents.SHEEP_SHEAR, SoundCategory.BLOCKS, 1.0F, 1.0F);
                worldIn.playSound(null, pos, SoundEvents.ITEM_PICKUP, SoundCategory.BLOCKS, 0.5F, 1.2F);
                
                // Remove the ETB block (already opened)
                worldIn.destroyBlock(pos, false);
            }
            
            return ActionResultType.sidedSuccess(worldIn.isClientSide);
        }
        
        return ActionResultType.PASS;
    }
    
    // Override to ensure block drops when broken
    @Override
    public void playerDestroy(World worldIn, PlayerEntity player, BlockPos pos, BlockState state, net.minecraft.tileentity.TileEntity te, ItemStack stack) {
        // Always drop the block item when broken unless in creative mode
        if (!player.isCreative()) {
            popResource(worldIn, pos, new ItemStack(this));
        }
        super.playerDestroy(worldIn, player, pos, state, te, stack);
    }
    
    // Metadata methods for factory pattern - can be overridden
    public String getSetCode() {
        return variant;
    }
    
    public String getDisplayName() {
        return variant.replace("etb_", "").replace("_", " ");
    }
    
    public String getVariant() {
        return variant;
    }
}