#!/usr/bin/env python3
"""Create a dark-themed GUI texture for the gamer table."""

from PIL import Image, ImageDraw, ImageFont
import os

def create_dark_gui():
    # Create 256x256 texture (Minecraft standard for GUI textures)
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark background panel (256x200)
    # Outer border - dark gray
    draw.rectangle([0, 0, 255, 199], fill=(25, 25, 30, 255), outline=(80, 80, 90, 255), width=2)
    
    # Inner gradient effect - darker center
    for i in range(5):
        alpha = 255 - (i * 30)
        draw.rectangle([2+i, 2+i, 253-i, 197-i], outline=(40+i*5, 40+i*5, 50+i*5, alpha), width=1)
    
    # Title area with tech border
    draw.rectangle([10, 5, 245, 25], fill=(20, 20, 25, 255), outline=(100, 200, 255, 255), width=1)
    
    # Pack slot area - highlighted box
    # Outer glow
    for i in range(3):
        alpha = 100 - (i * 30)
        draw.rectangle([125-i, 52-i, 130+18+i, 57+18+i], outline=(255, 0, 255, alpha), width=1)
    
    # Main slot background
    draw.rectangle([127, 54, 128+18, 55+18], fill=(40, 0, 40, 255), outline=(255, 0, 255, 255), width=1)
    
    # Pack slot frame decoration
    # Tech corners
    corner_size = 4
    # Top-left
    draw.line([127, 54, 127+corner_size, 54], fill=(0, 255, 255, 255), width=2)
    draw.line([127, 54, 127, 54+corner_size], fill=(0, 255, 255, 255), width=2)
    # Top-right
    draw.line([146-corner_size, 54, 146, 54], fill=(0, 255, 255, 255), width=2)
    draw.line([146, 54, 146, 54+corner_size], fill=(0, 255, 255, 255), width=2)
    # Bottom-left
    draw.line([127, 73-corner_size, 127, 73], fill=(0, 255, 255, 255), width=2)
    draw.line([127, 73, 127+corner_size, 73], fill=(0, 255, 255, 255), width=2)
    # Bottom-right
    draw.line([146-corner_size, 73, 146, 73], fill=(0, 255, 255, 255), width=2)
    draw.line([146, 73, 146, 73-corner_size], fill=(0, 255, 255, 255), width=2)
    
    # Player inventory area background
    inventory_y = 117
    # Main inventory (3 rows)
    for row in range(3):
        for col in range(9):
            x = 47 + col * 18
            y = inventory_y + row * 18
            # Slot background
            draw.rectangle([x, y, x+18, y+18], fill=(35, 35, 40, 255), outline=(70, 70, 80, 255), width=1)
            # Inner highlight
            draw.rectangle([x+1, y+1, x+17, y+17], outline=(50, 50, 60, 128), width=1)
    
    # Hotbar (1 row)
    hotbar_y = 175
    for col in range(9):
        x = 47 + col * 18
        y = hotbar_y
        # Slot background - slightly brighter for hotbar
        draw.rectangle([x, y, x+18, y+18], fill=(40, 40, 45, 255), outline=(80, 80, 90, 255), width=1)
        # Inner highlight
        draw.rectangle([x+1, y+1, x+17, y+17], outline=(60, 60, 70, 128), width=1)
    
    # Add decorative tech lines
    # Horizontal lines
    draw.line([10, 30, 245, 30], fill=(50, 150, 200, 100), width=1)
    draw.line([10, 110, 245, 110], fill=(50, 150, 200, 100), width=1)
    
    # Vertical accent lines
    draw.line([30, 35, 30, 105], fill=(200, 50, 150, 80), width=1)
    draw.line([225, 35, 225, 105], fill=(200, 50, 150, 80), width=1)
    
    # Add some tech patterns in corners
    # Top-left circuit pattern
    for i in range(3):
        draw.rectangle([15+i*3, 35+i*3, 17+i*3, 37+i*3], fill=(100, 200, 255, 50), width=0)
    
    # Top-right circuit pattern
    for i in range(3):
        draw.rectangle([238-i*3, 35+i*3, 240-i*3, 37+i*3], fill=(255, 100, 200, 50), width=0)
    
    # Save the texture
    output_path = "/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/textures/gui/gamer_table_dark.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created dark GUI texture at {output_path}")

if __name__ == "__main__":
    create_dark_gui()