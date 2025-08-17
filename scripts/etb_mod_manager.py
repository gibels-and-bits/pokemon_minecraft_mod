#!/usr/bin/env python3
"""
ETB Mod Manager - Main entry point for mod maintenance operations
"""

import argparse
import sys
from pathlib import Path

# Add script directories to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'download'))
sys.path.insert(0, str(Path(__file__).parent / 'image_processing'))
sys.path.insert(0, str(Path(__file__).parent / 'generation'))
sys.path.insert(0, str(Path(__file__).parent / 'validation'))

from download.download_manager import CardDownloadManager
from image_processing.image_processor import ImageProcessor, ETBTextureGenerator


class ETBModManager:
    """Main manager class for ETB mod operations."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.raw_images = self.project_root / 'raw_images'
        self.resources = self.project_root / 'src' / 'main' / 'resources'
        
    def download_cards(self, sets=None, all_sets=False):
        """Download card images for specified sets."""
        manager = CardDownloadManager(
            output_dir=str(self.raw_images / 'cards')
        )
        
        if all_sets:
            print("Downloading all available sets...")
            manager.download_all_sets()
        elif sets:
            print(f"Downloading sets: {', '.join(sets)}")
            manager.download_multiple_sets(sets)
        else:
            # Download mod's default sets
            mod_sets = self.get_mod_sets()
            print(f"Downloading mod sets: {', '.join(mod_sets)}")
            manager.download_multiple_sets(mod_sets)
    
    def process_images(self, input_dir=None, output_dir=None):
        """Process card images (remove borders, optimize)."""
        processor = ImageProcessor()
        
        if not input_dir:
            input_dir = self.raw_images / 'cards'
        if not output_dir:
            output_dir = self.resources / 'assets' / 'etbmod' / 'textures' / 'cards'
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Process each set directory
        for set_dir in input_path.iterdir():
            if set_dir.is_dir():
                print(f"Processing set: {set_dir.name}")
                set_output = output_path / set_dir.name
                processor.batch_process_cards(set_dir, set_output)
    
    def generate_etb_textures(self):
        """Generate ETB block textures from source images."""
        processor = ImageProcessor()
        etb_gen = ETBTextureGenerator(processor)
        
        etb_source = self.raw_images / 'etb_boxes'
        etb_output = self.resources / 'assets' / 'etbmod' / 'textures' / 'blocks'
        
        if not etb_source.exists():
            print(f"ETB source directory not found: {etb_source}")
            return
        
        for etb_image in etb_source.glob("*.png"):
            set_id = etb_image.stem
            print(f"Generating ETB textures for: {set_id}")
            etb_gen.generate_etb_textures(set_id, etb_image, etb_output)
    
    def validate_resources(self):
        """Validate that all required resources are present."""
        missing = []
        
        # Check for card textures
        cards_dir = self.resources / 'assets' / 'etbmod' / 'textures' / 'cards'
        for set_id in self.get_mod_sets():
            set_dir = cards_dir / set_id
            if not set_dir.exists():
                missing.append(f"Card textures for {set_id}")
        
        # Check for ETB textures
        blocks_dir = self.resources / 'assets' / 'etbmod' / 'textures' / 'blocks'
        for set_id in self.get_mod_sets():
            etb_texture = blocks_dir / f"etb_{set_id}_front.png"
            if not etb_texture.exists():
                missing.append(f"ETB texture for {set_id}")
        
        if missing:
            print("Missing resources:")
            for item in missing:
                print(f"  - {item}")
        else:
            print("All resources validated successfully!")
    
    def get_mod_sets(self):
        """Get list of sets used in the mod."""
        return [
            'black_bolt', 'breakpoint', 'brilliant_stars', 'burning_shadows',
            'cosmic_eclipse', 'crown_zenith', 'evolutions', 'evolving_skies',
            'hidden_fates', 'phantom_forces', 'primal_clash', 'prismatic_evolutions',
            'rebel_clash', 'shining_fates', 'shrouded_fable', 'surging_sparks',
            'team_up', 'unified_minds', 'vivid_voltage', 'white_flare',
            '151', 'celebrations', 'destined_rivals', 'generations',
            'groudon', 'journey_together', 'kyogre'
        ]
    
    def build_mod(self):
        """Build the mod JAR file."""
        import subprocess
        
        print("Building mod...")
        result = subprocess.run(
            ['./gradlew', 'build'],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Build successful!")
            jar_path = self.project_root / 'build' / 'libs'
            print(f"JAR file location: {jar_path}")
        else:
            print("Build failed!")
            print(result.stderr)
    
    def clean(self):
        """Clean build artifacts and temporary files."""
        import shutil
        
        # Clean build directory
        build_dir = self.project_root / 'build'
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print("Cleaned build directory")
        
        # Clean gradle cache
        gradle_dir = self.project_root / '.gradle'
        if gradle_dir.exists():
            shutil.rmtree(gradle_dir)
            print("Cleaned gradle cache")
        
        # Clean log files
        for log_file in self.project_root.glob("*.log"):
            log_file.unlink()
            print(f"Removed {log_file.name}")
        
        print("Clean complete!")


def main():
    parser = argparse.ArgumentParser(
        description="ETB Mod Manager - Manage Pokemon ETB Minecraft Mod",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s download --sets brilliant_stars evolving_skies
  %(prog)s process-images
  %(prog)s generate-etb
  %(prog)s validate
  %(prog)s build
  %(prog)s clean
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download card images')
    download_parser.add_argument('--sets', nargs='+', help='Specific sets to download')
    download_parser.add_argument('--all', action='store_true', help='Download all sets')
    
    # Process images command
    process_parser = subparsers.add_parser('process-images', help='Process card images')
    process_parser.add_argument('--input', help='Input directory')
    process_parser.add_argument('--output', help='Output directory')
    
    # Generate ETB textures command
    subparsers.add_parser('generate-etb', help='Generate ETB block textures')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate mod resources')
    
    # Build command
    subparsers.add_parser('build', help='Build the mod JAR')
    
    # Clean command
    subparsers.add_parser('clean', help='Clean build artifacts')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = ETBModManager()
    
    if args.command == 'download':
        manager.download_cards(args.sets, args.all)
    elif args.command == 'process-images':
        manager.process_images(args.input, args.output)
    elif args.command == 'generate-etb':
        manager.generate_etb_textures()
    elif args.command == 'validate':
        manager.validate_resources()
    elif args.command == 'build':
        manager.build_mod()
    elif args.command == 'clean':
        manager.clean()


if __name__ == "__main__":
    main()