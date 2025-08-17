# Booster Pack Pipeline Documentation

## Overview
The booster pack pipeline automates the process of converting booster pack artwork into game-ready textures for the Pokemon ETB Minecraft mod.

## Scripts

### 1. `booster_pack_pipeline.py`
Main pipeline script for processing individual booster packs.

#### Usage
```bash
python booster_pack_pipeline.py <set_name> <input_image_path>
```

#### Examples
```bash
# Process a new set called "Stellar Crown"
python booster_pack_pipeline.py stellar_crown raw_images/stellar_crown.png

# Process with WebP image
python booster_pack_pipeline.py temporal_forces raw_images/temporal_forces_booster.webp
```

#### What it does:
1. **Loads the input image** (supports PNG, JPG, WEBP)
2. **Removes white borders** automatically
3. **Creates booster pack texture** (128x128 pixels)
4. **Creates ETB block texture** (64x64 pixels)
5. **Saves textures** to the correct mod directories
6. **Provides integration instructions** for adding to the mod

### 2. `booster_pack_pipeline_batch.py`
Batch processing script for multiple booster packs.

#### Usage
```bash
python booster_pack_pipeline_batch.py <input_directory>
```

#### Example
```bash
# Process all images in the raw_images/booster_packs directory
python booster_pack_pipeline_batch.py raw_images/booster_packs/
```

## Step-by-Step Guide for Adding a New Set

### Step 1: Prepare Your Image
- Get a high-quality image of the booster pack
- Any format: PNG, JPG, or WEBP
- Don't worry about size or white borders - the script handles this

### Step 2: Run the Pipeline
```bash
python booster_pack_pipeline.py my_new_set path/to/booster_image.png
```

### Step 3: Follow Integration Instructions
The script will output specific instructions for integrating the new set:

1. **Add to ModBlocks.java** - Register the ETB block
2. **Add to ModItems.java** - Register the booster pack item
3. **Create card metadata** - Add cards_metadata.json
4. **Add card images** - Add individual card textures
5. **Update language file** - Add display names

### Step 4: Add Card Images (if new set)
Create directory: `src/main/resources/assets/etbmod/textures/cards/my_new_set/`

Add card images with normalized names:
- Format: `{number}_{rarity}_{name}.png`
- Example: `001_common_pikachu.png`
- All lowercase, no apostrophes, underscores for spaces

### Step 5: Create Card Metadata
Create `cards_metadata.json` in the cards directory:
```json
{
  "cards": [
    {
      "id": "my_new_set-001",
      "name": "Pikachu",
      "number": "001",
      "rarity": "common"
    }
    // ... more cards
  ]
}
```

### Step 6: Rebuild the Mod
```bash
./gradlew clean build
```

## Texture Specifications

### Booster Pack Texture (Item)
- **Size**: 128x128 pixels
- **Format**: PNG with transparency
- **Location**: `src/main/resources/assets/etbmod/textures/item/`
- **Naming**: `etb_{set_name}_booster.png`

### ETB Block Texture
- **Size**: 64x64 pixels (texture atlas)
- **Format**: PNG with transparency
- **Location**: `src/main/resources/assets/etbmod/textures/block/`
- **Naming**: `etb_{set_name}.png`

## Tips

1. **Set Names**: Use lowercase with underscores (e.g., `stellar_crown`, `temporal_forces`)

2. **White Border Removal**: The script automatically detects and removes white borders with a threshold of 240 (out of 255)

3. **Aspect Ratio**: The script maintains the original aspect ratio while fitting the image into the required dimensions

4. **Batch Processing**: Use the batch script when adding multiple sets at once

5. **Testing**: After rebuilding, test in-game by:
   - Checking the creative menu for the new ETB
   - Placing the ETB block
   - Using scissors to open it
   - Opening booster packs on the game table

## Troubleshooting

### Image not loading in game
- Check file names are all lowercase
- Verify textures are in correct directories
- Ensure mod was rebuilt after adding textures

### Texture appears too small/large
- Adjust the `max_size` parameter in the script (default 120)
- Check if white border removal is too aggressive

### Script fails to run
- Install required dependencies: `pip install Pillow numpy`
- Ensure Python 3.6+ is installed

## Example Full Workflow

```bash
# 1. Download booster pack image
curl -o stellar_crown.webp "https://example.com/stellar_crown_booster.webp"

# 2. Run the pipeline
python booster_pack_pipeline.py stellar_crown stellar_crown.webp

# 3. Add card images (manual step)
# Copy card images to src/main/resources/assets/etbmod/textures/cards/stellar_crown/

# 4. Create metadata file
# Create cards_metadata.json in the cards/stellar_crown directory

# 5. Update the mod code (follow printed instructions)
# Edit ModBlocks.java and ModItems.java

# 6. Rebuild
./gradlew clean build

# 7. Test in game
# Copy etbmod-X.X.jar to Minecraft mods folder
```

## Notes
- The pipeline preserves transparency in images
- Images are automatically centered and padded
- The script creates backup copies when replacing existing textures
- All textures use power-of-2 dimensions for Minecraft compatibility