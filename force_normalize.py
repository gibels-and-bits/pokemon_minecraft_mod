#!/usr/bin/env python3
"""
Force normalize all card filenames to lowercase.
This will handle duplicates by removing them.
"""

import os
import shutil
from pathlib import Path

def force_normalize():
    cards_dir = Path("/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/textures/cards")
    
    if not cards_dir.exists():
        print(f"Error: {cards_dir} does not exist")
        return
    
    total_renamed = 0
    total_processed = 0
    duplicates_removed = 0
    
    for set_dir in cards_dir.iterdir():
        if not set_dir.is_dir():
            continue
        
        print(f"\nProcessing set: {set_dir.name}")
        
        # Use a temporary directory for this set to avoid conflicts
        temp_dir = set_dir.parent / f"{set_dir.name}_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        # Process all PNG files
        for png_file in set_dir.glob("*.png"):
            total_processed += 1
            new_name = png_file.name.lower()
            new_path = temp_dir / new_name
            
            # If a file with this name already exists in temp, it's a duplicate
            if new_path.exists():
                print(f"  Duplicate found and skipped: {png_file.name}")
                duplicates_removed += 1
            else:
                # Copy with new name
                shutil.copy2(png_file, new_path)
                if png_file.name != new_name:
                    total_renamed += 1
                    print(f"  Normalized: {png_file.name} -> {new_name}")
        
        # Copy non-PNG files (like metadata)
        for other_file in set_dir.iterdir():
            if not other_file.name.endswith('.png') and other_file.is_file():
                shutil.copy2(other_file, temp_dir / other_file.name)
        
        # Replace original directory with temp
        shutil.rmtree(set_dir)
        temp_dir.rename(set_dir)
    
    print(f"\n{'='*50}")
    print(f"Normalization complete!")
    print(f"Total files processed: {total_processed}")
    print(f"Files renamed to lowercase: {total_renamed}")
    print(f"Duplicates removed: {duplicates_removed}")
    
    # Verify
    remaining_caps = 0
    for set_dir in cards_dir.iterdir():
        if not set_dir.is_dir():
            continue
        for png_file in set_dir.glob("*.png"):
            if png_file.name != png_file.name.lower():
                remaining_caps += 1
                print(f"Still has capitals: {set_dir.name}/{png_file.name}")
    
    if remaining_caps > 0:
        print(f"\nERROR: {remaining_caps} files still have capital letters!")
        return False
    else:
        print("\nSUCCESS: All files are now lowercase!")
        return True

if __name__ == "__main__":
    print("Starting forced normalization...")
    print("This will rename ALL files to lowercase and remove duplicates.")
    success = force_normalize()
    if not success:
        print("\nNormalization failed! Check the errors above.")
    else:
        print("\nNormalization succeeded!")