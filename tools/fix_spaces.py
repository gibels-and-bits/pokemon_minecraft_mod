#!/usr/bin/env python3
import os

def fix_spaces_in_filename(filepath):
    """Replace spaces with underscores in filename"""
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    if ' ' in filename:
        new_filename = filename.replace(' ', '_')
        new_filepath = os.path.join(directory, new_filename)
        os.rename(filepath, new_filepath)
        print(f"Renamed: {filename} -> {new_filename}")
        return True
    return False

def main():
    base_path = 'src/main/resources/assets/etbmod/textures/cards'
    fixed_count = 0
    
    # Find all PNG files with spaces
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.png') and ' ' in file:
                full_path = os.path.join(root, file)
                if fix_spaces_in_filename(full_path):
                    fixed_count += 1
    
    print(f"\nFixed {fixed_count} files with spaces")

if __name__ == '__main__':
    main()