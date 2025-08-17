#!/usr/bin/env python3
"""
Direct ETB image scraper - fetches from known product pages
"""

import os
import asyncio
import aiohttp
from pathlib import Path
import json

class DirectETBScraper:
    def __init__(self, output_dir="raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Direct links to ETB products (these are example URLs - replace with actual ones)
        self.etb_products = [
            {
                "name": "Surging Sparks",
                "images": [
                    "https://product-images.tcgplayer.com/516170.jpg",
                    "https://product-images.tcgplayer.com/516171.jpg"
                ]
            },
            {
                "name": "Stellar Crown", 
                "images": [
                    "https://product-images.tcgplayer.com/512890.jpg",
                    "https://product-images.tcgplayer.com/512891.jpg"
                ]
            },
            {
                "name": "Shrouded Fable",
                "images": [
                    "https://product-images.tcgplayer.com/509432.jpg",
                    "https://product-images.tcgplayer.com/509433.jpg"
                ]
            },
            {
                "name": "Twilight Masquerade",
                "images": [
                    "https://product-images.tcgplayer.com/505876.jpg",
                    "https://product-images.tcgplayer.com/505877.jpg"
                ]
            },
            {
                "name": "Temporal Forces",
                "images": [
                    "https://product-images.tcgplayer.com/502420.jpg",
                    "https://product-images.tcgplayer.com/502421.jpg"
                ]
            },
            {
                "name": "Paldea Evolved",
                "images": [
                    "https://product-images.tcgplayer.com/492722.jpg",
                    "https://product-images.tcgplayer.com/492723.jpg"
                ]
            },
            {
                "name": "Obsidian Flames",
                "images": [
                    "https://product-images.tcgplayer.com/496246.jpg",
                    "https://product-images.tcgplayer.com/496247.jpg"
                ]
            },
            {
                "name": "Paradox Rift",
                "images": [
                    "https://product-images.tcgplayer.com/499090.jpg",
                    "https://product-images.tcgplayer.com/499091.jpg"
                ]
            },
            {
                "name": "Scarlet Violet Base",
                "images": [
                    "https://product-images.tcgplayer.com/489322.jpg",
                    "https://product-images.tcgplayer.com/489323.jpg"
                ]
            },
            {
                "name": "Crown Zenith",
                "images": [
                    "https://product-images.tcgplayer.com/486066.jpg",
                    "https://product-images.tcgplayer.com/486067.jpg"
                ]
            }
        ]

    def sanitize_name(self, name):
        """Convert product name to valid folder name"""
        import re
        name = name.lower()
        name = re.sub(r'[^a-z0-9\s\-]', '', name)
        name = re.sub(r'\s+', '_', name)
        name = f"etb_{name}"
        return name[:50]

    async def download_image(self, session, url, save_path):
        """Download an image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    return True
                else:
                    print(f"    Failed to download (status {response.status}): {url}")
        except Exception as e:
            print(f"    Error downloading {url}: {e}")
        return False

    async def process_etb(self, session, etb_data):
        """Process a single ETB product"""
        name = etb_data["name"]
        print(f"\nProcessing: {name} Elite Trainer Box")
        
        variant_name = self.sanitize_name(name)
        variant_dir = self.output_dir / variant_name
        variant_dir.mkdir(exist_ok=True)
        
        # Download images
        downloaded = []
        for i, img_url in enumerate(etb_data["images"]):
            # Assign face names based on order
            face_names = ["front", "back", "left", "right", "top", "bottom"]
            face_name = face_names[i] if i < len(face_names) else f"extra_{i}"
            
            save_path = variant_dir / f"{face_name}.jpg"
            print(f"  Downloading {face_name} from {img_url}")
            
            if await self.download_image(session, img_url, save_path):
                downloaded.append(face_name)
                print(f"    ✓ Saved as {face_name}.jpg")
        
        # For missing faces, copy from available ones
        if "front" in downloaded:
            for face in ["left", "right", "top", "bottom"]:
                if face not in downloaded:
                    src = variant_dir / "front.jpg"
                    dst = variant_dir / f"{face}.jpg"
                    if src.exists():
                        import shutil
                        shutil.copy2(src, dst)
                        print(f"    Copied front to {face}")
        
        # Save metadata
        metadata = {
            "title": f"Pokemon {name} Elite Trainer Box",
            "variant_name": variant_name,
            "images_downloaded": downloaded,
            "source": "TCGplayer"
        }
        
        with open(variant_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return variant_name

    async def run(self):
        """Main scraping process"""
        print("Direct ETB Image Scraper")
        print("=" * 50)
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for etb_data in self.etb_products:
                tasks.append(self.process_etb(session, etb_data))
            
            results = await asyncio.gather(*tasks)
        
        print("\n" + "=" * 50)
        print(f"Scraping complete! Downloaded {len(results)} ETB sets")
        print(f"Images saved to: {self.output_dir.absolute()}")

def main():
    scraper = DirectETBScraper()
    asyncio.run(scraper.run())

if __name__ == "__main__":
    main()