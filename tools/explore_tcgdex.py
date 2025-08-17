#!/usr/bin/env python3
"""
Explore TCGdex API for booster pack and ETB images
"""

import requests
import json
from pathlib import Path

def explore_tcgdex():
    """Explore TCGdex API for product images"""
    
    print("Exploring TCGdex API for Pokemon TCG Product Images")
    print("=" * 60)
    
    # Get all sets
    sets_url = "https://api.tcgdex.net/v2/en/sets"
    response = requests.get(sets_url)
    sets = response.json()
    
    print(f"\nFound {len(sets)} sets in TCGdex")
    
    # Look at a few modern sets that likely have ETBs
    interesting_sets = [
        "swsh1",  # Sword & Shield Base
        "swsh12pt5",  # Crown Zenith
        "sv1",  # Scarlet & Violet Base
        "sv3pt5",  # 151
        "sv4pt5",  # Paldean Fates
        "sv6pt5",  # Shrouded Fable
    ]
    
    for set_id in interesting_sets:
        print(f"\n--- Checking set: {set_id} ---")
        
        # Get detailed set info
        set_url = f"https://api.tcgdex.net/v2/en/sets/{set_id}"
        response = requests.get(set_url)
        
        if response.status_code == 200:
            set_data = response.json()
            print(f"Name: {set_data.get('name', 'Unknown')}")
            
            # Check for logo
            if 'logo' in set_data:
                print(f"Logo URL: {set_data['logo']}")
            
            # Check for symbol
            if 'symbol' in set_data:
                print(f"Symbol URL: {set_data['symbol']}")
            
            # Try different potential booster/product URLs
            base_url = f"https://assets.tcgdex.net/en/{set_data.get('serie', {}).get('id', '')}/{set_id}"
            
            potential_urls = [
                f"{base_url}/booster",
                f"{base_url}/booster-pack",
                f"{base_url}/pack",
                f"{base_url}/etb",
                f"{base_url}/elite-trainer-box",
                f"{base_url}/product",
            ]
            
            print("Testing potential product URLs:")
            for url in potential_urls:
                # Try with .png extension
                test_url = f"{url}.png"
                response = requests.head(test_url)
                if response.status_code == 200:
                    print(f"  ✓ Found: {test_url}")
                else:
                    print(f"  ✗ Not found: {url}")
    
    # Also check TCG Pocket
    print("\n--- Checking TCG Pocket ---")
    pocket_url = "https://api.tcgdex.net/v2/en/sets?serie=tcgp"
    response = requests.get(pocket_url)
    if response.status_code == 200:
        pocket_sets = response.json()
        print(f"Found {len(pocket_sets)} TCG Pocket sets")
        
        for pocket_set in pocket_sets[:3]:  # Check first 3
            set_id = pocket_set.get('id')
            print(f"\nPocket Set: {pocket_set.get('name')}")
            
            # Check for booster images
            booster_url = f"https://assets.tcgdex.net/en/tcgp/{set_id}/booster"
            test_url = f"{booster_url}.png"
            response = requests.head(test_url)
            if response.status_code == 200:
                print(f"  ✓ Booster found: {test_url}")

if __name__ == "__main__":
    explore_tcgdex()