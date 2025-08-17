#!/usr/bin/env python3
"""
Verify all booster pack items are properly set up
"""

from pathlib import Path
import re

# Check all components
cards_dir = Path("src/main/resources/assets/etbmod/textures/cards")
textures_dir = Path("src/main/resources/assets/etbmod/textures/item")
models_dir = Path("src/main/resources/assets/etbmod/models/item")
items_file = Path("src/main/java/com/example/etbmod/registry/ModItems.java")

# Get all card sets
card_sets = set(d.name for d in cards_dir.iterdir() if d.is_dir())

# Get all booster textures
booster_textures = set(f.stem.replace("etb_", "").replace("_booster", "") 
                       for f in textures_dir.glob("etb_*_booster.png"))

# Get all booster models
booster_models = set(f.stem.replace("etb_", "").replace("_booster", "")
                    for f in models_dir.glob("etb_*_booster.json"))

# Check ModItems.java for registered boosters
registered_boosters = set()
with open(items_file, 'r') as f:
    content = f.read()
    # Find the etbVariants array
    match = re.search(r'String\[\] etbVariants = \{([^}]+)\}', content)
    if match:
        variants_str = match.group(1)
        # Extract all quoted strings
        registered_boosters = set(re.findall(r'"([^"]+)"', variants_str))

print("Booster Pack Setup Verification")
print("=" * 60)

print(f"\n📦 Card Sets: {len(card_sets)}")
print(f"🎨 Booster Textures: {len(booster_textures)}")
print(f"📄 Booster Models: {len(booster_models)}")
print(f"☕ Registered in ModItems: {len(registered_boosters)}")

# Check for mismatches
missing_textures = card_sets - booster_textures
missing_models = booster_textures - booster_models
missing_registration = card_sets - registered_boosters

if missing_textures:
    print(f"\n⚠️ Card sets without booster textures: {missing_textures}")
if missing_models:
    print(f"⚠️ Booster textures without models: {missing_models}")
if missing_registration:
    print(f"⚠️ Card sets not registered in ModItems: {missing_registration}")

if not (missing_textures or missing_models or missing_registration):
    print("\n✅ All booster packs are properly configured!")
    
print("\n" + "=" * 60)

# List ETB blocks and their associated sets
print("\nETB Blocks -> Booster Pack Mapping:")
print("-" * 40)

# ETB blocks that exist
etb_blocks = [
    "black_bolt", "breakpoint", "brilliant_stars", "burning_shadows",
    "cosmic_eclipse", "crown_zenith", "evolutions", "evolving_skies",
    "hidden_fates", "phantom_forces", "primal_clash", "prismatic_evolutions",
    "rebel_clash", "shining_fates", "shrouded_fable", "surging_sparks",
    "team_up", "unified_minds", "vivid_voltage", "white_flare",
    "151", "celebrations", "destined_rivals", "generations",
    "groudon", "journey_together", "kyogre"
]

for etb in sorted(etb_blocks):
    if etb in card_sets:
        print(f"  ETB_{etb.upper()} -> {etb}_booster ✓")
    else:
        print(f"  ETB_{etb.upper()} -> {etb}_booster (no cards)")

print("\nSets without ETB blocks (obtain via creative/commands):")
no_etb = card_sets - set(etb_blocks)
for set_name in sorted(no_etb):
    print(f"  • {set_name}")

print("=" * 60)