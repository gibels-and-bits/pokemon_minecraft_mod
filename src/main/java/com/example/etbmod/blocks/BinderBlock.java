package com.example.etbmod.blocks;

import com.example.etbmod.container.BinderContainer;
import com.example.etbmod.items.BinderItem;
import com.example.etbmod.tileentity.BinderTileEntity;
import net.minecraft.block.Block;
import net.minecraft.block.BlockRenderType;
import net.minecraft.block.BlockState;
import net.minecraft.block.HorizontalBlock;
import net.minecraft.block.SoundType;
import net.minecraft.block.material.Material;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.inventory.container.Container;
import net.minecraft.inventory.container.INamedContainerProvider;
import net.minecraft.item.BlockItemUseContext;
import net.minecraft.item.ItemStack;
import net.minecraft.loot.LootContext;
import net.minecraft.loot.LootParameters;
import net.minecraft.nbt.CompoundNBT;
import net.minecraft.state.DirectionProperty;
import net.minecraft.state.StateContainer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.ActionResultType;
import net.minecraft.util.Direction;
import net.minecraft.util.Hand;
import net.minecraft.util.Mirror;
import net.minecraft.util.Rotation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.BlockRayTraceResult;
import net.minecraft.util.math.shapes.ISelectionContext;
import net.minecraft.util.math.shapes.VoxelShape;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.World;
import net.minecraftforge.fml.network.NetworkHooks;

import javax.annotation.Nullable;
import java.util.Collections;
import java.util.List;

public class BinderBlock extends Block {
    public static final DirectionProperty FACING = HorizontalBlock.FACING;
    
    // Binder shape when placed (like a book laying flat on a table)
    private static final VoxelShape SHAPE_NORTH = Block.box(2, 0, 4, 14, 3, 12);
    private static final VoxelShape SHAPE_SOUTH = Block.box(2, 0, 4, 14, 3, 12);
    private static final VoxelShape SHAPE_WEST = Block.box(4, 0, 2, 12, 3, 14);
    private static final VoxelShape SHAPE_EAST = Block.box(4, 0, 2, 12, 3, 14);
    
    public BinderBlock() {
        super(Properties.of(Material.WOOL)
                .strength(0.5F)
                .sound(SoundType.WOOL)
                .noOcclusion());
        this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.NORTH));
    }
    
    @Override
    public VoxelShape getShape(BlockState state, IBlockReader world, BlockPos pos, ISelectionContext context) {
        Direction facing = state.getValue(FACING);
        switch (facing) {
            case NORTH:
                return SHAPE_NORTH;
            case SOUTH:
                return SHAPE_SOUTH;
            case WEST:
                return SHAPE_WEST;
            case EAST:
                return SHAPE_EAST;
            default:
                return SHAPE_NORTH;
        }
    }
    
    @Override
    public BlockState getStateForPlacement(BlockItemUseContext context) {
        return this.defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }
    
    @Override
    public BlockState rotate(BlockState state, Rotation rotation) {
        return state.setValue(FACING, rotation.rotate(state.getValue(FACING)));
    }
    
    @Override
    public BlockState mirror(BlockState state, Mirror mirror) {
        return state.rotate(mirror.getRotation(state.getValue(FACING)));
    }
    
    @Override
    protected void createBlockStateDefinition(StateContainer.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }
    
    @Override
    public boolean hasTileEntity(BlockState state) {
        return true;
    }
    
    @Nullable
    @Override
    public TileEntity createTileEntity(BlockState state, IBlockReader world) {
        return new BinderTileEntity();
    }
    
    @Override
    public ActionResultType use(BlockState state, World world, BlockPos pos, PlayerEntity player, Hand hand, BlockRayTraceResult hit) {
        if (!world.isClientSide) {
            TileEntity tileEntity = world.getBlockEntity(pos);
            if (tileEntity instanceof BinderTileEntity) {
                BinderTileEntity binderTile = (BinderTileEntity) tileEntity;
                
                NetworkHooks.openGui((ServerPlayerEntity) player, new INamedContainerProvider() {
                    @Override
                    public ITextComponent getDisplayName() {
                        return new StringTextComponent("Binder");
                    }
                    
                    @Override
                    @Nullable
                    public Container createMenu(int windowId, PlayerInventory playerInventory, PlayerEntity player) {
                        ItemStack binderStack = binderTile.getBinderStack();
                        return new BinderContainer(windowId, playerInventory, binderStack);
                    }
                }, buffer -> {
                    buffer.writeItem(binderTile.getBinderStack());
                });
            }
        }
        return ActionResultType.sidedSuccess(world.isClientSide);
    }
    
    @Override
    public void setPlacedBy(World world, BlockPos pos, BlockState state, @Nullable LivingEntity placer, ItemStack stack) {
        super.setPlacedBy(world, pos, state, placer, stack);
        
        TileEntity tileEntity = world.getBlockEntity(pos);
        if (tileEntity instanceof BinderTileEntity && stack.getItem() instanceof BinderItem) {
            BinderTileEntity binderTile = (BinderTileEntity) tileEntity;
            binderTile.setBinderStack(stack.copy());
        }
    }
    
    @Override
    public List<ItemStack> getDrops(BlockState state, LootContext.Builder builder) {
        TileEntity tileEntity = builder.getOptionalParameter(LootParameters.BLOCK_ENTITY);
        if (tileEntity instanceof BinderTileEntity) {
            BinderTileEntity binderTile = (BinderTileEntity) tileEntity;
            ItemStack binderStack = binderTile.getBinderStack();
            if (!binderStack.isEmpty()) {
                return Collections.singletonList(binderStack);
            }
        }
        
        // Return empty binder if no data
        ItemStack emptyBinder = new ItemStack(this.asItem());
        return Collections.singletonList(emptyBinder);
    }
    
    @Override
    public void onRemove(BlockState state, World world, BlockPos pos, BlockState newState, boolean isMoving) {
        if (!state.is(newState.getBlock())) {
            TileEntity tileEntity = world.getBlockEntity(pos);
            if (tileEntity instanceof BinderTileEntity) {
                BinderTileEntity binderTile = (BinderTileEntity) tileEntity;
                ItemStack binderStack = binderTile.getBinderStack();
                if (!binderStack.isEmpty()) {
                    popResource(world, pos, binderStack);
                }
            }
            super.onRemove(state, world, pos, newState, isMoving);
        }
    }
    
    @Override
    public BlockRenderType getRenderShape(BlockState state) {
        return BlockRenderType.MODEL;
    }
}