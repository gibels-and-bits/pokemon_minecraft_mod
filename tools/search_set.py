#!/usr/bin/env python3
"""
Search for a specific Pokemon TCG set and get full information
"""

import requests
import json
import time
from pathlib import Path
import urllib.request
import sys

# API Configuration
API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
API_BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

def search_sets(search_term):
    """Search for sets matching a term"""
    print(f"Searching for sets matching: '{search_term}'")
    print("=" * 60)
    
    url = f"{API_BASE_URL}/sets"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=60)
        response.raise_for_status()
        data = response.json()
        sets = data.get('data', [])
        
        matches = []
        for set_data in sets:
            name_lower = set_data['name'].lower()
            if search_term.lower() in name_lower:
                matches.append(set_data)
                print(f"\nFound: {set_data['name']}")
                print(f"  ID: {set_data['id']}")
                print(f"  Series: {set_data.get('series', 'N/A')}")
                print(f"  Release: {set_data.get('releaseDate', 'N/A')}")
                print(f"  Total Cards: {set_data.get('total', 'N/A')}")
                print(f"  Printed Total: {set_data.get('printedTotal', 'N/A')}")
        
        if not matches:
            # Try broader search in recent sets
            print("\nNo exact match. Checking recent sets (2023-2024)...")
            for set_data in sets:
                release = set_data.get('releaseDate', '')
                if '2023' in release or '2024' in release:
                    print(f"\n{set_data['name']}")
                    print(f"  ID: {set_data['id']}")
                    print(f"  Release: {release}")
                    print(f"  Total Cards: {set_data.get('total', 'N/A')}")
        
        return matches
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_all_cards_from_set(set_id, set_name=None):
    """Fetch ALL cards from a specific set"""
    print(f"\nFetching ALL cards from set: {set_id}")
    if set_name:
        print(f"Set name: {set_name}")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path(f"raw_images/cards/{set_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_cards = []
    page = 1
    total_downloaded = 0
    rarity_counts = {}
    
    while True:
        url = f"{API_BASE_URL}/cards"
        params = {
            "q": f"set.id:{set_id}",
            "page": page,
            "pageSize": 250,
            "orderBy": "number"
        }
        
        try:
            print(f"\nFetching page {page}...")
            response = requests.get(url, headers=HEADERS, params=params, timeout=60)
            
            # Check if we got a 400 error (bad set ID)
            if response.status_code == 400:
                print(f"Invalid set ID: {set_id}")
                # Try searching by set name instead
                if set_name:
                    params["q"] = f"set.name:\"{set_name}\""
                    response = requests.get(url, headers=HEADERS, params=params, timeout=60)
            
            response.raise_for_status()
            data = response.json()
            cards = data.get('data', [])
            
            if not cards:
                break
            
            print(f"  Found {len(cards)} cards on page {page}")
            
            # Process each card
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
                            print(f"    Downloading [{total_downloaded + 1}]: {card_name} ({card_rarity})")
                            urllib.request.urlretrieve(image_url, output_path)
                            total_downloaded += 1
                            time.sleep(0.3)  # Rate limiting
                        except Exception as e:
                            print(f"      Error: {e}")
                    else:
                        total_downloaded += 1
                
                all_cards.append({
                    'id': card['id'],
                    'name': card['name'],
                    'number': card_number,
                    'rarity': card_rarity,
                    'types': card.get('types', []),
                    'hp': card.get('hp'),
                    'artist': card.get('artist'),
                    'set_name': card.get('set', {}).get('name', ''),
                    'set_id': card.get('set', {}).get('id', ''),
                    'image_url': image_url
                })
            
            # Check if there are more pages
            if len(cards) < 250:
                break
            
            page += 1
            time.sleep(1)  # Rate limiting between pages
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    
    # Save metadata
    if all_cards:
        metadata_file = output_dir / "cards_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump({
                'set_id': set_id,
                'total_cards': len(all_cards),
                'downloaded': total_downloaded,
                'rarity_distribution': rarity_counts,
                'cards': all_cards
            }, f, indent=2)
        
        print(f"\n" + "=" * 60)
        print(f"COMPLETE!")
        print(f"  Total cards found: {len(all_cards)}")
        print(f"  Downloaded: {total_downloaded}")
        print(f"  Location: {output_dir}")
        
        print(f"\nRarity Distribution:")
        for rarity, count in sorted(rarity_counts.items()):
            percentage = (count / len(all_cards)) * 100
            print(f"  • {rarity}: {count} cards ({percentage:.1f}%)")
    else:
        print("No cards found for this set")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python search_set.py <search_term>  # Search for sets")
        print("  python search_set.py --fetch <set_id> [set_name]  # Fetch all cards from set")
        return
    
    if sys.argv[1] == "--fetch":
        if len(sys.argv) < 3:
            print("Please provide a set ID")
            return
        set_id = sys.argv[2]
        set_name = sys.argv[3] if len(sys.argv) > 3 else None
        fetch_all_cards_from_set(set_id, set_name)
    else:
        search_term = " ".join(sys.argv[1:])
        search_sets(search_term)

if __name__ == "__main__":
    main()