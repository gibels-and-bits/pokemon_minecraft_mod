#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os

# Create directories if they don't exist
texture_path = "src/main/resources/assets/etbmod/textures/block"
gui_path = "src/main/resources/assets/etbmod/textures/gui"
os.makedirs(texture_path, exist_ok=True)
os.makedirs(gui_path, exist_ok=True)

# Use 128x128 for high-res textures (8x the default resolution)
TEXTURE_SIZE = 128

# Color palette based on the actual Pokemon vending machine
YELLOW_MAIN = (252, 203, 50)     # Bright Pokemon yellow
YELLOW_LIGHT = (255, 220, 100)   # Lighter yellow for highlights  
YELLOW_DARK = (220, 170, 20)     # Darker yellow for shading
PIKACHU_YELLOW = (255, 215, 0)   # Pikachu yellow accent
BLUE_GLASS = (180, 220, 250)     # Light blue for glass display
BLUE_DARK = (100, 150, 200)      # Darker blue for glass depth
BLUE_SCREEN = (50, 100, 180)     # Digital screen blue
BLACK = (20, 20, 20)             # Pure black for details
WHITE = (250, 250, 250)          # Bright white
RED = (237, 28, 36)              # Pokemon red
GRAY_METAL = (160, 160, 170)     # Light metal
GRAY_DARK = (80, 80, 90)         # Dark metal
PURPLE_ACCENT = (120, 80, 180)   # Purple for buttons/details

