#!/usr/bin/env python3
"""
Find and download booster pack images using direct image searches
"""

import requests
from pathlib import Path
import time

# Direct image URLs for known booster packs
BOOSTER_IMAGE_URLS = {
    "etb_151": [
        "https://product-images.tcgplayer.com/fit-in/437x437/507507.jpg",  # 151 booster
        "https://m.media-amazon.com/images/I/71l6e1HLOUL._AC_SL1500_.jpg",
        "https://www.pokemon.com/static-assets/content-assets/cms2/img/trading-card-game/series/incrementals/scarlet-violet-151/products/booster-packs/sv3pt5-booster-pack-1-169-en.png"
    ],
    "etb_brilliant_stars": [
        "https://product-images.tcgplayer.com/fit-in/437x437/264298.jpg",
        "https://m.media-amazon.com/images/I/81gKJB0mN7L._AC_SL1500_.jpg",
        "https://www.pokemoncenter.com/images/DAMRoot/High/10000/P8526_710-95986_01.jpg"
    ],
    "etb_celebrations": [
        "https://product-images.tcgplayer.com/fit-in/437x437/250097.jpg",
        "https://m.media-amazon.com/images/I/81Vc8ZJNuML._AC_SL1500_.jpg",
        "https://www.pokemoncenter.com/images/DAMRoot/High/10000/P8162_710-87962_01.jpg"
    ],
    "etb_surging_sparks": [
        "https://product-images.tcgplayer.com/fit-in/437x437/573431.jpg",
        "https://m.media-amazon.com/images/I/71QnmXf1gJL._AC_SL1500_.jpg"
    ],
    "etb_prismatic_evolutions": [
        "https://product-images.tcgplayer.com/fit-in/437x437/595324.jpg",
        "https://52f4e29a8321344e30ae-0f55c9129972ac85d6b1f4e703468e6b.ssl.cf2.rackcdn.com/products/pictures/1870045.jpg"
    ],
    "etb_generations": [
        "https://product-images.tcgplayer.com/fit-in/437x437/110863.jpg",
        "https://m.media-amazon.com/images/I/91DpkvO3VvL._AC_SL1500_.jpg"
    ],
    "etb_groudon": [  # Primal Clash
        "https://product-images.tcgplayer.com/fit-in/437x437/96252.jpg",
        "https://m.media-amazon.com/images/I/91u-jHOOTkL._AC_SL1500_.jpg"
    ],
    "etb_kyogre": [  # Primal Clash (different art)
        "https://product-images.tcgplayer.com/fit-in/437x437/96251.jpg",
        "https://m.media-amazon.com/images/I/91ykgNTLvgL._AC_SL1500_.jpg"
    ],
    "etb_destined_rivals": [  # Astral Radiance
        "https://product-images.tcgplayer.com/fit-in/437x437/268836.jpg",
        "https://m.media-amazon.com/images/I/81QVgD0p7hL._AC_SL1500_.jpg"
    ],
    "etb_white_flare": [  # Silver Tempest
        "https://product-images.tcgplayer.com/fit-in/437x437/295021.jpg",
        "https://m.media-amazon.com/images/I/81o9Tg7WGKL._AC_SL1500_.jpg"
    ],
    "etb_journey_together": [  # Paldea Evolved
        "https://product-images.tcgplayer.com/fit-in/437x437/495494.jpg",
        "https://m.media-amazon.com/images/I/71JYQxO0u7L._AC_SL1500_.jpg"
    ],
    "etb_black_bolt": [  # Lost Origin
        "https://product-images.tcgplayer.com/fit-in/437x437/286741.jpg",
        "https://m.media-amazon.com/images/I/81vNOGOJQDL._AC_SL1500_.jpg"
    ]
}

def download_image(url, save_path):
    """Download an image from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200 and len(response.content) > 1000:  # At least 1KB
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    Error: {e}")
    
    return False

def main():
    """Download booster pack images"""
    print("Downloading Booster Pack Images")
    print("=" * 60)
    
    output_dir = Path("raw_images/booster_packs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    for etb_name, urls in BOOSTER_IMAGE_URLS.items():
        print(f"\n{etb_name}:")
        print("-" * 40)
        
        found = False
        for i, url in enumerate(urls):
            print(f"  Trying source {i+1}: {url[:50]}...")
            
            # Determine extension from URL
            if '.png' in url.lower():
                ext = '.png'
            else:
                ext = '.jpg'
            
            save_path = output_dir / f"{etb_name}_booster{ext}"
            
            if download_image(url, save_path):
                print(f"  ✓ Downloaded to: {save_path.name}")
                results[etb_name] = str(save_path)
                found = True
                break
            
            time.sleep(0.5)  # Be polite
        
        if not found:
            print(f"  ✗ Could not download from any source")
            results[etb_name] = None
    
    # Summary
    print("\n" + "=" * 60)
    found_count = sum(1 for v in results.values() if v)
    print(f"Successfully downloaded {found_count}/{len(results)} booster pack images")
    
    # List what we got
    print("\nDownloaded booster packs:")
    for etb_name, path in results.items():
        if path:
            print(f"  ✓ {etb_name}: {Path(path).name}")
        else:
            print(f"  ✗ {etb_name}: Not found")
    
    return results

if __name__ == "__main__":
    main()