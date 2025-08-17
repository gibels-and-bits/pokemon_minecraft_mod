#!/usr/bin/env python3
"""
High-resolution TCGplayer ETB scraper
Clicks into each product to get full resolution images
"""

import os
import asyncio
import aiohttp
from pathlib import Path
import json
from playwright.async_api import async_playwright
from urllib.parse import urljoin, quote
from PIL import Image
import numpy as np

class HiResETBScraper:
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

    async def get_product_links(self):
        """Get all product links from the search page"""
        products = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Navigate to the search page
                search_url = "https://www.tcgplayer.com/search/pokemon/product?page=1&productLineName=pokemon&q=elite+trainer+box&view=grid"
                print(f"Loading search page...")
                await page.goto(search_url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(2000)
                
                # Get all product links
                print("Finding product links...")
                
                # Wait for page to fully load
                await page.wait_for_timeout(3000)
                
                # Try to find product cards with different selectors
                product_elements = await page.query_selector_all('div.search-result')
                
                if not product_elements:
                    product_elements = await page.query_selector_all('.product-card')
                
                if not product_elements:
                    # Look for any links with Elite Trainer Box in them
                    all_links = await page.query_selector_all('a')
                    product_elements = []
                    for link in all_links:
                        try:
                            text = await link.inner_text()
                            if text and ("elite trainer" in text.lower() or "etb" in text.lower()):
                                product_elements.append(link)
                        except:
                            continue
                
                print(f"Found {len(product_elements)} product links")
                
                for elem in product_elements[:15]:  # Get first 15 products
                    try:
                        # Get tag name to determine element type
                        tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                        
                        if tag_name == 'div':
                            # It's a search result div, find the link inside
                            link_elem = await elem.query_selector('a')
                            if link_elem:
                                href = await link_elem.get_attribute('href')
                            else:
                                continue
                            
                            # Try to get title from various places
                            title = ""
                            title_selectors = ['.product-card__title', 'h3', 'h4', 'span']
                            for sel in title_selectors:
                                title_elem = await elem.query_selector(sel)
                                if title_elem:
                                    title = await title_elem.inner_text()
                                    break
                        else:
                            # It's already a link
                            href = await elem.get_attribute('href')
                            title = await elem.inner_text()
                        
                        if href and title and ("elite trainer" in title.lower() or "etb" in title.lower()):
                            full_url = urljoin(self.base_url, href)
                            products.append({
                                'url': full_url,
                                'title': title.strip()
                            })
                            print(f"  Found: {title.strip()}")
                    except Exception as e:
                        print(f"    Error processing element: {e}")
                        continue
                
            except Exception as e:
                print(f"Error getting product links: {e}")
            finally:
                await browser.close()
        
        return products

    async def get_hires_image(self, product_url, product_title):
        """Click into product page and get the high-res image"""
        images = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                print(f"  Loading product page: {product_title}")
                await page.goto(product_url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(2000)
                
                # Look for the main product image (usually larger)
                main_image = None
                
                # Try clicking on the image to get full size
                try:
                    # Find the main product image
                    main_img_elem = await page.query_selector('.product-details__image img, .product-image img, [data-testid="product-image"] img')
                    
                    if main_img_elem:
                        # Try to click it to open larger version
                        await main_img_elem.click()
                        await page.wait_for_timeout(1000)
                        
                        # Look for modal/zoomed image
                        zoomed = await page.query_selector('.modal img, .zoom img, .magnify img, [role="dialog"] img')
                        if zoomed:
                            main_image = await zoomed.get_attribute('src')
                            if not main_image:
                                main_image = await zoomed.get_attribute('data-src')
                        
                        # Close modal if opened
                        close_btn = await page.query_selector('.modal-close, .close, [aria-label="Close"]')
                        if close_btn:
                            await close_btn.click()
                except:
                    pass
                
                # If no zoomed image, get the main display image
                if not main_image:
                    selectors = [
                        '.product-details__image img',
                        '.product-image--main img',
                        '.product-image img',
                        '[data-testid="product-image"] img',
                        '.listing-item__image img',
                        'img[alt*="Elite Trainer"]',
                        'img[alt*="ETB"]'
                    ]
                    
                    for selector in selectors:
                        elem = await page.query_selector(selector)
                        if elem:
                            src = await elem.get_attribute('src')
                            if not src:
                                src = await elem.get_attribute('data-src')
                            
                            if src and not src.startswith('data:'):
                                main_image = src
                                break
                
                if main_image:
                    # Convert to high-res URL if it's a TCGplayer image
                    if 'tcgplayer.com' in main_image:
                        # Remove size constraints from URL
                        main_image = main_image.replace('/200x200/', '/680x680/')
                        main_image = main_image.replace('/400x400/', '/680x680/')
                        main_image = main_image.replace('/fit-in/', '/680x680/')
                        
                        # Try to get the original image URL
                        if 'product-images.tcgplayer.com' in main_image:
                            # Extract product ID and reconstruct URL
                            import re
                            match = re.search(r'/(\d+)\.jpg', main_image)
                            if match:
                                product_id = match.group(1)
                                main_image = f"https://product-images.tcgplayer.com/{product_id}.jpg"
                    
                    images.append(main_image)
                    print(f"    Found high-res image: {main_image}")
                
            except Exception as e:
                print(f"    Error getting high-res image: {e}")
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

    def create_black_texture(self, size=32):
        """Create a plain black texture"""
        img = Image.new('RGB', (size, size), (0, 0, 0))
        return img

    def extract_front_from_angled(self, image_path):
        """Extract the front face from an angled box image"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # For angled ETB images, the front is usually on the left side
            # Crop to get mainly the front face (left 60% of image)
            front_crop = img.crop((0, 0, int(width * 0.6), height))
            
            # Resize to square
            size = min(front_crop.size)
            left = (front_crop.width - size) // 2
            top = (front_crop.height - size) // 2
            front_crop = front_crop.crop((left, top, left + size, top + size))
            
            return front_crop
        except Exception as e:
            print(f"      Error extracting front: {e}")
            return None

    def extract_side_from_angled(self, image_path):
        """Extract the side face from an angled box image"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # For angled ETB images, the side is usually on the right
            # Crop to get mainly the side face (right 40% of image)
            side_crop = img.crop((int(width * 0.6), 0, width, height))
            
            # The side is at an angle, so we'll do a simple perspective adjustment
            # For now, just resize to square
            size = min(side_crop.size)
            left = (side_crop.width - size) // 2
            top = (side_crop.height - size) // 2
            side_crop = side_crop.crop((left, top, left + size, top + size))
            
            return side_crop
        except Exception as e:
            print(f"      Error extracting side: {e}")
            return None

    async def process_product(self, session, product, index):
        """Process a single ETB product"""
        title = product['title']
        print(f"\n[{index}] Processing: {title}")
        
        variant_name = self.sanitize_name(title)
        variant_dir = self.output_dir / variant_name
        variant_dir.mkdir(exist_ok=True)
        
        # Get high-res image from product page
        images = await self.get_hires_image(product['url'], title)
        
        if not images:
            print(f"    No images found for {title}")
            return None
        
        # Download the main image
        main_image_path = variant_dir / "main.jpg"
        
        print(f"    Downloading high-res image...")
        if await self.download_image(session, images[0], main_image_path):
            print(f"      ✓ Downloaded main image")
            
            # Extract front and side from the angled image
            print(f"    Extracting faces from angled image...")
            
            front_img = self.extract_front_from_angled(main_image_path)
            if front_img:
                front_img.save(variant_dir / "front.jpg", quality=95)
                print(f"      ✓ Extracted front face")
            
            side_img = self.extract_side_from_angled(main_image_path)
            if side_img:
                side_img.save(variant_dir / "left.jpg", quality=95)
                side_img.save(variant_dir / "right.jpg", quality=95)  # Mirror for other side
                print(f"      ✓ Extracted side faces")
            
            # Create black textures for back, top, and bottom
            print(f"    Creating black textures for other faces...")
            black = self.create_black_texture(256)
            black.save(variant_dir / "back.jpg", quality=95)
            black.save(variant_dir / "top.jpg", quality=95)
            black.save(variant_dir / "bottom.jpg", quality=95)
            print(f"      ✓ Created black textures")
        
        # Save metadata
        metadata = {
            "title": title,
            "url": product['url'],
            "variant_name": variant_name,
            "source": "TCGplayer (high-res)"
        }
        
        with open(variant_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return variant_name

    async def run(self):
        """Main scraping process"""
        print("=" * 60)
        print("High-Resolution TCGplayer ETB Scraper")
        print("=" * 60)
        
        # Step 1: Get product links
        print("\nStep 1: Getting product links from search page...")
        products = await self.get_product_links()
        
        if not products:
            print("No products found!")
            return
        
        print(f"\nFound {len(products)} ETB products")
        
        # Step 2: Process each product
        print("\nStep 2: Downloading high-res images...")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, product in enumerate(products[:10], 1):  # Process first 10
                tasks.append(self.process_product(session, product, i))
            
            results = await asyncio.gather(*tasks)
            results = [r for r in results if r]  # Filter out None
        
        print("\n" + "=" * 60)
        print(f"✓ Scraping complete!")
        print(f"✓ Downloaded {len(results)} ETB sets with high-res images")
        print(f"✓ Images saved to: {self.output_dir.absolute()}")

def main():
    scraper = HiResETBScraper()
    asyncio.run(scraper.run())

if __name__ == "__main__":
    main()