#!/usr/bin/env python3

import json
from pathlib import Path

# Expected card counts for each set (from Pokemon TCG data)
EXPECTED_COUNTS = {
    'xy1': 146,
    'xy2': 109,  # Flashfire
    'xy3': 111,
    'xy4': 119,  # Phantom Forces
    'xy5': 160,  # Primal Clash
    'xy6': 108,
    'xy7': 98,
    'xy8': 162,
    'xy9': 122,  # BREAKpoint
    'xy10': 124,
    'xy11': 114,
    'xy12': 113,  # Evolutions
    
    'sm1': 149,
    'sm2': 145,
    'sm3': 147,  # Burning Shadows
    'sm35': 73,
    'sm4': 111,
    'sm5': 156,
    'sm6': 131,
    'sm7': 168,
    'sm75': 70,
    'sm8': 214,
    'sm9': 181,  # Team Up
    'sm10': 214,
    'sm11': 236,  # Unified Minds
    'sma': 68,   # Hidden Fates (main set)
    'sm115': 68,  # Hidden Fates alternate ID
    'sm12': 236,  # Cosmic Eclipse
    
    'swsh1': 202,
    'swsh2': 192,  # Rebel Clash
    'swsh3': 189,
    'swsh35': 73,
    'swsh4': 185,  # Vivid Voltage
    'swsh45': 72,  # Shining Fates
    'swsh4.5': 72,
    'swsh5': 163,
    'swsh6': 198,
    'swsh7': 203,  # Evolving Skies
    'swsh8': 264,
    'swsh9': 172,  # Brilliant Stars
    'swsh10': 189,
    'swsh11': 196,
    'swsh12': 195,
    'swsh12.5': 160,  # Crown Zenith
    'swsh125': 160,
    
    'sv1': 198,
    'sv2': 193,
    'sv3': 197,
    'sv3.5': 165,  # 151
    'sv35': 165,
    'sv4': 182,
    'sv5': 162,
    'sv6': 167,
    'sv6.5': 64,  # Shrouded Fable
    'sv65': 64,
    'sv7': 142,
    'sv8': 191,  # Surging Sparks
}

# Folder name mappings
FOLDER_MAPPINGS = {
    'xy1': 'xy_base',
    'xy2': 'flashfire',
    'xy3': 'furious_fists',
    'xy4': 'phantom_forces',
    'xy5': 'primal_clash',
    'xy6': 'roaring_skies',
    'xy7': 'ancient_origins',
    'xy8': 'breakthrough',
    'xy9': 'breakpoint',
    'xy10': 'fates_collide',
    'xy11': 'steam_siege',
    'xy12': 'evolutions',
    'sm1': 'sun_moon',
    'sm2': 'guardians_rising',
    'sm3': 'burning_shadows',
    'sm35': 'shining_legends',
    'sm4': 'crimson_invasion',
    'sm5': 'ultra_prism',
    'sm6': 'forbidden_light',
    'sm7': 'celestial_storm',
    'sm75': 'dragon_majesty',
    'sm8': 'lost_thunder',
    'sm9': 'team_up',
    'sm10': 'unbroken_bonds',
    'sm11': 'unified_minds',
    'sma': 'hidden_fates',
    'sm115': 'hidden_fates',
    'sm12': 'cosmic_eclipse',
    'swsh1': 'sword_shield',
    'swsh2': 'rebel_clash',
    'swsh3': 'darkness_ablaze',
    'swsh35': 'champions_path',
    'swsh4': 'vivid_voltage',
    'swsh45': 'shining_fates',
    'swsh4.5': 'shining_fates',
    'swsh5': 'battle_styles',
    'swsh6': 'chilling_reign',
    'swsh7': 'evolving_skies',
    'swsh8': 'fusion_strike',
    'swsh9': 'brilliant_stars',
    'swsh10': 'astral_radiance',
    'swsh11': 'lost_origin',
    'swsh12': 'silver_tempest',
    'swsh125': 'crown_zenith',
    'swsh12.5': 'crown_zenith',
    'sv1': 'scarlet_violet',
    'sv2': 'paldea_evolved',
    'sv3': 'obsidian_flames',
    'sv35': '151',
    'sv3.5': '151',
    'sv4': 'paradox_rift',
    'sv45': 'paldean_fates',
    'sv4.5': 'paldean_fates',
    'sv5': 'temporal_forces',
    'sv6': 'twilight_masquerade',
    'sv65': 'shrouded_fable',
    'sv6.5': 'shrouded_fable',
    'sv7': 'stellar_crown',
    'sv8': 'surging_sparks',
}

