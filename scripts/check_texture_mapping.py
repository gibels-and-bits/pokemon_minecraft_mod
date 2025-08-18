#!/usr/bin/env python3
"""
Check that card textures can be properly loaded by verifying metadata matches actual files.
"""

import json
from pathlib import Path

def build_expected_filename(number, rarity, name):
    """Build expected filename matching CardDatabase.java logic."""
    # Clean the name
    clean_name = name.lower()
    clean_name = clean_name.replace("'", "").replace(" ", "_").replace("-", "_")
    clean_name = clean_name.replace(".", "_").replace("é", "e").replace("è", "e").replace("à", "a")
    
    # Handle special Pokemon characters
    clean_name = clean_name.replace("♀", "f").replace("♂", "m")
    clean_name = clean_name.replace(":", "").replace(",", "").replace("!", "")
    clean_name = clean_name.replace("(", "").replace(")", "")
    clean_name = clean_name.replace('"', "").replace("'", "")
    clean_name = clean_name.replace("&", "and")
    clean_name = clean_name.replace("'", "").replace("'", "")  # Different apostrophe types
    
    # Handle Pokémon -> pokemon
    clean_name = clean_name.replace("pokémon", "pokemon")
    clean_name = clean_name.replace("pokégear", "pokegear")
    
    # Build filename
    num_padded = str(number).zfill(3)
    rarity_file = rarity.lower().replace(" ", "_")
    
    return f"{num_padded}_{rarity_file}_{clean_name}.png"

def check_set(set_dir):
    """Check a single set for texture mapping issues."""
    set_name = set_dir.name
    metadata_path = set_dir / "cards_metadata.json"
    
    if not metadata_path.exists():
        return None, []
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    issues = []
    success_count = 0
    total_count = 0
    
    for card in metadata.get('cards', []):
        total_count += 1
        number = card['number']
        name = card['name']
        rarity = card['rarity']
        
        # Build expected filename
        expected = build_expected_filename(number, rarity, name)
        expected_path = set_dir / expected
        
        if expected_path.exists():
            success_count += 1
        else:
            # Find actual file with this number
            num_padded = str(number).zfill(3)
            pattern = f"{num_padded}_*"
            actual_files = list(set_dir.glob(pattern + "*.png"))
            
            if actual_files:
                actual = actual_files[0].name
                issues.append({
                    'number': number,
                    'name': name,
                    'expected': expected,
                    'actual': actual
                })
            else:
                issues.append({
                    'number': number,
                    'name': name,
                    'expected': expected,
                    'actual': None
                })
    
    return (success_count, total_count), issues

def main():
    cards_dir = Path("src/main/resources/assets/etbmod/textures/cards")
    
    print("Checking texture mapping for all sets...")
    print("=" * 70)
    
    all_good = True
    
    for set_dir in sorted(cards_dir.iterdir()):
        if not set_dir.is_dir():
            continue
        
        result = check_set(set_dir)
        if result[0] is None:
            continue
        
        (success, total), issues = result
        
        if issues:
            all_good = False
            print(f"\n{set_dir.name}: {success}/{total} textures mapped correctly")
            print(f"  Issues found: {len(issues)}")
            
            # Show first 3 issues as examples
            for issue in issues[:3]:
                print(f"    Card #{issue['number']}: {issue['name']}")
                print(f"      Expected: {issue['expected']}")
                if issue['actual']:
                    print(f"      Found:    {issue['actual']}")
                else:
                    print(f"      Found:    MISSING")
            
            if len(issues) > 3:
                print(f"    ... and {len(issues) - 3} more issues")
        else:
            print(f"{set_dir.name}: ✓ All {total} textures mapped correctly")
    
    print("=" * 70)
    
    if all_good:
        print("\n✅ All texture mappings are correct!")
    else:
        print("\n⚠️  Some texture mappings have issues.")
        print("The most common issues are:")
        print("  - Special characters in names (é, ', &)")
        print("  - Missing texture files")
        print("  - Different rarity classifications between metadata and filename")

if __name__ == "__main__":
    main()