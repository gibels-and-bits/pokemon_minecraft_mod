#!/usr/bin/env python3
"""
Scrape booster pack images for Pokemon TCG sets
"""

import os
import requests
from pathlib import Path
import time
import json

# Mapping of our ETB names to actual set names/identifiers
SET_MAPPINGS = {
    "etb_151": {
        "name": "151",
        "search_terms": ["pokemon 151 booster pack", "scarlet violet 151 booster"],
        "set_code": "sv3pt5",
        "series": "Scarlet & Violet"
    },
    "etb_black_bolt": {
        "name": "Black Bolt",
        "search_terms": ["pokemon black bolt booster pack"],
        "set_code": None,
        "series": None
    },
    "etb_brilliant_stars": {
        "name": "Brilliant Stars", 
        "search_terms": ["pokemon brilliant stars booster pack"],
        "set_code": "swsh9",
        "series": "Sword & Shield"
    },
    "etb_celebrations": {
        "name": "Celebrations",
        "search_terms": ["pokemon celebrations booster pack", "25th anniversary booster"],
        "set_code": "cel25",
        "series": "Sword & Shield"
    },
    "etb_destined_rivals": {
        "name": "Astral Radiance",  # Destined Rivals might be a mistranslation
        "search_terms": ["pokemon astral radiance booster pack"],
        "set_code": "swsh10",
        "series": "Sword & Shield"
    },
    "etb_generations": {
        "name": "Generations",
        "search_terms": ["pokemon generations booster pack", "generations 20th anniversary"],
        "set_code": "g1",
        "series": "XY"
    },
    "etb_groudon": {
        "name": "Primal Clash",  # Groudon featured set
        "search_terms": ["pokemon primal clash booster pack", "groudon booster"],
        "set_code": "xy5",
        "series": "XY"
    },
    "etb_journey_together": {
        "name": "Journey Together",
        "search_terms": ["pokemon journey together booster pack"],
        "set_code": None,
        "series": "Scarlet & Violet"
    },
    "etb_kyogre": {
        "name": "Primal Clash",  # Kyogre featured set
        "search_terms": ["pokemon primal clash booster pack", "kyogre booster"],
        "set_code": "xy5",
        "series": "XY"
    },
    "etb_prismatic_evolutions": {
        "name": "Prismatic Evolutions",
        "search_terms": ["pokemon prismatic evolutions booster pack", "eevee booster"],
        "set_code": "sv08",
        "series": "Scarlet & Violet"
    },
    "etb_surging_sparks": {
        "name": "Surging Sparks",
        "search_terms": ["pokemon surging sparks booster pack"],
        "set_code": "sv07",
        "series": "Scarlet & Violet"
    },
    "etb_white_flare": {
        "name": "Silver Tempest",  # White Flare might be Japanese name
        "search_terms": ["pokemon silver tempest booster pack"],
        "set_code": "swsh12",
        "series": "Sword & Shield"
    }
}

def search_tcgplayer_for_booster(set_name):
    """Search TCGPlayer for booster pack images"""
    base_url = "https://www.tcgplayer.com/search/pokemon/product"
    
    # Search for booster packs
    search_query = f"{set_name} booster pack"
    params = {
        "productLineName": "pokemon",
        "q": search_query,
        "view": "grid"
    }
    
    print(f"  Searching TCGPlayer for: {search_query}")
    
    # Note: This would need actual web scraping with Playwright
    # For now, returning known patterns
    return None

def get_pokemon_com_booster_url(set_info):
    """Try to construct Pokemon.com booster pack URL"""
    # Known patterns for Pokemon.com assets
    patterns = [
        "https://www.pokemon.com/static-assets/content-assets/cms2/img/trading-card-game/series/incrementals/{series}/{set}/booster-pack.png",
        "https://www.pokemon.com/static-assets/content-assets/cms2/img/trading-card-game/series/incrementals/{series}/{set}/products/booster.png",
        "https://tcg.pokemon.com/assets/img/expansions/{set}/products/booster-pack.png"
    ]
    
    # Try different URL patterns
    for pattern in patterns:
        if set_info.get("series"):
            series_slug = set_info["series"].lower().replace(" ", "-")
            set_slug = set_info["name"].lower().replace(" ", "-")
            
            url = pattern.format(series=series_slug, set=set_slug)
            return url
    
    return None

def download_booster_image(url, save_path):
    """Download booster pack image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    Error downloading: {e}")
    
    return False

def main():
    """Main function to collect booster pack images"""
    print("Searching for Booster Pack Images")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("raw_images/booster_packs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Track results
    results = {}
    
    for etb_name, set_info in SET_MAPPINGS.items():
        print(f"\n{etb_name}: {set_info['name']}")
        print("-" * 40)
        
        # Try different sources
        found = False
        
        # 1. Try Pokemon.com patterns
        pokemon_url = get_pokemon_com_booster_url(set_info)
        if pokemon_url:
            print(f"  Testing: {pokemon_url}")
            save_path = output_dir / f"{etb_name}_booster.png"
            if download_booster_image(pokemon_url, save_path):
                print(f"  ✓ Downloaded from Pokemon.com")
                results[etb_name] = str(save_path)
                found = True
        
        # 2. Try TCGPlayer (would need actual scraping)
        if not found:
            tcg_url = search_tcgplayer_for_booster(set_info['name'])
            if tcg_url:
                save_path = output_dir / f"{etb_name}_booster.png"
                if download_booster_image(tcg_url, save_path):
                    print(f"  ✓ Downloaded from TCGPlayer")
                    results[etb_name] = str(save_path)
                    found = True
        
        if not found:
            print(f"  ✗ Could not find booster pack image")
            results[etb_name] = None
        
        time.sleep(0.5)  # Be polite to servers
    
    # Save results
    results_file = output_dir / "booster_pack_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Results saved to: {results_file}")
    
    # Summary
    found_count = sum(1 for v in results.values() if v)
    print(f"\nFound {found_count}/{len(results)} booster pack images")
    
    return results

if __name__ == "__main__":
    main()