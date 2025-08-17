# Pokemon ETB Mod for Minecraft

A Minecraft Forge mod (1.16.5) that brings the Pokemon Trading Card Game experience to Minecraft! Open Elite Trainer Boxes, collect booster packs, and build your card collection.

## Features

### Elite Trainer Boxes (ETBs)
- **27 different ETB sets** available as placeable 3D blocks
- Rotatable blocks with realistic box art textures
- Open ETBs with scissors to receive 9 booster packs
- Instant-break blocks that drop when punched

### Booster Packs & Cards
- Each pack contains 10 cards with realistic TCG pull rates
- 8 rarity tiers with color-coded names
- Right-click cards to view full artwork
- Cards display detailed tooltips with set info and rarity

### Gamer Table
- Special crafting station for bulk pack opening
- Interactive GUI for managing your collection
- Automatically distributes cards to inventory

## Project Structure

```
etb-mod/
├── src/                      # Java source and resources
│   ├── main/java/           # Mod code
│   └── main/resources/      # Assets and textures
├── scripts/                 # Organized Python utilities
│   ├── etb_mod_manager.py  # Main management script
│   ├── download/           # Card download utilities
│   ├── image_processing/   # Image optimization tools
│   ├── generation/         # Texture generation scripts
│   └── validation/         # Resource validation tools
├── raw_images/             # Source images (not in git)
└── build.gradle           # Build configuration
```

## Quick Start

### Building the Mod

```bash
./gradlew build
```

The JAR file will be generated in `build/libs/`

### Managing Resources

Use the unified management script for all operations:

```bash
# Download card images for the mod's sets
python scripts/etb_mod_manager.py download

# Process and optimize card images
python scripts/etb_mod_manager.py process-images

# Generate ETB block textures
python scripts/etb_mod_manager.py generate-etb

# Validate all resources
python scripts/etb_mod_manager.py validate

# Build the mod
python scripts/etb_mod_manager.py build

# Clean build artifacts
python scripts/etb_mod_manager.py clean
```

## Development

### Requirements
- Java 8
- Minecraft Forge 1.16.5-36.2.39
- Python 3.8+ (for resource management scripts)
- Gradle 6.9+

### Code Organization

#### Java Code
- **ETBBlock**: Base class for all ETB blocks with rotation and interaction logic
- **ETBBlockFactory**: Factory pattern for creating ETB blocks efficiently
- **ModBlocks**: Registry for all blocks using optimized registration
- **ETBConfig**: Centralized configuration constants
- **GamerTable**: Special block for pack opening interface

#### Python Scripts
- **download_manager.py**: Unified card download system with retry logic
- **image_processor.py**: Consolidated image processing pipeline
- **etb_mod_manager.py**: Main entry point for all mod operations

### Adding New Sets

1. Add the set ID to `ETBBlockFactory.java`
2. Register in `scripts/etb_mod_manager.py` get_mod_sets()
3. Add textures to `src/main/resources/assets/etbmod/textures/`
4. Run validation: `python scripts/etb_mod_manager.py validate`

## Available Sets

### Modern Sets
- 151, Surging Sparks, Prismatic Evolutions, Journey Together

### Sword & Shield Era
- Brilliant Stars, Cosmic Eclipse, Crown Zenith, Evolving Skies
- Hidden Fates, Rebel Clash, Shining Fates, Shrouded Fable
- Team Up, Unified Minds, Vivid Voltage

### Sun & Moon Era
- Burning Shadows, Breakpoint, Phantom Forces

### Classic Sets
- Black Bolt, White Flare, Evolutions, Primal Clash
- Celebrations, Destined Rivals, Generations
- Groudon Collection, Kyogre Collection

## Performance Optimizations

- **Factory Pattern**: Reduced memory footprint by eliminating 27 individual block classes
- **Texture Caching**: Implements TTL-based texture cache for better performance
- **Optimized Pull Rates**: Pre-calculated probability distributions
- **Batch Processing**: Efficient bulk operations for pack opening

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation: `python scripts/etb_mod_manager.py validate`
5. Submit a pull request

## License

See LICENSE.txt for details.

## Credits

- Card images sourced from Pokemon TCG API
- Minecraft Forge MDK
- Pokemon and Pokemon TCG are trademarks of Nintendo/Creatures Inc./GAME FREAK inc.