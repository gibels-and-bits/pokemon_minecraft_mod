#!/usr/bin/env python3
"""Create a simple, clean GUI texture for the gamer table."""

from PIL import Image, ImageDraw
import os

def create_simple_gui():
    # Create standard GUI size (176x166 like a chest)
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main panel background (176x166)
    # Light gray background
    draw.rectangle([0, 0, 175, 165], fill=(198, 198, 198, 255))
    
    # Darker border
    draw.rectangle([0, 0, 175, 165], outline=(85, 85, 85, 255), width=3)
    
    # Inner lighter area
    draw.rectangle([4, 4, 171, 161], fill=(220, 220, 220, 255))
    
    # Title area background
    draw.rectangle([4, 4, 171, 17], fill=(200, 200, 200, 255))
    
    # Pack slot area (single slot at top center)
    # Slot position: x=79, y=19 (for 18x18 slot)
    slot_x = 79
    slot_y = 19
    
    # Draw slot background
    draw.rectangle([slot_x, slot_y, slot_x + 18, slot_y + 18], 
                   fill=(139, 139, 139, 255))
    # Slot border
    draw.rectangle([slot_x - 1, slot_y - 1, slot_x + 19, slot_y + 19], 
                   outline=(55, 55, 55, 255), width=1)
    # Inner highlight
    draw.rectangle([slot_x + 1, slot_y + 1, slot_x + 17, slot_y + 17], 
                   outline=(255, 255, 255, 100), width=1)
    
    # Add decorative label area for pack slot
    draw.rectangle([30, 19, 146, 37], outline=(100, 100, 100, 128), width=1)
    
    # Player inventory area background (slightly darker)
    draw.rectangle([7, 83, 168, 139], fill=(180, 180, 180, 255))
    draw.rectangle([7, 83, 168, 139], outline=(100, 100, 100, 255), width=1)
    
    # Hotbar area background
    draw.rectangle([7, 141, 168, 159], fill=(180, 180, 180, 255))
    draw.rectangle([7, 141, 168, 159], outline=(100, 100, 100, 255), width=1)
    
    # Draw inventory slots (9x3)
    for row in range(3):
        for col in range(9):
            x = 7 + col * 18
            y = 83 + row * 18
            # Slot background
            draw.rectangle([x, y, x + 18, y + 18], fill=(139, 139, 139, 255))
            # Inner darker area
            draw.rectangle([x + 1, y + 1, x + 17, y + 17], fill=(85, 85, 85, 255))
            # Highlight
            draw.line([x + 1, y + 1, x + 17, y + 1], fill=(255, 255, 255, 100), width=1)
            draw.line([x + 1, y + 1, x + 1, y + 17], fill=(255, 255, 255, 100), width=1)
    
    # Draw hotbar slots (9x1)
    for col in range(9):
        x = 7 + col * 18
        y = 141
        # Slot background
        draw.rectangle([x, y, x + 18, y + 18], fill=(139, 139, 139, 255))
        # Inner darker area
        draw.rectangle([x + 1, y + 1, x + 17, y + 17], fill=(85, 85, 85, 255))
        # Highlight
        draw.line([x + 1, y + 1, x + 17, y + 1], fill=(255, 255, 255, 100), width=1)
        draw.line([x + 1, y + 1, x + 1, y + 17], fill=(255, 255, 255, 100), width=1)
    
    # Save the texture
    output_path = "/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/textures/gui/gamer_table_v2.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created simple GUI texture at {output_path}")

if __name__ == "__main__":
    create_simple_gui()