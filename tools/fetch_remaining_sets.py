#!/usr/bin/env python3
"""Fetch remaining Pokemon TCG sets from the API."""

import requests
import json
import os
import time
from PIL import Image
from io import BytesIO

API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

def search_for_set(set_name):
    """Search for a set by name."""
    print(f"\nSearching for set: {set_name}")
    
    # Try exact name match first
    url = f"{BASE_URL}/sets"
    params = {"q": f'name:"{set_name}"'}
    
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            for set_info in data["data"]:
                print(f"  Found: {set_info['name']} (ID: {set_info['id']}, Released: {set_info.get('releaseDate', 'Unknown')})")
            return data["data"]
    
    # Try partial match
    params = {"q": f'name:{set_name}'}
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            print(f"  Partial matches found:")
            for set_info in data["data"]:
                print(f"    - {set_info['name']} (ID: {set_info['id']}, Released: {set_info.get('releaseDate', 'Unknown')})")
            return data["data"]
    
    print(f"  No sets found matching: {set_name}")
    return []

def fetch_set_cards(set_id, set_name, output_folder):
    """Fetch all cards from a specific set."""
    print(f"\nFetching cards for {set_name} (ID: {set_id})")
    
    # Create output directory
    output_dir = os.path.join(output_folder, set_name.lower().replace(" ", "_"))
    os.makedirs(output_dir, exist_ok=True)
    
    # Fetch cards
    url = f"{BASE_URL}/cards"
    params = {"q": f"set.id:{set_id}", "pageSize": 250}
    
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if response.status_code != 200:
        print(f"  Error fetching cards: {response.status_code}")
        return 0
    
    data = response.json()
    cards = data.get("data", [])
    print(f"  Found {len(cards)} cards")
    
    if not cards:
        return 0
    
    # Prepare metadata
    metadata = {
        "set_id": set_id,
        "set_name": set_name,
        "total_cards": len(cards),
        "downloaded": 0,
        "rarity_distribution": {},
        "cards": []
    }
    
    # Download card images
    downloaded = 0
    for i, card in enumerate(cards):
        card_id = card.get("id", "unknown")
        card_name = card.get("name", "Unknown")
        card_number = card.get("number", "0")
        card_rarity = card.get("rarity", "Common")
        
        # Update rarity distribution
        metadata["rarity_distribution"][card_rarity] = metadata["rarity_distribution"].get(card_rarity, 0) + 1
        
        # Add to metadata
        metadata["cards"].append({
            "id": card_id,
            "name": card_name,
            "number": card_number,
            "rarity": card_rarity
        })
        
        # Download image
        image_url = card.get("images", {}).get("large")
        if not image_url:
            image_url = card.get("images", {}).get("small")
        
        if image_url:
            try:
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    # Save image
                    img = Image.open(BytesIO(img_response.content))
                    
                    # Resize for mod (250x350 max)
                    img.thumbnail((250, 350), Image.Resampling.LANCZOS)
                    
                    # Convert to RGB if needed
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as JPEG
                    filename = f"{card_number.zfill(3)}_{card_rarity.lower().replace(' ', '_')}_{card_name.replace('/', '-').replace(':', '')}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    img.save(filepath, 'JPEG', optimize=True, quality=75)
                    
                    downloaded += 1
                    if downloaded % 10 == 0:
                        print(f"    Downloaded {downloaded}/{len(cards)} cards...")
                    
                    # Rate limit
                    time.sleep(0.5)
            except Exception as e:
                print(f"    Error downloading {card_name}: {e}")
    
    metadata["downloaded"] = downloaded
    
    # Save metadata
    metadata_path = os.path.join(output_dir, "cards_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  Downloaded {downloaded} cards to {output_dir}")
    return downloaded

def main():
    output_folder = "/Users/gibels_and_bits/Development/etb-mod/raw_images/cards"
    
    # Define sets to fetch
    sets_to_fetch = [
        # First try to find "151" set (might be MEW or similar)
        {"search_name": "151", "folder_name": "151"},
        {"search_name": "MEW", "folder_name": "151"},
        {"search_name": "Scarlet Violet 151", "folder_name": "151"},
        
        # Prismatic Evolutions (might not exist yet as it's very new)
        {"search_name": "Prismatic Evolutions", "folder_name": "prismatic_evolutions"},
        {"search_name": "Prismatic", "folder_name": "prismatic_evolutions"},
    ]
    
    found_sets = {}
    
    # Search for each set
    for set_info in sets_to_fetch:
        results = search_for_set(set_info["search_name"])
        if results:
            # Let user choose or auto-select most recent
            most_recent = max(results, key=lambda x: x.get("releaseDate", "0000"))
            found_sets[set_info["folder_name"]] = most_recent
            print(f"  Selected: {most_recent['name']} for {set_info['folder_name']}")
    
    # Fetch cards for found sets
    total_downloaded = 0
    for folder_name, set_data in found_sets.items():
        count = fetch_set_cards(set_data["id"], folder_name, output_folder)
        total_downloaded += count
    
    print(f"\n✅ Total cards downloaded: {total_downloaded}")

if __name__ == "__main__":
    main()