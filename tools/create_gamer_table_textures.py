#!/usr/bin/env python3
"""
Create textures for the gamer table
"""

from PIL import Image, ImageDraw
from pathlib import Path

def create_gui_texture():
    """Create the GUI texture for the gamer table"""
    # Standard GUI size is 176x166
    gui = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gui)
    
    # Main GUI background (176x166)
    # Dark gray background
    draw.rectangle([0, 0, 175, 165], fill=(139, 139, 139, 255))
    # Lighter inner area
    draw.rectangle([7, 17, 168, 82], fill=(198, 198, 198, 255))
    # Inventory area
    draw.rectangle([7, 83, 168, 165], fill=(139, 139, 139, 255))
    
    # Slot for booster pack (in center of top area)
    # Standard slot is 18x18
    slot_x, slot_y = 79, 34
    draw.rectangle([slot_x, slot_y, slot_x + 17, slot_y + 17], fill=(56, 56, 56, 255))
    draw.rectangle([slot_x + 1, slot_y + 1, slot_x + 16, slot_y + 16], fill=(139, 139, 139, 255))
    
    # Player inventory slots (9x3 + hotbar)
    for row in range(3):
        for col in range(9):
            x = 7 + col * 18
            y = 83 + row * 18
            draw.rectangle([x, y, x + 17, y + 17], fill=(56, 56, 56, 255))
            draw.rectangle([x + 1, y + 1, x + 16, y + 16], fill=(139, 139, 139, 255))
    
    # Hotbar slots
    for col in range(9):
        x = 7 + col * 18
        y = 141
        draw.rectangle([x, y, x + 17, y + 17], fill=(56, 56, 56, 255))
        draw.rectangle([x + 1, y + 1, x + 16, y + 16], fill=(139, 139, 139, 255))
    
    gui_path = Path("src/main/resources/assets/etbmod/textures/gui/gamer_table.png")
    gui.save(gui_path, 'PNG')
    print(f"✓ Created GUI texture: {gui_path}")
    
def create_block_texture():
    """Create the block texture for the gamer table"""
    # Base colors - dark oak wood and gaming surface
    wood_dark = (56, 40, 28, 255)
    wood_light = (72, 52, 36, 255)
    surface_dark = (15, 15, 20, 255)
    surface_mid = (25, 25, 35, 255)
    surface_light = (35, 35, 50, 255)
    
    # Neon accent colors for gaming aesthetic
    neon_blue = (0, 180, 255, 255)
    neon_purple = (180, 0, 255, 255)
    neon_cyan = (0, 255, 240, 255)
    
    # Create TOP texture - gaming mat with cool pattern
    top = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw_top = ImageDraw.Draw(top)
    
    # Dark gaming mat base
    draw_top.rectangle([0, 0, 15, 15], fill=surface_dark)
    
    # Wood frame around edges
    draw_top.rectangle([0, 0, 15, 0], fill=wood_dark)
    draw_top.rectangle([0, 15, 15, 15], fill=wood_dark)
    draw_top.rectangle([0, 0, 0, 15], fill=wood_dark)
    draw_top.rectangle([15, 0, 15, 15], fill=wood_dark)
    
    # Gaming mat with hex grid pattern
    draw_top.rectangle([1, 1, 14, 14], fill=surface_mid)
    
    # Subtle grid lines
    for i in range(4, 14, 4):
        draw_top.line([i, 1, i, 14], fill=surface_light)
        draw_top.line([1, i, 14, i], fill=surface_light)
    
    # Neon accents in corners for gaming feel
    # Top-left corner accent
    draw_top.rectangle([1, 1, 2, 2], fill=neon_blue)
    draw_top.point([2, 1], fill=neon_cyan)
    draw_top.point([1, 2], fill=neon_cyan)
    
    # Top-right corner accent
    draw_top.rectangle([13, 1, 14, 2], fill=neon_purple)
    draw_top.point([13, 1], fill=neon_cyan)
    draw_top.point([14, 2], fill=neon_cyan)
    
    # Bottom-left corner accent
    draw_top.rectangle([1, 13, 2, 14], fill=neon_purple)
    draw_top.point([2, 14], fill=neon_cyan)
    draw_top.point([1, 13], fill=neon_cyan)
    
    # Bottom-right corner accent
    draw_top.rectangle([13, 13, 14, 14], fill=neon_blue)
    draw_top.point([13, 14], fill=neon_cyan)
    draw_top.point([14, 13], fill=neon_cyan)
    
    # Center decoration - stylized card symbol
    draw_top.rectangle([7, 7, 8, 8], fill=neon_cyan)
    
    top_path = Path("src/main/resources/assets/etbmod/textures/block/gamer_table_top.png")
    top.save(top_path, 'PNG')
    print(f"✓ Created top texture: {top_path}")
    
    # Create BOTTOM texture - wood planks
    bottom = Image.new('RGBA', (16, 16), wood_dark)
    draw_bottom = ImageDraw.Draw(bottom)
    
    # Wood plank pattern
    for y in range(0, 16, 4):
        draw_bottom.rectangle([0, y, 15, y+3], fill=wood_dark)
        draw_bottom.line([0, y+3, 15, y+3], fill=(40, 28, 20, 255))
    
    # Add some wood grain
    for x in range(2, 16, 5):
        for y in range(1, 16, 2):
            draw_bottom.point([x, y], fill=wood_light)
    
    bottom_path = Path("src/main/resources/assets/etbmod/textures/block/gamer_table_bottom.png")
    bottom.save(bottom_path, 'PNG')
    print(f"✓ Created bottom texture: {bottom_path}")
    
    # Create SIDE texture - wood with gaming strip
    side = Image.new('RGBA', (16, 16), wood_dark)
    draw_side = ImageDraw.Draw(side)
    
    # Wood base
    draw_side.rectangle([0, 0, 15, 15], fill=wood_dark)
    
    # Dark gaming surface strip on top
    draw_side.rectangle([0, 0, 15, 2], fill=surface_dark)
    draw_side.rectangle([0, 1, 15, 1], fill=surface_mid)
    
    # Neon accent line
    draw_side.line([0, 2, 15, 2], fill=neon_cyan)
    
    # Wood detail
    for y in range(3, 16, 3):
        draw_side.line([0, y, 15, y], fill=(40, 28, 20, 255))
    
    # Add wood grain details
    for x in range(1, 16, 3):
        for y in range(4, 16, 2):
            draw_side.point([x, y], fill=wood_light)
            
    # Small neon accents for style
    draw_side.point([1, 1], fill=neon_blue)
    draw_side.point([14, 1], fill=neon_purple)
    
    side_path = Path("src/main/resources/assets/etbmod/textures/block/gamer_table_side.png")
    side.save(side_path, 'PNG')
    print(f"✓ Created side texture: {side_path}")
    
    # Also save the main texture (same as top for legacy)
    texture_path = Path("src/main/resources/assets/etbmod/textures/block/gamer_table.png")
    top.save(texture_path, 'PNG')
    
    print(f"✓ Created all block textures")

def main():
    print("Creating Gamer Table Textures")
    print("=" * 60)
    
    create_gui_texture()
    create_block_texture()
    
    print("\n✓ All textures created successfully!")

if __name__ == "__main__":
    main()