#!/usr/bin/env python3
"""
Unified download manager for Pokemon TCG card images.
Consolidates functionality from multiple download scripts.
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CardDownloadManager:
    """Manages downloading of Pokemon TCG card images from various sources."""
    
    API_BASE_URL = "https://api.pokemontcg.io/v2"
    GITHUB_BASE = "https://raw.githubusercontent.com/PokemonTCG/pokemon-tcg-data/master/cards/en/"
    
    def __init__(self, output_dir: str = "raw_images/cards", max_workers: int = 5):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': os.getenv('POKEMON_TCG_API_KEY', '')})
        self.progress_file = Path("download_progress.json")
        self.progress = self.load_progress()
    
    def load_progress(self) -> Dict:
        """Load download progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {"completed_sets": [], "failed_downloads": {}}
    
    def save_progress(self):
        """Save download progress to file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_all_sets(self) -> List[Dict]:
        """Fetch all available sets from the API."""
        try:
            response = self.session.get(f"{self.API_BASE_URL}/sets")
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Failed to fetch sets: {e}")
            return []
    
    def get_cards_for_set(self, set_id: str) -> List[Dict]:
        """Fetch all cards for a specific set."""
        cards = []
        page = 1
        
        while True:
            try:
                response = self.session.get(
                    f"{self.API_BASE_URL}/cards",
                    params={'q': f'set.id:{set_id}', 'page': page, 'pageSize': 250}
                )
                response.raise_for_status()
                data = response.json()
                cards.extend(data.get('data', []))
                
                if page >= data.get('totalPages', 1):
                    break
                page += 1
                
            except Exception as e:
                logger.error(f"Failed to fetch cards for set {set_id}: {e}")
                break
        
        return cards
    
    def download_card_image(self, card: Dict, set_dir: Path) -> bool:
        """Download a single card image."""
        card_number = card.get('number', '').zfill(3)
        card_name = card.get('name', 'unknown').replace('/', '_').replace(':', '')
        rarity = card.get('rarity', 'common').lower().replace(' ', '_')
        
        filename = f"{card_number}_{rarity}_{card_name}.png"
        filepath = set_dir / filename
        
        if filepath.exists():
            return True
        
        # Try different image sources
        image_urls = [
            card.get('images', {}).get('large'),
            card.get('images', {}).get('small'),
            f"{self.GITHUB_BASE}{card.get('set', {}).get('id', '')}/{card_number}.png"
        ]
        
        for url in image_urls:
            if url:
                try:
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()
                    filepath.write_bytes(response.content)
                    return True
                except Exception:
                    continue
        
        return False
    
    def download_set(self, set_id: str, set_name: str = None) -> Dict:
        """Download all cards for a specific set."""
        if set_id in self.progress.get("completed_sets", []):
            logger.info(f"Set {set_id} already completed, skipping")
            return {"success": 0, "failed": 0, "skipped": 1}
        
        set_dir = self.output_dir / set_id
        set_dir.mkdir(exist_ok=True)
        
        logger.info(f"Downloading set: {set_name or set_id}")
        cards = self.get_cards_for_set(set_id)
        
        if not cards:
            logger.warning(f"No cards found for set {set_id}")
            return {"success": 0, "failed": 0, "skipped": 0}
        
        success_count = 0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.download_card_image, card, set_dir): card
                for card in cards
            }
            
            for future in as_completed(futures):
                card = futures[future]
                try:
                    if future.result():
                        success_count += 1
                    else:
                        failed_count += 1
                        card_id = f"{set_id}_{card.get('number', 'unknown')}"
                        self.progress.setdefault("failed_downloads", {})[card_id] = card.get('name', 'unknown')
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Error downloading card: {e}")
        
        # Save metadata
        metadata = {
            "set_id": set_id,
            "set_name": set_name,
            "total_cards": len(cards),
            "downloaded": success_count,
            "failed": failed_count,
            "cards": [
                {
                    "number": card.get('number'),
                    "name": card.get('name'),
                    "rarity": card.get('rarity'),
                    "types": card.get('types', []),
                    "hp": card.get('hp'),
                    "artist": card.get('artist')
                }
                for card in cards
            ]
        }
        
        metadata_file = set_dir / "cards_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        if failed_count == 0:
            self.progress.setdefault("completed_sets", []).append(set_id)
            self.save_progress()
        
        logger.info(f"Set {set_id}: {success_count} downloaded, {failed_count} failed")
        return {"success": success_count, "failed": failed_count, "skipped": 0}
    
    def download_multiple_sets(self, set_ids: List[str]) -> Dict:
        """Download multiple sets."""
        all_sets = {s['id']: s['name'] for s in self.get_all_sets()}
        total_stats = {"success": 0, "failed": 0, "skipped": 0}
        
        for set_id in set_ids:
            if set_id in all_sets:
                stats = self.download_set(set_id, all_sets[set_id])
                for key in total_stats:
                    total_stats[key] += stats[key]
            else:
                logger.warning(f"Set {set_id} not found")
        
        return total_stats
    
    def download_all_sets(self):
        """Download all available sets."""
        all_sets = self.get_all_sets()
        set_ids = [s['id'] for s in all_sets]
        return self.download_multiple_sets(set_ids)
    
    def retry_failed_downloads(self):
        """Retry all previously failed downloads."""
        failed = self.progress.get("failed_downloads", {})
        retry_count = 0
        success_count = 0
        
        for card_id in list(failed.keys()):
            set_id, card_number = card_id.rsplit('_', 1)
            set_dir = self.output_dir / set_id
            
            # Attempt to re-download
            cards = self.get_cards_for_set(set_id)
            for card in cards:
                if card.get('number') == card_number:
                    if self.download_card_image(card, set_dir):
                        success_count += 1
                        del failed[card_id]
                    retry_count += 1
                    break
        
        self.save_progress()
        logger.info(f"Retried {retry_count} downloads, {success_count} successful")
        return {"retried": retry_count, "success": success_count}


def main():
    """Main entry point for the download manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pokemon TCG Card Download Manager")
    parser.add_argument('--sets', nargs='+', help='Specific set IDs to download')
    parser.add_argument('--all', action='store_true', help='Download all available sets')
    parser.add_argument('--retry', action='store_true', help='Retry failed downloads')
    parser.add_argument('--workers', type=int, default=5, help='Number of concurrent downloads')
    parser.add_argument('--output', default='raw_images/cards', help='Output directory')
    
    args = parser.parse_args()
    
    manager = CardDownloadManager(output_dir=args.output, max_workers=args.workers)
    
    if args.retry:
        manager.retry_failed_downloads()
    elif args.all:
        manager.download_all_sets()
    elif args.sets:
        manager.download_multiple_sets(args.sets)
    else:
        # Download sets used in the mod
        mod_sets = [
            'swsh12pt5', 'swsh45', 'swsh11', 'swsh35', 'sm10', 'sm12', 
            'xy2', 'xy5', 'sm3', 'xy9', 'xy12', 'cel25', 'swsh12', 
            'sv6pt5', 'sv8', 'sv7', 'swsh4', 'sv9', 'sma', 'bwp', 
            'sv6', 'g1', 'ex13', 'ex14'
        ]
        manager.download_multiple_sets(mod_sets)


if __name__ == "__main__":
    main()