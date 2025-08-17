#!/usr/bin/env python3
"""
ETB Mod Agent Orchestrator
Coordinates the entire ETB mod generation pipeline
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
import argparse

class ETBModOrchestrator:
    def __init__(self, skip_scrape=False, skip_build=False, test_mode=False):
        self.project_root = Path.cwd()
        self.tools_dir = self.project_root / "tools"
        self.skip_scrape = skip_scrape
        self.skip_build = skip_build
        self.test_mode = test_mode
        
        # Check Python dependencies
        self.required_packages = [
            'playwright',
            'aiohttp',
            'pillow',
            'numpy'
        ]
        
        self.steps = [
            ("Check dependencies", self.check_dependencies),
            ("Scrape ETB images", self.scrape_images),
            ("Rectify images", self.rectify_images),
            ("Generate assets", self.generate_assets),
            ("Build mod", self.build_mod),
            ("Verify build", self.verify_build)
        ]

    def run_command(self, command, cwd=None):
        """Run a shell command and return success status"""
        if cwd is None:
            cwd = self.project_root
        
        print(f"  Running: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout:
                print(f"  Output: {result.stdout[:200]}")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"  Error: {e}")
            if e.stderr:
                print(f"  Stderr: {e.stderr}")
            return False

    def check_dependencies(self):
        """Check and install required Python packages"""
        print("Checking Python dependencies...")
        
        missing_packages = []
        for package in self.required_packages:
            try:
                __import__(package)
                print(f"  ✓ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                print(f"  ✗ {package} is missing")
        
        if missing_packages:
            print("\nInstalling missing packages...")
            for package in missing_packages:
                if package == 'pillow':
                    package = 'Pillow'  # Correct package name for pip
                
                if not self.run_command([sys.executable, "-m", "pip", "install", package]):
                    print(f"Failed to install {package}")
                    return False
            
            # Special setup for playwright
            if 'playwright' in missing_packages:
                print("Installing Playwright browsers...")
                if not self.run_command([sys.executable, "-m", "playwright", "install", "chromium"]):
                    print("Failed to install Playwright browsers")
                    return False
        
        return True

    def scrape_images(self):
        """Run the TCGplayer scraper"""
        if self.skip_scrape:
            print("Skipping image scraping (--skip-scrape flag)")
            return True
        
        if self.test_mode:
            print("Skipping scraping in test mode")
            return True
        
        print("Scraping ETB images from TCGplayer...")
        
        scraper_script = self.tools_dir / "scrape_tcgplayer.py"
        if not scraper_script.exists():
            print(f"Scraper script not found: {scraper_script}")
            return False
        
        return self.run_command([sys.executable, str(scraper_script)])

    def rectify_images(self):
        """Run the image rectification script"""
        print("Rectifying images and creating textures...")
        
        rectify_script = self.tools_dir / "etb_rectify_batch.py"
        if not rectify_script.exists():
            print(f"Rectification script not found: {rectify_script}")
            return False
        
        if self.test_mode:
            # Generate test textures instead
            print("Generating test textures...")
            return self.run_command([sys.executable, str(rectify_script), "--test"])
        else:
            return self.run_command([sys.executable, str(rectify_script)])

    def generate_assets(self):
        """Run the asset generation script"""
        print("Generating mod assets and registry...")
        
        generator_script = self.tools_dir / "generate_assets_and_registry.py"
        if not generator_script.exists():
            print(f"Generator script not found: {generator_script}")
            return False
        
        return self.run_command([sys.executable, str(generator_script)])

    def build_mod(self):
        """Build the mod using Gradle"""
        if self.skip_build:
            print("Skipping mod build (--skip-build flag)")
            return True
        
        print("Building mod with Gradle...")
        
        # Check for gradlew
        gradlew = self.project_root / ("gradlew.bat" if os.name == 'nt' else "gradlew")
        if not gradlew.exists():
            print(f"Gradle wrapper not found: {gradlew}")
            print("Please ensure you're in the correct directory with the Forge MDK")
            return False
        
        # Make gradlew executable on Unix systems
        if os.name != 'nt':
            os.chmod(gradlew, 0o755)
        
        # Clean and build
        print("Cleaning previous build...")
        if not self.run_command([str(gradlew), "clean"]):
            print("Clean failed, continuing anyway...")
        
        print("Building mod...")
        return self.run_command([str(gradlew), "build"])

    def verify_build(self):
        """Verify the mod JAR was created"""
        print("Verifying build output...")
        
        build_dir = self.project_root / "build" / "libs"
        if not build_dir.exists():
            print(f"Build directory not found: {build_dir}")
            return False
        
        jar_files = list(build_dir.glob("*.jar"))
        if not jar_files:
            print("No JAR files found in build/libs/")
            return False
        
        for jar_file in jar_files:
            size_mb = jar_file.stat().st_size / (1024 * 1024)
            print(f"  ✓ Found: {jar_file.name} ({size_mb:.2f} MB)")
        
        print(f"\nMod JAR location: {jar_files[0].absolute()}")
        return True

    def run(self):
        """Run the complete orchestration pipeline"""
        print("=" * 60)
        print("ETB MOD ORCHESTRATOR")
        print("=" * 60)
        print(f"Project root: {self.project_root}")
        print(f"Test mode: {self.test_mode}")
        print()
        
        start_time = time.time()
        failed_step = None
        
        for step_name, step_func in self.steps:
            print(f"\n{'=' * 40}")
            print(f"Step: {step_name}")
            print(f"{'=' * 40}")
            
            if not step_func():
                print(f"\n✗ Step failed: {step_name}")
                failed_step = step_name
                break
            
            print(f"✓ {step_name} completed")
        
        elapsed = time.time() - start_time
        
        print(f"\n{'=' * 60}")
        if failed_step:
            print(f"ORCHESTRATION FAILED")
            print(f"Failed at step: {failed_step}")
        else:
            print(f"ORCHESTRATION COMPLETE")
            print(f"All steps completed successfully!")
            print(f"\nNext steps:")
            print(f"1. Test locally: ./gradlew runClient")
            print(f"2. Find JAR in: build/libs/")
            print(f"3. Upload to private cloud storage")
            print(f"4. Install via CurseForge app")
        
        print(f"\nTotal time: {elapsed:.1f} seconds")
        print(f"{'=' * 60}")
        
        return failed_step is None

def main():
    parser = argparse.ArgumentParser(description='Orchestrate ETB mod generation')
    parser.add_argument('--skip-scrape', action='store_true',
                       help='Skip image scraping (use existing images)')
    parser.add_argument('--skip-build', action='store_true',
                       help='Skip Gradle build')
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode (generate test textures)')
    
    args = parser.parse_args()
    
    orchestrator = ETBModOrchestrator(
        skip_scrape=args.skip_scrape,
        skip_build=args.skip_build,
        test_mode=args.test
    )
    
    success = orchestrator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()