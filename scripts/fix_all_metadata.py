#!/usr/bin/env python3
"""
Fix ALL metadata files to ensure consistent format and correct rarity strings.
This ensures all sets work properly with the texture loading system.
"""

import json
import os
from pathlib import Path

def normalize_rarity(rarity_str):
    """Normalize rarity string to match expected format."""
    if not rarity_str:
        return "common"
    
    # Convert to lowercase and normalize
    rarity = rarity_str.lower().strip()
    
    # Map various rarity formats to standard ones
    rarity_map = {
        "common": "common",
        "uncommon": "uncommon",
        "rare": "rare",
        "rare holo": "rare holo",
        "rare_holo": "rare holo",
        "double rare": "double rare",
        "double_rare": "double rare",
        "ultra rare": "ultra rare",
        "ultra_rare": "ultra rare",
        "illustration rare": "illustration rare",
        "illustration_rare": "illustration rare",
        "special illustration rare": "special illustration rare",
        "special_illustration_rare": "special illustration rare",
        "rare holo ex": "rare holo ex",
        "rare_holo_ex": "rare holo ex",
        "rare holo v": "rare holo v",
        "rare_holo_v": "rare holo v",
        "rare holo vmax": "rare holo vmax",
        "rare_holo_vmax": "rare holo vmax",
        "rare holo vstar": "rare holo vstar",
        "rare_holo_vstar": "rare holo vstar",
        "rare break": "rare break",
        "rare_break": "rare break",
        "rare secret": "rare secret",
        "rare_secret": "rare secret",
        "rare ultra": "rare ultra",
        "rare_ultra": "rare ultra",
        "trainer gallery rare holo": "trainer gallery rare holo",
        "trainer_gallery_rare_holo": "trainer gallery rare holo",
        "classic collection": "classic collection",
        "classic_collection": "classic collection",
        "promo": "promo",
        "black white rare": "black white rare",
        "black_white_rare": "black white rare"
    }
    
    # Check for exact match first
    if rarity in rarity_map:
        return rarity_map[rarity]
    
    # Check with underscores replaced by spaces
    rarity_spaces = rarity.replace("_", " ")
    if rarity_spaces in rarity_map:
        return rarity_map[rarity_spaces]
    
    # Default to original if no match found
    return rarity

