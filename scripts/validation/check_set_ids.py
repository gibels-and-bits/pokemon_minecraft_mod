#!/usr/bin/env python3
"""
Check correct Pokemon TCG API set IDs
"""

# Known correct set IDs from Pokemon TCG API documentation
CORRECT_SET_IDS = {
    # XY Series
    'xy1': 'XY Base Set',
    'xy2': 'Flashfire',
    'xy3': 'Furious Fists', 
    'xy4': 'Phantom Forces',
    'xy5': 'Primal Clash',
    'xy6': 'Roaring Skies',
    'xy7': 'Ancient Origins',
    'xy8': 'BREAKthrough',
    'xy9': 'BREAKpoint',
    'xy10': 'Fates Collide',
    'xy11': 'Steam Siege',
    'xy12': 'Evolutions',
    
    # Sun & Moon Series
    'sm1': 'Sun & Moon Base',
    'sm2': 'Guardians Rising',
    'sm3': 'Burning Shadows',
    'sm35': 'Shining Legends',
    'sm4': 'Crimson Invasion', 
    'sm5': 'Ultra Prism',
    'sm6': 'Forbidden Light',
    'sm7': 'Celestial Storm',
    'sm75': 'Dragon Majesty',
    'sm8': 'Lost Thunder',
    'sm9': 'Team Up',
    'sm10': 'Unbroken Bonds',
    'sm11': 'Unified Minds',
    'sm115': 'Hidden Fates',  # This might be 'sma' in the API
    'sm12': 'Cosmic Eclipse',
    
    # Sword & Shield Series  
    'swsh1': 'Sword & Shield Base',
    'swsh2': 'Rebel Clash',
    'swsh3': 'Darkness Ablaze',
    'swsh35': 'Champions Path',
    'swsh4': 'Vivid Voltage',
    'swsh45': 'Shining Fates',  # Might be 'swsh4.5'
    'swsh5': 'Battle Styles',
    'swsh6': 'Chilling Reign',
    'swsh7': 'Evolving Skies',
    'swsh8': 'Fusion Strike',
    'swsh9': 'Brilliant Stars',
    'swsh10': 'Astral Radiance',
    'swsh11': 'Lost Origin',
    'swsh12': 'Silver Tempest',
    'swsh125': 'Crown Zenith',  # Might be 'swsh12.5'
    
    # Scarlet & Violet Series
    'sv1': 'Scarlet & Violet Base',
    'sv2': 'Paldea Evolved',
    'sv3': 'Obsidian Flames',
    'sv35': '151',  # Might be 'sv3.5' or 'sv3pt5'
    'sv4': 'Paradox Rift',
    'sv45': 'Paldean Fates',
    'sv5': 'Temporal Forces',
    'sv6': 'Twilight Masquerade',
    'sv65': 'Shrouded Fable',  # Might be 'sv6.5'
    'sv7': 'Stellar Crown',
    'sv8': 'Surging Sparks',
}

# The issue is that the API might use different IDs
# Common variations:
# - sm115 might be 'sma' (Hidden Fates Shiny Vault)
# - swsh45 might be 'swsh4.5'
# - sv35 might be 'svp' or 'sv3.5'

print("Checking your requested sets:")
print("-" * 60)

requested = ['xy2','xy4','xy5','xy9','xy12','swsh2','swsh4',
             'swsh45','swsh45sv','swsh7','swsh12pt5','swsh12pt5gg',
             'sm3','sm9','sm11','sm115','sm12','sv6pt5','sv8',
             'sv8pt5','zsv10pt5','rsv10pt5']

for set_id in requested:
    if set_id in CORRECT_SET_IDS:
        print(f"✓ {set_id}: {CORRECT_SET_IDS[set_id]}")
    else:
        print(f"✗ {set_id}: UNKNOWN - needs correct ID")

print("\nLikely corrections needed:")
print("- sm115 → Try 'sma' (Hidden Fates)")
print("- swsh45 → Try 'swsh4.5' (Shining Fates)")
print("- swsh45sv → Shining Fates Shiny Vault (part of swsh4.5)")
print("- swsh12pt5 → Try 'swsh12.5' (Crown Zenith)")
print("- sv6pt5 → Try 'sv6.5' (Shrouded Fable)")
print("- sv8pt5 → Not released yet (Prismatic Evolutions)")
print("- zsv10pt5/rsv10pt5 → Japanese sets, not in English API")
