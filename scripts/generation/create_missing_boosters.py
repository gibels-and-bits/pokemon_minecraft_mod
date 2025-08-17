#!/usr/bin/env python3
"""
Create placeholder booster pack textures for all card sets
"""

import shutil
from pathlib import Path

# Paths
texture_dir = Path("src/main/resources/assets/etbmod/textures/item")
card_sets_dir = Path("src/main/resources/assets/etbmod/textures/cards")
placeholder = texture_dir / "etb_white_flare_booster.png"

# Get all card sets
card_sets = [d.name for d in card_sets_dir.iterdir() if d.is_dir()]

# Create booster textures
created = []
already_exists = []

for set_name in sorted(card_sets):
    booster_name = f"etb_{set_name}_booster.png"
    booster_path = texture_dir / booster_name
    
    if booster_path.exists():
        already_exists.append(set_name)
    else:
        shutil.copy2(placeholder, booster_path)
        created.append(set_name)

print("Booster Pack Texture Creation")
print("=" * 60)
print(f"Created {len(created)} new booster pack textures:")
for name in created:
    print(f"  • {name}")

print(f"\nAlready existed: {len(already_exists)}")
print("=" * 60)