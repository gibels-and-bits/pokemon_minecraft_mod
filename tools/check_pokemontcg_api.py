#!/usr/bin/env python3
"""
Check Pokemon TCG API for booster pack and product images
"""

import requests
import json

def check_pokemontcg_api():
    """Check Pokemon TCG API for product images"""
    
    print("Checking Pokemon TCG API for Product Images")
    print("=" * 60)
    
    # Get sets from Pokemon TCG API
    headers = {
        'X-Api-Key': ''  # No API key required for basic access
    }
    
    # Check a specific modern set that definitely has ETBs
    sets_to_check = [
        'swsh1',  # Sword & Shield Base
        'sv3pt5',  # 151 - known to have ETBs
        'cel25',  # Celebrations
    ]
    
    for set_id in sets_to_check:
        print(f"\n--- Checking {set_id} ---")
        
        # Get set info
        url = f"https://api.pokemontcg.io/v2/sets/{set_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            set_data = data.get('data', {})
            
            print(f"Name: {set_data.get('name')}")
            print(f"Series: {set_data.get('series')}")
            print(f"Release Date: {set_data.get('releaseDate')}")
            
            # Check available images
            images = set_data.get('images', {})
            print("\nAvailable Images:")
            for img_type, img_url in images.items():
                print(f"  {img_type}: {img_url}")
            
            # Try to find additional product images
            base_url = img_url.rsplit('/', 1)[0] if images else None
            if base_url:
                print("\nTesting for additional product images:")
                potential_products = [
                    'booster',
                    'booster_pack', 
                    'boosterpack',
                    'etb',
                    'elite_trainer_box',
                    'elitetrainerbox',
                    'bundle',
                    'theme_deck',
                    'product'
                ]
                
                for product in potential_products:
                    test_url = f"{base_url}/{product}.png"
                    response = requests.head(test_url)
                    if response.status_code == 200:
                        print(f"  ✓ Found: {test_url}")
    
    # Also check if there's a pattern for product images
    print("\n\nTesting direct Pokemon.com product image patterns:")
    
    # These are known product image patterns from Pokemon.com
    pokemon_com_patterns = [
        "https://www.pokemon.com/static-assets/content-assets/cms2/img/trading-card-game/series/incrementals/scarlet-violet-151/elite-trainer-box/scarlet-violet-151-elite-trainer-box-169-en.png",
        "https://www.pokemon.com/static-assets/content-assets/cms2/img/trading-card-game/series/incrementals/celebrations/products/en-us/elite-trainer-box.png",
    ]
    
    for url in pokemon_com_patterns:
        response = requests.head(url)
        if response.status_code == 200:
            print(f"  ✓ Valid Pokemon.com URL: {url}")
        else:
            print(f"  ✗ Invalid: {url}")

if __name__ == "__main__":
    check_pokemontcg_api()