def draw_pokeball(draw, x, y, size):
    """Draw a pokeball at specified position and size"""
    # Top half (red)
    draw.ellipse([x, y, x + size, y + size], fill=RED)
    # Bottom half (white)
    draw.pieslice([x, y, x + size, y + size], 180, 360, fill=WHITE)
    # Center band
    band_y = y + size // 2 - size // 16
    draw.rectangle([x, band_y, x + size, band_y + size // 8], fill=BLACK)
    # Center button
    center_size = size // 4
    center_x = x + size // 2 - center_size // 2
    center_y = y + size // 2 - center_size // 2
    draw.ellipse([center_x, center_y, center_x + center_size, center_y + center_size], fill=WHITE)
    inner_size = center_size // 2
    inner_x = center_x + center_size // 4
    inner_y = center_y + center_size // 4
    draw.ellipse([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill=BLACK)

def create_front_texture():
    """Create high-res front face texture matching the real vending machine"""
    img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE), YELLOW_MAIN)
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(TEXTURE_SIZE):
        color_factor = i / TEXTURE_SIZE
        r = int(YELLOW_MAIN[0] * (1 - color_factor * 0.1))
        g = int(YELLOW_MAIN[1] * (1 - color_factor * 0.1))
        b = int(YELLOW_MAIN[2] * (1 - color_factor * 0.1))
        draw.rectangle([0, i, TEXTURE_SIZE, i + 1], fill=(r, g, b))
    
    # Draw main frame edges with gradient
    edge_width = 4
    for i in range(edge_width):
        darkness = 1 - (i * 0.2)
        edge_color = (int(YELLOW_DARK[0] * darkness), int(YELLOW_DARK[1] * darkness), int(YELLOW_DARK[2] * darkness))
        draw.rectangle([i, i, TEXTURE_SIZE - i - 1, TEXTURE_SIZE - i - 1], outline=edge_color, width=1)
    
    # Draw large display window (showing products)
    display_x, display_y = 12, 10
    display_w, display_h = 104, 60
    # Glass background with gradient
    for i in range(display_h):
        blue_factor = 1 - (i / display_h * 0.3)
        r = int(BLUE_GLASS[0] * blue_factor)
        g = int(BLUE_GLASS[1] * blue_factor)
        b = int(BLUE_GLASS[2] * blue_factor)
        draw.rectangle([display_x, display_y + i, display_x + display_w, display_y + i + 1], fill=(r, g, b))
    
    # Display frame
    draw.rectangle([display_x - 2, display_y - 2, display_x + display_w + 2, display_y + display_h + 2], 
                   outline=BLACK, width=2)
    draw.rectangle([display_x - 1, display_y - 1, display_x + display_w + 1, display_y + display_h + 1], 
                   outline=GRAY_DARK, width=1)
    
    # Draw product grid inside display (6x3 grid of packs)
    for row in range(3):
        for col in range(6):
            pack_x = display_x + 5 + col * 16
            pack_y = display_y + 5 + row * 18
            # Mini booster pack representations
            draw.rectangle([pack_x, pack_y, pack_x + 12, pack_y + 15], fill=(200, 200, 220))
            draw.rectangle([pack_x, pack_y, pack_x + 12, pack_y + 15], outline=(100, 100, 120), width=1)
            # Add tiny pokeball on packs
            if (row + col) % 2 == 0:
                draw.ellipse([pack_x + 4, pack_y + 5, pack_x + 8, pack_y + 9], fill=RED)
            else:
                draw.ellipse([pack_x + 4, pack_y + 5, pack_x + 8, pack_y + 9], fill=(100, 150, 200))
    
    # Draw Pokeball logo at top
    draw_pokeball(draw, 48, 2, 32)
    
    # Draw digital display screen (for prices/selection)
    screen_x, screen_y = 20, 75
    screen_w, screen_h = 88, 20
    draw.rectangle([screen_x, screen_y, screen_x + screen_w, screen_y + screen_h], fill=BLACK)
    draw.rectangle([screen_x + 2, screen_y + 2, screen_x + screen_w - 2, screen_y + screen_h - 2], fill=BLUE_SCREEN)
    # Add digital text effect
    for i in range(3):
        for j in range(8):
            dot_x = screen_x + 5 + j * 10
            dot_y = screen_y + 5 + i * 5
            draw.ellipse([dot_x, dot_y, dot_x + 2, dot_y + 2], fill=(100, 200, 255))
    
    # Draw coin slot (for diamonds)
    slot_x, slot_y = 25, 100
    draw.rectangle([slot_x, slot_y, slot_x + 20, slot_y + 8], fill=BLACK)
    draw.rectangle([slot_x + 2, slot_y + 2, slot_x + 18, slot_y + 6], fill=GRAY_DARK)
    draw.rectangle([slot_x + 8, slot_y + 1, slot_x + 12, slot_y + 7], fill=BLACK)
    
    # Draw button panel
    button_y = 100
    # Button 1 - red
    draw.ellipse([55, button_y, 65, button_y + 10], fill=RED)
    draw.ellipse([56, button_y + 1, 64, button_y + 9], fill=(255, 100, 100))
    # Button 2 - green
    draw.ellipse([70, button_y, 80, button_y + 10], fill=(50, 200, 50))
    draw.ellipse([71, button_y + 1, 79, button_y + 9], fill=(100, 255, 100))
    # Button 3 - blue
    draw.ellipse([85, button_y, 95, button_y + 10], fill=(50, 50, 200))
    draw.ellipse([86, button_y + 1, 94, button_y + 9], fill=(100, 100, 255))
    
    # Draw dispensing slot at bottom
    dispense_x, dispense_y = 30, 112
    dispense_w, dispense_h = 68, 12
    draw.rectangle([dispense_x, dispense_y, dispense_x + dispense_w, dispense_y + dispense_h], fill=BLACK)
    draw.rectangle([dispense_x + 2, dispense_y + 2, dispense_x + dispense_w - 2, dispense_y + dispense_h - 2], 
                   fill=GRAY_DARK)
    # Add push door effect
    draw.rectangle([dispense_x + 10, dispense_y + 1, dispense_x + dispense_w - 10, dispense_y + 8], 
                   fill=(60, 60, 60))
    
    # Add Pikachu silhouettes as decoration
    for i in range(3):
        x = 10 + i * 40
        y = 118
        draw.ellipse([x, y, x + 4, y + 4], fill=PIKACHU_YELLOW)
    
    img.save(os.path.join(texture_path, "vending_machine_front.png"))
    print(f"Created vending_machine_front.png ({TEXTURE_SIZE}x{TEXTURE_SIZE})")

def create_side_texture():
    """Create high-res side panel texture"""
    img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE), YELLOW_MAIN)
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(TEXTURE_SIZE):
        color_factor = i / TEXTURE_SIZE
        r = int(YELLOW_MAIN[0] * (1 - color_factor * 0.15))
        g = int(YELLOW_MAIN[1] * (1 - color_factor * 0.15))
        b = int(YELLOW_MAIN[2] * (1 - color_factor * 0.15))
        draw.rectangle([0, i, TEXTURE_SIZE, i + 1], fill=(r, g, b))
    
    # Draw frame edges
    edge_width = 4
    for i in range(edge_width):
        darkness = 1 - (i * 0.2)
        edge_color = (int(YELLOW_DARK[0] * darkness), int(YELLOW_DARK[1] * darkness), int(YELLOW_DARK[2] * darkness))
        draw.rectangle([i, i, TEXTURE_SIZE - i - 1, TEXTURE_SIZE - i - 1], outline=edge_color, width=1)
    
    # Draw raised panel sections
    panel_x, panel_y = 10, 10
    panel_w, panel_h = 108, 30
    draw.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=YELLOW_DARK)
    draw.rectangle([panel_x + 2, panel_y + 2, panel_x + panel_w - 2, panel_y + panel_h - 2], fill=YELLOW_MAIN)
    
    # Add Pokemon logo text area
    draw.rectangle([panel_x + 10, panel_y + 5, panel_x + panel_w - 10, panel_y + panel_h - 5], fill=YELLOW_LIGHT)
    
    # Draw multiple Pokeballs as decoration
    draw_pokeball(draw, 25, 15, 20)
    draw_pokeball(draw, 55, 18, 15)
    draw_pokeball(draw, 80, 15, 20)
    
    # Draw ventilation grilles
    grille_y = 50
    for i in range(8):
        y = grille_y + i * 8
        draw.rectangle([15, y, 113, y + 4], fill=GRAY_DARK)
        draw.rectangle([16, y + 1, 112, y + 3], fill=(100, 100, 110))
        # Add depth
        draw.line([(16, y + 2), (112, y + 2)], fill=BLACK, width=1)
    
    # Draw Pikachu pattern
    pika_x, pika_y = 45, 100
    # Body
    draw.ellipse([pika_x, pika_y, pika_x + 30, pika_y + 20], fill=PIKACHU_YELLOW)
    # Ears
    draw.polygon([(pika_x + 5, pika_y), (pika_x + 2, pika_y - 8), (pika_x + 8, pika_y + 2)], fill=PIKACHU_YELLOW)
    draw.polygon([(pika_x + 22, pika_y), (pika_x + 28, pika_y - 8), (pika_x + 25, pika_y + 2)], fill=PIKACHU_YELLOW)
    # Ear tips
    draw.polygon([(pika_x + 2, pika_y - 8), (pika_x + 1, pika_y - 5), (pika_x + 4, pika_y - 5)], fill=BLACK)
    draw.polygon([(pika_x + 26, pika_y - 8), (pika_x + 28, pika_y - 5), (pika_x + 25, pika_y - 5)], fill=BLACK)
    # Eyes
    draw.ellipse([pika_x + 8, pika_y + 5, pika_x + 10, pika_y + 7], fill=BLACK)
    draw.ellipse([pika_x + 20, pika_y + 5, pika_x + 22, pika_y + 7], fill=BLACK)
    # Cheeks
    draw.ellipse([pika_x + 3, pika_y + 8, pika_x + 7, pika_y + 12], fill=RED)
    draw.ellipse([pika_x + 23, pika_y + 8, pika_x + 27, pika_y + 12], fill=RED)
    
    img.save(os.path.join(texture_path, "vending_machine_side.png"))
    print(f"Created vending_machine_side.png ({TEXTURE_SIZE}x{TEXTURE_SIZE})")

