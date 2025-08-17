#!/usr/bin/env python3
"""
Fix the failed normalization - properly rename ALL files to lowercase.
This script will handle duplicates and conflicts.
"""

import os
import shutil
from pathlib import Path

def normalize_all_cards():
    cards_dir = Path("/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/textures/cards")
    
    if not cards_dir.exists():
        print(f"Error: {cards_dir} does not exist")
        return
    
    total_renamed = 0
    total_processed = 0
    
    for set_dir in cards_dir.iterdir():
        if not set_dir.is_dir():
            continue
        
        print(f"\nProcessing set: {set_dir.name}")
        set_renames = []
        
        # First pass: collect all files that need renaming
        files_to_rename = []
        for png_file in set_dir.glob("*.png"):
            total_processed += 1
            new_name = png_file.name.lower()
            
            if png_file.name != new_name:
                files_to_rename.append((png_file, new_name))
        
        # Second pass: handle renames
        for old_file, new_name in files_to_rename:
            new_file = set_dir / new_name
            
            # If lowercase version exists, remove it first (it's likely a duplicate)
            if new_file.exists() and new_file != old_file:
                print(f"  Removing duplicate: {new_name}")
                new_file.unlink()
            
            # Now rename the file
            try:
                old_file.rename(new_file)
                total_renamed += 1
                print(f"  Renamed: {old_file.name} -> {new_name}")
            except Exception as e:
                print(f"  ERROR renaming {old_file.name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Normalization complete!")
    print(f"Total files processed: {total_processed}")
    print(f"Files renamed: {total_renamed}")
    
    # Verify no capitals remain
    remaining_caps = 0
    for set_dir in cards_dir.iterdir():
        if not set_dir.is_dir():
            continue
        for png_file in set_dir.glob("*.png"):
            if png_file.name != png_file.name.lower():
                remaining_caps += 1
                print(f"Still has capitals: {set_dir.name}/{png_file.name}")
    
    if remaining_caps > 0:
        print(f"\nWARNING: {remaining_caps} files still have capital letters!")
    else:
        print("\nSUCCESS: All files are now lowercase!")

if __name__ == "__main__":
    print("Starting aggressive normalization fix...")
    normalize_all_cards()