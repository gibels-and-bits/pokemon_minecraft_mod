package com.example.etbmod.blocks;

import com.example.etbmod.tileentities.GradedSlabTileEntity;
import net.minecraft.block.*;
import net.minecraft.block.material.Material;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.BlockItemUseContext;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.state.DirectionProperty;
import net.minecraft.state.StateContainer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.*;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.BlockRayTraceResult;
import net.minecraft.util.math.shapes.ISelectionContext;
import net.minecraft.util.math.shapes.VoxelShape;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.World;
import net.minecraftforge.common.ToolType;

import javax.annotation.Nullable;

public class GradedSlabBlock extends Block implements ITileEntityProvider {
    public static final DirectionProperty FACING = HorizontalBlock.FACING;
    
    // Thin slab shape - like a picture frame on the wall
    private static final VoxelShape SHAPE_NORTH = Block.box(0.0D, 0.0D, 15.0D, 16.0D, 16.0D, 16.0D);
    private static final VoxelShape SHAPE_SOUTH = Block.box(0.0D, 0.0D, 0.0D, 16.0D, 16.0D, 1.0D);
    private static final VoxelShape SHAPE_WEST = Block.box(15.0D, 0.0D, 0.0D, 16.0D, 16.0D, 16.0D);
    private static final VoxelShape SHAPE_EAST = Block.box(0.0D, 0.0D, 0.0D, 1.0D, 16.0D, 16.0D);
    
    public GradedSlabBlock() {
        super(Properties.of(Material.GLASS)
                .strength(0.3F)
                .sound(SoundType.GLASS)
                .noOcclusion()
                .harvestTool(ToolType.PICKAXE)
                .harvestLevel(0));
        this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.NORTH));
    }
    
    @Override
    public VoxelShape getShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        Direction direction = state.getValue(FACING);
        switch (direction) {
            case NORTH:
                return SHAPE_NORTH;
            case SOUTH:
                return SHAPE_SOUTH;
            case WEST:
                return SHAPE_WEST;
            case EAST:
            default:
                return SHAPE_EAST;
        }
    }
    
    @Override
    public BlockState getStateForPlacement(BlockItemUseContext context) {
        // Place facing the player
        return this.defaultBlockState().setValue(FACING, context.getHorizontalDirection());
    }
    
    @Override
    public void setPlacedBy(World worldIn, BlockPos pos, BlockState state, @Nullable LivingEntity placer, ItemStack stack) {
        super.setPlacedBy(worldIn, pos, state, placer, stack);
        
        // Transfer NBT data from item to tile entity
        if (stack.hasTag()) {
            TileEntity tileEntity = worldIn.getBlockEntity(pos);
            if (tileEntity instanceof GradedSlabTileEntity) {
                GradedSlabTileEntity gradedSlab = (GradedSlabTileEntity) tileEntity;
                CompoundNBT tag = stack.getTag();
                
                gradedSlab.setCardData(
                    tag.getInt("grade"),
                    tag.getString("cardId"),
                    tag.getString("cardName"),
                    tag.getString("cardNumber"),
                    tag.getString("cardRarity"),
                    tag.getString("cardSet"),
                    tag.getString("cardImagePath")
                );
            }
        }
    }
    
    @Override
    public void playerWillDestroy(World worldIn, BlockPos pos, BlockState state, PlayerEntity player) {
        if (!worldIn.isClientSide && !player.isCreative()) {
            TileEntity tileEntity = worldIn.getBlockEntity(pos);
            if (tileEntity instanceof GradedSlabTileEntity) {
                GradedSlabTileEntity gradedSlab = (GradedSlabTileEntity) tileEntity;
                ItemStack itemStack = new ItemStack(this);
                
                // Transfer data from tile entity to item
                CompoundNBT tag = new CompoundNBT();
                tag.putInt("grade", gradedSlab.getGrade());
                tag.putString("cardId", gradedSlab.getCardId());
                tag.putString("cardName", gradedSlab.getCardName());
                tag.putString("cardNumber", gradedSlab.getCardNumber());
                tag.putString("cardRarity", gradedSlab.getCardRarity());
                tag.putString("cardSet", gradedSlab.getCardSet());
                tag.putString("cardImagePath", gradedSlab.getCardImagePath());
                itemStack.setTag(tag);
                
                // Drop the item
                popResource(worldIn, pos, itemStack);
            }
        }
        super.playerWillDestroy(worldIn, pos, state, player);
    }
    
    @Override
    public ActionResultType use(BlockState state, World worldIn, BlockPos pos, PlayerEntity player, 
                                Hand hand, BlockRayTraceResult hit) {
        if (!worldIn.isClientSide) {
            TileEntity tileEntity = worldIn.getBlockEntity(pos);
            if (tileEntity instanceof GradedSlabTileEntity) {
                GradedSlabTileEntity gradedSlab = (GradedSlabTileEntity) tileEntity;
                
                // Show card info in chat
                player.displayClientMessage(
                    new StringTextComponent("§6PSA " + gradedSlab.getGrade() + " §f" + gradedSlab.getCardName()), 
                    true
                );
            }
        }
        return ActionResultType.sidedSuccess(worldIn.isClientSide);
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
    public BlockRenderType getRenderShape(BlockState state) {
        return BlockRenderType.MODEL;
    }
    
    @Nullable
    @Override
    public TileEntity newBlockEntity(IBlockReader worldIn) {
        return new GradedSlabTileEntity();
    }
    
    @Override
    public boolean hasTileEntity(BlockState state) {
        return true;
    }
}