#!/usr/bin/env python3
"""
Scrape booster pack images from TCGPlayer using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import json
import time

# Updated mappings with correct search terms
BOOSTER_SEARCHES = {
    "etb_151": "Pokemon 151 Booster Pack",
    "etb_brilliant_stars": "Brilliant Stars Booster Pack",
    "etb_celebrations": "Celebrations Booster Pack", 
    "etb_generations": "Generations Booster Pack",
    "etb_groudon": "Primal Clash Booster Pack",
    "etb_kyogre": "Primal Clash Booster Pack",
    "etb_prismatic_evolutions": "Prismatic Evolutions Booster Pack",
    "etb_surging_sparks": "Surging Sparks Booster Pack",
    "etb_white_flare": "Silver Tempest Booster Pack",
    "etb_journey_together": "Paldea Evolved Booster Pack",  # Might be wrong set
    "etb_destined_rivals": "Astral Radiance Booster Pack",
    "etb_black_bolt": "Lost Origin Booster Pack"  # Guessing based on timing
}

async def scrape_tcgplayer_boosters():
    """Scrape booster pack images from TCGPlayer"""
    
    output_dir = Path("raw_images/booster_packs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set a reasonable viewport
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        for etb_name, search_term in BOOSTER_SEARCHES.items():
            print(f"\nSearching for: {etb_name} - {search_term}")
            print("-" * 40)
            
            try:
                # Go to TCGPlayer search
                search_url = f"https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&q={search_term.replace(' ', '%20')}&view=grid"
                print(f"  URL: {search_url}")
                
                await page.goto(search_url, wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(2000)  # Let images load
                
                # Look for product images
                # TCGPlayer uses lazy loading, so we need to find the right selectors
                product_selectors = [
                    'div.product-card__image img',
                    'img.product-image',
                    'div.search-result__image img',
                    'img[alt*="Booster"]',
                    'img[alt*="Pack"]'
                ]
                
                image_url = None
                for selector in product_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        if elements:
                            for element in elements[:3]:  # Check first 3 results
                                src = await element.get_attribute('src')
                                if src and ('booster' in src.lower() or 'pack' in src.lower() or search_term.split()[0].lower() in src.lower()):
                                    image_url = src
                                    break
                            if image_url:
                                break
                    except:
                        continue
                
                if not image_url:
                    # Try to get any product image as fallback
                    try:
                        first_product = await page.query_selector('div.product-card__image img, img.product-image')
                        if first_product:
                            image_url = await first_product.get_attribute('src')
                    except:
                        pass
                
                if image_url:
                    # Ensure we have a full URL
                    if image_url.startswith('//'):
                        image_url = 'https:' + image_url
                    elif image_url.startswith('/'):
                        image_url = 'https://www.tcgplayer.com' + image_url
                    
                    print(f"  ✓ Found image: {image_url}")
                    
                    # Download the image
                    save_path = output_dir / f"{etb_name}_booster.jpg"
                    
                    # Navigate to image URL and take screenshot
                    await page.goto(image_url)
                    await page.screenshot(path=str(save_path))
                    
                    results[etb_name] = str(save_path)
                    print(f"  ✓ Saved to: {save_path}")
                else:
                    print(f"  ✗ No booster pack image found")
                    results[etb_name] = None
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                results[etb_name] = None
            
            # Be polite
            await page.wait_for_timeout(1000)
        
        await browser.close()
    
    # Save results
    results_file = output_dir / "booster_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    found_count = sum(1 for v in results.values() if v)
    print(f"Found {found_count}/{len(results)} booster pack images")
    print(f"Results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(scrape_tcgplayer_boosters())