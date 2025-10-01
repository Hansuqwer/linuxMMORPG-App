"""
Game database registry for MMORPGs
Contains metadata, installation instructions, and server information
"""

GAMES_DATABASE = {
    # === Classic Western MMORPGs ===
    "wow-warmane-icecrown": {
        "name": "World of Warcraft - Warmane Icecrown",
        "genre": "Fantasy MMORPG",
        "server": "Warmane Icecrown (7x WotLK)",
        "population": "Very High (5,000-10,000+ concurrent)",
        "description": "7x WotLK server, PvP-focused with massive population",
        "website": "https://warmane.com",
        "client_download_url": "https://warmane.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "Wow.exe",
        "install_notes": "Download WoW 3.3.5a client from warmane.com. Script sets realmlist to logon.warmane.com.",
        "native": False,
        "tested": True
    },

    "wow-turtle": {
        "name": "World of Warcraft - Turtle WoW",
        "genre": "Fantasy MMORPG",
        "server": "Turtle WoW (Vanilla+)",
        "population": "High (1,000-3,000 concurrent)",
        "description": "Vanilla+ with custom content and dedicated community",
        "website": "https://turtle-wow.org",
        "client_download_url": "https://turtle-wow.org/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "WoW.exe",
        "install_notes": "Download Turtle WoW client. Includes custom content patches. Linux guide on official site.",
        "native": False,
        "tested": True
    },

    "warhammer-ror": {
        "name": "Warhammer Online - Return of Reckoning",
        "genre": "RvR MMORPG",
        "server": "Return of Reckoning",
        "population": "High (400-3,500 concurrent)",
        "description": "Only active WAR server. Massive realm vs realm battles.",
        "website": "https://returnofreckoning.com",
        "client_download_url": "https://returnofreckoning.com/downloads",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "WAR.exe",
        "install_notes": "Client auto-downloads during setup. Official Linux guide available.",
        "native": False,
        "tested": True
    },

    "everquest-p1999": {
        "name": "EverQuest - Project 1999",
        "genre": "Classic MMORPG",
        "server": "Project 1999 Blue",
        "population": "High (several hundred concurrent)",
        "description": "Classic 1999 MMORPG experience with official Daybreak licensing",
        "website": "https://project1999.com",
        "client_download_url": "https://project1999.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts"],
        "executable": "eqgame.exe",
        "install_notes": "Titanium client required. Edit eqclient.ini: VertexShaders=FALSE. Long load times (5-20 min) are normal.",
        "native": False,
        "tested": True
    },

    "swtor": {
        "name": "Star Wars: The Old Republic",
        "genre": "Sci-Fi MMORPG",
        "server": "Official",
        "population": "Very High",
        "description": "Story-driven Star Wars MMO. Free-to-play with optional subscription.",
        "website": "https://swtor.com",
        "client_download_url": "https://swtor.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "winetricks"],
        "executable": "swtor.exe",
        "install_notes": "Critical: Set bitraider_disable:true in launcher.settings. Use 32-bit Wine prefix.",
        "native": False,
        "tested": True
    },

    "lotro": {
        "name": "Lord of the Rings Online",
        "genre": "Fantasy MMORPG",
        "server": "Official",
        "population": "High",
        "description": "Explore Middle-earth. Gold tier Wine compatibility via Steam.",
        "website": "https://lotro.com",
        "client_download_url": "steam://install/212500",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "lotroclient.exe",
        "install_notes": "Install via Steam with Proton 5.13-6 or newer. Works flawlessly.",
        "native": False,
        "tested": True
    },

    # === Asian MMORPGs ===
    "l2-essence": {
        "name": "Lineage 2 - L2Essence",
        "genre": "Fantasy MMORPG",
        "server": "L2Essence (x20)",
        "population": "High (1,000+ concurrent)",
        "description": "Essence x20 rates, no wipes, active PvP",
        "website": "https://l2essence.com",
        "client_download_url": "https://l2essence.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "corefonts", "d3dx9", "dotnet20"],
        "executable": "system/L2.exe",
        "install_notes": "Windows 98 compatibility mode. Install Tahoma fonts.",
        "native": False,
        "tested": True
    },

    "l2-elmorelab": {
        "name": "Lineage 2 - Elmorelab",
        "genre": "Fantasy MMORPG",
        "server": "Elmorelab Teon (C4 x1)",
        "population": "High (500+ concurrent)",
        "description": "Classic Chronicle 4 experience, hardcore",
        "website": "https://elmorelab.com",
        "client_download_url": "https://elmorelab.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "vcrun2008"],
        "executable": "system/L2.exe",
        "install_notes": "C4 client. No dual-box, hardcore buffer system.",
        "native": False,
        "tested": True
    },

    "ragnarok-revivalro": {
        "name": "Ragnarok Online - RevivalRO",
        "genre": "Anime MMORPG",
        "server": "RevivalRO Freya (Renewal)",
        "population": "High",
        "description": "Episode 21 Renewal with 4th jobs. 30x/30x/10x rates.",
        "website": "https://ragnarevival.com",
        "client_download_url": "https://ragnarevival.com/download",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "RevivalRO.exe",
        "install_notes": "Gepard Shield anti-cheat is Linux compatible.",
        "native": False,
        "tested": True
    },

    "ragnarok-talonro": {
        "name": "Ragnarok Online - TalonRO",
        "genre": "Anime MMORPG",
        "server": "TalonRO (Pre-renewal)",
        "population": "High",
        "description": "Pre-renewal classic since 2007. Low-rate authentic.",
        "website": "https://talonro.com",
        "client_download_url": "https://talonro.com/download",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "tRO.exe",
        "install_notes": "Very stable on Linux. Long-running server.",
        "native": False,
        "tested": True
    },

    "aion-gamezaion": {
        "name": "Aion - GamezAion",
        "genre": "Fantasy MMORPG",
        "server": "GamezAion (4.8)",
        "population": "High",
        "description": "4.8 PvPvE, no P2W, EU dedicated",
        "website": "https://gamezaion.com",
        "client_download_url": "https://gamezaion.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "winetricks"],
        "executable": "bin64/aion.bin",
        "install_notes": "No GameGuard on private servers. Free Patron status.",
        "native": False,
        "tested": True
    },

    "rf-online": {
        "name": "RF Online",
        "genre": "Sci-Fi MMORPG",
        "server": "Community Server",
        "population": "Medium",
        "description": "Three-race factional wars with massive chip wars",
        "website": "https://rfonline.com",
        "client_download_url": "https://rfonline.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "RF.exe",
        "install_notes": "Territorial control PvP, unique faction system.",
        "native": False,
        "tested": True
    },

    # === Action MMORPGs ===
    "tera-menma": {
        "name": "TERA - Menma's TERA",
        "genre": "Action MMORPG",
        "server": "Menma's TERA (EU/RU)",
        "population": "High (500-600 concurrent)",
        "description": "Post-shutdown preservation. Action combat with true aim.",
        "website": "https://menmastera.com",
        "client_download_url": "https://menmastera.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "winetricks"],
        "executable": "Binaries/TERA.exe",
        "install_notes": "No XIGNCODE3. Classic 2013 Island of Dawn restored. Excellent compatibility.",
        "native": False,
        "tested": True
    },

    "gw2": {
        "name": "Guild Wars 2",
        "genre": "Fantasy MMORPG",
        "server": "Official",
        "population": "Very High",
        "description": "Dynamic events MMORPG. Platinum tier on ProtonDB.",
        "website": "https://guildwars2.com",
        "client_download_url": "steam://install/1284210",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "Gw2-64.exe",
        "install_notes": "Install via Steam. For existing accounts add '-provider Portal' launch parameter.",
        "native": False,
        "tested": True
    },

    "archeage": {
        "name": "ArcheAge - ArcheRage",
        "genre": "Sandbox MMORPG",
        "server": "ArcheRage (9.5)",
        "population": "High",
        "description": "Post-shutdown preservation. Housing, farming, naval combat.",
        "website": "https://archerage.to",
        "client_download_url": "https://archerage.to/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "bin64/archeage.exe",
        "install_notes": "Most established post-shutdown server. Free Patron, increased rates.",
        "native": False,
        "tested": True
    },

    # === Story-Driven MMORPGs ===
    "ffxiv": {
        "name": "Final Fantasy XIV",
        "genre": "Fantasy MMORPG",
        "server": "Official (use XIVLauncher)",
        "population": "Very High",
        "description": "Critically acclaimed story-driven MMO. Gold tier with XIVLauncher.",
        "website": "https://finalfantasyxiv.com",
        "client_download_url": "flatpak://dev.goats.xivlauncher",
        "install_type": "aur",
        "aur_package": "xivlauncher",
        "launch_command": "xivlauncher",
        "dependencies": ["flatpak", "xivlauncher"],
        "executable": "ffxiv_dx11.exe",
        "install_notes": "XIVLauncher is ESSENTIAL for FFXIV on Linux. Prefers AUR on Arch, falls back to Flatpak.",
        "native": False,
        "tested": True
    },

    "pso-ephinea": {
        "name": "Phantasy Star Online - Ephinea",
        "genre": "Sci-Fi Action RPG",
        "server": "Ephinea",
        "population": "High",
        "description": "Classic Dreamcast/Xbox MMO preserved with active community",
        "website": "https://ephinea.pioneer2.net",
        "client_download_url": "https://ephinea.pioneer2.net/download",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "online.exe",
        "install_notes": "US/EU servers, weekly events. Works perfectly, runs on low-end hardware.",
        "native": False,
        "tested": True
    },

    # === Native Linux MMORPGs ===
    "albion": {
        "name": "Albion Online",
        "genre": "Sandbox MMORPG",
        "server": "Official (Native Linux)",
        "population": "Very High",
        "description": "Cross-platform sandbox with player-driven economy. Native Linux support!",
        "website": "https://albiononline.com",
        "client_download_url": "https://albiononline.com/download",
        "install_type": "native",
        "dependencies": ["flatpak"],
        "executable": "Albion-Online",
        "install_notes": "Native Linux support! No Wine/Proton needed.",
        "native": True,
        "tested": True
    },

    "osrs": {
        "name": "Old School RuneScape",
        "genre": "Fantasy MMORPG",
        "server": "Official (RuneLite)",
        "population": "Very High (Massive playerbase)",
        "description": "2007 RuneScape with native RuneLite client",
        "website": "https://oldschool.runescape.com",
        "client_download_url": "https://runelite.net/downloads/linux",
        "install_type": "native",
        "dependencies": ["java"],
        "executable": "runelite",
        "install_notes": "Native Linux support! Java-based, runs anywhere.",
        "native": True,
        "tested": True
    },

    "rs3": {
        "name": "RuneScape 3",
        "genre": "Fantasy MMORPG",
        "server": "Official (Native Client)",
        "population": "Very High",
        "description": "Modern RuneScape with updated graphics",
        "website": "https://runescape.com",
        "client_download_url": "flatpak://com.jagex.RuneScape",
        "install_type": "aur",
        "aur_package": "runescape-launcher",
        "launch_command": "runescape-launcher",
        "dependencies": [],
        "executable": "runescape",
        "install_notes": "Native Linux client! Prefers AUR on Arch, falls back to Flatpak.",
        "native": True,
        "tested": True
    }
}


def get_all_games():
    """Return list of all games"""
    return GAMES_DATABASE


def get_game_by_id(game_id):
    """Get specific game by ID"""
    return GAMES_DATABASE.get(game_id)


def get_games_by_genre(genre):
    """Filter games by genre"""
    return {k: v for k, v in GAMES_DATABASE.items() if genre.lower() in v['genre'].lower()}


def get_native_games():
    """Get only native Linux games"""
    return {k: v for k, v in GAMES_DATABASE.items() if v['native']}


def get_tested_games():
    """Get only tested/working games"""
    return {k: v for k, v in GAMES_DATABASE.items() if v['tested']}
