#!/usr/bin/env python3
"""
Validate the ETB mod JAR file for common issues
"""

import zipfile
import json
import sys
from pathlib import Path

def validate_mod(jar_path):
    """Validate mod structure and contents"""
    print(f"Validating: {jar_path}")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    with zipfile.ZipFile(jar_path, 'r') as jar:
        files = jar.namelist()
        
        # 1. Check for mods.toml
        if 'META-INF/mods.toml' not in files:
            issues.append("❌ Missing META-INF/mods.toml")
        else:
            print("✓ Found mods.toml")
            # Check mods.toml content
            with jar.open('META-INF/mods.toml') as f:
                content = f.read().decode('utf-8')
                if 'examplemod' in content.lower():
                    issues.append("❌ mods.toml contains 'examplemod' reference")
                if 'etbmod' not in content:
                    issues.append("❌ mods.toml missing 'etbmod' mod ID")
                else:
                    print("✓ mods.toml has correct mod ID")
        
        # 2. Check for main mod class
        etb_class_found = False
        example_class_found = False
        
        for file in files:
            if 'ETBMod.class' in file:
                etb_class_found = True
            if 'ExampleMod.class' in file:
                example_class_found = True
                issues.append(f"❌ Found ExampleMod class: {file}")
        
        if etb_class_found:
            print("✓ Found ETBMod main class")
        else:
            issues.append("❌ Missing ETBMod main class")
        
        # 3. Check for block classes
        block_classes = [f for f in files if 'ETBBlock.class' in f or 'ModBlocks.class' in f]
        if block_classes:
            print(f"✓ Found {len(block_classes)} block-related classes")
        else:
            warnings.append("⚠ No block classes found")
        
        # 4. Check for assets
        blockstates = [f for f in files if f.startswith('assets/etbmod/blockstates/')]
        models = [f for f in files if f.startswith('assets/etbmod/models/')]
        textures = [f for f in files if f.startswith('assets/etbmod/textures/')]
        lang = [f for f in files if f.startswith('assets/etbmod/lang/')]
        
        print(f"✓ Found {len(blockstates)} blockstate files")
        print(f"✓ Found {len(models)} model files")
        print(f"✓ Found {len(textures)} texture files")
        print(f"✓ Found {len(lang)} language files")
        
        if len(blockstates) == 0:
            warnings.append("⚠ No blockstate files found")
        if len(textures) == 0:
            warnings.append("⚠ No texture files found")
        
        # 5. Check for loot tables
        loot_tables = [f for f in files if f.startswith('data/etbmod/loot_tables/')]
        if loot_tables:
            print(f"✓ Found {len(loot_tables)} loot table files")
        else:
            warnings.append("⚠ No loot tables found")
        
        # 6. List ETB variants found
        etb_variants = set()
        for f in blockstates:
            if 'etb_' in f and f.endswith('.json'):
                variant = f.split('/')[-1].replace('.json', '')
                etb_variants.add(variant)
        
        if etb_variants:
            print(f"\n✓ Found {len(etb_variants)} ETB variants:")
            for variant in sorted(etb_variants):
                print(f"  - {variant}")
        
        # 7. Check for problematic nested structures
        nested_src = [f for f in files if 'src/main/' in f or 'gradle/' in f]
        if nested_src:
            issues.append(f"❌ Found nested source files: {len(nested_src)} files")
    
    # Summary
    print("\n" + "=" * 50)
    if issues:
        print("❌ VALIDATION FAILED")
        print("\nIssues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ VALIDATION PASSED")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  {warning}")
    
    print("\n" + "=" * 50)
    
    if not issues:
        print("✅ This mod should load correctly in Minecraft 1.16.5 with Forge!")
    else:
        print("❌ Fix the issues above before loading in Minecraft")
    
    return len(issues) == 0

if __name__ == "__main__":
    jar_path = Path("build/libs/etbmod-1.4.jar")
    if not jar_path.exists():
        print(f"Error: JAR file not found at {jar_path}")
        sys.exit(1)
    
    success = validate_mod(jar_path)
    sys.exit(0 if success else 1)