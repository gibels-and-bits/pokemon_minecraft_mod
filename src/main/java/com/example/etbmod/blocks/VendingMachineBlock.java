package com.example.etbmod.blocks;

import com.example.etbmod.tileentity.VendingMachineTileEntity;
import net.minecraft.block.*;
import net.minecraft.block.material.Material;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.item.BlockItemUseContext;
import net.minecraft.item.ItemStack;
import net.minecraft.state.BooleanProperty;
import net.minecraft.state.DirectionProperty;
import net.minecraft.state.EnumProperty;
import net.minecraft.state.StateContainer;
import net.minecraft.state.properties.BlockStateProperties;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.*;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.BlockRayTraceResult;
import net.minecraft.util.math.shapes.ISelectionContext;
import net.minecraft.util.math.shapes.VoxelShape;
import net.minecraft.util.math.shapes.VoxelShapes;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.IWorld;
import net.minecraft.world.World;
import net.minecraftforge.common.ToolType;
import net.minecraftforge.fml.network.NetworkHooks;

import javax.annotation.Nullable;

public class VendingMachineBlock extends ContainerBlock {
    
    public static final DirectionProperty FACING = BlockStateProperties.HORIZONTAL_FACING;
    public static final BooleanProperty MASTER = BooleanProperty.create("master");
    
    // Different part types for the 2x3x2 structure
    public enum MachinePart implements IStringSerializable {
        BOTTOM_LEFT("bottom_left"),
        BOTTOM_RIGHT("bottom_right"),
        MIDDLE_LEFT("middle_left"),
        MIDDLE_RIGHT("middle_right"),
        TOP_LEFT("top_left"),
        TOP_RIGHT("top_right");
        
        private final String name;
        
        MachinePart(String name) {
            this.name = name;
        }
        
        @Override
        public String getSerializedName() {
            return this.name;
        }
    }
    
    public static final EnumProperty<MachinePart> PART = EnumProperty.create("part", MachinePart.class);
    
    public VendingMachineBlock() {
        super(AbstractBlock.Properties.of(Material.METAL)
                .strength(4.0f, 6.0f)
                .sound(SoundType.METAL)
                .requiresCorrectToolForDrops()
                .harvestTool(ToolType.PICKAXE)
                .harvestLevel(1)
                .noOcclusion());
        
        this.registerDefaultState(this.stateDefinition.any()
                .setValue(FACING, Direction.NORTH)
                .setValue(MASTER, true)
                .setValue(PART, MachinePart.BOTTOM_LEFT));
    }
    
