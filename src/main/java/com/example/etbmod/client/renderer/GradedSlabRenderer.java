package com.example.etbmod.client.renderer;

import com.example.etbmod.blocks.GradedSlabBlock;
import com.example.etbmod.client.texture.CardTextureManager;
import com.example.etbmod.tileentities.GradedSlabTileEntity;
import com.mojang.blaze3d.matrix.MatrixStack;
import com.mojang.blaze3d.vertex.IVertexBuilder;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.FontRenderer;
import net.minecraft.client.renderer.IRenderTypeBuffer;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.renderer.tileentity.TileEntityRenderer;
import net.minecraft.client.renderer.tileentity.TileEntityRendererDispatcher;
import net.minecraft.util.Direction;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.vector.Matrix4f;
import net.minecraft.util.math.vector.Vector3f;

public class GradedSlabRenderer extends TileEntityRenderer<GradedSlabTileEntity> {
    
    public GradedSlabRenderer(TileEntityRendererDispatcher rendererDispatcherIn) {
        super(rendererDispatcherIn);
    }
    
    @Override
    public void render(GradedSlabTileEntity tileEntity, float partialTicks, MatrixStack matrixStackIn,
                       IRenderTypeBuffer bufferIn, int combinedLightIn, int combinedOverlayIn) {
        
        String imagePath = tileEntity.getCardImagePath();
        if (imagePath == null || imagePath.isEmpty()) {
            // Debug: No image path set
            return;
        }
        
        // Get card texture
        ResourceLocation cardTexture = CardTextureManager.getOrLoadCardTexture(imagePath);
        if (cardTexture == null) {
            // Debug: Failed to load texture
            com.example.etbmod.ETBMod.LOGGER.debug("Failed to load card texture for graded slab: " + imagePath);
            return;
        }
        
        matrixStackIn.pushPose();
        
        // Get the block's facing direction
        Direction facing = tileEntity.getBlockState().getValue(GradedSlabBlock.FACING);
        
        // Position and rotate based on facing - place card in front of the frame
        switch (facing) {
            case NORTH:
                matrixStackIn.translate(0.5, 0.5, 0.93);  // Slightly in front of frame
                break;
            case SOUTH:
                matrixStackIn.translate(0.5, 0.5, 0.07);  // Slightly in front of frame
                matrixStackIn.mulPose(Vector3f.YP.rotationDegrees(180));
                break;
            case WEST:
                matrixStackIn.translate(0.93, 0.5, 0.5);  // Slightly in front of frame
                matrixStackIn.mulPose(Vector3f.YP.rotationDegrees(90));
                break;
            case EAST:
                matrixStackIn.translate(0.07, 0.5, 0.5);  // Slightly in front of frame
                matrixStackIn.mulPose(Vector3f.YP.rotationDegrees(-90));
                break;
        }
        
        // Scale to fit nicely in the frame (slightly smaller to show frame edges)
        float scale = 0.4f; // Increased card display size
        matrixStackIn.scale(scale, scale, scale);
        
        // Render the card texture with proper transparency
        IVertexBuilder vertexBuilder = bufferIn.getBuffer(RenderType.entityTranslucent(cardTexture));
        Matrix4f matrix = matrixStackIn.last().pose();
        
        // Make the card slightly larger and properly positioned
        float size = 0.9f;  // Card quad size
        
        // Draw card quad (facing outward) with corrected UV mapping
        float u0 = 0.0f, v0 = 0.0f;
        float u1 = 1.0f, v1 = 1.0f;
        
        // Increased light to make card more visible
        int lightLevel = 0xF000F0;  // Full brightness
        
        vertexBuilder.vertex(matrix, -size, -size, 0.0f).color(255, 255, 255, 255).uv(u0, v1).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(lightLevel).normal(0, 0, 1).endVertex();
        vertexBuilder.vertex(matrix, size, -size, 0.0f).color(255, 255, 255, 255).uv(u1, v1).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(lightLevel).normal(0, 0, 1).endVertex();
        vertexBuilder.vertex(matrix, size, size, 0.0f).color(255, 255, 255, 255).uv(u1, v0).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(lightLevel).normal(0, 0, 1).endVertex();
        vertexBuilder.vertex(matrix, -size, size, 0.0f).color(255, 255, 255, 255).uv(u0, v0).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(lightLevel).normal(0, 0, 1).endVertex();
        
        matrixStackIn.popPose();
        
        // Render PSA grade label
        renderGradeLabel(tileEntity, matrixStackIn, bufferIn, combinedLightIn, facing);
    }
    
