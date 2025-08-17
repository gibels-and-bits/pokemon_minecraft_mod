#!/usr/bin/env python3
"""Analyze all available Pokemon TCG sets"""

import requests
import json
from collections import Counter

# Fetch all sets
response = requests.get("https://api.pokemontcg.io/v2/sets", timeout=60)
data = response.json()
sets = data['data']

print(f"Total sets available: {len(sets)}")
print(f"=" * 60)

# Calculate totals
total_cards = sum(s.get('total', 0) for s in sets)
print(f"Total cards across all sets: {total_cards:,}")
print(f"Average cards per set: {total_cards//len(sets)}")
print()

# Series breakdown
series_count = Counter([s['series'] for s in sets])
print("Cards by series:")
for series, count in sorted(series_count.items()):
    series_cards = sum(s.get('total', 0) for s in sets if s['series'] == series)
    print(f"  {series}: {count} sets, {series_cards:,} cards")
print()

# Largest sets
largest = sorted(sets, key=lambda x: x.get('total', 0), reverse=True)[:10]
print("10 Largest sets:")
for s in largest:
    print(f"  {s['id']}: {s['name']} - {s.get('total', 0)} cards")
print()

# Recent sets (2024-2025)
print("Recent sets (2024-2025):")
recent = [s for s in sets if s.get('releaseDate', '').startswith(('2024', '2025'))]
for s in sorted(recent, key=lambda x: x.get('releaseDate', '')):
    print(f"  {s['id']}: {s['name']} ({s.get('releaseDate', 'N/A')}) - {s.get('total', 0)} cards")
print()

# Save all set IDs to file
with open('all_set_ids.json', 'w') as f:
    set_info = [{'id': s['id'], 'name': s['name'], 'series': s['series'], 'total': s.get('total', 0)} for s in sets]
    json.dump(set_info, f, indent=2)
print(f"Saved {len(sets)} set IDs to all_set_ids.json")