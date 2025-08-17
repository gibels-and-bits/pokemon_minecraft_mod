#!/usr/bin/env python3
"""
List all available Pokemon TCG sets from the API
"""

import requests
import json
from pathlib import Path

API_KEY = "5e6e30b3-0ae2-4df5-9c43-801bba46c0bf"
API_BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": API_KEY}

def list_all_sets():
    """Get and display all available sets"""
    print("Fetching all available sets from Pokemon TCG API...")
    print("=" * 60)
    
    url = f"{API_BASE_URL}/sets"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        sets = data.get('data', [])
        
        # Save full data
        output_file = Path("raw_images/cards/all_sets.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(sets, f, indent=2)
        
        print(f"Found {len(sets)} sets total\n")
        
        # Look for our specific sets
        print("Searching for matches to our ETB sets:")
        print("-" * 60)
        
        keywords = ['151', 'celebrations', 'brilliant', 'stars', 'generations', 
                   'primal', 'clash', 'surging', 'sparks', 'prismatic', 
                   'scarlet', 'violet', 'crown', 'zenith', 'astral']
        
        matches = []
        for set_data in sets:
            name_lower = set_data['name'].lower()
            if any(keyword in name_lower for keyword in keywords):
                matches.append(set_data)
                print(f"ID: {set_data['id']:<15} | {set_data['name']:<40} | {set_data.get('releaseDate', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("Recent sets (2022-2024):")
        print("-" * 60)
        
        for set_data in sets:
            release = set_data.get('releaseDate', '')
            if release and ('2022' in release or '2023' in release or '2024' in release):
                print(f"ID: {set_data['id']:<15} | {set_data['name']:<40} | {release}")
        
        print(f"\n✓ Full list saved to: {output_file}")
        
        return sets
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    list_all_sets()