def create_top_texture():
    """Create high-res top texture"""
    img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE), YELLOW_MAIN)
    draw = ImageDraw.Draw(img)
    
    # Metal top surface
    for i in range(TEXTURE_SIZE):
        for j in range(TEXTURE_SIZE):
            # Create brushed metal effect
            if (i + j) % 4 < 2:
                draw.point((i, j), fill=GRAY_METAL)
            else:
                draw.point((i, j), fill=(150, 150, 160))
    
    # Draw border frame
    draw.rectangle([0, 0, TEXTURE_SIZE - 1, TEXTURE_SIZE - 1], outline=YELLOW_DARK, width=8)
    draw.rectangle([4, 4, TEXTURE_SIZE - 5, TEXTURE_SIZE - 5], outline=BLACK, width=2)
    
    # Center panel with Pokemon branding
    center_size = 80
    center_pos = (TEXTURE_SIZE - center_size) // 2
    draw.rectangle([center_pos, center_pos, center_pos + center_size, center_pos + center_size], 
                   fill=YELLOW_MAIN)
    draw.rectangle([center_pos, center_pos, center_pos + center_size, center_pos + center_size], 
                   outline=YELLOW_DARK, width=3)
    
    # Large center Pokeball
    draw_pokeball(draw, center_pos + 20, center_pos + 20, 40)
    
    # Corner decorations
    for corner_x, corner_y in [(10, 10), (TEXTURE_SIZE - 30, 10), 
                                (10, TEXTURE_SIZE - 30), (TEXTURE_SIZE - 30, TEXTURE_SIZE - 30)]:
        draw_pokeball(draw, corner_x, corner_y, 20)
    
    img.save(os.path.join(texture_path, "vending_machine_top.png"))
    print(f"Created vending_machine_top.png ({TEXTURE_SIZE}x{TEXTURE_SIZE})")

