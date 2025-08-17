#!/usr/bin/env python3
"""
Batch Booster Pack Pipeline
============================

Process multiple booster packs at once from a directory.

Usage:
    python booster_pack_pipeline_batch.py <input_directory>
    
Example:
    python booster_pack_pipeline_batch.py raw_images/booster_packs/

This will process all image files in the directory, using the filename
(without extension) as the set name.
"""

import sys
import os
from pathlib import Path
from booster_pack_pipeline import BoosterPackPipeline

def process_directory(input_dir):
    """Process all images in a directory."""
    input_path = Path(input_dir)
    
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: Directory not found: {input_dir}")
        return False
    
    # Supported image extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG', '.WEBP'}
    
    # Find all image files
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f"*{ext}"))
    
    if not image_files:
        print(f"No image files found in {input_dir}")
        return False
    
    print(f"Found {len(image_files)} image files to process")
    
    # Create pipeline instance
    pipeline = BoosterPackPipeline()
    
    # Process each file
    success_count = 0
    failed_files = []
    
    for img_file in image_files:
        # Extract set name from filename
        set_name = img_file.stem  # filename without extension
        
        # Clean up common suffixes
        for suffix in ['_booster', '_pack', '_booster_pack']:
            if set_name.endswith(suffix):
                set_name = set_name[:-len(suffix)]
                break
        
        print(f"\nProcessing: {img_file.name} -> {set_name}")
        
        try:
            if pipeline.process_booster_pack(set_name, str(img_file)):
                success_count += 1
            else:
                failed_files.append(img_file.name)
        except Exception as e:
            print(f"Error processing {img_file.name}: {e}")
            failed_files.append(img_file.name)
    
    # Print summary
    print(f"\n{'='*60}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total files: {len(image_files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_files)}")
    
    if failed_files:
        print("\nFailed files:")
        for f in failed_files:
            print(f"  - {f}")
    
    return len(failed_files) == 0

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    if process_directory(input_dir):
        print("\n✅ Batch processing completed successfully!")
    else:
        print("\n⚠️ Batch processing completed with some failures")
        sys.exit(1)

if __name__ == "__main__":
    main()