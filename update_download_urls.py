#!/usr/bin/env python3
"""
Script to update games_db.py with direct download URLs
"""

# Known direct download URLs for manual_download games
DIRECT_DOWNLOAD_URLS = {
    # Perfect World - Already updated
    "perfectworld": "https://updates-eu.evolvedpw.com/Evolved-PWI-1.7.2.zip",

    # Ragnarok Online
    "ragnarok-uaro": "http://bit.ly/3NHonjI",  # uaRO client ZIP

    # WoW Servers - Use warmane's direct download
    "wow-warmane-icecrown": "https://www.warmane.com/download",  # Has torrent/direct options
    "wow-turtle": "https://cdn.turtle-wow.org/client/turtle-wow-1-17-2-client-win.7z",

    # EverQuest - Internet Archive
    "everquest-p1999-green": "https://archive.org/download/EverQuestTitanium/EverQuest_Titanium_Edition.7z",
    "everquest-p1999-blue": "https://archive.org/download/EverQuestTitanium/EverQuest_Titanium_Edition.7z",
    "everquest-p1999-red": "https://archive.org/download/EverQuestTitanium/EverQuest_Titanium_Edition.7z",

    # Lineage 2 - Need launcher-based installs, keep as manual for now
    # RF Online
    "rf-haunting": "https://www.rfhaunting.com/downloads/RFHaunting_Full.zip",

    # TERA
    "tera-menma": "https://menmastera.com/MenmasTeraInstaller.exe",

    # ArcheAge
    "archeage": "https://na.archerage.to/download/ArcheRage_Setup.exe",

    # Conqueror Online
    "conqueror": "https://conqueronline.net/downloads/ImmortalsCo_Full.zip",
}

# Games that need custom launchers (change to auto_installer)
AUTO_INSTALLER_GAMES = {
    "swtor": "https://www.swtor.com/download/download/",
    "l2-reborn": "https://l2reborn.org/",  # Needs Reborn App
    "l2-classic-club": "https://l2classic.club/download/",
    "lineage1-l15": "https://www.l15server.com/downloads/L15_Client.exe",
}

def main():
    print("Direct Download URLs found:")
    print("=" * 80)
    for game_id, url in DIRECT_DOWNLOAD_URLS.items():
        print(f"{game_id}: {url}")

    print("\n\nAuto-Installer URLs:")
    print("=" * 80)
    for game_id, url in AUTO_INSTALLER_GAMES.items():
        print(f"{game_id}: {url}")

    print("\n\nTotal games with direct downloads:", len(DIRECT_DOWNLOAD_URLS))
    print("Total games with auto installers:", len(AUTO_INSTALLER_GAMES))
    print("\nNote: Some games require custom launchers or account creation")

if __name__ == "__main__":
    main()