def create_gui_texture():
    """Create the GUI background texture with Pokemon theme"""
    img = Image.new('RGBA', (176, 166), (198, 198, 198))
    draw = ImageDraw.Draw(img)
    
    # Main container background with gradient
    for i in range(166):
        gray_val = 198 - int((i / 166) * 20)
        draw.rectangle([0, i, 175, i + 1], fill=(gray_val, gray_val, gray_val))
    
    # Draw stylized border
    draw.rectangle([0, 0, 175, 165], outline=(85, 85, 85), width=2)
    draw.line([(1, 1), (174, 1)], fill=(255, 255, 255), width=1)
    draw.line([(1, 1), (1, 164)], fill=(255, 255, 255), width=1)
    
    # Title area with Pokemon yellow gradient
    for i in range(26):
        yellow_factor = 1 - (i / 26 * 0.2)
        r = int(YELLOW_MAIN[0] * yellow_factor)
        g = int(YELLOW_MAIN[1] * yellow_factor)
        b = int(YELLOW_MAIN[2] * yellow_factor)
        draw.rectangle([4, 4 + i, 171, 5 + i], fill=(r, g, b))
    
    draw.rectangle([4, 4, 171, 30], outline=YELLOW_DARK, width=2)
    
    # Diamond input slot with 3D effect
    draw.rectangle([24, 33, 44, 53], fill=(169, 169, 169))
    draw.rectangle([25, 34, 43, 52], fill=(139, 139, 139))
    draw.rectangle([26, 35, 42, 51], fill=(55, 55, 55))
    # Diamond shape
    draw.polygon([(34, 38), (39, 43), (34, 48), (29, 43)], fill=(185, 242, 255))
    draw.polygon([(34, 38), (39, 43), (36, 41), (32, 41)], fill=(210, 250, 255))
    
    # Output slots area (3x3 grid) with highlighting
    for row in range(3):
        for col in range(3):
            x = 115 + col * 18
            y = 16 + row * 18
            # 3D slot effect
            draw.rectangle([x, y, x + 18, y + 18], fill=(169, 169, 169))
            draw.rectangle([x + 1, y + 1, x + 17, y + 17], fill=(139, 139, 139))
            draw.rectangle([x + 1, y + 1, x + 16, y + 16], fill=(55, 55, 55))
    
    # Product selection area with Pokemon theme
    draw.rectangle([7, 32, 110, 76], fill=(190, 190, 190))
    draw.rectangle([8, 33, 109, 75], fill=(240, 240, 240))
    draw.rectangle([8, 33, 109, 75], outline=YELLOW_DARK, width=1)
    
    # Player inventory slots with 3D effect
    for row in range(3):
        for col in range(9):
            x = 7 + col * 18
            y = 83 + row * 18
            draw.rectangle([x, y, x + 18, y + 18], fill=(169, 169, 169))
            draw.rectangle([x + 1, y + 1, x + 17, y + 17], fill=(139, 139, 139))
            draw.rectangle([x + 1, y + 1, x + 16, y + 16], fill=(55, 55, 55))
    
    # Player hotbar slots
    for col in range(9):
        x = 7 + col * 18
        y = 141
        draw.rectangle([x, y, x + 18, y + 18], fill=(169, 169, 169))
        draw.rectangle([x + 1, y + 1, x + 17, y + 17], fill=(139, 139, 139))
        draw.rectangle([x + 1, y + 1, x + 16, y + 16], fill=(55, 55, 55))
    
    # Add decorative pokeball in corner
    draw.ellipse([150, 8, 165, 23], fill=RED)
    draw.ellipse([150, 14, 165, 17], fill=BLACK)
    draw.ellipse([155, 12, 160, 19], fill=WHITE)
    draw.ellipse([156, 13, 159, 18], fill=BLACK)
    draw.ellipse([157, 14, 158, 17], fill=WHITE)
    
    # Add small Pikachu face decoration
    draw.ellipse([10, 8, 25, 23], fill=PIKACHU_YELLOW)
    draw.ellipse([13, 12, 15, 14], fill=BLACK)  # Eye
    draw.ellipse([20, 12, 22, 14], fill=BLACK)  # Eye
    draw.ellipse([11, 16, 14, 19], fill=RED)    # Cheek
    draw.ellipse([21, 16, 24, 19], fill=RED)    # Cheek
    
    img.save(os.path.join(gui_path, "vending_machine.png"))
    print("Created vending_machine.png GUI texture (176x166)")

if __name__ == "__main__":
    print(f"Creating high-resolution Pokemon vending machine textures ({TEXTURE_SIZE}x{TEXTURE_SIZE})...")
    create_front_texture()
    create_side_texture()
    create_top_texture()
    create_gui_texture()
    print("\nAll textures created successfully!")
    print("The textures have been saved to:")
    print(f"  - {texture_path}/ (Block textures at {TEXTURE_SIZE}x{TEXTURE_SIZE})")
    print(f"  - {gui_path}/ (GUI texture at 176x166)")
    print("\nNote: These are high-resolution textures (8x vanilla resolution).")
    print("They will work perfectly in Minecraft and scale down automatically!")