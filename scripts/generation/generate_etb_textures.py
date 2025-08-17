#!/usr/bin/env python3
"""
Generate Minecraft ETB block textures from processed ETB images.
Creates 6 faces for each ETB block: top, bottom, front, back, left, right.
"""

import os
from PIL import Image
import numpy as np

# Define the ETB sets to process
ETB_SETS = [
    "black_bolt", "breakpoint", "brilliant_stars", "burning_shadows",
    "cosmic_eclipse", "crown_zenith", "evolutions", "evolving_skies",
    "hidden_fates", "phantom_forces", "primal_clash", "prismatic_evolutions",
    "rebel_clash", "shining_fates", "shrouded_fable", "surging_sparks",
    "team_up", "unified_minds", "vivid_voltage", "white_flare",
    "151", "celebrations", "destined_rivals", "generations",
    "journey_together"
]

def create_etb_face_texture(front_img, side_img, face_type, texture_size=256):
    """
    Create a high-resolution texture for a specific face of the ETB block.
    
    Args:
        front_img: PIL Image of the ETB front
        side_img: PIL Image of the ETB side
        face_type: Type of face (top, bottom, front, back, left, right)
        texture_size: Size of the texture (default 256x256 for high quality)
    
    Returns:
        PIL Image: High-resolution texture for the face
    """
    # Create base texture with specified size
    texture = Image.new('RGBA', (texture_size, texture_size), (0, 0, 0, 0))
    
    if face_type == 'front':
        # Use the front image, resize to fit texture_size
        resized = front_img.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        texture = resized
        
    elif face_type == 'back':
        # Mirror the front image for back
        flipped = front_img.transpose(Image.FLIP_LEFT_RIGHT)
        resized = flipped.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        texture = resized
        
    elif face_type in ['left', 'right']:
        # Use the side image for left/right faces
        if side_img.width > 0 and side_img.height > 0:
            # Resize side image to fit texture_size
            resized = side_img.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
            texture = resized
        else:
            # If no side image, create a simplified version from front
            edge_strip = front_img.crop((0, 0, front_img.width // 8, front_img.height))
            resized = edge_strip.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
            texture = resized
            
    elif face_type == 'top':
        # Create top texture from top portion of front image
        top_strip = front_img.crop((0, 0, front_img.width, front_img.height // 4))
        resized = top_strip.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        texture = resized
        
    elif face_type == 'bottom':
        # Create bottom texture from bottom portion of front image
        bottom_strip = front_img.crop((0, front_img.height * 3 // 4, front_img.width, front_img.height))
        resized = bottom_strip.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        texture = resized
    
    return texture

def create_advanced_etb_textures(front_path, side_path, output_dir, texture_size=256):
    """
    Create high-resolution ETB block textures with proper scaling and detail preservation.
    
    Args:
        front_path: Path to the front image
        side_path: Path to the side image
        output_dir: Directory to save the textures
        texture_size: Size of the output textures (default 256x256 for high quality)
    """
    # Load images
    front_img = Image.open(front_path).convert('RGBA')
    side_img = Image.open(side_path).convert('RGBA') if os.path.exists(side_path) else None
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate each face texture
    faces = {
        'front': front_img,
        'back': front_img.transpose(Image.FLIP_LEFT_RIGHT),
        'left': side_img if side_img else front_img,
        'right': side_img if side_img else front_img,
        'top': front_img,
        'bottom': front_img
    }
    
    for face_name, source_img in faces.items():
        if source_img is None:
            continue
            
        # For top and bottom, we'll create a more appropriate texture
        if face_name == 'top':
            # Use top portion of the image
            h = source_img.height
            cropped = source_img.crop((0, 0, source_img.width, h // 3))
            texture = cropped.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        elif face_name == 'bottom':
            # Use bottom portion of the image
            h = source_img.height
            cropped = source_img.crop((0, h * 2 // 3, source_img.width, h))
            texture = cropped.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        else:
            # For front, back, left, right - resize the full image
            texture = source_img.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        
        # Save the texture
        output_path = os.path.join(output_dir, f'etb_{face_name}.png')
        texture.save(output_path, 'PNG')

def main():
    """
    Main function to generate all ETB textures.
    """
    input_dir = "raw_images/etb_views_processed"
    base_output_dir = "src/main/resources/assets/etbmod/textures/block"
    
    print("Generating ETB Block Textures")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for etb_set in ETB_SETS:
        front_path = os.path.join(input_dir, f"{etb_set}_etb_front.png")
        side_path = os.path.join(input_dir, f"{etb_set}_etb_side.png")
        
        if not os.path.exists(front_path):
            print(f"✗ Missing front image for {etb_set}")
            error_count += 1
            continue
        
        # Create output directory for this ETB set
        output_dir = os.path.join(base_output_dir, f"etb_{etb_set}")
        
        try:
            # Generate high-resolution textures (256x256)
            create_advanced_etb_textures(front_path, side_path, output_dir, texture_size=256)
            print(f"✓ Generated high-resolution textures for {etb_set}")
            success_count += 1
        except Exception as e:
            print(f"✗ Error generating {etb_set}: {e}")
            error_count += 1
    
    print("=" * 60)
    print(f"Texture Generation Complete!")
    print(f"Success: {success_count} ETB sets")
    print(f"Errors: {error_count}")
    print(f"Output: {base_output_dir}/etb_*/")

if __name__ == "__main__":
    main()