#!/usr/bin/env python3
"""Fetch the 151 Pokemon TCG set."""

import requests
import json
import os
import time
from PIL import Image
from io import BytesIO

API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

def fetch_151_set():
    """Fetch the 151 set (sv3pt5)."""
    set_id = "sv3pt5"
    set_name = "151"
    output_folder = "/Users/gibels_and_bits/Development/etb-mod/raw_images/cards/151"
    
    print(f"Fetching 151 set (ID: {set_id})")
    os.makedirs(output_folder, exist_ok=True)
    
    # Fetch cards with retry logic
    url = f"{BASE_URL}/cards"
    params = {"q": f"set.id:{set_id}", "pageSize": 250}
    
    for attempt in range(3):
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=60)
            if response.status_code == 200:
                break
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    else:
        print("Failed to fetch cards after 3 attempts")
        return
    
    data = response.json()
    cards = data.get("data", [])
    print(f"Found {len(cards)} cards")
    
    # Prepare metadata
    metadata = {
        "set_id": set_id,
        "set_name": set_name,
        "total_cards": len(cards),
        "downloaded": 0,
        "rarity_distribution": {},
        "cards": []
    }
    
    # Download cards
    downloaded = 0
    for i, card in enumerate(cards):
        card_name = card.get("name", "Unknown")
        card_number = card.get("number", "0")
        card_rarity = card.get("rarity", "Common")
        
        metadata["rarity_distribution"][card_rarity] = metadata["rarity_distribution"].get(card_rarity, 0) + 1
        metadata["cards"].append({
            "id": card.get("id"),
            "name": card_name,
            "number": card_number,
            "rarity": card_rarity
        })
        
        # Get image URL
        image_url = card.get("images", {}).get("large")
        if not image_url:
            image_url = card.get("images", {}).get("small")
        
        if image_url:
            try:
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    img = Image.open(BytesIO(img_response.content))
                    
                    # Resize
                    img.thumbnail((250, 350), Image.Resampling.LANCZOS)
                    
                    # Convert to RGB
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save
                    filename = f"{card_number.zfill(3)}_{card_rarity.lower().replace(' ', '_')}_{card_name.replace('/', '-').replace(':', '')}.jpg"
                    filepath = os.path.join(output_folder, filename)
                    img.save(filepath, 'JPEG', optimize=True, quality=75)
                    
                    downloaded += 1
                    if downloaded % 10 == 0:
                        print(f"  Downloaded {downloaded}/{len(cards)}...")
                    
                    time.sleep(0.3)  # Rate limit
            except Exception as e:
                print(f"  Error downloading {card_name}: {e}")
    
    metadata["downloaded"] = downloaded
    
    # Save metadata
    with open(os.path.join(output_folder, "cards_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Downloaded {downloaded} cards for 151 set")
    print(f"📁 Saved to: {output_folder}")

if __name__ == "__main__":
    fetch_151_set()