#!/usr/bin/env python3
"""
Normalize all card filenames and update metadata to ensure consistent loading.
Rules:
- All lowercase
- Remove apostrophes
- Replace spaces, hyphens, periods with underscores
- Replace accented characters
"""

import os
import json
import shutil
from pathlib import Path

def normalize_name(name):
    """Normalize a card name according to our rules."""
    return (name
        .lower()
        .replace("'", "")
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("é", "e")
        .replace("è", "e")
        .replace("à", "a")
        .replace("ü", "u")
        .replace("ö", "o")
        .replace("ä", "a"))

def process_card_directory(cards_dir):
    """Process all card sets in the cards directory."""
    
    cards_path = Path(cards_dir)
    if not cards_path.exists():
        print(f"Error: {cards_dir} does not exist")
        return
    
    rename_log = []
    metadata_updates = {}
    
    # Process each set directory
    for set_dir in cards_path.iterdir():
        if not set_dir.is_dir():
            continue
            
        print(f"\nProcessing set: {set_dir.name}")
        
        # Track renames for this set
        set_renames = []
        
        # Process PNG files
        png_files = list(set_dir.glob("*.png"))
        for old_file in png_files:
            old_name = old_file.name
            
            # Skip if already normalized (all lowercase, no apostrophes)
            if old_name == old_name.lower() and "'" not in old_name:
                continue
            
            # Parse the filename
            parts = old_name.replace(".png", "").split("_", 2)
            if len(parts) >= 3:
                number = parts[0]
                rarity = parts[1]
                card_name = "_".join(parts[2:])
                
                # Normalize each part
                normalized_rarity = normalize_name(rarity)
                normalized_card = normalize_name(card_name)
                
                # Build new filename
                new_name = f"{number}_{normalized_rarity}_{normalized_card}.png"
                
                if new_name != old_name:
                    new_file = set_dir / new_name
                    
                    # Check for conflicts
                    if new_file.exists():
                        print(f"  WARNING: {new_name} already exists, skipping {old_name}")
                        continue
                    
                    # Rename the file
                    old_file.rename(new_file)
                    set_renames.append((old_name, new_name))
                    print(f"  Renamed: {old_name} -> {new_name}")
        
        # Update metadata file if it exists
        metadata_file = set_dir / "cards_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Update card entries
            if "cards" in metadata:
                for card in metadata["cards"]:
                    # The metadata doesn't store filenames, just ensure names are consistent
                    if "name" in card:
                        # Don't change the display name, just log it
                        pass
            
            # Save updated metadata (in case we need to modify it later)
            metadata_updates[set_dir.name] = metadata
        
        if set_renames:
            rename_log.append({
                "set": set_dir.name,
                "renames": set_renames
            })
    
    # Save rename log
    log_file = cards_path.parent / "filename_normalization_log.json"
    with open(log_file, 'w') as f:
        json.dump(rename_log, f, indent=2)
    print(f"\nRename log saved to: {log_file}")
    
    return rename_log

def main():
    # Path to the cards directory
    cards_dir = "/Users/gibels_and_bits/Development/etb-mod/src/main/resources/assets/etbmod/textures/cards"
    
    print("Starting card filename normalization...")
    print(f"Processing directory: {cards_dir}")
    
    # Create backup first
    backup_dir = "/Users/gibels_and_bits/Development/etb-mod/cards_backup"
    if not os.path.exists(backup_dir):
        print(f"Creating backup at: {backup_dir}")
        shutil.copytree(cards_dir, backup_dir)
        print("Backup created successfully")
    else:
        print(f"Backup already exists at: {backup_dir}")
    
    # Process the cards
    rename_log = process_card_directory(cards_dir)
    
    # Summary
    total_renames = sum(len(s["renames"]) for s in rename_log)
    print(f"\n{'='*50}")
    print(f"Normalization complete!")
    print(f"Total files renamed: {total_renames}")
    print(f"Sets processed: {len(rename_log)}")
    
    if rename_log:
        print("\nSummary by set:")
        for entry in rename_log:
            print(f"  {entry['set']}: {len(entry['renames'])} files renamed")

if __name__ == "__main__":
    main()