#!/usr/bin/env python3
"""
Create texture for the Pokemon card item
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_card_texture():
    """Create a 16x16 texture for the Pokemon card item"""
    
    # Create a 16x16 image
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Card background - white with colored border
    # Main card body (white/light gray)
    draw.rectangle([1, 1, 14, 14], fill=(240, 240, 240, 255))
    
    # Colored border (blue for Pokemon card)
    draw.rectangle([0, 0, 15, 0], fill=(0, 100, 200, 255))  # Top
    draw.rectangle([0, 15, 15, 15], fill=(0, 100, 200, 255))  # Bottom
    draw.rectangle([0, 0, 0, 15], fill=(0, 100, 200, 255))  # Left
    draw.rectangle([15, 0, 15, 15], fill=(0, 100, 200, 255))  # Right
    
    # Inner border (darker blue)
    draw.rectangle([1, 1, 14, 1], fill=(0, 70, 150, 255))  # Top
    draw.rectangle([1, 14, 14, 14], fill=(0, 70, 150, 255))  # Bottom
    draw.rectangle([1, 1, 1, 14], fill=(0, 70, 150, 255))  # Left
    draw.rectangle([14, 1, 14, 14], fill=(0, 70, 150, 255))  # Right
    
    # Card artwork area (top half) - gradient effect
    for y in range(2, 8):
        gray_val = 200 - (y - 2) * 10
        draw.rectangle([2, y, 13, y], fill=(gray_val, gray_val + 10, gray_val + 20, 255))
    
    # Small pokeball symbol in center
    center_x, center_y = 8, 5
    # Pokeball circle
    draw.ellipse([center_x-2, center_y-2, center_x+1, center_y+1], 
                 outline=(200, 0, 0, 255), fill=(255, 255, 255, 255))
    # Pokeball center line
    draw.line([center_x-2, center_y, center_x+1, center_y], fill=(50, 50, 50, 255))
    # Pokeball center dot
    draw.point([center_x, center_y], fill=(50, 50, 50, 255))
    
    # Card text area (bottom half) - light with lines
    for y in range(9, 13):
        draw.line([3, y, 12, y], fill=(220, 220, 220, 255))
    
    # Energy symbol in bottom right
    draw.rectangle([11, 11, 12, 12], fill=(255, 200, 0, 255))
    
    # Holographic effect pixels (for rare cards)
    draw.point([3, 3], fill=(180, 220, 255, 255))
    draw.point([12, 3], fill=(255, 180, 220, 255))
    draw.point([3, 12], fill=(220, 255, 180, 255))
    
    # Save the texture
    output_path = Path("src/main/resources/assets/etbmod/textures/item/pokemon_card.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"✓ Created card item texture: {output_path}")
    
    return img

def main():
    print("Creating Pokemon Card Item Texture")
    print("=" * 40)
    
    create_card_texture()
    
    print("\n✓ Card texture created successfully!")

if __name__ == "__main__":
    main()