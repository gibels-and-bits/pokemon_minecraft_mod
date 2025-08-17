package com.example.etbmod.blocks;

import com.example.etbmod.tileentity.GamerTableTileEntity;
import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.SoundType;
import net.minecraft.block.material.Material;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.ServerPlayerEntity;
import net.minecraft.inventory.InventoryHelper;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.ActionResultType;
import net.minecraft.util.Hand;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.BlockRayTraceResult;
import net.minecraft.util.math.shapes.ISelectionContext;
import net.minecraft.util.math.shapes.VoxelShape;
import net.minecraft.world.IBlockReader;
import net.minecraft.world.World;
import net.minecraftforge.common.ToolType;
import net.minecraftforge.fml.network.NetworkHooks;

public class GamerTableBlock extends Block {
    
    // Table is 14x10x14 pixels (slightly smaller than full block for style)
    private static final VoxelShape SHAPE = Block.box(1.0D, 0.0D, 1.0D, 15.0D, 10.0D, 15.0D);
    
    public GamerTableBlock() {
        super(Properties.of(Material.WOOD)
                .strength(2.5F)
                .sound(SoundType.WOOD)
                .harvestTool(ToolType.AXE)
                .harvestLevel(0)
                .noOcclusion());
    }
    
    @Override
    public VoxelShape getShape(BlockState state, IBlockReader worldIn, BlockPos pos, ISelectionContext context) {
        return SHAPE;
    }
    
    @Override
    public boolean hasTileEntity(BlockState state) {
        return true;
    }
    
    @Override
    public TileEntity createTileEntity(BlockState state, IBlockReader world) {
        return new GamerTableTileEntity();
    }
    
    @Override
    public ActionResultType use(BlockState state, World worldIn, BlockPos pos, PlayerEntity player, 
                                Hand hand, BlockRayTraceResult hit) {
        if (!worldIn.isClientSide) {
            TileEntity tileEntity = worldIn.getBlockEntity(pos);
            if (tileEntity instanceof GamerTableTileEntity) {
                NetworkHooks.openGui((ServerPlayerEntity) player, (GamerTableTileEntity) tileEntity, pos);
            }
        }
        return ActionResultType.sidedSuccess(worldIn.isClientSide);
    }
    
    @Override
    public void onRemove(BlockState state, World worldIn, BlockPos pos, BlockState newState, boolean isMoving) {
        if (!state.is(newState.getBlock())) {
            TileEntity tileEntity = worldIn.getBlockEntity(pos);
            if (tileEntity instanceof GamerTableTileEntity) {
                InventoryHelper.dropContents(worldIn, pos, (GamerTableTileEntity) tileEntity);
            }
            super.onRemove(state, worldIn, pos, newState, isMoving);
        }
    }
    
    @Override
    public boolean useShapeForLightOcclusion(BlockState state) {
        return true;
    }
}