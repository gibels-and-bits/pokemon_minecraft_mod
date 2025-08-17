# Project Structure Overview

## Main Directories

### `/src/`
Source code for the Minecraft mod
- `main/java/com/github/sirblobman/etb/` - Java mod code
- `main/resources/assets/etbmod/` - Textures and assets
  - `textures/blocks/` - ETB block textures
  - `textures/cards/` - Card textures for each set
  - `textures/items/` - Booster pack item textures

### `/raw_images/`
Original high-resolution images
- `cards/` - Raw card images organized by set
  - `151/` - Scarlet & Violet 151 set
  - `brilliant_stars/` - Brilliant Stars set
  - `celebrations/` - Celebrations set
  - `destined_rivals/` - Destined Rivals set
  - `journey_together/` - Journey Together set
  - `surging_sparks/` - Surging Sparks set
  - `prismatic_evolutions/` - Prismatic Evolutions set
  - Plus legacy sets: black_bolt, white_flare, generations, groudon, kyogre
- `booster_packs/` - Original booster pack images
- `booster_packs_clean/` - Processed booster pack textures

### `/tools/`
Utility scripts for asset processing
- Card fetching and processing scripts
- Booster pack pipeline tools
- Texture generation utilities
- Validation scripts

### `/archive/`
Archived scripts (old versions, tests, etc.)
- `fetch_scripts/` - Old card fetching scripts
- `old_scripts/` - Deprecated processing scripts
- `test_scripts/` - Test utilities

### `/build/`
Gradle build outputs
- `libs/` - Compiled JAR files

### `/gradle/`
Gradle wrapper files

### `/run/`
Minecraft runtime directory (for testing)

## Key Files

- `build.gradle` - Gradle build configuration
- `gradle.properties` - Gradle properties
- `README.md` - Project documentation
- `.gitignore` - Git ignore configuration
- `download_all_raw_cards.py` - Active card downloader script

## Current Status

- **Mod Version**: 4.8
- **Minecraft Version**: 1.16.5
- **Forge Version**: 36.2.39
- **Total Card Sets**: 13
- **Active Sets Being Downloaded**: 8 main sets

## Cleanup Summary

### Removed
- Python cache directories (__pycache__)
- Virtual environment (venv)
- Old backup directories (cards_backup, raw)
- Temporary files and logs
- .DS_Store files
- Compiled .class files from build
- Duplicate/obsolete scripts

### Organized
- Moved utility scripts to /tools/
- Archived old scripts to /archive/
- Cleaned up raw_images structure
- Updated .gitignore for better coverage
- Created proper documentation

### Preserved
- All source code
- Card metadata and textures
- Raw card images (downloading)
- Build configuration
- Essential tools and scripts