#!/usr/bin/env python3
"""
Validate the downloaded and processed Pokemon card collection
"""

import json
import os
from pathlib import Path
from PIL import Image
import re
from collections import defaultdict

class CollectionValidator:
    def __init__(self):
        self.raw_dir = Path("raw_images/cards")
        self.processed_dir = Path("raw_images/processed")
        self.issues = defaultdict(list)
        self.stats = {
            "total_sets": 0,
            "total_raw_cards": 0,
            "total_processed_cards": 0,
            "valid_pngs": 0,
            "correct_height": 0,
            "correct_naming": 0,
            "missing_metadata": 0
        }
    
    def validate_filename(self, filename):
        """Check if filename follows pattern: 001_rarity_name.png"""
        pattern = r'^(\d{3}|TG\d+)_[a-z_]+_[a-z0-9_]+\.png$'
        return bool(re.match(pattern, filename))
    
    def validate_image(self, image_path):
        """Validate image is PNG and has 256px height"""
        try:
            with Image.open(image_path) as img:
                is_png = img.format == 'PNG'
                correct_height = img.height == 256
                return is_png, correct_height, img.size
        except Exception as e:
            return False, False, None
    
    def validate_set(self, set_id):
        """Validate a single set"""
        print(f"\nValidating {set_id}...")
        
        raw_set_dir = self.raw_dir / set_id
        processed_set_dir = self.processed_dir / set_id
        
        # Check directories exist
        if not processed_set_dir.exists():
            self.issues[set_id].append("No processed directory")
            return
        
        # Count cards
        raw_cards = list(raw_set_dir.glob("*")) if raw_set_dir.exists() else []
        processed_cards = list(processed_set_dir.glob("*.png"))
        
        self.stats["total_raw_cards"] += len(raw_cards)
        self.stats["total_processed_cards"] += len(processed_cards)
        
        # Check metadata
        metadata_path = processed_set_dir / f"{set_id}_metadata.json"
        if not metadata_path.exists():
            self.issues[set_id].append("Missing metadata file")
            self.stats["missing_metadata"] += 1
        
        # Validate each processed card
        for card_path in processed_cards:
            filename = card_path.name
            
            # Check filename format
            if not self.validate_filename(filename):
                self.issues[set_id].append(f"Invalid filename: {filename}")
            else:
                self.stats["correct_naming"] += 1
            
            # Check image format and size
            is_png, correct_height, size = self.validate_image(card_path)
            
            if is_png:
                self.stats["valid_pngs"] += 1
            else:
                self.issues[set_id].append(f"Not PNG: {filename}")
            
            if correct_height:
                self.stats["correct_height"] += 1
            else:
                if size:
                    self.issues[set_id].append(f"Wrong height ({size[1]}px): {filename}")
                else:
                    self.issues[set_id].append(f"Cannot read image: {filename}")
    
    def run(self):
        """Run validation on all sets"""
        print("="*60)
        print("Pokemon TCG Collection Validator")
        print("="*60)
        
        # Get all processed sets
        if not self.processed_dir.exists():
            print("No processed directory found!")
            return
        
        set_dirs = [d for d in self.processed_dir.iterdir() if d.is_dir()]
        self.stats["total_sets"] = len(set_dirs)
        
        # Validate each set
        for set_dir in sorted(set_dirs):
            self.validate_set(set_dir.name)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        print("\nStatistics:")
        print(f"  Total sets: {self.stats['total_sets']}")
        print(f"  Total raw cards: {self.stats['total_raw_cards']}")
        print(f"  Total processed cards: {self.stats['total_processed_cards']}")
        print(f"  Valid PNGs: {self.stats['valid_pngs']}")
        print(f"  Correct height (256px): {self.stats['correct_height']}")
        print(f"  Correct naming: {self.stats['correct_naming']}")
        print(f"  Sets missing metadata: {self.stats['missing_metadata']}")
        
        # Success rate
        if self.stats['total_processed_cards'] > 0:
            png_rate = (self.stats['valid_pngs'] / self.stats['total_processed_cards']) * 100
            height_rate = (self.stats['correct_height'] / self.stats['total_processed_cards']) * 100
            naming_rate = (self.stats['correct_naming'] / self.stats['total_processed_cards']) * 100
            
            print(f"\nSuccess Rates:")
            print(f"  PNG format: {png_rate:.1f}%")
            print(f"  Correct height: {height_rate:.1f}%")
            print(f"  Correct naming: {naming_rate:.1f}%")
        
        # Issues summary
        if self.issues:
            print(f"\nIssues found in {len(self.issues)} sets:")
            for set_id, issues in sorted(self.issues.items()):
                if len(issues) <= 3:
                    print(f"  {set_id}: {', '.join(issues)}")
                else:
                    print(f"  {set_id}: {len(issues)} issues")
            
            # Save detailed issues to file
            with open("validation_issues.json", "w") as f:
                json.dump(dict(self.issues), f, indent=2)
            print("\nDetailed issues saved to validation_issues.json")
        else:
            print("\n✅ No issues found!")
        
        print("="*60)

if __name__ == "__main__":
    validator = CollectionValidator()
    validator.run()