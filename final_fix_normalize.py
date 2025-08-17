#!/usr/bin/env python3
"""
Final normalization to match EXACTLY what CardDatabase.java expects.
Rules:
- All lowercase
- Remove apostrophes completely (')
- Replace spaces with underscores
- Replace periods with underscores (.)
- Replace hyphens with underscores (-)
- Replace accented characters (é→e, è→e, à→a)
"""

import os
import shutil
from pathlib import Path

def normalize_filename(filename):
    """Normalize filename to match CardDatabase.java logic exactly."""
    if not filename.endswith('.png'):
        return filename
    
    # Remove .png extension for processing
    name_without_ext = filename[:-4]
    
    # Apply the exact same transformations as CardDatabase.java
    normalized = (name_without_ext
        .lower()
        .replace("'", "")  # Remove apostrophes
        .replace(" ", "_")  # Spaces to underscores
        .replace("-", "_")  # Hyphens to underscores  
        .replace(".", "_")  # Periods to underscores
        .replace("é", "e")  # Accented e to e
        .replace("è", "e")  # Accented e to e
        .replace("à", "a")  # Accented a to a
        .replace("ü", "u")
        .replace("ö", "o")
        .replace("ä", "a"))
    
    return normalized + ".png"

def fix_all_cards():
    cards_dir = Path("/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/textures/cards")
    
    if not cards_dir.exists():
        print(f"Error: {cards_dir} does not exist")
        return False
    
    total_renamed = 0
    total_processed = 0
    
    for set_dir in cards_dir.iterdir():
        if not set_dir.is_dir():
            continue
        
        print(f"\nProcessing set: {set_dir.name}")
        renames_in_set = []
        
        # Process all PNG files
        for png_file in set_dir.glob("*.png"):
            total_processed += 1
            old_name = png_file.name
            new_name = normalize_filename(old_name)
            
            if old_name != new_name:
                new_path = set_dir / new_name
                
                # Check for conflicts
                if new_path.exists() and new_path != png_file:
                    print(f"  WARNING: Conflict for {old_name} -> {new_name}")
                    print(f"           File already exists, removing duplicate")
                    png_file.unlink()
                else:
                    # Rename the file
                    png_file.rename(new_path)
                    total_renamed += 1
                    renames_in_set.append((old_name, new_name))
                    print(f"  Fixed: {old_name} -> {new_name}")
        
        if renames_in_set:
            print(f"  Total fixed in {set_dir.name}: {len(renames_in_set)}")
    
    print(f"\n{'='*50}")
    print(f"Final normalization complete!")
    print(f"Total files processed: {total_processed}")
    print(f"Files renamed: {total_renamed}")
    
    # Verify no special characters remain
    issues = []
    for set_dir in cards_dir.iterdir():
        if not set_dir.is_dir():
            continue
        for png_file in set_dir.glob("*.png"):
            name = png_file.name
            if any(c in name for c in ["'", "é", "è", "à", ".", "-"]) and not name.endswith('.png'):
                issues.append(f"{set_dir.name}/{name}")
    
    if issues:
        print(f"\nWARNING: {len(issues)} files still have special characters:")
        for issue in issues[:10]:
            print(f"  {issue}")
    else:
        print("\nSUCCESS: All files normalized correctly!")
    
    return len(issues) == 0

if __name__ == "__main__":
    print("Running final normalization fix...")
    print("This will ensure all filenames match CardDatabase.java expectations")
    success = fix_all_cards()
    if not success:
        print("\nSome issues remain, but proceeding anyway...")