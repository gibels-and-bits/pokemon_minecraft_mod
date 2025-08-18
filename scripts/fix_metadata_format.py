#!/usr/bin/env python3
"""
Fix metadata format inconsistencies across all card sets.
Ensures all sets use the same metadata structure as black_bolt.
"""

import json
import os
from pathlib import Path

def fix_metadata_format(metadata_path, set_name):
    """Fix metadata format to match expected structure."""
    
    with open(metadata_path, 'r') as f:
        data = json.load(f)
    
    # Check if already in correct format
    if data.get('cards') and len(data['cards']) > 0:
        first_card = data['cards'][0]
        if 'id' in first_card:
            print(f"  {set_name}: Already in correct format")
            return False
    
    # Convert to correct format
    fixed_cards = []
    cards = data.get('cards', [])
    
    for card in cards:
        # Extract data from either format
        number = str(card.get('number', ''))
        name = card.get('name', '')
        rarity = card.get('rarity', 'common')
        
        # Normalize rarity format (remove underscores, lowercase)
        rarity = rarity.lower().replace('_', ' ')
        
        # Create card ID
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
    with open(metadata_path, 'w') as f:
        json.dump(fixed_metadata, f, indent=2)
    
    print(f"  {set_name}: Fixed {len(fixed_cards)} cards")
    return True

def main():
    # Path to card textures
    cards_dir = Path("src/main/resources/assets/etbmod/textures/cards")
    
    if not cards_dir.exists():
        print(f"Cards directory not found: {cards_dir}")
        return
    
    print("Fixing metadata format for all card sets...")
    
    fixed_count = 0
    total_count = 0
    
    # Process each set directory
    for set_dir in sorted(cards_dir.iterdir()):
        if not set_dir.is_dir():
            continue
        
        set_name = set_dir.name
        metadata_path = set_dir / "cards_metadata.json"
        
        if not metadata_path.exists():
            print(f"  {set_name}: No metadata file found")
            continue
        
        total_count += 1
        
        try:
            if fix_metadata_format(metadata_path, set_name):
                fixed_count += 1
        except Exception as e:
            print(f"  {set_name}: Error - {e}")
    
    print(f"\nSummary: Fixed {fixed_count}/{total_count} metadata files")
    
    # Verify all files now have consistent structure
    print("\nVerifying metadata structure...")
    for set_dir in sorted(cards_dir.iterdir()):
        if not set_dir.is_dir():
            continue
        
        metadata_path = set_dir / "cards_metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                data = json.load(f)
                cards = data.get('cards', [])
                if cards:
                    has_id = 'id' in cards[0]
                    has_name = 'name' in cards[0]
                    has_number = 'number' in cards[0]
                    has_rarity = 'rarity' in cards[0]
                    
                    if not (has_id and has_name and has_number and has_rarity):
                        print(f"  {set_dir.name}: MISSING FIELDS - id:{has_id} name:{has_name} number:{has_number} rarity:{has_rarity}")

if __name__ == "__main__":
    main()