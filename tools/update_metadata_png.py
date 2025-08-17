#!/usr/bin/env python3
import os
import json

def update_metadata_to_png(set_path):
    """Update cards_metadata.json to reference .png files"""
    metadata_path = os.path.join(set_path, 'cards_metadata.json')
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Update is not needed since metadata doesn't store file extensions
        # The image path is constructed in Java code
        print(f"Metadata in {os.path.basename(set_path)} has {len(metadata['cards'])} cards")

def main():
    base_path = 'src/main/resources/assets/etbmod/textures/cards'
    
    for set_folder in os.listdir(base_path):
        set_path = os.path.join(base_path, set_folder)
        if os.path.isdir(set_path):
            update_metadata_to_png(set_path)

if __name__ == '__main__':
    main()