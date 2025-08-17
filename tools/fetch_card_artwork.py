#!/usr/bin/env python3
"""
Fetch card artwork from pokemontcg.io API for ETB sets
"""

import requests
import json
import time
from pathlib import Path
import urllib.request
from urllib.parse import urlparse

# API Configuration
API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
API_BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

# Map our ETB variants to Pokemon TCG set IDs
# These need to be verified/updated with correct set IDs
SET_MAPPING = {
    "151": "mew1",  # 151 set (Scarlet & Violet)
    "black_bolt": "cel25c",  # Might be a promo or special set
    "brilliant_stars": "swsh9",  # Brilliant Stars
    "celebrations": "cel25",  # Celebrations
    "destined_rivals": "swsh11",  # Silver Tempest or Lost Origin
    "generations": "g1",  # Generations
    "groudon": "xy5",  # Primal Clash (Groudon)
    "journey_together": "sv",  # Journey Together might be base Scarlet & Violet
    "kyogre": "xy5",  # Primal Clash (Kyogre) 
    "prismatic_evolutions": "sv",  # Prismatic Evolutions (special set)
    "surging_sparks": "sv08",  # Surging Sparks
    "white_flare": "sv"  # White Flare might be Japanese exclusive
}

def get_sets_info():
    """Get information about available sets"""
    print("Fetching available sets...")
    url = f"{API_BASE_URL}/sets"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        sets_file = Path("raw_images/cards/sets_info.json")
        sets_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(sets_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Found {len(data['data'])} sets")
        
        # Print sets that might match our ETBs
        print("\nPotential matches for our ETBs:")
        for set_data in data['data']:
            name_lower = set_data['name'].lower()
            if any(keyword in name_lower for keyword in [
                '151', 'celebrations', 'brilliant', 'generations', 
                'primal', 'surging', 'prismatic', 'journey'
            ]):
                print(f"  - {set_data['id']}: {set_data['name']} ({set_data.get('releaseDate', 'N/A')})")
        
        return data['data']
    except Exception as e:
        print(f"✗ Error fetching sets: {e}")
        return []

def fetch_cards_for_set(set_id, set_name):
    """Fetch all cards for a specific set"""
    print(f"\nFetching cards for {set_name} (set: {set_id})...")
    
    all_cards = []
    page = 1
    page_size = 250
    
    while True:
        url = f"{API_BASE_URL}/cards"
        params = {
            "q": f"set.id:{set_id}",
            "page": page,
            "pageSize": page_size,
            "orderBy": "number"
        }
        
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            
            cards = data.get('data', [])
            if not cards:
                break
                
            all_cards.extend(cards)
            
            # Check if there are more pages
            if len(cards) < page_size:
                break
                
            page += 1
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"  ✗ Error fetching page {page}: {e}")
            break
    
    print(f"  ✓ Found {len(all_cards)} cards")
    return all_cards

def download_card_image(card, output_dir):
    """Download a single card image and save card metadata"""
    card_id = card['id']
    card_name = card['name'].replace('/', '-').replace(':', '')  # Sanitize filename
    card_number = card.get('number', 'unknown')
    card_rarity = card.get('rarity', 'unknown')
    
    # Get the highest quality image available
    images = card.get('images', {})
    image_url = images.get('large') or images.get('small')
    
    if not image_url:
        return False, None
    
    # Create filename with rarity prefix for easy sorting
    rarity_prefix = card_rarity.replace(' ', '_').lower()
    filename = f"{card_number:0>3}_{rarity_prefix}_{card_name}.png"
    output_path = output_dir / filename
    
    if output_path.exists():
        return True, card_rarity  # Already downloaded
    
    try:
        # Download the image
        urllib.request.urlretrieve(image_url, output_path)
        return True, card_rarity
    except Exception as e:
        print(f"    ✗ Error downloading {card_name}: {e}")
        return False, None

def process_set(etb_variant, set_id):
    """Process all cards for a specific ETB set"""
    print(f"\n{'=' * 60}")
    print(f"Processing: {etb_variant}")
    print(f"{'=' * 60}")
    
    # Create output directory
    output_dir = Path(f"raw_images/cards/{etb_variant}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch cards
    cards = fetch_cards_for_set(set_id, etb_variant)
    
    if not cards:
        print(f"  ⚠ No cards found for set {set_id}")
        return 0
    
    # Save card data
    data_file = output_dir / "cards_data.json"
    with open(data_file, 'w') as f:
        json.dump(cards, f, indent=2)
    
    # Download images and track rarity
    print(f"  Downloading {len(cards)} card images...")
    downloaded = 0
    rarity_counts = {}
    card_metadata = []
    
    for i, card in enumerate(cards, 1):
        success, rarity = download_card_image(card, output_dir)
        if success:
            downloaded += 1
            if rarity:
                rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
            
            # Store metadata for each card
            card_metadata.append({
                'id': card['id'],
                'name': card['name'],
                'number': card.get('number', 'unknown'),
                'rarity': card.get('rarity', 'unknown'),
                'types': card.get('types', []),
                'hp': card.get('hp'),
                'artist': card.get('artist'),
                'set_name': card.get('set', {}).get('name', ''),
                'image_url': card.get('images', {}).get('large', '')
            })
        
        # Progress indicator
        if i % 10 == 0:
            print(f"    Progress: {i}/{len(cards)}")
        
        # Rate limiting
        if i % 5 == 0:
            time.sleep(0.5)
    
    # Save card metadata with rarity info
    metadata_file = output_dir / "cards_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump({
            'total_cards': len(card_metadata),
            'rarity_distribution': rarity_counts,
            'cards': card_metadata
        }, f, indent=2)
    
    print(f"  ✓ Downloaded {downloaded}/{len(cards)} cards to {output_dir}")
    print(f"  ✓ Rarity distribution: {rarity_counts}")
    return downloaded, rarity_counts

def main():
    print("Pokemon TCG Card Artwork Fetcher")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...")
    print()
    
    # First, get info about available sets
    sets = get_sets_info()
    
    # Process each ETB variant
    total_downloaded = 0
    processed_sets = []
    all_rarity_stats = {}
    
    for etb_variant, set_id in SET_MAPPING.items():
        result = process_set(etb_variant, set_id)
        if isinstance(result, tuple):
            downloaded, rarity_counts = result
        else:
            downloaded = result
            rarity_counts = {}
        
        total_downloaded += downloaded
        if downloaded > 0:
            processed_sets.append(etb_variant)
            all_rarity_stats[etb_variant] = rarity_counts
    
    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"✓ Total cards downloaded: {total_downloaded}")
    print(f"✓ Sets processed: {len(processed_sets)}")
    print(f"  Sets: {', '.join(processed_sets)}")
    
    # Create a summary file with rarity info
    summary = {
        "total_cards": total_downloaded,
        "sets_processed": processed_sets,
        "set_mapping": SET_MAPPING,
        "rarity_statistics": all_rarity_stats,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    summary_file = Path("raw_images/cards/download_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✓ Summary saved to {summary_file}")
    
    # Print rarity breakdown
    print("\nRarity Breakdown by Set:")
    for set_name, rarities in all_rarity_stats.items():
        if rarities:
            print(f"  {set_name}:")
            for rarity, count in sorted(rarities.items()):
                print(f"    - {rarity}: {count} cards")

if __name__ == "__main__":
    main()