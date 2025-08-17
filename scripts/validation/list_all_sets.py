#!/usr/bin/env python3
"""
List all Pokemon TCG sets with their IDs, names, and card counts
"""

import requests
import json
from datetime import datetime

def fetch_and_list_sets():
    """Fetch and display all available sets"""
    
    print("Fetching sets from Pokemon TCG API...")
    
    try:
        response = requests.get("https://api.pokemontcg.io/v2/sets", timeout=60)
        if response.status_code != 200:
            print(f"Error fetching sets: {response.status_code}")
            return None
        
        data = response.json()
        sets = data.get('data', [])
        
        # Sort by series and release date
        sets.sort(key=lambda x: (x.get('series', ''), x.get('releaseDate', '')))
        
        print(f"\nFound {len(sets)} total sets")
        print("="*80)
        
        # Group by series
        current_series = None
        series_sets = {}
        
        for s in sets:
            series = s.get('series', 'Unknown')
            if series not in series_sets:
                series_sets[series] = []
            series_sets[series].append(s)
        
        # Display sets grouped by series
        total_cards = 0
        all_set_ids = []
        
        for series in sorted(series_sets.keys()):
            print(f"\n{series} Series:")
            print("-"*60)
            
            for s in series_sets[series]:
                set_id = s.get('id', 'unknown')
                name = s.get('name', 'Unknown')
                card_count = s.get('total', 0)
                release = s.get('releaseDate', 'N/A')
                
                all_set_ids.append(set_id)
                total_cards += card_count
                
                # Format output
                print(f"  {set_id:<15} | {name:<40} | {card_count:>4} cards | {release}")
        
        print("\n" + "="*80)
        print(f"Total: {len(sets)} sets, {total_cards:,} cards")
        print("="*80)
        
        # Save to file for easy reference
        with open('all_sets_detailed.json', 'w') as f:
            json.dump(sets, f, indent=2)
        
        # Create a simple ID list file
        with open('set_ids_list.txt', 'w') as f:
            f.write("# Pokemon TCG Set IDs\n")
            f.write(f"# Total: {len(sets)} sets\n")
            f.write("# Format: set_id | set_name | card_count\n")
            f.write("#" + "="*60 + "\n\n")
            
            for series in sorted(series_sets.keys()):
                f.write(f"\n# {series} Series\n")
                for s in series_sets[series]:
                    f.write(f"{s.get('id'):<15} | {s.get('name'):<40} | {s.get('total', 0)} cards\n")
        
        print("\n📁 Saved detailed data to:")
        print("  - all_sets_detailed.json (full API data)")
        print("  - set_ids_list.txt (simple reference list)")
        
        return all_set_ids
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_download_list_template():
    """Create a template file for selecting sets to download"""
    
    template = """# Pokemon TCG Sets to Download
# Uncomment the sets you want to download (remove the # at the beginning of the line)
# Save this file and use it with: python3 download_selected_sets.py sets_to_download.txt

# === MODERN SETS (Recommended) ===

# Scarlet & Violet Series (2023-2025)
sv1      # Scarlet & Violet (258 cards)
sv2      # Paldea Evolved (279 cards)
sv3      # Obsidian Flames (230 cards)
sv3pt5   # 151 (207 cards)
sv4      # Paradox Rift (266 cards)
sv4pt5   # Paldean Fates (245 cards)
sv5      # Temporal Forces (218 cards)
sv6      # Twilight Masquerade (226 cards)
sv6pt5   # Shrouded Fable (99 cards)
sv7      # Stellar Crown (175 cards)
sv8      # Surging Sparks (252 cards)
sv8pt5   # Prismatic Evolutions (180 cards)
sv9      # Journey Together (190 cards)
sv10     # Destined Rivals (244 cards)

# Sword & Shield Series (2020-2023)
swsh1    # Sword & Shield (216 cards)
swsh2    # Rebel Clash (209 cards)
swsh3    # Darkness Ablaze (201 cards)
swsh4    # Vivid Voltage (203 cards)
swsh5    # Battle Styles (183 cards)
swsh6    # Chilling Reign (233 cards)
swsh7    # Evolving Skies (237 cards)
swsh8    # Fusion Strike (284 cards)
swsh9    # Brilliant Stars (186 cards)
swsh9tg  # Brilliant Stars Trainer Gallery (30 cards)
swsh10   # Astral Radiance (216 cards)
swsh10tg # Astral Radiance Trainer Gallery (30 cards)
swsh11   # Lost Origin (217 cards)
swsh11tg # Lost Origin Trainer Gallery (30 cards)
swsh12   # Silver Tempest (215 cards)
swsh12tg # Silver Tempest Trainer Gallery (30 cards)
swsh12pt5 # Crown Zenith (230 cards)

# Special/Celebration Sets
cel25    # Celebrations (25 cards)
cel25c   # Celebrations: Classic Collection (25 cards)

# === CLASSIC SETS ===

# Sun & Moon Series (2017-2019)
# sm1      # Sun & Moon (163 cards)
# sm2      # Guardians Rising (169 cards)
# sm3      # Burning Shadows (169 cards)
# sm4      # Crimson Invasion (124 cards)
# sm5      # Ultra Prism (173 cards)
# sm6      # Forbidden Light (146 cards)
# sm7      # Celestial Storm (183 cards)
# sm8      # Lost Thunder (236 cards)
# sm9      # Team Up (196 cards)
# sm10     # Unbroken Bonds (234 cards)
# sm11     # Unified Minds (260 cards)
# sm12     # Cosmic Eclipse (272 cards)

# XY Series (2014-2017)
# xy1      # XY (146 cards)
# xy2      # Flashfire (109 cards)
# xy3      # Furious Fists (113 cards)
# xy4      # Phantom Forces (122 cards)
# xy5      # Primal Clash (164 cards)
# xy6      # Roaring Skies (110 cards)
# xy7      # Ancient Origins (100 cards)
# xy8      # BREAKthrough (164 cards)
# xy9      # BREAKpoint (123 cards)
# xy10     # Fates Collide (125 cards)
# xy11     # Steam Siege (116 cards)
# xy12     # Evolutions (113 cards)

# Black & White Series (2011-2013)
# bw1      # Black & White (115 cards)
# bw2      # Emerging Powers (98 cards)
# bw3      # Noble Victories (102 cards)
# bw4      # Next Destinies (103 cards)
# bw5      # Dark Explorers (111 cards)
# bw6      # Dragons Exalted (128 cards)
# bw7      # Boundaries Crossed (153 cards)
# bw8      # Plasma Storm (138 cards)
# bw9      # Plasma Freeze (122 cards)
# bw10     # Plasma Blast (105 cards)
# bw11     # Legendary Treasures (140 cards)

# === VINTAGE SETS ===

# Base Series (1999-2000)
# base1    # Base (102 cards)
# base2    # Jungle (64 cards)
# base3    # Fossil (62 cards)
# base4    # Base Set 2 (130 cards)
# base5    # Team Rocket (83 cards)
# base6    # Gym Heroes (132 cards)
# gym1     # Gym Heroes (132 cards)
# gym2     # Gym Challenge (132 cards)

# Neo Series (2000-2001)
# neo1     # Neo Genesis (111 cards)
# neo2     # Neo Discovery (75 cards)
# neo3     # Neo Revelation (66 cards)
# neo4     # Neo Destiny (113 cards)
"""
    
    with open('sets_to_download.txt', 'w') as f:
        f.write(template)
    
    print("\n📝 Created sets_to_download.txt")
    print("   Edit this file to select which sets you want to download")
    print("   Uncomment the lines for sets you want (remove the # at the start)")

if __name__ == "__main__":
    print("="*80)
    print("Pokemon TCG Sets Listing Tool")
    print("="*80)
    
    # List all sets
    set_ids = fetch_and_list_sets()
    
    if set_ids:
        # Create download template
        create_download_list_template()
        
        print("\n" + "="*80)
        print("Next steps:")
        print("1. Edit 'sets_to_download.txt' to select sets you want")
        print("2. Run: python3 download_selected_sets.py sets_to_download.txt")
        print("="*80)