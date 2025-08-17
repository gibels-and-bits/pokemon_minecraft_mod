#!/usr/bin/env python3
"""
Find alternative sources for Pokemon TCG card data
"""

import requests
import json
from pathlib import Path

def check_sources():
    """Check various alternative sources for Pokemon TCG data"""
    
    sources = []
    
    # 1. Check GitHub for Pokemon TCG datasets
    print("Checking GitHub for Pokemon TCG datasets...")
    github_repos = [
        "PokemonTCG/pokemon-tcg-data",
        "ratnim/SelfbuildPokemonTCG",
        "jbonnett92/PokemonTCG",
    ]
    
    for repo in github_repos:
        try:
            url = f"https://api.github.com/repos/{repo}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  ✓ Found: {repo}")
                print(f"    Description: {data.get('description', 'N/A')[:60]}")
                sources.append(('github', repo, data.get('html_url')))
        except:
            pass
    
    # 2. Check Scryfall (MTG site that sometimes has Pokemon data)
    print("\nChecking card database sites...")
    
    # 3. Check TCGPlayer
    try:
        resp = requests.get("https://api.tcgplayer.com/v1.39.0/catalog/categories", timeout=5)
        if resp.status_code == 200:
            print("  ✓ TCGPlayer API accessible (requires key)")
    except:
        pass
    
    # 4. Check for Pokemon TCG SDK alternatives
    print("\nChecking Pokemon TCG SDKs and mirrors...")
    
    sdk_urls = [
        "https://github.com/PokemonTCG/pokemon-tcg-sdk-python",
        "https://github.com/PokemonTCG/pokemon-tcg-sdk-javascript",
    ]
    
    for url in sdk_urls:
        try:
            repo_name = url.split('/')[-2] + '/' + url.split('/')[-1]
            api_url = f"https://api.github.com/repos/{repo_name}"
            resp = requests.get(api_url, timeout=5)
            if resp.status_code == 200:
                print(f"  ✓ SDK found: {url}")
                sources.append(('sdk', repo_name, url))
        except:
            pass
    
    return sources

def check_pokemontcg_github():
    """Check the official PokemonTCG GitHub for data files"""
    print("\nChecking PokemonTCG official GitHub...")
    
    # Look for JSON data files
    base_url = "https://raw.githubusercontent.com/PokemonTCG/pokemon-tcg-data/master"
    
    sets_to_check = [
        "sets/en.json",
        "cards/en/sv8.json",  # Surging Sparks
        "cards/en/sm3.json",  # Burning Shadows
        "cards/en/sm9.json",  # Team Up
    ]
    
    found = []
    for file_path in sets_to_check:
        try:
            url = f"{base_url}/{file_path}"
            resp = requests.head(url, timeout=5)
            if resp.status_code == 200:
                print(f"  ✓ Found: {file_path}")
                found.append(url)
        except:
            pass
    
    return found

def search_bulbapedia():
    """Check if Bulbapedia has card lists"""
    print("\nChecking Bulbapedia for card lists...")
    
    sets_to_check = {
        'Surging Sparks': 'Surging_Sparks_(TCG)',
        'Burning Shadows': 'Burning_Shadows_(TCG)',
        'Team Up': 'Team_Up_(TCG)',
    }
    
    for set_name, page in sets_to_check.items():
        try:
            url = f"https://bulbapedia.bulbagarden.net/wiki/{page}"
            resp = requests.head(url, timeout=5)
            if resp.status_code == 200:
                print(f"  ✓ {set_name}: {url}")
        except:
            pass

def main():
    print("Searching for alternative Pokemon TCG data sources...")
    print("=" * 60)
    
    # Check various sources
    sources = check_sources()
    github_data = check_pokemontcg_github()
    search_bulbapedia()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Found {len(sources)} alternative sources")
    print(f"Found {len(github_data)} data files on GitHub")
    
    print("\nRecommendations:")
    print("1. PokemonTCG GitHub organization may have card data")
    print("2. Bulbapedia has card lists with images")
    print("3. TCGPlayer has an API but requires authentication")
    print("4. Could scrape from Pokemon TCG Online Database when available")

if __name__ == "__main__":
    main()
