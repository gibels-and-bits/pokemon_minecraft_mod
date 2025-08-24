#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os

# Create directory if it doesn't exist
gui_path = "src/main/resources/assets/etbmod/textures/gui"
os.makedirs(gui_path, exist_ok=True)

# Colors
YELLOW_MAIN = (252, 203, 50)
YELLOW_DARK = (220, 170, 20)
RED = (237, 28, 36)
WHITE = (250, 250, 250)
BLACK = (20, 20, 20)
PIKACHU_YELLOW = (255, 215, 0)

def create_fixed_gui_texture():
    """Create properly aligned GUI texture for vending machine"""
    # Standard Minecraft GUI size
    img = Image.new('RGBA', (176, 166), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main background (standard Minecraft GUI gray)
    draw.rectangle([0, 0, 175, 165], fill=(198, 198, 198))
    
    # Border
    # Top and left darker
    draw.line([(0, 0), (175, 0)], fill=(85, 85, 85), width=1)
    draw.line([(0, 0), (0, 165)], fill=(85, 85, 85), width=1)
    # Bottom and right lighter
    draw.line([(0, 165), (175, 165)], fill=(255, 255, 255), width=1)
    draw.line([(175, 0), (175, 165)], fill=(255, 255, 255), width=1)
    
    # Inner border for depth
    draw.line([(1, 1), (174, 1)], fill=(139, 139, 139), width=1)
    draw.line([(1, 1), (1, 164)], fill=(139, 139, 139), width=1)
    draw.line([(1, 164), (174, 164)], fill=(198, 198, 198), width=1)
    draw.line([(174, 1), (174, 164)], fill=(198, 198, 198), width=1)
    
    # Title area - Pokemon Yellow themed
    draw.rectangle([4, 4, 171, 25], fill=YELLOW_MAIN)
    draw.rectangle([4, 4, 171, 5], fill=YELLOW_DARK)
    draw.rectangle([4, 24, 171, 25], fill=YELLOW_DARK)
    draw.rectangle([4, 4, 5, 25], fill=YELLOW_DARK)
    draw.rectangle([170, 4, 171, 25], fill=YELLOW_DARK)
    
    # Diamond input slot (at exact position 26, 35)
    # Outer border
    draw.rectangle([25, 34, 43, 52], fill=(85, 85, 85))
    # Inner slot
    draw.rectangle([26, 35, 42, 51], fill=(139, 139, 139))
    # Slot depression
    draw.line([(26, 35), (42, 35)], fill=(55, 55, 55), width=1)
    draw.line([(26, 35), (26, 51)], fill=(55, 55, 55), width=1)
    draw.line([(26, 51), (42, 51)], fill=(255, 255, 255), width=1)
    draw.line([(42, 35), (42, 51)], fill=(255, 255, 255), width=1)
    
    # Output slots (3x3 grid starting at 116, 17)
    for row in range(3):
        for col in range(3):
            x = 116 + col * 18
            y = 17 + row * 18
            # Slot background
            draw.rectangle([x - 1, y - 1, x + 17, y + 17], fill=(85, 85, 85))
            draw.rectangle([x, y, x + 16, y + 16], fill=(139, 139, 139))
            # Slot depression effect
            draw.line([(x, y), (x + 16, y)], fill=(55, 55, 55), width=1)
            draw.line([(x, y), (x, y + 16)], fill=(55, 55, 55), width=1)
            draw.line([(x, y + 16), (x + 16, y + 16)], fill=(255, 255, 255), width=1)
            draw.line([(x + 16, y), (x + 16, y + 16)], fill=(255, 255, 255), width=1)
    
    # Button/selection area background
    draw.rectangle([50, 30, 110, 75], fill=(220, 220, 220))
    draw.rectangle([50, 30, 110, 31], fill=(139, 139, 139))
    draw.rectangle([50, 74, 110, 75], fill=(255, 255, 255))
    draw.rectangle([50, 30, 51, 75], fill=(139, 139, 139))
    draw.rectangle([109, 30, 110, 75], fill=(255, 255, 255))
    
    # Player inventory (27 slots starting at y=84)
    for row in range(3):
        for col in range(9):
            x = 8 + col * 18
            y = 84 + row * 18
            # Slot background
            draw.rectangle([x - 1, y - 1, x + 17, y + 17], fill=(85, 85, 85))
            draw.rectangle([x, y, x + 16, y + 16], fill=(139, 139, 139))
            # Slot depression
            draw.line([(x, y), (x + 16, y)], fill=(55, 55, 55), width=1)
            draw.line([(x, y), (x, y + 16)], fill=(55, 55, 55), width=1)
            draw.line([(x, y + 16), (x + 16, y + 16)], fill=(255, 255, 255), width=1)
            draw.line([(x + 16, y), (x + 16, y + 16)], fill=(255, 255, 255), width=1)
    
    # Player hotbar (9 slots at y=142)
    for col in range(9):
        x = 8 + col * 18
        y = 142
        # Slot background
        draw.rectangle([x - 1, y - 1, x + 17, y + 17], fill=(85, 85, 85))
        draw.rectangle([x, y, x + 16, y + 16], fill=(139, 139, 139))
        # Slot depression
        draw.line([(x, y), (x + 16, y)], fill=(55, 55, 55), width=1)
        draw.line([(x, y), (x, y + 16)], fill=(55, 55, 55), width=1)
        draw.line([(x, y + 16), (x + 16, y + 16)], fill=(255, 255, 255), width=1)
        draw.line([(x + 16, y), (x + 16, y + 16)], fill=(255, 255, 255), width=1)
    
    # Add small Pokeball decoration in title
    center_x, center_y = 160, 14
    size = 10
    # Top half red
    draw.pieslice([center_x - size//2, center_y - size//2, 
                   center_x + size//2, center_y + size//2], 
                  0, 180, fill=RED)
    # Bottom half white
    draw.pieslice([center_x - size//2, center_y - size//2,
                   center_x + size//2, center_y + size//2], 
                  180, 360, fill=WHITE)
    # Center line
    draw.rectangle([center_x - size//2, center_y - 1, 
                    center_x + size//2, center_y + 1], fill=BLACK)
    # Center button
    draw.ellipse([center_x - 2, center_y - 2, 
                  center_x + 2, center_y + 2], fill=WHITE)
    draw.ellipse([center_x - 1, center_y - 1, 
                  center_x + 1, center_y + 1], fill=BLACK)
    
    img.save(os.path.join(gui_path, "vending_machine.png"))
    print(f"Created fixed vending_machine.png GUI texture")

if __name__ == "__main__":
    create_fixed_gui_texture()
    print("GUI texture has been fixed with proper slot alignment!")