    @Override
    public VoxelShape getShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        // Full block shape for all parts
        return VoxelShapes.block();
    }
    
    @Override
    public BlockState getStateForPlacement(BlockItemUseContext context) {
        World world = context.getLevel();
        BlockPos pos = context.getClickedPos();
        Direction facing = context.getHorizontalDirection().getOpposite();
        
        // Check if we have space for 2x2x2 structure
        if (hasSpaceForMachine(world, pos, facing)) {
            // Place all blocks of the structure
            placeMachineStructure(world, pos, facing);
            return this.defaultBlockState()
                    .setValue(FACING, facing)
                    .setValue(MASTER, true)
                    .setValue(PART, MachinePart.BOTTOM_LEFT);
        }
        
        return null; // Cancel placement if no space
    }
    
    private boolean hasSpaceForMachine(World world, BlockPos pos, Direction facing) {
        // Check all 12 positions (2x3x2)
        for (int x = 0; x < 2; x++) {
            for (int y = 0; y < 3; y++) {
                for (int z = 0; z < 2; z++) {
                    BlockPos checkPos = getRelativePos(pos, x, y, z, facing);
                    if (!world.getBlockState(checkPos).getMaterial().isReplaceable()) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
    
    private void placeMachineStructure(World world, BlockPos masterPos, Direction facing) {
        // Place bottom layer
        world.setBlock(masterPos, this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, true)
                .setValue(PART, MachinePart.BOTTOM_LEFT), 3);
        
        world.setBlock(getRelativePos(masterPos, 1, 0, 0, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.BOTTOM_RIGHT), 3);
        
        world.setBlock(getRelativePos(masterPos, 0, 0, 1, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.BOTTOM_LEFT), 3);
        
        world.setBlock(getRelativePos(masterPos, 1, 0, 1, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.BOTTOM_RIGHT), 3);
        
        // Place middle layer
        world.setBlock(getRelativePos(masterPos, 0, 1, 0, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.MIDDLE_LEFT), 3);
        
        world.setBlock(getRelativePos(masterPos, 1, 1, 0, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.MIDDLE_RIGHT), 3);
        
        world.setBlock(getRelativePos(masterPos, 0, 1, 1, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.MIDDLE_LEFT), 3);
        
        world.setBlock(getRelativePos(masterPos, 1, 1, 1, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.MIDDLE_RIGHT), 3);
        
        // Place top layer
        world.setBlock(getRelativePos(masterPos, 0, 2, 0, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.TOP_LEFT), 3);
        
        world.setBlock(getRelativePos(masterPos, 1, 2, 0, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.TOP_RIGHT), 3);
        
        world.setBlock(getRelativePos(masterPos, 0, 2, 1, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.TOP_LEFT), 3);
        
        world.setBlock(getRelativePos(masterPos, 1, 2, 1, facing), this.defaultBlockState()
                .setValue(FACING, facing)
                .setValue(MASTER, false)
                .setValue(PART, MachinePart.TOP_RIGHT), 3);
    }
    
    private BlockPos getRelativePos(BlockPos pos, int x, int y, int z, Direction facing) {
        switch (facing) {
            case NORTH:
                return pos.offset(x, y, z);
            case SOUTH:
                return pos.offset(-x, y, -z);
            case EAST:
                return pos.offset(-z, y, x);
            case WEST:
                return pos.offset(z, y, -x);
            default:
                return pos.offset(x, y, z);
        }
    }
    
    private BlockPos getMasterPos(World world, BlockPos pos, BlockState state) {
        if (state.getValue(MASTER)) {
            return pos;
        }
        
        Direction facing = state.getValue(FACING);
        MachinePart part = state.getValue(PART);
        
        // Find master block based on current part
        for (int x = -1; x <= 1; x++) {
            for (int y = -1; y <= 1; y++) {
                for (int z = -1; z <= 1; z++) {
                    BlockPos checkPos = getRelativePos(pos, x, y, z, facing);
                    BlockState checkState = world.getBlockState(checkPos);
                    if (checkState.getBlock() == this && checkState.getValue(MASTER)) {
                        return checkPos;
                    }
                }
            }
        }
        
        return pos;
    }
    
    @Override
    public void setPlacedBy(World world, BlockPos pos, BlockState state, @Nullable LivingEntity placer, ItemStack stack) {
        super.setPlacedBy(world, pos, state, placer, stack);
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
        builder.add(FACING, MASTER, PART);
    }
    
    @Override
    public ActionResultType use(BlockState state, World worldIn, BlockPos pos, PlayerEntity player, 
                                Hand handIn, BlockRayTraceResult hit) {
        if (!worldIn.isClientSide) {
            BlockPos masterPos = getMasterPos(worldIn, pos, state);
            TileEntity tileEntity = worldIn.getBlockEntity(masterPos);
            if (tileEntity instanceof VendingMachineTileEntity) {
                NetworkHooks.openGui((ServerPlayerEntity) player, (VendingMachineTileEntity) tileEntity, masterPos);
            }
        }
        return ActionResultType.sidedSuccess(worldIn.isClientSide);
    }
    
    @Override
    public void onRemove(BlockState state, World worldIn, BlockPos pos, BlockState newState, boolean isMoving) {
        if (!state.is(newState.getBlock())) {
            // Only drop items from master block
            if (state.getValue(MASTER)) {
                TileEntity tileentity = worldIn.getBlockEntity(pos);
                if (tileentity instanceof VendingMachineTileEntity) {
                    ((VendingMachineTileEntity) tileentity).dropContents(worldIn, pos);
                }
            }
            
            // Remove all parts of the structure
            if (!isMoving) {
                breakMachineStructure(worldIn, pos, state);
            }
            
            super.onRemove(state, worldIn, pos, newState, isMoving);
        }
    }
    
    private void breakMachineStructure(World world, BlockPos pos, BlockState state) {
        Direction facing = state.getValue(FACING);
        BlockPos masterPos = getMasterPos(world, pos, state);
        
        // Remove all 12 blocks
        for (int x = 0; x < 2; x++) {
            for (int y = 0; y < 3; y++) {
                for (int z = 0; z < 2; z++) {
                    BlockPos removePos = getRelativePos(masterPos, x, y, z, facing);
                    if (!removePos.equals(pos)) { // Don't remove the block that's already being removed
                        BlockState removeState = world.getBlockState(removePos);
                        if (removeState.getBlock() == this) {
                            world.setBlock(removePos, Blocks.AIR.defaultBlockState(), 35);
                        }
                    }
                }
            }
        }
    }
    
    @Nullable
    @Override
    public TileEntity newBlockEntity(IBlockReader worldIn) {
        // Only create tile entity for master block
        return new VendingMachineTileEntity();
    }
    
    @Override
    public boolean hasTileEntity(BlockState state) {
        // Only master block has tile entity
        return state.getValue(MASTER);
    }
    
    @Override
    public BlockRenderType getRenderShape(BlockState state) {
        // Only render the master block, others are invisible
        return state.getValue(MASTER) ? BlockRenderType.MODEL : BlockRenderType.INVISIBLE;
    }
    
    @Override
    public BlockState updateShape(BlockState state, Direction facing, BlockState facingState, IWorld world, 
                                  BlockPos currentPos, BlockPos facingPos) {
        // Check if structure is still intact
        if (state.getValue(MASTER)) {
            for (int x = 0; x < 2; x++) {
                for (int y = 0; y < 3; y++) {
                    for (int z = 0; z < 2; z++) {
                        if (x == 0 && y == 0 && z == 0) continue; // Skip master block
                        BlockPos checkPos = getRelativePos(currentPos, x, y, z, state.getValue(FACING));
                        if (world.getBlockState(checkPos).getBlock() != this) {
                            // Structure is broken, remove it
                            return Blocks.AIR.defaultBlockState();
                        }
                    }
                }
            }
        }
        return super.updateShape(state, facing, facingState, world, currentPos, facingPos);
    }
}