    private void renderGradeLabel(GradedSlabTileEntity tileEntity, MatrixStack matrixStackIn,
                                 IRenderTypeBuffer bufferIn, int combinedLightIn, Direction facing) {
        int grade = tileEntity.getGrade();
        String gradeText = "PSA " + grade;
        
        matrixStackIn.pushPose();
        
        // Position label at top-center of the slab, more prominently displayed
        switch (facing) {
            case NORTH:
                matrixStackIn.translate(0.5, 0.85, 0.946);  // Positioned at top of card
                break;
            case SOUTH:
                matrixStackIn.translate(0.5, 0.85, 0.054);
                matrixStackIn.mulPose(Vector3f.YP.rotationDegrees(180));
                break;
            case WEST:
                matrixStackIn.translate(0.946, 0.85, 0.5);
                matrixStackIn.mulPose(Vector3f.YP.rotationDegrees(90));
                break;
            case EAST:
                matrixStackIn.translate(0.054, 0.85, 0.5);
                matrixStackIn.mulPose(Vector3f.YP.rotationDegrees(-90));
                break;
        }
        
        // Scale for readability
        float labelScale = 0.01f;  // Slightly larger for better visibility
        matrixStackIn.scale(labelScale, -labelScale, labelScale);
        
        FontRenderer fontRenderer = Minecraft.getInstance().font;
        float width = fontRenderer.width(gradeText);
        float x = -width / 2;
        float y = 0;
        
        // Draw a black background box first
        int padding = 3;
        float boxX1 = x - padding;
        float boxY1 = y - padding;
        float boxX2 = x + width + padding;
        float boxY2 = y + fontRenderer.lineHeight + padding;
        
        // Get vertex builder for rendering the background
        IVertexBuilder vertexBuilder = bufferIn.getBuffer(RenderType.solid());
        Matrix4f matrix = matrixStackIn.last().pose();
        
        // Draw black background quad
        vertexBuilder.vertex(matrix, boxX1, boxY1, -0.01f).color(0, 0, 0, 255).uv(0, 0).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(0, 0, 1).endVertex();
        vertexBuilder.vertex(matrix, boxX2, boxY1, -0.01f).color(0, 0, 0, 255).uv(1, 0).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(0, 0, 1).endVertex();
        vertexBuilder.vertex(matrix, boxX2, boxY2, -0.01f).color(0, 0, 0, 255).uv(1, 1).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(0, 0, 1).endVertex();
        vertexBuilder.vertex(matrix, boxX1, boxY2, -0.01f).color(0, 0, 0, 255).uv(0, 1).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(0, 0, 1).endVertex();
        
        // Draw white text on top of the black background
        fontRenderer.drawInBatch(gradeText, x, y, 0xFFFFFFFF, false,
                matrixStackIn.last().pose(), bufferIn, false, 0, 0xF000F0);
        
        // Add a colored border around the PSA label based on grade
        int borderColor = getGradeBorderColor(grade);
        
        // Draw colored border (thin lines)
        IVertexBuilder borderBuilder = bufferIn.getBuffer(RenderType.lines());
        float r = ((borderColor >> 16) & 255) / 255.0f;
        float g = ((borderColor >> 8) & 255) / 255.0f;
        float b = (borderColor & 255) / 255.0f;
        
        // Top border
        borderBuilder.vertex(matrix, boxX1, boxY1, 0).color(r, g, b, 1.0f).endVertex();
        borderBuilder.vertex(matrix, boxX2, boxY1, 0).color(r, g, b, 1.0f).endVertex();
        // Right border
        borderBuilder.vertex(matrix, boxX2, boxY1, 0).color(r, g, b, 1.0f).endVertex();
        borderBuilder.vertex(matrix, boxX2, boxY2, 0).color(r, g, b, 1.0f).endVertex();
        // Bottom border
        borderBuilder.vertex(matrix, boxX2, boxY2, 0).color(r, g, b, 1.0f).endVertex();
        borderBuilder.vertex(matrix, boxX1, boxY2, 0).color(r, g, b, 1.0f).endVertex();
        // Left border
        borderBuilder.vertex(matrix, boxX1, boxY2, 0).color(r, g, b, 1.0f).endVertex();
        borderBuilder.vertex(matrix, boxX1, boxY1, 0).color(r, g, b, 1.0f).endVertex();
        
        matrixStackIn.popPose();
    }
    
    private int getGradeBackgroundColor(int grade) {
        // Background colors for different grades
        switch (grade) {
            case 10: return 0x40FFD700; // Gold
            case 9:  return 0x40FFFF00; // Yellow
            case 8:  return 0x4000FF00; // Green
            case 7:  return 0x4000FFFF; // Cyan
            default: return 0x40808080; // Gray
        }
    }
    
    private int getGradeTextColor(int grade) {
        // Text colors for different grades - bright colors for visibility
        switch (grade) {
            case 10: return 0xFFFFD700; // Gold
            case 9:  return 0xFFFFFF00; // Yellow
            case 8:  return 0xFF00FF00; // Green
            case 7:  return 0xFF00FFFF; // Cyan
            case 6:  return 0xFFFF8C00; // Orange
            default: return 0xFFAAAAAA; // Light Gray
        }
    }
    
    private int getGradeBorderColor(int grade) {
        // Border colors for different grades - matches the grade quality
        switch (grade) {
            case 10: return 0xFFD700; // Gold
            case 9:  return 0xFFFF00; // Yellow
            case 8:  return 0x00FF00; // Green
            case 7:  return 0x00FFFF; // Cyan
            case 6:  return 0xFF8C00; // Orange
            case 5:  return 0xFF0000; // Red
            default: return 0x808080; // Gray
        }
    }
}