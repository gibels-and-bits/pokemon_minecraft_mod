#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Source directory with new cards from API
NEW_CARDS_DIR = "cards"

# Target directories to update
TARGET_DIRS = [
    "src/main/resources/assets/etbmod/textures/cards",
    "raw_images/cards"
]

def replace_cards(set_name):
    """Replace old cards with new ones from API"""
    
    source_dir = os.path.join(NEW_CARDS_DIR, set_name)
    
    if not os.path.exists(source_dir):
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    # Get all new card files
    new_cards = os.listdir(source_dir)
    print(f"\n📦 Processing {set_name}: {len(new_cards)} cards")
    
    for target_base in TARGET_DIRS:
        target_dir = os.path.join(target_base, set_name)
        
        if not os.path.exists(target_dir):
            print(f"  ⚠️ Target directory not found: {target_dir}")
            continue
            
        print(f"\n  📂 Updating: {target_dir}")
        
        # First, backup and remove old cards
        old_cards = os.listdir(target_dir)
        for old_card in old_cards:
            if old_card.endswith('.png'):
                old_path = os.path.join(target_dir, old_card)
                os.remove(old_path)
        print(f"    ✓ Removed {len(old_cards)} old cards")
        
        # Copy new cards with lowercase filenames
        copied = 0
        for new_card in new_cards:
            if new_card.endswith('.png'):
                source_path = os.path.join(source_dir, new_card)
                # Convert filename to lowercase to match old convention
                target_filename = new_card.lower()
                target_path = os.path.join(target_dir, target_filename)
                
                shutil.copy2(source_path, target_path)
                copied += 1
        
        print(f"    ✓ Copied {copied} new cards")

def main():
    print("🔄 Replacing Black Bolt and White Flare cards with API versions")
    print("=" * 60)
    
    # Process both sets
    replace_cards("black_bolt")
    replace_cards("white_flare")
    
    # Also update build directory if it exists
    build_dir = "build/resources/main/assets/etbmod/textures/cards"
    if os.path.exists(build_dir):
        print(f"\n📂 Also updating build directory: {build_dir}")
        
        for set_name in ["black_bolt", "white_flare"]:
            source_dir = os.path.join(NEW_CARDS_DIR, set_name)
            target_dir = os.path.join(build_dir, set_name)
            
            if os.path.exists(source_dir) and os.path.exists(target_dir):
                # Clear old cards
                for old_card in os.listdir(target_dir):
                    if old_card.endswith('.png'):
                        os.remove(os.path.join(target_dir, old_card))
                
                # Copy new cards with lowercase names
                for new_card in os.listdir(source_dir):
                    if new_card.endswith('.png'):
                        source_path = os.path.join(source_dir, new_card)
                        target_path = os.path.join(target_dir, new_card.lower())
                        shutil.copy2(source_path, target_path)
                
                print(f"  ✓ Updated {set_name} in build directory")
    
    print("\n" + "=" * 60)
    print("✅ Card replacement complete!")
    print("\nOld card locations have been updated with new API cards:")
    print("  • src/main/resources/assets/etbmod/textures/cards/black_bolt/")
    print("  • src/main/resources/assets/etbmod/textures/cards/white_flare/")
    print("  • raw_images/cards/black_bolt/")
    print("  • raw_images/cards/white_flare/")
    if os.path.exists(build_dir):
        print("  • build/resources/main/assets/etbmod/textures/cards/black_bolt/")
        print("  • build/resources/main/assets/etbmod/textures/cards/white_flare/")

if __name__ == "__main__":
    main()