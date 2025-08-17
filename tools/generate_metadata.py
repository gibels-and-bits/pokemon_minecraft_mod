#!/usr/bin/env python3
import os
import json
import re

def parse_card_filename(filename):
    """Parse card info from filename like '001_common_Snivy.png' or '005_double_rare_Whimsicott_ex.png'"""
    # Known multi-word rarities
    multi_word_rarities = [
        'double_rare',
        'illustration_rare', 
        'ultra_rare',
        'special_illustration_rare',
        'black_white_rare',
        'special_energy'
    ]
    
    # First, try to match with multi-word rarities
    for rarity in multi_word_rarities:
        pattern = r'(\d+)_' + rarity + r'_(.+)\.png'
        match = re.match(pattern, filename)
        if match:
            return {
                'number': match.group(1),
                'rarity': rarity.replace('_', ' '),
                'name': match.group(2).replace('_', ' ')
            }
    
    # If no multi-word rarity matched, use single-word pattern
    match = re.match(r'(\d+)_([^_]+)_(.+)\.png', filename)
    if match:
        number = match.group(1)
        rarity = match.group(2)
        name = match.group(3).replace('_', ' ')
        return {
            'number': number,
            'rarity': rarity,
            'name': name
        }
    return None

def generate_metadata_for_set(set_path, set_name):
    """Generate cards_metadata.json for a set"""
    cards = []
    
    for filename in sorted(os.listdir(set_path)):
        if filename.endswith('.png'):
            card_info = parse_card_filename(filename)
            if card_info:
                cards.append({
                    'id': f"{set_name}-{card_info['number']}",
                    'name': card_info['name'],
                    'number': card_info['number'],
                    'rarity': card_info['rarity'].replace('_', ' ')
                })
    
    metadata = {'cards': cards}
    metadata_path = os.path.join(set_path, 'cards_metadata.json')
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Generated metadata for {set_name}: {len(cards)} cards")

def main():
    base_path = 'src/main/resources/assets/etbmod/textures/cards'
    
    # Process each set folder
    for set_folder in os.listdir(base_path):
        set_path = os.path.join(base_path, set_folder)
        if os.path.isdir(set_path):
            generate_metadata_for_set(set_path, set_folder)

if __name__ == '__main__':
    main()