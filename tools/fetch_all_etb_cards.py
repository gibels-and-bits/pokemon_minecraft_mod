#!/usr/bin/env python3
"""
Fetch card artwork for all ETB sets with proper search terms
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

# Map ETB variants to search terms
ETB_SEARCHES = {
    "151": "set.name:151",
    "black_bolt": "set.name:\"Crown Zenith\"",
    "brilliant_stars": "set.name:\"Brilliant Stars\"",
    "celebrations": "set.name:Celebrations",
    "destined_rivals": "set.name:\"Astral Radiance\"",
    "generations": "set.name:Generations",
    "groudon": "set.name:\"Primal Clash\"",
    "journey_together": "set.name:\"Scarlet & Violet\"",
    "kyogre": "set.name:\"Primal Clash\"",
    "prismatic_evolutions": "set.name:\"Prismatic\"",
    "surging_sparks": "set.name:\"Surging Sparks\"",
    "white_flare": "set.name:\"Twilight Masquerade\""
}

def fetch_cards_for_etb(etb_name, search_query, limit=30):
    """Fetch cards for a specific ETB set"""
    print(f"\nFetching {etb_name}...")
    print(f"  Search: {search_query}")
    
    # Create output directory
    output_dir = Path(f"raw_images/cards/{etb_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if already downloaded
    metadata_file = output_dir / "cards_metadata.json"
    if metadata_file.exists():
        print(f"  ✓ Already downloaded, skipping...")
        with open(metadata_file, 'r') as f:
            data = json.load(f)
            return data.get('downloaded', 0), data.get('rarity_distribution', {})
    
    # Fetch cards
    url = f"{API_BASE_URL}/cards"
    params = {
        "q": search_query,
        "pageSize": limit,
        "orderBy": "set.releaseDate,number"
    }
    
    try:
        print(f"  Fetching from API...")
        response = requests.get(url, headers=HEADERS, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        cards = data.get('data', [])
        
        if not cards:
            print(f"  ⚠ No cards found")
            return 0, {}
        
        print(f"  Found {len(cards)} cards")
        
        # Process cards
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
                        print(f"    [{i}/{len(cards)}] Downloading: {card_name} ({card_rarity})")
                        urllib.request.urlretrieve(image_url, output_path)
                        downloaded += 1
                        time.sleep(0.5)  # Rate limiting
                    except Exception as e:
                        print(f"      Error: {e}")
                else:
                    downloaded += 1
                    print(f"    [{i}/{len(cards)}] Already exists: {card_name}")
            
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
                'set_id': card.get('set', {}).get('id', ''),
                'image_url': image_url
            })
        
        # Save metadata
        with open(metadata_file, 'w') as f:
            json.dump({
                'etb_name': etb_name,
                'search_query': search_query,
                'total_cards': len(card_metadata),
                'downloaded': downloaded,
                'rarity_distribution': rarity_counts,
                'cards': card_metadata
            }, f, indent=2)
        
        print(f"  ✓ Downloaded {downloaded} cards")
        print(f"  ✓ Rarity: {rarity_counts}")
        
        return downloaded, rarity_counts
        
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout - API is slow")
        return 0, {}
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return 0, {}

def main():
    print("=" * 60)
    print("ETB Card Artwork Fetcher")
    print("=" * 60)
    print(f"API Key: {API_KEY[:10]}...")
    
    total_downloaded = 0
    all_rarity_stats = {}
    successful_sets = []
    
    for etb_name, search_query in ETB_SEARCHES.items():
        downloaded, rarity_counts = fetch_cards_for_etb(etb_name, search_query)
        
        if downloaded > 0:
            total_downloaded += downloaded
            all_rarity_stats[etb_name] = rarity_counts
            successful_sets.append(etb_name)
        
        # Rate limiting between sets
        time.sleep(2)
    
    # Create summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Total cards downloaded: {total_downloaded}")
    print(f"✓ Successful sets: {len(successful_sets)}/{len(ETB_SEARCHES)}")
    
    if successful_sets:
        print(f"\nSuccessful sets: {', '.join(successful_sets)}")
    
    # Save summary
    summary_file = Path("raw_images/cards/download_summary.json")
    with open(summary_file, 'w') as f:
        json.dump({
            'total_cards': total_downloaded,
            'successful_sets': successful_sets,
            'rarity_statistics': all_rarity_stats,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2)
    
    print(f"\n✓ Summary saved to: {summary_file}")
    
    # Show rarity breakdown
    if all_rarity_stats:
        print("\nRarity Breakdown:")
        for set_name, rarities in all_rarity_stats.items():
            if rarities:
                total = sum(rarities.values())
                print(f"\n  {set_name} ({total} cards):")
                for rarity, count in sorted(rarities.items()):
                    print(f"    • {rarity}: {count}")

if __name__ == "__main__":
    main()