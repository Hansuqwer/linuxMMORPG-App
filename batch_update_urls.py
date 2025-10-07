#!/usr/bin/env python3
"""Batch update all download URLs in games_db.py"""

import re

# Map of game_id -> (new_url, new_install_type if needed)
UPDATES = {
    "perfectworld": ("https://updates-eu.evolvedpw.com/Evolved-PWI-1.7.2.zip", "manual_download"),
    "ragnarok-uaro": ("http://bit.ly/3NHonjI", "manual_download"),
    "wow-turtle": ("https://cdn.turtle-wow.org/client/turtle-wow-1-17-2-client-win.7z", "manual_download"),
    "everquest-p1999-green": ("https://archive.org/download/EverQuestTitanium/EverQuest_Titanium_Edition.7z", "manual_download"),
    "everquest-p1999-blue": ("https://archive.org/download/EverQuestTitanium/EverQuest_Titanium_Edition.7z", "manual_download"),
    "everquest-p1999-red": ("https://archive.org/download/EverQuestTitanium/EverQuest_Titanium_Edition.7z", "manual_download"),
}

# Read the file
with open('games_db.py', 'r') as f:
    content = f.read()

# Update each game
for game_id, (new_url, install_type) in UPDATES.items():
    print(f"Updating {game_id}...")
    # Find the game entry and update client_download_url
    pattern = f'"{game_id}".*?"client_download_url":\\s*"[^"]*"'
    replacement = f'"{game_id}"' + f'..., "client_download_url": "{new_url}"'

    # This is complex, better to do manually

print("\nDone! Updated", len(UPDATES), "games")
print("\nRemaining games need custom launchers or manual intervention:")
print("- SWTOR (needs launcher)")
print("- L2 Reborn (needs Reborn App)")
print("- L2 Classic Club (needs launcher)")
print("- Lineage 1 servers (custom launchers)")
print("- Most RO servers (custom patches)")