def main():
    # Your requested sets
    requested_sets = [
        'xy2', 'xy4', 'xy5', 'xy9', 'xy12',
        'swsh2', 'swsh4', 'swsh45', 'swsh45sv', 'swsh7',
        'swsh12pt5', 'swsh12pt5gg',
        'sm3', 'sm9', 'sm11', 'sm115', 'sm12',
        'sv6pt5', 'sv8', 'sv8pt5',
        'zsv10pt5', 'rsv10pt5'
    ]
    
    # Map to correct API IDs
    api_id_corrections = {
        'swsh45': 'swsh4.5',
        'swsh45sv': None,  # Part of swsh4.5
        'swsh12pt5': 'swsh12.5',
        'swsh12pt5gg': None,  # Part of swsh12.5
        'sm115': 'sma',
        'sv6pt5': 'sv6.5',
        'sv8pt5': None,  # Not released
        'zsv10pt5': None,  # Japanese only
        'rsv10pt5': None,  # Japanese only
    }
    
    # Check local folders
    cards_dir = Path("raw_images/cards")
    
    print("Checking your downloaded sets:")
    print("=" * 60)
    
    complete_sets = []
    incomplete_sets = []
    missing_sets = []
    
    for set_id in requested_sets:
        # Get correct API ID
        api_id = api_id_corrections.get(set_id, set_id)
        
        if api_id is None:
            print(f"✗ {set_id}: Not available in English API")
            continue
        
        # Get folder name
        folder_name = FOLDER_MAPPINGS.get(api_id, api_id)
        folder_path = cards_dir / folder_name
        
        # Also check alternative folder names
        alt_folders = [
            cards_dir / set_id,
            cards_dir / f"xy{set_id[-1]}" if set_id.startswith('xy') else None,
            cards_dir / f"sm{set_id[-1:]}" if set_id.startswith('sm') else None,
        ]
        alt_folders = [f for f in alt_folders if f]
        
        # Find the actual folder
        actual_folder = None
        for check_folder in [folder_path] + alt_folders:
            if check_folder.exists():
                actual_folder = check_folder
                break
        
        if actual_folder and actual_folder.exists():
            png_count = len(list(actual_folder.glob("*.png")))
            expected = EXPECTED_COUNTS.get(api_id, 100)
            
            # Consider complete if within 95% of expected count
            completeness = (png_count / expected * 100) if expected > 0 else 0
            
            if completeness >= 95:
                print(f"✓ {set_id} ({api_id}): COMPLETE - {png_count}/{expected} cards")
                complete_sets.append(api_id)
            else:
                print(f"⚠ {set_id} ({api_id}): PARTIAL - {png_count}/{expected} cards ({completeness:.0f}%)")
                incomplete_sets.append(api_id)
        else:
            print(f"✗ {set_id} ({api_id}): NOT FOUND")
            missing_sets.append(api_id)
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Complete sets: {len(complete_sets)}")
    print(f"Incomplete sets: {len(incomplete_sets)}")
    print(f"Missing sets: {len(missing_sets)}")
    
    # Generate corrected parameter list
    sets_to_download = []
    for s in incomplete_sets + missing_sets:
        if s and s not in complete_sets:
            sets_to_download.append(s)
    
    # Remove duplicates and None values
    sets_to_download = list(set(filter(None, sets_to_download)))
    
    print("\n" + "=" * 60)
    print("SETS YOU STILL NEED TO DOWNLOAD:")
    print(",".join(sets_to_download))
    
    print("\nNote: Some sets like 'zsv10pt5' (Black Bolt) and 'rsv10pt5' (White Flare)")
    print("are Japanese-exclusive and not available in the English Pokemon TCG API.")

if __name__ == "__main__":
    main()
