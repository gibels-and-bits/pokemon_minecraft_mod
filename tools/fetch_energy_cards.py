#!/usr/bin/env python3
"""
Fetch energy cards for specific Pokemon TCG sets
"""

import requests
import json
import time
from pathlib import Path
import urllib.request

# API Configuration
API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
API_BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

def fetch_energy_cards(set_id, set_name, output_folder):
    """Fetch energy cards from a specific set"""
    print(f"\nFetching energy cards from {set_name} ({set_id})...")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path(f"raw_images/cards/{output_folder}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Search for energy cards in this set
    url = f"{API_BASE_URL}/cards"
    params = {
        "q": f"set.id:{set_id} supertype:Energy",
        "pageSize": 250,
        "orderBy": "number"
    }
    
    try:
        print("Searching for energy cards...")
        response = requests.get(url, headers=HEADERS, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        cards = data.get('data', [])
        
        if not cards:
            print(f"No energy cards found in {set_name}")
            return 0
        
        print(f"Found {len(cards)} energy cards")
        
        downloaded = 0
        energy_metadata = []
        
        for card in cards:
            card_name = card['name'].replace('/', '-').replace(':', '')
            card_number = card.get('number', 'unknown')
            card_rarity = card.get('rarity', 'unknown')
            card_subtype = card.get('subtypes', [''])[0] if card.get('subtypes') else 'Basic'
            
            # Get image URL
            images = card.get('images', {})
            image_url = images.get('large') or images.get('small')
            
            if image_url:
                # Create filename for energy cards
                filename = f"{card_number:0>3}_energy_{card_subtype.lower()}_{card_name}.png"
                output_path = output_dir / filename
                
                if not output_path.exists():
                    try:
                        print(f"  Downloading: {card_name} ({card_subtype} Energy)")
                        urllib.request.urlretrieve(image_url, output_path)
                        downloaded += 1
                        time.sleep(0.3)  # Rate limiting
                    except Exception as e:
                        print(f"    Error: {e}")
                else:
                    print(f"  Already exists: {card_name}")
                    downloaded += 1
            
            # Store metadata
            energy_metadata.append({
                'id': card['id'],
                'name': card['name'],
                'number': card_number,
                'rarity': card_rarity,
                'supertype': card.get('supertype'),
                'subtypes': card.get('subtypes', []),
                'set_name': set_name,
                'set_id': set_id,
                'image_url': image_url
            })
        
        # Save energy metadata
        metadata_file = output_dir / "energy_cards_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump({
                'set_name': set_name,
                'set_id': set_id,
                'total_energy_cards': len(energy_metadata),
                'downloaded': downloaded,
                'energy_cards': energy_metadata
            }, f, indent=2)
        
        print(f"\n✓ Downloaded {downloaded} energy cards")
        print(f"✓ Saved to: {output_dir}")
        
        return downloaded
        
    except Exception as e:
        print(f"Error: {e}")
        return 0

def main():
    print("=" * 60)
    print("Pokemon TCG Energy Card Fetcher")
    print("=" * 60)
    
    # Fetch energy cards for Black Bolt
    black_bolt_count = fetch_energy_cards("zsv10pt5", "Black Bolt", "black_bolt")
    
    # Fetch energy cards for White Flare
    white_flare_count = fetch_energy_cards("rsv10pt5", "White Flare", "white_flare")
    
    # Also check if there are any special energy cards in these sets
    print("\nChecking for special energy cards...")
    
    # Search for special energies
    url = f"{API_BASE_URL}/cards"
    params = {
        "q": '(set.id:zsv10pt5 OR set.id:rsv10pt5) subtypes:"Special"',
        "pageSize": 250
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        special_cards = data.get('data', [])
        
        if special_cards:
            print(f"Found {len(special_cards)} special energy cards:")
            for card in special_cards:
                print(f"  - {card['name']} from {card.get('set', {}).get('name', 'Unknown')}")
    except Exception as e:
        print(f"Error checking special energies: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Black Bolt energy cards: {black_bolt_count}")
    print(f"✓ White Flare energy cards: {white_flare_count}")
    print(f"✓ Total energy cards downloaded: {black_bolt_count + white_flare_count}")

if __name__ == "__main__":
    main()