def fix_metadata_file(metadata_path, set_name):
    """Fix a single metadata file to ensure correct format."""
    
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  {set_name}: Error reading file - {e}")
        return False
    
    # Ensure we have a cards array
    if 'cards' not in data:
        print(f"  {set_name}: No 'cards' array found")
        return False
    
    fixed_cards = []
    cards = data.get('cards', [])
    
    if not cards:
        print(f"  {set_name}: Empty cards array")
        return False
    
    for idx, card in enumerate(cards):
        # Extract data from various possible formats
        number = str(card.get('number', idx + 1))
        name = card.get('name', f'Card {number}')
        
        # Get and normalize rarity
        original_rarity = card.get('rarity', 'common')
        rarity = normalize_rarity(original_rarity)
        
        # Create or update card ID
        card_id = card.get('id', f"{set_name}-{number.zfill(3)}")
        if not card_id.startswith(set_name):
            card_id = f"{set_name}-{number.zfill(3)}"
        
        fixed_card = {
            "id": card_id,
            "name": name,
            "number": number,
            "rarity": rarity
        }
        
        fixed_cards.append(fixed_card)
    
    # Create fixed metadata
    fixed_metadata = {
        "cards": fixed_cards
    }
    
    # Write back
    try:
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(fixed_metadata, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  {set_name}: Error writing file - {e}")
        return False

def verify_file_names(set_dir, metadata):
    """Verify that actual file names match what the metadata expects."""
    issues = []
    
    for card in metadata.get('cards', []):
        number = card['number']
        name = card['name']
        rarity = card['rarity']
        
        # Build expected filename (matching CardDatabase.java logic)
        clean_name = name.lower()
        clean_name = clean_name.replace("'", "").replace(" ", "_").replace("-", "_")
        clean_name = clean_name.replace(".", "_").replace("é", "e").replace("è", "e").replace("à", "a")
        
        # Handle special characters in Pokemon names
        clean_name = clean_name.replace("♀", "f").replace("♂", "m")
        clean_name = clean_name.replace(":", "").replace(",", "").replace("!", "")
        clean_name = clean_name.replace("(", "").replace(")", "")
        clean_name = clean_name.replace("'", "").replace('"', "")
        
        # Build expected filename
        num_padded = str(number).zfill(3)
        rarity_file = rarity.lower().replace(" ", "_")
        expected_file = f"{num_padded}_{rarity_file}_{clean_name}.png"
        
        # Check if file exists
        file_path = set_dir / expected_file
        if not file_path.exists():
            # Try to find a similar file
            pattern = f"{num_padded}_*"
            similar = list(set_dir.glob(pattern + "*.png"))
            if similar:
                actual = similar[0].name
                if actual != expected_file:
                    issues.append(f"    Expected: {expected_file}")
                    issues.append(f"    Found:    {actual}")
            else:
                issues.append(f"    Missing: {expected_file}")
    
    return issues

def main():
    # Path to card textures
    cards_dir = Path("src/main/resources/assets/etbmod/textures/cards")
    
    if not cards_dir.exists():
        print(f"Cards directory not found: {cards_dir}")
        return
    
    print("Fixing ALL metadata files for proper texture loading...")
    print("=" * 60)
    
    fixed_count = 0
    total_count = 0
    sets_with_issues = []
    
    # Process each set directory
    for set_dir in sorted(cards_dir.iterdir()):
        if not set_dir.is_dir():
            continue
        
        set_name = set_dir.name
        metadata_path = set_dir / "cards_metadata.json"
        
        if not metadata_path.exists():
            print(f"  {set_name}: No metadata file - SKIPPING")
            sets_with_issues.append(set_name)
            continue
        
        total_count += 1
        
        # Fix the metadata
        if fix_metadata_file(metadata_path, set_name):
            fixed_count += 1
            print(f"  {set_name}: ✓ Fixed metadata")
            
            # Verify file names match
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            issues = verify_file_names(set_dir, metadata)
            if issues:
                print(f"    WARNING: File name mismatches detected:")
                for issue in issues[:5]:  # Show first 5 issues
                    print(f"      {issue}")
                if len(issues) > 5:
                    print(f"      ... and {len(issues) - 5} more issues")
                sets_with_issues.append(set_name)
        else:
            print(f"  {set_name}: ✗ Failed to fix")
            sets_with_issues.append(set_name)
    
    print("=" * 60)
    print(f"Summary: Fixed {fixed_count}/{total_count} metadata files")
    
    if sets_with_issues:
        print(f"\nSets with issues: {', '.join(sets_with_issues)}")
    else:
        print("\nAll sets processed successfully!")
    
    # Final verification
    print("\nFinal verification of metadata structure...")
    all_valid = True
    
    for set_dir in sorted(cards_dir.iterdir()):
        if not set_dir.is_dir():
            continue
        
        metadata_path = set_dir / "cards_metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r') as f:
                    data = json.load(f)
                    cards = data.get('cards', [])
                    if cards:
                        first_card = cards[0]
                        has_id = 'id' in first_card
                        has_name = 'name' in first_card  
                        has_number = 'number' in first_card
                        has_rarity = 'rarity' in first_card
                        
                        if not (has_id and has_name and has_number and has_rarity):
                            print(f"  {set_dir.name}: INVALID - Missing required fields")
                            all_valid = False
                    else:
                        print(f"  {set_dir.name}: EMPTY - No cards in metadata")
                        all_valid = False
            except Exception as e:
                print(f"  {set_dir.name}: ERROR - {e}")
                all_valid = False
    
    if all_valid:
        print("  ✓ All metadata files have correct structure!")

if __name__ == "__main__":
    main()