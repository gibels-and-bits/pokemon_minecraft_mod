#!/usr/bin/env python3
"""
Fetch card artwork for a single Pokemon TCG set with rarity tracking
"""

import requests
import json
import time
import sys
from pathlib import Path
import urllib.request

# API Configuration
API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
API_BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

# Updated set mappings based on actual Pokemon TCG sets
SET_MAPPING = {
    "151": "sv3pt5",      # Scarlet & Violet - 151
    "black_bolt": "swsh12pt5",  # Crown Zenith (Black Bolt related)
    "brilliant_stars": "swsh9",   # Brilliant Stars
    "celebrations": "cel25",      # Celebrations
    "destined_rivals": "swsh10",  # Astral Radiance
    "generations": "g1",          # Generations
    "groudon": "xy5",            # Primal Clash
    "journey_together": "sv1",    # Scarlet & Violet Base
    "kyogre": "xy5",             # Primal Clash
    "prismatic_evolutions": "sv8", # Prismatic Evolutions (if exists)
    "surging_sparks": "sv8",      # Surging Sparks
    "white_flare": "sv6"          # Twilight Masquerade or similar
}

def fetch_and_download_set(set_name, limit=None):
    """Fetch and download cards for a specific set"""
    
    if set_name not in SET_MAPPING:
        print(f"Unknown set: {set_name}")
        print(f"Available sets: {', '.join(SET_MAPPING.keys())}")
        return
    
    set_id = SET_MAPPING[set_name]
    print(f"Fetching {set_name} (API ID: {set_id})...")
    
    # Create output directory
    output_dir = Path(f"raw_images/cards/{set_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch cards - try by set name first
    url = f"{API_BASE_URL}/cards"
    params = {
        "q": f"set.name:*{set_name}*",
        "pageSize": limit if limit else 250,
        "orderBy": "set.releaseDate,number"
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        cards = data.get('data', [])
        
        if not cards:
            print(f"No cards found for set {set_id}")
            return
        
        print(f"Found {len(cards)} cards")
        
        # Analyze rarity distribution
        rarity_counts = {}
        card_metadata = []
        downloaded = 0
        
        for i, card in enumerate(cards, 1):
            card_name = card['name'].replace('/', '-').replace(':', '')
            card_number = card.get('number', 'unknown')
            card_rarity = card.get('rarity', 'unknown')
            
            # Track rarity
            rarity_counts[card_rarity] = rarity_counts.get(card_rarity, 0) + 1
            
            # Get image URL
            images = card.get('images', {})
            image_url = images.get('large') or images.get('small')
            
            if image_url:
                # Create filename with rarity
                rarity_prefix = card_rarity.replace(' ', '_').lower()
                filename = f"{card_number:0>3}_{rarity_prefix}_{card_name}.png"
                output_path = output_dir / filename
                
                if not output_path.exists():
                    try:
                        print(f"  Downloading [{i}/{len(cards)}]: {card_name} ({card_rarity})")
                        urllib.request.urlretrieve(image_url, output_path)
                        downloaded += 1
                        time.sleep(0.3)  # Rate limiting
                    except Exception as e:
                        print(f"    Error: {e}")
                else:
                    downloaded += 1
            
            # Store metadata
            card_metadata.append({
                'id': card['id'],
                'name': card['name'],
                'number': card_number,
                'rarity': card_rarity,
                'types': card.get('types', []),
                'hp': card.get('hp'),
                'artist': card.get('artist'),
                'set_name': card.get('set', {}).get('name', ''),
                'image_url': image_url
            })
        
        # Save metadata
        metadata_file = output_dir / "cards_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump({
                'set_name': set_name,
                'set_id': set_id,
                'total_cards': len(card_metadata),
                'downloaded': downloaded,
                'rarity_distribution': rarity_counts,
                'cards': card_metadata
            }, f, indent=2)
        
        print(f"\n✓ Downloaded {downloaded}/{len(cards)} cards")
        print(f"✓ Saved to: {output_dir}")
        print("\nRarity Distribution:")
        for rarity, count in sorted(rarity_counts.items()):
            print(f"  - {rarity}: {count} cards")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_single_set.py <set_name> [limit]")
        print(f"Available sets: {', '.join(SET_MAPPING.keys())}")
        print("\nExample: python fetch_single_set.py celebrations 10")
        return
    
    set_name = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    fetch_and_download_set(set_name, limit)

if __name__ == "__main__":
    main()