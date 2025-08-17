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
    # Create a 16x16 texture with a cool gaming table design
    texture = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture)
    
    # Dark wood base
    base_color = (42, 31, 22, 255)
    draw.rectangle([0, 0, 15, 15], fill=base_color)
    
    # Table surface - darker gaming mat style
    surface_color = (20, 20, 25, 255)
    draw.rectangle([1, 1, 14, 14], fill=surface_color)
    
    # Gaming mat pattern - subtle grid
    grid_color = (30, 30, 40, 255)
    for i in range(2, 14, 3):
        draw.line([i, 1, i, 14], fill=grid_color)
        draw.line([1, i, 14, i], fill=grid_color)
    
    # Cool neon accent in corners
    accent_color = (100, 200, 255, 255)
    draw.point([2, 2], fill=accent_color)
    draw.point([13, 2], fill=accent_color)
    draw.point([2, 13], fill=accent_color)
    draw.point([13, 13], fill=accent_color)
    
    texture_path = Path("src/main/resources/assets/etbmod/textures/block/gamer_table.png")
    texture.save(texture_path, 'PNG')
    print(f"✓ Created block texture: {texture_path}")
    
    # Also create top, bottom, and side textures
    # Top texture (same as main)
    texture.save(texture_path.parent / "gamer_table_top.png", 'PNG')
    
    # Bottom texture (just wood)
    bottom = Image.new('RGBA', (16, 16), base_color)
    bottom.save(texture_path.parent / "gamer_table_bottom.png", 'PNG')
    
    # Side texture (wood with dark strip)
    side = Image.new('RGBA', (16, 16), base_color)
    draw_side = ImageDraw.Draw(side)
    draw_side.rectangle([0, 0, 15, 10], fill=surface_color)
    side.save(texture_path.parent / "gamer_table_side.png", 'PNG')
    
    print(f"✓ Created all block textures")

def main():
    print("Creating Gamer Table Textures")
    print("=" * 60)
    
    create_gui_texture()
    create_block_texture()
    
    print("\n✓ All textures created successfully!")

if __name__ == "__main__":
    main()