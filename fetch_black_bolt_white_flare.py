#!/usr/bin/env python3
import requests
import json
import os
import time
from pathlib import Path
import urllib.request
from urllib.parse import urlparse

# API Base URL
API_BASE = "https://api.pokemontcg.io/v2"

# Set IDs from the API
SET_IDS = {
    "black_bolt": "zsv10pt5",
    "white_flare": "rsv10pt5"
}

# Output directories
OUTPUT_BASE = "cards"
METADATA_DIR = "cards_metadata"

def fetch_cards_from_set(set_id, set_name):
    """Fetch all cards from a specific set"""
    print(f"\n📥 Fetching cards from {set_name} (ID: {set_id})...")
    
    cards = []
    page = 1
    page_size = 250  # Maximum allowed
    
    while True:
        url = f"{API_BASE}/cards?q=set.id:{set_id}&page={page}&pageSize={page_size}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and data['data']:
                cards.extend(data['data'])
                print(f"  ✓ Fetched page {page} ({len(data['data'])} cards)")
                
                # Check if there are more pages
                total_count = data.get('totalCount', 0)
                if len(cards) >= total_count:
                    break
                    
                page += 1
                time.sleep(0.5)  # Be nice to the API
            else:
                break
                
        except Exception as e:
            print(f"  ✗ Error fetching page {page}: {e}")
            break
    
    print(f"  📊 Total cards fetched: {len(cards)}")
    return cards

def download_card_image(card, output_dir):
    """Download card image with proper naming"""
    try:
        # Get the high-resolution image URL
        image_url = card.get('images', {}).get('large') or card.get('images', {}).get('small')
        
        if not image_url:
            print(f"  ⚠ No image URL for {card['name']}")
            return False
        
        # Construct filename with number, rarity, and name
        number = card.get('number', '000').zfill(3)
        rarity = card.get('rarity', 'unknown').lower().replace(' ', '_')
        name = card['name'].replace(' ', '_').replace("'", "").replace("/", "_")
        
        # Handle special characters in Pokemon names
        name = name.replace("é", "e").replace("É", "E")
        
        filename = f"{number}_{rarity}_{name}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Skip if already exists
        if os.path.exists(filepath):
            print(f"  ⏭ Skipping {filename} (already exists)")
            return True
        
        # Download the image
        urllib.request.urlretrieve(image_url, filepath)
        print(f"  ✓ Downloaded {filename}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error downloading {card['name']}: {e}")
        return False

def save_metadata(cards, set_name):
    """Save card metadata to JSON file"""
    metadata_file = os.path.join(METADATA_DIR, f"{set_name}_cards.json")
    
    # Prepare metadata
    metadata = []
    for card in cards:
        meta = {
            "id": card.get('id'),
            "name": card['name'],
            "number": card.get('number'),
            "rarity": card.get('rarity'),
            "types": card.get('types', []),
            "hp": card.get('hp'),
            "artist": card.get('artist'),
            "set_id": card.get('set', {}).get('id'),
            "set_name": card.get('set', {}).get('name'),
            "national_pokedex_numbers": card.get('nationalPokedexNumbers', []),
            "attacks": card.get('attacks', []),
            "weaknesses": card.get('weaknesses', []),
            "resistances": card.get('resistances', []),
            "retreat_cost": card.get('retreatCost', []),
            "converted_retreat_cost": card.get('convertedRetreatCost'),
            "supertype": card.get('supertype'),
            "subtypes": card.get('subtypes', []),
            "images": card.get('images', {})
        }
        metadata.append(meta)
    
    # Save to file
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  💾 Saved metadata to {metadata_file}")

def process_set(set_name, set_id):
    """Process a complete set: fetch cards, download images, save metadata"""
    print(f"\n{'='*50}")
    print(f"Processing {set_name.upper()}")
    print(f"{'='*50}")
    
    # Create directories
    output_dir = os.path.join(OUTPUT_BASE, set_name)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)
    
    # Fetch cards
    cards = fetch_cards_from_set(set_id, set_name)
    
    if not cards:
        print(f"  ⚠ No cards found for {set_name}")
        return
    
    # Sort cards by number
    cards.sort(key=lambda x: int(x.get('number', '0').split('/')[-1]) if x.get('number', '0').isdigit() or '/' in x.get('number', '0') else 999)
    
    # Download images
    print(f"\n📥 Downloading card images for {set_name}...")
    success_count = 0
    for i, card in enumerate(cards, 1):
        if download_card_image(card, output_dir):
            success_count += 1
        
        # Small delay between downloads
        if i % 10 == 0:
            time.sleep(1)
    
    print(f"\n✅ Downloaded {success_count}/{len(cards)} images successfully")
    
    # Save metadata
    save_metadata(cards, set_name)

def main():
    """Main function to process both sets"""
    print("🎴 Pokemon TCG Card Fetcher")
    print("Fetching Black Bolt and White Flare sets from PokemonTCG.io API")
    
    # Process each set
    for set_name, set_id in SET_IDS.items():
        process_set(set_name, set_id)
    
    print("\n" + "="*50)
    print("✨ All sets processed successfully!")
    print("="*50)

if __name__ == "__main__":
    main()