#!/usr/bin/env python3
"""
Create a simple scissors texture for the ETB mod
"""

from PIL import Image, ImageDraw

def create_scissors_texture():
    # Create a 16x16 transparent image
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    blade_color = (200, 200, 210, 255)  # Light gray/silver
    handle_color = (139, 69, 19, 255)   # Brown
    highlight_color = (255, 255, 255, 255)  # White
    
    # Draw scissor blades (X shape)
    # First blade
    draw.line([(4, 3), (12, 11)], fill=blade_color, width=2)
    draw.line([(3, 3), (11, 11)], fill=blade_color, width=1)
    
    # Second blade
    draw.line([(12, 3), (4, 11)], fill=blade_color, width=2)
    draw.line([(13, 3), (5, 11)], fill=blade_color, width=1)
    
    # Draw handles
    draw.ellipse([(2, 11), (6, 15)], fill=handle_color, outline=blade_color)
    draw.ellipse([(10, 11), (14, 15)], fill=handle_color, outline=blade_color)
    
    # Add highlights
    draw.point((5, 4), fill=highlight_color)
    draw.point((11, 4), fill=highlight_color)
    
    # Center pivot point
    draw.point((8, 7), fill=blade_color)
    draw.point((7, 7), fill=blade_color)
    draw.point((8, 8), fill=blade_color)
    draw.point((7, 8), fill=blade_color)
    
    # Save the texture
    output_path = "src/main/resources/assets/etbmod/textures/item/scissors.png"
    img.save(output_path, "PNG")
    print(f"✓ Created scissors texture at {output_path}")

if __name__ == "__main__":
    create_scissors_texture()