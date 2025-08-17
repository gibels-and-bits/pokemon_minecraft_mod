#!/usr/bin/env python3
"""
TCGplayer Elite Trainer Box Image Scraper
Collects ETB images from TCGplayer and saves them organized by variant
"""

import os
import sys
import json
import time
import asyncio
import aiohttp
from pathlib import Path
from urllib.parse import urlparse, quote
from playwright.async_api import async_playwright

class ETBScraper:
    def __init__(self, output_dir="raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.etb_searches = [
            "pokemon elite trainer box",
            "pokemon etb box",
            "elite trainer box sealed"
        ]
        
        self.known_etbs = [
            "paldea evolved",
            "obsidian flames", 
            "paradox rift",
            "temporal forces",
            "twilight masquerade",
            "shrouded fable",
            "stellar crown",
            "surging sparks",
            "scarlet violet base",
            "sword shield base",
            "brilliant stars",
            "astral radiance",
            "lost origin",
            "silver tempest",
            "crown zenith",
            "evolving skies",
            "fusion strike",
            "chilling reign",
            "battle styles",
            "vivid voltage",
            "darkness ablaze",
            "rebel clash",
            "champions path",
            "shining fates",
            "celebrations",
            "pokemon go"
        ]

    async def search_tcgplayer(self, search_term):
        """Search TCGplayer for ETB products"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Run with UI for debugging
            page = await browser.new_page()
            
            results = []
            
            try:
                # Simpler search URL
                search_url = f"https://www.tcgplayer.com/search/all/product?q={quote(search_term)}"
                print(f"  Navigating to: {search_url}")
                await page.goto(search_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)  # Wait longer for content to load
                
                product_links = await page.query_selector_all('a.product-card__content')
                
                for link in product_links[:10]:  # Limit to first 10 results
                    href = await link.get_attribute('href')
                    if href:
                        full_url = f"https://www.tcgplayer.com{href}" if href.startswith('/') else href
                        title_elem = await link.query_selector('.product-card__title')
                        title = await title_elem.inner_text() if title_elem else "Unknown"
                        
                        if any(etb_keyword in title.lower() for etb_keyword in ['elite trainer', 'etb']):
                            results.append({
                                'url': full_url,
                                'title': title
                            })
                
            except Exception as e:
                print(f"Error searching TCGplayer: {e}")
            finally:
                await browser.close()
            
            return results

    async def scrape_product_images(self, product_url, product_title):
        """Scrape images from a TCGplayer product page"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            images = []
            
            try:
                await page.goto(product_url, wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                # Try to find product images
                image_selectors = [
                    'img.product-details__image',
                    '.product-image img',
                    '.gallery-image img',
                    'img[alt*="Elite Trainer"]',
                    'img[alt*="ETB"]'
                ]
                
                for selector in image_selectors:
                    imgs = await page.query_selector_all(selector)
                    for img in imgs:
                        src = await img.get_attribute('src')
                        if src and not src.startswith('data:'):
                            if not src.startswith('http'):
                                src = f"https://www.tcgplayer.com{src}"
                            images.append(src)
                
                # Remove duplicates while preserving order
                images = list(dict.fromkeys(images))
                
            except Exception as e:
                print(f"Error scraping product {product_url}: {e}")
            finally:
                await browser.close()
            
            return images

    async def download_image(self, session, url, save_path):
        """Download an image from URL"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        return False

    def sanitize_name(self, name):
        """Convert product name to valid folder name"""
        import re
        name = name.lower()
        name = re.sub(r'[^a-z0-9\s\-]', '', name)
        name = re.sub(r'\s+', '_', name)
        name = name.replace('elite_trainer_box', 'etb')
        name = name.replace('pokemon_tcg', '')
        name = name.replace('pokemon', '')
        name = re.sub(r'_+', '_', name)
        name = name.strip('_')
        return name[:50]  # Limit length

    async def process_etb(self, search_term):
        """Process a single ETB search"""
        print(f"\nSearching for: {search_term}")
        
        products = await self.search_tcgplayer(search_term)
        
        if not products:
            print(f"No products found for: {search_term}")
            return
        
        async with aiohttp.ClientSession() as session:
            for product in products[:3]:  # Limit to first 3 products per search
                print(f"\nProcessing: {product['title']}")
                
                images = await self.scrape_product_images(product['url'], product['title'])
                
                if images:
                    variant_name = self.sanitize_name(product['title'])
                    variant_dir = self.output_dir / variant_name
                    variant_dir.mkdir(exist_ok=True)
                    
                    # Save metadata
                    metadata = {
                        'title': product['title'],
                        'url': product['url'],
                        'images': images,
                        'variant_name': variant_name
                    }
                    
                    with open(variant_dir / 'metadata.json', 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    # Download images
                    for i, img_url in enumerate(images[:6]):  # Max 6 images per ETB
                        ext = Path(urlparse(img_url).path).suffix or '.jpg'
                        save_path = variant_dir / f"image_{i}{ext}"
                        
                        if await self.download_image(session, img_url, save_path):
                            print(f"  Downloaded: image_{i}{ext}")
                    
                    # Try to assign faces based on image names/order
                    self.assign_face_names(variant_dir)

    def assign_face_names(self, variant_dir):
        """Try to intelligently assign face names to images"""
        images = list(variant_dir.glob("image_*"))
        
        if not images:
            return
        
        face_mapping = {
            0: "front.jpg",
            1: "back.jpg",
            2: "left.jpg",
            3: "right.jpg",
            4: "top.jpg",
            5: "bottom.jpg"
        }
        
        for img_path in images:
            # Extract index from filename
            try:
                index = int(img_path.stem.split('_')[1])
                if index in face_mapping:
                    new_path = variant_dir / face_mapping[index]
                    img_path.rename(new_path)
                    print(f"  Renamed to: {face_mapping[index]}")
            except:
                pass

    async def run(self):
        """Main scraping process"""
        print("Starting ETB Image Scraper")
        print("=" * 50)
        
        # Search for known ETBs
        for etb_name in self.known_etbs[:5]:  # Limit for testing
            search_term = f"pokemon {etb_name} elite trainer box"
            await self.process_etb(search_term)
            await asyncio.sleep(2)  # Be respectful with requests
        
        print("\n" + "=" * 50)
        print("Scraping complete!")
        print(f"Images saved to: {self.output_dir.absolute()}")

def main():
    scraper = ETBScraper()
    asyncio.run(scraper.run())

if __name__ == "__main__":
    main()