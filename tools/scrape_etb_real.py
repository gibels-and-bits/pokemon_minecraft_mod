#!/usr/bin/env python3
"""
Real TCGplayer ETB scraper using the provided search URL
"""

import os
import asyncio
import aiohttp
from pathlib import Path
import json
from playwright.async_api import async_playwright
from urllib.parse import urljoin

class RealETBScraper:
    def __init__(self, output_dir="raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.base_url = "https://www.tcgplayer.com"
        
    def sanitize_name(self, name):
        """Convert product name to valid folder name"""
        import re
        name = name.lower()
        # Remove Pokemon TCG prefix if present
        name = name.replace("pokemon tcg:", "").replace("pokémon tcg:", "")
        name = re.sub(r'[^a-z0-9\s\-]', '', name)
        name = re.sub(r'\s+', '_', name)
        name = name.replace("elite_trainer_box", "").strip("_")
        name = f"etb_{name}" if not name.startswith("etb_") else name
        return name[:50]

    async def scrape_search_page(self):
        """Scrape the search results page for ETB products"""
        products = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Use the provided URL
                search_url = "https://www.tcgplayer.com/search/pokemon/product?page=1&productLineName=pokemon&q=elite+trainer+box&view=grid"
                print(f"Navigating to search page...")
                await page.goto(search_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                
                # Find all product cards
                print("Finding ETB products...")
                product_cards = await page.query_selector_all('div.search-result')
                
                if not product_cards:
                    # Try alternative selector
                    product_cards = await page.query_selector_all('article.product-card')
                
                if not product_cards:
                    # Try another alternative
                    product_cards = await page.query_selector_all('[data-testid="product-card"]')
                
                print(f"Found {len(product_cards)} potential products")
                
                for card in product_cards[:20]:  # Process first 20 products
                    try:
                        # Try to get product link
                        link_elem = await card.query_selector('a')
                        if link_elem:
                            href = await link_elem.get_attribute('href')
                            if href:
                                product_url = urljoin(self.base_url, href)
                            else:
                                continue
                        else:
                            continue
                        
                        # Try to get product title
                        title_elem = await card.query_selector('.product-card__title, h3, [data-testid="product-title"]')
                        if not title_elem:
                            title_elem = await card.query_selector('span')
                        
                        title = await title_elem.inner_text() if title_elem else "Unknown ETB"
                        
                        # Filter for ETBs
                        if "elite trainer" in title.lower() or "etb" in title.lower():
                            # Try to get image
                            img_elem = await card.query_selector('img')
                            img_url = None
                            if img_elem:
                                img_url = await img_elem.get_attribute('src')
                                if not img_url:
                                    img_url = await img_elem.get_attribute('data-src')
                            
                            products.append({
                                'title': title,
                                'url': product_url,
                                'image': img_url
                            })
                            print(f"  Found: {title}")
                            
                    except Exception as e:
                        print(f"  Error processing card: {e}")
                        continue
                
            except Exception as e:
                print(f"Error scraping search page: {e}")
            finally:
                await browser.close()
        
        return products

    async def scrape_product_page(self, product_url, product_title):
        """Scrape images from a product detail page"""
        images = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                print(f"  Fetching product page: {product_title}")
                await page.goto(product_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)
                
                # Look for product images
                image_selectors = [
                    'img.product-image',
                    'img[alt*="Elite Trainer"]',
                    'img[alt*="ETB"]',
                    '.product-details__image img',
                    '.gallery-image img',
                    '[data-testid="product-image"] img'
                ]
                
                for selector in image_selectors:
                    imgs = await page.query_selector_all(selector)
                    for img in imgs:
                        src = await img.get_attribute('src')
                        if not src:
                            src = await img.get_attribute('data-src')
                        
                        if src and not src.startswith('data:'):
                            if not src.startswith('http'):
                                src = urljoin(self.base_url, src)
                            
                            # Skip small images (likely thumbnails)
                            if 'thumbnail' not in src.lower() and '50x50' not in src:
                                images.append(src)
                
                # Remove duplicates
                images = list(dict.fromkeys(images))
                
            except Exception as e:
                print(f"    Error scraping product page: {e}")
            finally:
                await browser.close()
        
        return images

    async def download_image(self, session, url, save_path):
        """Download an image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Referer': 'https://www.tcgplayer.com/'
            }
            
            # Handle TCGplayer image URLs
            if 'tcgplayer.com' in url and '/fit-in/' in url:
                # Try to get the full resolution version
                url = url.replace('/fit-in/200x200/', '/fit-in/600x600/')
                url = url.replace('/fit-in/400x400/', '/fit-in/600x600/')
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    return True
                else:
                    print(f"      Failed to download (status {response.status})")
        except Exception as e:
            print(f"      Error downloading: {e}")
        return False

    async def process_product(self, session, product, index):
        """Process a single ETB product"""
        title = product['title']
        print(f"\n[{index}] Processing: {title}")
        
        variant_name = self.sanitize_name(title)
        variant_dir = self.output_dir / variant_name
        variant_dir.mkdir(exist_ok=True)
        
        # Collect all images
        all_images = []
        
        # Add the main image if available
        if product.get('image'):
            all_images.append(product['image'])
        
        # Get more images from product page
        if product.get('url'):
            page_images = await self.scrape_product_page(product['url'], title)
            all_images.extend(page_images)
        
        # Remove duplicates
        all_images = list(dict.fromkeys(all_images))
        
        if not all_images:
            print(f"    No images found for {title}")
            return None
        
        # Download images
        face_names = ["front", "back", "left", "right", "top", "bottom"]
        downloaded = []
        
        for i, img_url in enumerate(all_images[:6]):  # Max 6 images
            face_name = face_names[i] if i < len(face_names) else f"extra_{i}"
            save_path = variant_dir / f"{face_name}.jpg"
            
            print(f"    Downloading {face_name}...")
            if await self.download_image(session, img_url, save_path):
                downloaded.append(face_name)
                print(f"      ✓ Saved as {face_name}.jpg")
        
        # Duplicate front image for missing faces
        if "front" in downloaded:
            front_path = variant_dir / "front.jpg"
            for face in face_names:
                if face not in downloaded:
                    dst = variant_dir / f"{face}.jpg"
                    if front_path.exists():
                        import shutil
                        shutil.copy2(front_path, dst)
                        print(f"    Duplicated front to {face}")
        
        # Save metadata
        metadata = {
            "title": title,
            "url": product.get('url'),
            "variant_name": variant_name,
            "images_downloaded": downloaded,
            "source": "TCGplayer"
        }
        
        with open(variant_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return variant_name

    async def run(self):
        """Main scraping process"""
        print("=" * 60)
        print("TCGplayer Elite Trainer Box Scraper")
        print("=" * 60)
        
        # Step 1: Get products from search page
        print("\nStep 1: Searching for ETB products...")
        products = await self.scrape_search_page()
        
        if not products:
            print("No products found!")
            return
        
        print(f"\nFound {len(products)} ETB products")
        
        # Step 2: Process each product
        print("\nStep 2: Downloading images for each ETB...")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, product in enumerate(products[:10], 1):  # Process first 10
                tasks.append(self.process_product(session, product, i))
            
            results = await asyncio.gather(*tasks)
            results = [r for r in results if r]  # Filter out None
        
        print("\n" + "=" * 60)
        print(f"✓ Scraping complete!")
        print(f"✓ Downloaded {len(results)} ETB sets")
        print(f"✓ Images saved to: {self.output_dir.absolute()}")

def main():
    scraper = RealETBScraper()
    asyncio.run(scraper.run())

if __name__ == "__main__":
    main()