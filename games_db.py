"""
Game database registry for MMORPGs
Contains metadata, installation instructions, and server information
"""
from typing import Dict, Any, Optional

GAMES_DATABASE = {
    # === Classic Western MMORPGs ===
    "wow-warmane-icecrown": {
        "name": "World of Warcraft - Warmane Icecrown",
        "genre": "Fantasy MMORPG",
        "server": "Warmane Icecrown (7x WotLK)",
        "population": "Very High (5,000-10,000+ concurrent)",
        "description": "7x WotLK server, PvP-focused with massive population",
        "website": "https://warmane.com",
        "client_download_url": "https://www.warmane.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "Wow.exe",
        "install_notes": "Manual download required from warmane.com. Has torrent and direct download options. Set realmlist to logon.warmane.com after install.",
        "native": False,
        "tested": True
    },

    "wow-turtle": {
        "name": "World of Warcraft - Turtle WoW",
        "genre": "Fantasy MMORPG",
        "server": "Turtle WoW (Vanilla+)",
        "population": "High (1,000-3,000 concurrent)",
        "description": "Vanilla+ with custom content and dedicated community. Native Linux client available!",
        "website": "https://turtle-wow.org",
        "client_download_url": "https://cdn.turtle-wow.org/launcher/turtle-wow-launcher-linux.AppImage",
        "install_type": "aur",
        "aur_package": "turtle-wow",
        "install_script": "install_turtlewow.sh",
        "dependencies": [],
        "executable": "turtle-wow",
        "install_notes": "Native Linux client! AUR package available (turtle-wow) for Arch users. Falls back to AppImage for other distros. No Wine needed! Launcher auto-downloads game files on first run.",
        "native": True,
        "tested": True
    },

    "warhammer-ror": {
        "name": "Warhammer Online - Return of Reckoning",
        "genre": "RvR MMORPG",
        "server": "Return of Reckoning",
        "population": "High (400-3,500 concurrent)",
        "description": "Only active WAR server. Massive realm vs realm battles.",
        "website": "https://returnofreckoning.com",
        "client_download_url": "http://launcher.returnofreckoning.com/RoRLauncher.exe",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "RoRLauncher.exe",
        "install_notes": "RoR Launcher auto-downloads game files. Run launcher with UMU. Official Linux guide available.",
        "native": False,
        "tested": True
    },

    "everquest-p1999": {
        "name": "EverQuest - Project 1999 (Green/Blue/Red)",
        "genre": "Classic MMORPG",
        "server": "Project 1999 - Choose Green/Blue/Red in-game",
        "population": "Very High (1,000+ on Green, ~300 on Blue, ~50 on Red PvP)",
        "description": "Classic 1999-2001 EverQuest. GREEN: Velious-locked PvE (most popular, 1,000+ players). BLUE: Full classic progression PvE (established economy, ~300 players). RED: PvP server (teams/FFA zones, ~50 players). Server selection in-game launcher. Officially licensed by Daybreak.",
        "website": "https://project1999.com",
        "client_download_url": "https://archive.org/download/EQP99V46/EQ%20P99%20v46.zip",
        "install_type": "manual_download",
        "install_script": "install_p99.sh",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts", "unzip"],
        "executable": "Launch Titanium.bat",
        "install_notes": "Auto-installer downloads Titanium + P99 v46 (1.3GB), extracts game files, applies latest P99 patches. Choose server in-game via 'Launch Titanium' launcher. CRITICAL: ALWAYS use 'Launch Titanium.bat', NEVER run eqgame.exe or patch! Account: https://www.project1999.com/account/?Play",
        "native": False,
        "tested": True
    },

    "everquest-quarm": {
        "name": "EverQuest - Project Quarm",
        "genre": "Classic MMORPG",
        "server": "Project Quarm (Time-locked Progression, Officially Licensed)",
        "population": "Very High (1,200 cap + queue, offline Bazaar excluded)",
        "description": "Officially licensed by Daybreak! Time-locked progression through PoP. STRICT one-box policy (no multiboxing). Solo Self-Found ruleset available. Legacy camps/items, raid rotation, offline Bazaar trading. Currently on Luclin era.",
        "website": "https://projectquarm.com",
        "forums": "https://www.takproject.net/forums/index.php",
        "reddit": "https://www.reddit.com/r/ProjectQuarm",
        "server_stats": "https://www.eqemulator.org/index.php?pageid=serverinfo&worldid=3962",
        "client_download_url": "https://drive.google.com/file/d/1qoBktDeJMJKPBr-EZxub1vspJhz11i1y/view",
        "patcher_url": "https://projectquarm.com",
        "install_type": "manual_download",
        "install_script": "install_quarm.sh",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts"],
        "executable": "eqgame.exe",
        "install_notes": "OFFICIALLY LICENSED by Daybreak Games! Auto-installer script downloads TAKP client from Google Drive and extracts QuarmPatcher from Downloads. Features: One-Box Policy (strictly enforced via IP), Solo Self-Found (SSF) opt-in ruleset, custom cultural tradeskill NPCs, legacy camp/item system, raid rotations, 1,200 player cap with queue. ACCOUNT: Create forum account at takproject.net/forums → 'Game Accounts' → 'Create Login Server Account'. After install: 1) launch_patcher.sh to update. 2) launch_game.sh to play.",
        "native": False,
        "tested": False
    },

    "everquest-ezserver": {
        "name": "EverQuest - EZ Server",
        "genre": "Classic MMORPG",
        "server": "EZ Server (Custom High-Rate)",
        "population": "Medium (active community)",
        "description": "Custom high-rate progression with extensive custom content. MacroQuest supported/encouraged.",
        "website": "https://ezserver.online",
        "client_download_url": "http://wiki.ezserver.online/EZ_Server_Files",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "eqgame.exe",
        "install_notes": "Requires Rain of Fear 2 (ROF2) client. Download EZ files from wiki and extract to main EQ directory. Different client than P99/Quarm.",
        "native": False,
        "tested": False
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

    # Lineage 1
    "lineage1-l15": {
        "name": "Lineage 1 - L1.5",
        "genre": "Classic MMORPG",
        "server": "L1.5 (Never Wiped - 16+ years)",
        "population": "High (huge and helpful community)",
        "description": "16+ years running, NEVER WIPED. Mix of classic and custom content with new end-game dungeons. 99.999% uptime.",
        "website": "https://www.l15server.com",
        "client_download_url": "https://www.l15server.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "lineage.exe",
        "install_notes": "Long-term stable server. Active development and regular events. Register at lineagehd.com/register.html. Windows client works via Wine.",
        "native": False,
        "tested": False
    },

    "lineage1-l1justice": {
        "name": "Lineage 1 - L1Justice",
        "genre": "Classic MMORPG",
        "server": "L1Justice (Updated Client)",
        "population": "High (top private server)",
        "description": "Classic Lineage 1 with updated 3.63 client. Described as top Lin1 private server.",
        "website": "https://l1justice.com/lineage/",
        "client_download_url": "https://l1justice.com/lineage/",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "jLauncher.exe",
        "install_notes": "Download jLauncher.exe from website. Client version 3.63 (updated August 2025). May require Wine configuration.",
        "native": False,
        "tested": False
    },

    # Lineage 2
    "l2-reborn": {
        "name": "Lineage 2 - L2 Reborn",
        "genre": "Fantasy MMORPG",
        "server": "L2 Reborn Eternal Interlude (x10)",
        "population": "Very High (massive server)",
        "description": "Vanilla Interlude, no wipes since October 2019. No pay-to-win, strict anti-cheat. Midrate x10 server.",
        "website": "https://l2reborn.org",
        "client_download_url": "https://l2reborn.org",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "winetricks", "d3dx9", "dotnet20", "vcrun2008"],
        "executable": "system/L2.exe",
        "install_notes": "Interlude client. Install dependencies: d3dx9, dotnet20, vcrun2008. DirectX 9.0c required. May need to change ALT key to SUPER in Linux. Use Lutris for easier setup.",
        "native": False,
        "tested": False
    },

    "l2-classic-club": {
        "name": "Lineage 2 - L2 Classic Club",
        "genre": "Fantasy MMORPG",
        "server": "L2 Classic Club Dion (x3)",
        "population": "Very High (thousands of players)",
        "description": "7+ years active. Classic 2.0 European server. Free-to-play, international community. Stats at l2classic.club/stats",
        "website": "https://l2classic.club",
        "client_download_url": "https://l2classic.club",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "winetricks", "d3dx9", "dotnet20", "vcrun2008"],
        "executable": "system/L2.exe",
        "install_notes": "Classic 2.0 client. Established long-term server. Active events and updates. Same Wine requirements as other L2 servers.",
        "native": False,
        "tested": False
    },

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
        "description": "Episode 21 Renewal with 4th jobs. 30x/30x/10x rates. PC & Android support.",
        "website": "https://ragnarevival.com",
        "client_download_url": "https://loki.ragnarevival.com/?module=main&action=downloads",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "RevivalRO.exe",
        "install_notes": "WARNING: Anti-cheat compatibility unclear. If GameGuard is used, Wine/Proton may be blocked. Verify with community before installing. 2GB RAM, 2GB disk required.",
        "native": False,
        "tested": False
    },

    "ragnarok-talonro": {
        "name": "Ragnarok Online - TalonRO",
        "genre": "Anime MMORPG",
        "server": "TalonRO (Pre-renewal)",
        "population": "High (established since 2007)",
        "description": "Pre-renewal classic, medium-rate, nostalgic with custom features. Friendly community.",
        "website": "https://www.talonro.com",
        "client_download_url": "https://www.talonro.com/download",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "tRO.exe",
        "install_notes": "WARNING: Gepard Shield anti-cheat BLOCKS Wine/VMs. NOT RECOMMENDED for Linux users. Server had Linux wiki guide but Gepard update broke compatibility.",
        "native": False,
        "tested": False
    },

    "ragnarok-originsro": {
        "name": "Ragnarok Online - OriginsRO",
        "genre": "Anime MMORPG",
        "server": "OriginsRO (Classic 5x)",
        "population": "Medium",
        "description": "Classic rates 5x/5x/5x server. Check RateMyServer for current status.",
        "website": "https://ratemyserver.net/index.php?page=detailedlistserver&serid=16761",
        "client_download_url": "https://ratemyserver.net/index.php?page=detailedlistserver&serid=16761",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "Ragnarok.exe",
        "install_notes": "WARNING: Check anti-cheat status with server community. If no GameGuard, should work with Wine. If GameGuard is present, Wine/Proton will be blocked.",
        "native": False,
        "tested": False
    },

    "ragnarok-uaro": {
        "name": "Ragnarok Online - uaRO",
        "genre": "Anime MMORPG",
        "server": "uaRO (Private Server)",
        "population": "Active",
        "description": "Ragnarok Online private server with Linux compatibility. No GameGuard blocking.",
        "website": "https://uaro.net/",
        "client_download_url": "http://bit.ly/3NHonjI",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "Uaro.exe",
        "install_notes": "Works on Linux via Wine/Proton. No anti-cheat blocking. Client auto-downloads and extracts.",
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

    "rf-haunting": {
        "name": "RF Online - RF Haunting",
        "genre": "Sci-Fi MMORPG",
        "server": "RF Haunting (Private Server)",
        "population": "High (active)",
        "description": "Ultimate RF experience. Fantasy sci-fi 3D MMORPG with three-race factional wars and massive chip wars. Free to play.",
        "website": "https://www.rfhaunting.com",
        "client_download_url": "https://rfhaunting.com/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "RF.exe",
        "install_notes": "Download client from website with installation guide. Works with Wine/Proton. CodeWeavers CrossOver and PlayOnLinux officially support RF Online. Wine 10.0 compatible.",
        "native": False,
        "tested": False
    },

    "rf-altruism": {
        "name": "RF Online - RF Altruism",
        "genre": "Sci-Fi MMORPG",
        "server": "RF Altruism (EU Private Server)",
        "population": "Medium (EU-focused)",
        "description": "EU-focused RF Online server. Play without requiring money to enjoy and compete. Three-race territorial control PvP.",
        "website": "https://www.rfaltruism.co.uk",
        "client_download_url": "https://www.rfaltruism.co.uk",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "RFAltruismLauncher.exe",
        "install_notes": "Good choice for European players (time zone friendly). Same Wine/Proton compatibility as other RF servers. Extract and install via Wine.",
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
        "client_download_url": "http://files.pioneer2.net/Ephinea_PSOBB_Installer.exe",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "vcrun2015", "dotnet48"],
        "executable": "online.exe",
        "install_notes": "Installer auto-downloads Blue Burst client. US/EU servers, weekly events. Works perfectly, runs on low-end hardware.",
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
    },

    # === Additional Classic Western MMORPGs ===
    "daoc-eden": {
        "name": "Dark Age of Camelot - Eden",
        "genre": "RvR MMORPG",
        "server": "Eden (Private Server - Classic)",
        "population": "Medium-High",
        "description": "Classic DAoC freeshard with three-realm RvR. No subscription required.",
        "website": "https://eden-daoc.net",
        "client_download_url": "https://eden-daoc.net/viewtopic.php?t=3527",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "dotnet40", "dotnet45"],
        "executable": "game.dll",
        "install_notes": "Use Lutris with lutris-fshack-7.2-x86_64 wine version. Install dotnet40/45 via winetricks. Enable DXVK if launcher doesn't display correctly.",
        "native": False,
        "tested": True
    },

    "uo-outlands": {
        "name": "Ultima Online - Outlands",
        "genre": "Sandbox MMORPG",
        "server": "UO Outlands (Private Server)",
        "population": "High (2,000+ concurrent)",
        "description": "Most popular UO freeshard. Custom content, balanced gameplay, Renaissance era.",
        "website": "https://uooutlands.com",
        "client_download_url": "https://wiki.uooutlands.com/Install_UO_on_Linux",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "Launcher.exe",
        "install_notes": "Use GE-Proton9-27. Install via Lutris or Bottles. Official Linux installation wiki available.",
        "native": False,
        "tested": True
    },

    "coh-homecoming": {
        "name": "City of Heroes - Homecoming",
        "genre": "Superhero MMORPG",
        "server": "Homecoming (Community Server)",
        "population": "High",
        "description": "Community-run resurrection of CoH. Create custom superheroes, extensive character customization.",
        "website": "https://homecomingservers.com",
        "client_download_url": "https://manifest.cohhc.gg/launcher/hcinstall.exe",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "dotnet35", "dinput8"],
        "executable": "cityofheroes.exe",
        "install_notes": "HC Installer auto-downloads game files. Install dotnet35 and dinput8 via winetricks. Often better performance than Windows.",
        "native": False,
        "tested": True
    },

    "swg-legends": {
        "name": "Star Wars Galaxies - Legends",
        "genre": "Sandbox Sci-Fi MMORPG",
        "server": "SWG Legends (Private Server)",
        "population": "Medium-High",
        "description": "Post-shutdown SWG preservation. 32 professions, player cities, space combat.",
        "website": "https://swglegends.com",
        "client_download_url": "https://swglegends.com/wiki/index.php?title=SWG_Legends_Launcher",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "SWGEmu.exe",
        "install_notes": "Use 32-bit Wine prefix with .NET 4.0 for launcher. Set DXVK to v1.8.1L (graphical issues with newer versions). Lutris installer available.",
        "native": False,
        "tested": True
    },

    # === Official Steam MMORPGs ===
    "eso": {
        "name": "Elder Scrolls Online",
        "genre": "Fantasy MMORPG",
        "server": "Official",
        "population": "Very High",
        "description": "Explore Tamriel. Story-driven quests, PvP, housing.",
        "website": "https://www.elderscrollsonline.com",
        "client_download_url": "steam://install/306130",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "eso64.exe",
        "install_notes": "Use Proton Experimental or Proton 7+. Similar FPS to Windows. Minion addon manager works. Very well supported.",
        "native": False,
        "tested": True
    },

    "bdo": {
        "name": "Black Desert Online",
        "genre": "Action MMORPG",
        "server": "Official",
        "population": "Very High",
        "description": "Action combat, life skills, node wars, extensive character customization.",
        "website": "https://www.naeu.playblackdesert.com",
        "client_download_url": "steam://install/582660",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "BlackDesert64.exe",
        "install_notes": "Use Proton Experimental or ProtonGE 8-28. Steam version recommended. Works well but requires Proton tuning.",
        "native": False,
        "tested": True
    },

    "neverwinter": {
        "name": "Neverwinter Online",
        "genre": "Action MMORPG",
        "server": "Official",
        "population": "High",
        "description": "D&D-based action MMORPG. Story-driven campaigns.",
        "website": "https://www.playneverwinter.com",
        "client_download_url": "steam://install/109600",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "Neverwinter.exe",
        "install_notes": "Use Proton 10.0-2 or newer. Valve actively improving support. Runs smoothly on Linux.",
        "native": False,
        "tested": True
    },

    "dcuo": {
        "name": "DC Universe Online",
        "genre": "Superhero MMORPG",
        "server": "Official",
        "population": "Medium-High",
        "description": "Create DC superheroes/villains. Action combat.",
        "website": "https://www.dcuniverseonline.com",
        "client_download_url": "steam://install/24200",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "DCGAME.EXE",
        "install_notes": "Works with Proton 5.0.10. Avoid Proton 7/8/Experimental (DXVK regression). Free-to-play.",
        "native": False,
        "tested": True
    },

    "poe2": {
        "name": "Path of Exile 2",
        "genre": "Action RPG/MMORPG",
        "server": "Official",
        "population": "Very High",
        "description": "Diablo-like ARPG with MMORPG elements. Extensive skill system.",
        "website": "https://www.pathofexile.com",
        "client_download_url": "steam://install/2694490",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "PathOfExile2.exe",
        "install_notes": "Works with Proton 9.0-3 or newer. December 2024 Early Access works excellently on Linux.",
        "native": False,
        "tested": True
    },

    "apb": {
        "name": "APB Reloaded",
        "genre": "Action MMORPG",
        "server": "Official",
        "population": "Medium",
        "description": "Cops vs Criminals open-world action MMO. Extensive customization.",
        "website": "https://www.gamersfirst.com/apb",
        "client_download_url": "steam://install/113400",
        "install_type": "steam",
        "dependencies": ["steam", "proton-ge", "battleye-runtime"],
        "executable": "APB.exe",
        "install_notes": "BattlEye Linux support enabled (Sept 2024). Use Proton-GE. Install Proton BattlEye Runtime via Steam. Longer login times than Windows.",
        "native": False,
        "tested": True
    },

    # === Additional Native Linux MMORPGs ===
    "ryzom": {
        "name": "Ryzom",
        "genre": "Sci-Fi Fantasy MMORPG",
        "server": "Official (Native Linux, Open Source)",
        "population": "Medium",
        "description": "Classless sandbox MMORPG. Complex crafting, dynamic environments.",
        "website": "https://www.ryzom.com",
        "client_download_url": "steam://install/373720",
        "install_type": "steam",
        "dependencies": ["steam"],
        "executable": "ryzom_client",
        "install_notes": "Native Linux client. Open source (AGPLv3). Available via website or Steam.",
        "native": True,
        "tested": True
    },

    "wurm": {
        "name": "Wurm Online",
        "genre": "Sandbox MMORPG",
        "server": "Official (Native Linux)",
        "population": "Medium",
        "description": "Terraforming, building, crafting-focused sandbox. Extremely deep systems.",
        "website": "https://www.wurmonline.com",
        "client_download_url": "https://www.wurmonline.com/download",
        "install_type": "native",
        "dependencies": [],
        "executable": "WurmLauncher",
        "install_notes": "Native Linux client via launcher or Steam. Not officially supported but community provides assistance.",
        "native": True,
        "tested": True
    },

    "vendetta": {
        "name": "Vendetta Online",
        "genre": "Space Combat MMORPG",
        "server": "Official (Native Linux)",
        "population": "Medium",
        "description": "3D space combat MMO. Cross-platform (PC/Mac/Linux/Android/iOS/VR).",
        "website": "https://www.vendetta-online.com",
        "client_download_url": "https://www.vendetta-online.com/h/download.html",
        "install_type": "native",
        "dependencies": [],
        "executable": "vendetta",
        "install_notes": "Native Linux support since 2004. Cross-platform play. 20+ years of Linux support.",
        "native": True,
        "tested": True
    },

    "tibia": {
        "name": "Tibia",
        "genre": "Classic MMORPG",
        "server": "Official (Native Linux)",
        "population": "Medium-High",
        "description": "Oldest active MMORPG (1997). New Monk class added Summer 2025.",
        "website": "https://www.tibia.com",
        "client_download_url": "https://www.tibia.com/support/?subtopic=gethelp&entryid=121",
        "install_type": "native",
        "dependencies": [],
        "executable": "Tibia",
        "install_notes": "Tibia 11 Linux client available. Not officially supported by CipSoft but provided.",
        "native": True,
        "tested": True
    },

    "flyff": {
        "name": "Flyff Universe",
        "genre": "Anime MMORPG",
        "server": "Official (Browser-based)",
        "population": "High",
        "description": "Flying system, anime aesthetic. Browser-based remake of Flyff.",
        "website": "https://universe.flyff.com",
        "client_download_url": "https://universe.flyff.com/play",
        "install_type": "native",
        "dependencies": [],
        "executable": "Web browser",
        "install_notes": "No download required. Play in any modern browser (Firefox, Chrome, etc.). Cross-platform.",
        "native": True,
        "tested": True
    },

    # === Additional Asian MMORPGs ===
    "perfectworld": {
        "name": "Perfect World - Evolved PW",
        "genre": "Fantasy MMORPG",
        "server": "Evolved PW (Private Server)",
        "population": "Medium-High",
        "description": "Flying system, martial arts combat, multiple races/classes.",
        "website": "https://evolvedpw.com",
        "client_download_url": "https://updates-eu.evolvedpw.com/Evolved-PWI-1.7.2.zip",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "elementclient.exe",
        "install_notes": "Client will auto-download and extract. Launch with UMU launcher. Recent updates transitioned from 32-bit to 64-bit executables.",
        "native": False,
        "tested": True
    },

    "conqueror": {
        "name": "Conqueror Online - ImmortalsCo",
        "genre": "Action MMORPG",
        "server": "ImmortalsCo (Private Server)",
        "population": "High (7,000+ daily)",
        "description": "Martial arts-themed action MMORPG. Fast-paced combat.",
        "website": "https://conqueronline.net",
        "client_download_url": "https://conqueronline.net",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "Conquer.exe",
        "install_notes": "Use full 1.6GB+ installer (not small patcher). Minor non-game-breaking bugs on Linux.",
        "native": False,
        "tested": True
    },

    "metin2": {
        "name": "Metin2 - Private Servers",
        "genre": "Asian Action MMORPG",
        "server": "Various Private Servers",
        "population": "Medium-High (varies)",
        "description": "Action combat Korean MMORPG. Multiple private servers with custom features.",
        "website": "https://metin2pserver.net",
        "client_download_url": "https://metin2pserver.net",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "metin2client.exe",
        "install_notes": "Private servers without anti-cheat work Gold/Platinum. Check server-specific compatibility.",
        "native": False,
        "tested": True
    },

    "drakensang": {
        "name": "Drakensang Online",
        "genre": "Action RPG/MMORPG",
        "server": "Official",
        "population": "Medium-High",
        "description": "Browser-based action MMORPG. Also available on Steam.",
        "website": "https://www.drakensang.com",
        "client_download_url": "steam://install/2067850",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "DrakensangOnline.exe",
        "install_notes": "Browser version works directly on Linux (no Wine needed). Steam version: use Proton Experimental.",
        "native": False,
        "tested": True
    },

    "wakfu": {
        "name": "Wakfu",
        "genre": "Tactical MMORPG",
        "server": "Official",
        "population": "Medium",
        "description": "Turn-based tactical combat. Environmental/political systems.",
        "website": "https://www.wakfu.com",
        "client_download_url": "https://support.ankama.com/hc/en-us/articles/360017472154",
        "install_type": "manual_download",
        "dependencies": ["java-10-openjdk"],
        "executable": "Wakfu",
        "install_notes": "Ankama Launcher AppImage available. Also on Steam. Requires Java 10.",
        "native": False,
        "tested": True
    },


    "silkroad-zenger": {
        "name": "Silkroad Online - Zenger",
        "genre": "Action MMORPG",
        "server": "Zenger Online (Cap 100 ISRO-R)",
        "population": "Medium",
        "description": "Silk Road trading MMORPG. Cap 100 with ISRO-R files. Trade, hunt thieves, PvP.",
        "website": "https://www.zengeronline.com",
        "client_download_url": "https://www.zengeronline.com/ZengerOnline.rar",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "sro_client.exe",
        "install_notes": "Client auto-downloads and extracts. 2.0GB RAR file. Launch with UMU.",
        "native": False,
        "tested": False
    },

    "silkroad-phoenix": {
        "name": "Silkroad Online - Phoenix",
        "genre": "Action MMORPG",
        "server": "SRO Phoenix (Cap 110)",
        "population": "Medium-High",
        "description": "European Silkroad server with balanced rates. Active trading system and job system (trader/thief/hunter).",
        "website": "https://srophoenix.com",
        "client_download_url": "https://srophoenix.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "sro_client.exe",
        "install_notes": "European server with English support. Balanced gameplay and active community.",
        "native": False,
        "tested": False
    },

    "silkroad-legend": {
        "name": "Silkroad Online - Legend",
        "genre": "Action MMORPG",
        "server": "SRO Legend (Cap 120)",
        "population": "Medium",
        "description": "High-cap Silkroad server with extended content. Custom features and active development.",
        "website": "https://srolegend.com",
        "client_download_url": "https://srolegend.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "sro_client.exe",
        "install_notes": "Cap 120 with extended content. Custom features and events.",
        "native": False,
        "tested": False
    },

    "knight-myko": {
        "name": "Knight Online - MyKO",
        "genre": "Fantasy MMORPG",
        "server": "MyKO (v1299)",
        "population": "High (international community)",
        "description": "Level cap 72 PvP MMORPG. Nation wars, castle sieges, intense PvP combat.",
        "website": "https://ko-myko.com",
        "client_download_url": "https://ko-myko.com/downloads",
        "install_type": "manual_download",
        "install_script": "install_knight_myko.sh",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts", "cjkfonts"],
        "executable": "Client_KOMYKO.exe",
        "install_notes": "Download client_myko.zip or Client_KOMYKO.zip from ko-myko.com/downloads and save to Downloads folder. Auto-installer will extract the archive and set up Wine dependencies. Client_KOMYKO.exe is the game launcher (no separate installation needed).",
        "native": False,
        "tested": True
    },

    # === Additional Games with Special Notes ===
    "lostark": {
        "name": "Lost Ark",
        "genre": "Action MMORPG",
        "server": "Official",
        "population": "Very High",
        "description": "Isometric action MMORPG. Raids, dungeons, multiple classes. WARNING: EAC support unstable.",
        "website": "https://www.playlostark.com",
        "client_download_url": "steam://install/1599340",
        "install_type": "steam",
        "dependencies": ["steam", "proton"],
        "executable": "LostArk.exe",
        "install_notes": "Easy Anti-Cheat Linux support re-enabled (July 2025). Use Proton 9.0.4. WARNING: Support sporadic - has been enabled/disabled in past.",
        "native": False,
        "tested": True
    },

    "regnum": {
        "name": "Champions of Regnum",
        "genre": "RvR MMORPG",
        "server": "Official (Native Linux)",
        "population": "Low-Medium",
        "description": "Three-realm PvP focused MMORPG. Native Linux support.",
        "website": "https://www.championsofregnum.com",
        "client_download_url": "steam://install/222520",
        "install_type": "steam",
        "dependencies": ["steam", "proton-ge"],
        "executable": "regnum",
        "install_notes": "Native Linux client exists but community recommends Proton-GE for better stability.",
        "native": True,
        "tested": True
    },

    # === Final Fantasy XI Servers ===
    "ffxi-horizon": {
        "name": "Final Fantasy XI - Horizon",
        "genre": "Fantasy MMORPG",
        "server": "Horizon (75 Cap, Classic Experience)",
        "population": "Very High (1,500+ concurrent)",
        "description": "Most popular FFXI private server. Classic 75-cap experience with quality-of-life improvements. Active development and events.",
        "website": "https://horizonxi.com",
        "client_download_url": "https://horizonxi.com/install",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "pol.exe",
        "install_notes": "Download client from website. Use PlayOnline Viewer (pol.exe) to launch. Excellent Wine compatibility.",
        "native": False,
        "tested": True
    },

    "ffxi-eden": {
        "name": "Final Fantasy XI - Eden",
        "genre": "Fantasy MMORPG",
        "server": "Eden (75 Cap, Retail-like)",
        "population": "High (500-800 concurrent)",
        "description": "Retail-accurate 75-cap server. Authentic classic FFXI experience with minimal custom changes.",
        "website": "https://edenxi.com",
        "client_download_url": "https://edenxi.com/downloads",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "pol.exe",
        "install_notes": "Requires FFXI retail client. More hardcore than Horizon with authentic retail mechanics.",
        "native": False,
        "tested": True
    },

    "ffxi-era": {
        "name": "Final Fantasy XI - Era",
        "genre": "Fantasy MMORPG",
        "server": "Era (Wings of the Goddess)",
        "population": "Medium (200-400 concurrent)",
        "description": "Wings of the Goddess era server (80 cap). Includes ToAU and WotG content.",
        "website": "https://ffxiera.com",
        "client_download_url": "https://ffxiera.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "pol.exe",
        "install_notes": "Extended cap beyond 75. Includes additional expansions. Good Wine compatibility.",
        "native": False,
        "tested": False
    },

    "ffxi-nocturnal": {
        "name": "Final Fantasy XI - Nocturnal Souls",
        "genre": "Fantasy MMORPG",
        "server": "Nocturnal Souls (Custom Rate)",
        "population": "Medium",
        "description": "Custom rate FFXI server with quality-of-life features. More casual-friendly progression.",
        "website": "https://nocturnalsouls.net",
        "client_download_url": "https://nocturnalsouls.net",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "pol.exe",
        "install_notes": "Custom rates make leveling less grindy. Good for players wanting faster progression.",
        "native": False,
        "tested": False
    },

    "ffxi-catseye": {
        "name": "Final Fantasy XI - CatsEye",
        "genre": "Fantasy MMORPG",
        "server": "CatsEye (Retail-like)",
        "population": "Medium",
        "description": "Retail-accurate FFXI private server. Classic 75-cap era with authentic mechanics.",
        "website": "https://catseyexi.com",
        "client_download_url": "https://catseyexi.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "pol.exe",
        "install_notes": "Focuses on retail accuracy. Small but dedicated community.",
        "native": False,
        "tested": False
    },

    # === MU Online Servers ===
    "mu-icemu": {
        "name": "MU Online - IceMU",
        "genre": "Action MMORPG",
        "server": "IceMU (Season Server)",
        "population": "High",
        "description": "Popular MU Online season server. Regular resets and competitive gameplay.",
        "website": "https://icemu.net",
        "client_download_url": "https://icemu.net/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "main.exe",
        "install_notes": "Download client from website. Season server with regular updates and events.",
        "native": False,
        "tested": False
    },

    "mu-muaway": {
        "name": "MU Online - MuAway",
        "genre": "Action MMORPG",
        "server": "MuAway (Private Server)",
        "population": "Medium-High",
        "description": "Established MU Online private server with custom features.",
        "website": "https://muaway.com",
        "client_download_url": "https://muaway.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "main.exe",
        "install_notes": "Custom content and balanced PvP. Works well with Wine/Proton.",
        "native": False,
        "tested": False
    },

    "mu-mucore": {
        "name": "MU Online - MuCore",
        "genre": "Action MMORPG",
        "server": "MuCore (Private Server)",
        "population": "Medium",
        "description": "MU Online private server focused on classic gameplay.",
        "website": "https://mucore.net",
        "client_download_url": "https://mucore.net",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "main.exe",
        "install_notes": "Classic MU experience with minimal custom changes. Good compatibility.",
        "native": False,
        "tested": False
    },

    "mu-phenixmu": {
        "name": "MU Online - PhenixMU",
        "genre": "Action MMORPG",
        "server": "PhenixMU (Private Server)",
        "population": "Medium-High",
        "description": "Long-running MU Online private server with active community.",
        "website": "https://phenixmu.com",
        "client_download_url": "https://phenixmu.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "main.exe",
        "install_notes": "Established server with regular events. Good Wine compatibility.",
        "native": False,
        "tested": False
    },

    "mu-zhypermu": {
        "name": "MU Online - ZhyperMU",
        "genre": "Action MMORPG",
        "server": "ZhyperMU (Private Server)",
        "population": "Medium",
        "description": "MU Online private server with custom features and rates.",
        "website": "https://zhypermu.com",
        "client_download_url": "https://zhypermu.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008", "corefonts"],
        "executable": "main.exe",
        "install_notes": "Custom rates and features. Works with Wine/UMU launcher.",
        "native": False,
        "tested": False
    },

    # === Additional Conquer Online Servers ===
    "conqueror-classic": {
        "name": "Conqueror Online - Classic Conquer",
        "genre": "Action MMORPG",
        "server": "Classic Conquer (Private Server)",
        "population": "Medium",
        "description": "Classic Conquer Online experience with traditional rates and mechanics.",
        "website": "https://classicconquer.com",
        "client_download_url": "https://classicconquer.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008"],
        "executable": "Conquer.exe",
        "install_notes": "Classic rates and mechanics. Good for nostalgic players.",
        "native": False,
        "tested": False
    },

    "conqueror-classiclords": {
        "name": "Conqueror Online - ClassicLords",
        "genre": "Action MMORPG",
        "server": "ClassicLords (Private Server)",
        "population": "Medium",
        "description": "Conquer Online private server with balanced gameplay.",
        "website": "https://classiclords.com",
        "client_download_url": "https://classiclords.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008"],
        "executable": "Conquer.exe",
        "install_notes": "Balanced rates and active PvP. Wine compatible.",
        "native": False,
        "tested": False
    },

    "conqueror-dragonconquer": {
        "name": "Conqueror Online - DragonConquer",
        "genre": "Action MMORPG",
        "server": "DragonConquer (Private Server)",
        "population": "Medium-High",
        "description": "Popular Conquer Online server with custom content.",
        "website": "https://dragonconquer.com",
        "client_download_url": "https://dragonconquer.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008"],
        "executable": "Conquer.exe",
        "install_notes": "Custom content and events. Active community.",
        "native": False,
        "tested": False
    },

    "conqueror-paragonco": {
        "name": "Conqueror Online - ParagonCO",
        "genre": "Action MMORPG",
        "server": "ParagonCO (Private Server)",
        "population": "Medium",
        "description": "Conquer Online server with enhanced features and balanced PvP.",
        "website": "https://paragonco.com",
        "client_download_url": "https://paragonco.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9", "vcrun2008"],
        "executable": "Conquer.exe",
        "install_notes": "Enhanced features with balanced gameplay. Good Wine support.",
        "native": False,
        "tested": False
    },

    # === Additional Aion Servers ===
    "aion-classic": {
        "name": "Aion - Aion Classic 1.2",
        "genre": "Fantasy MMORPG",
        "server": "Aion Classic 1.2 (Private Server)",
        "population": "Medium-High",
        "description": "Classic Aion 1.2 experience. Pre-4.0 classic gameplay.",
        "website": "https://aionclassic.com",
        "client_download_url": "https://aionclassic.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "vcrun2010", "corefonts"],
        "executable": "bin64/aion.bin",
        "install_notes": "Classic 1.2 client. No GameGuard on private servers. Excellent compatibility.",
        "native": False,
        "tested": False
    },

    "aion-eldenaion": {
        "name": "Aion - EldenAion",
        "genre": "Fantasy MMORPG",
        "server": "EldenAion (Private Server)",
        "population": "High",
        "description": "Popular Aion private server with custom features and balanced rates.",
        "website": "https://eldenaion.com",
        "client_download_url": "https://eldenaion.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "vcrun2010", "corefonts"],
        "executable": "NCLauncher.exe",
        "install_notes": "Custom content and balanced PvP. No anti-cheat blocking.",
        "native": False,
        "tested": False
    },

    "aion-elyon": {
        "name": "Aion - Elyon Aion 3.0",
        "genre": "Fantasy MMORPG",
        "server": "Elyon Aion 3.0 (Private Server)",
        "population": "Medium-High",
        "description": "Aion 3.0 private server. Classic patch with balanced gameplay.",
        "website": "https://elyonaion.com",
        "client_download_url": "https://elyonaion.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "vcrun2010", "corefonts"],
        "executable": "bin64/aion.bin",
        "install_notes": "Version 3.0 client. Good balance between classic and modern features.",
        "native": False,
        "tested": False
    },

    "aion-eternalwar": {
        "name": "Aion - Eternal War",
        "genre": "Fantasy MMORPG",
        "server": "Eternal War (Private Server)",
        "population": "Medium",
        "description": "PvP-focused Aion private server. Active fortress battles and sieges.",
        "website": "https://aion-eternalwar.com",
        "client_download_url": "https://aion-eternalwar.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "vcrun2010", "corefonts"],
        "executable": "bin64/aion.bin",
        "install_notes": "PvP-focused with active sieges. No GameGuard.",
        "native": False,
        "tested": False
    },

    "aion-nostalg": {
        "name": "Aion - Nostalg Aion",
        "genre": "Fantasy MMORPG",
        "server": "Nostalg Aion (Classic Private Server)",
        "population": "Medium",
        "description": "Classic Aion experience with nostalgic gameplay. Pre-transformation era.",
        "website": "https://nostalgaion.com",
        "client_download_url": "https://nostalgaion.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2008", "vcrun2010", "corefonts"],
        "executable": "bin64/aion.bin",
        "install_notes": "Classic pre-transformation gameplay. Nostalgic for veteran players.",
        "native": False,
        "tested": False
    },

    # === Additional RF Online Servers ===
    "rf-novaverso": {
        "name": "RF Online - NovaVerso",
        "genre": "Sci-Fi MMORPG",
        "server": "NovaVerso (Private Server)",
        "population": "Medium",
        "description": "Brazilian RF Online server with custom features. Three-race faction PvP.",
        "website": "https://novaverso.com",
        "client_download_url": "https://novaverso.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9"],
        "executable": "RF.exe",
        "install_notes": "Brazilian server with international players. Custom content and events.",
        "native": False,
        "tested": False
    },

    "rf-universe": {
        "name": "RF Online - RF Universe",
        "genre": "Sci-Fi MMORPG",
        "server": "RF Universe (Private Server)",
        "population": "Medium",
        "description": "International RF Online server with balanced rates.",
        "website": "https://rfuniverse.net",
        "client_download_url": "https://rfuniverse.net",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9"],
        "executable": "RF.exe",
        "install_notes": "Balanced rates and active chip wars. Wine 10.0 compatible.",
        "native": False,
        "tested": False
    },

    "rf-banana": {
        "name": "RF Online - RFBanana",
        "genre": "Sci-Fi MMORPG",
        "server": "RFBanana (Private Server)",
        "population": "Medium",
        "description": "RF Online private server with custom content and events.",
        "website": "https://rfbanana.com",
        "client_download_url": "https://rfbanana.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9"],
        "executable": "RF.exe",
        "install_notes": "Custom content with regular events. Good Wine compatibility.",
        "native": False,
        "tested": False
    },

    "rf-fenix": {
        "name": "RF Online - RFFenix",
        "genre": "Sci-Fi MMORPG",
        "server": "RFFenix (Private Server)",
        "population": "Medium",
        "description": "Latin American RF Online server with active community.",
        "website": "https://rffenix.com",
        "client_download_url": "https://rffenix.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9"],
        "executable": "RF.exe",
        "install_notes": "Latin American server with international support. Active chip wars.",
        "native": False,
        "tested": False
    },

    # === Additional TERA Servers ===
    "tera-arborea": {
        "name": "TERA - Arborea Reborn",
        "genre": "Action MMORPG",
        "server": "Arborea Reborn (Private Server)",
        "population": "Medium",
        "description": "Post-shutdown TERA server. Classic action combat preserved.",
        "website": "https://arborea-reborn.com",
        "client_download_url": "https://arborea-reborn.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2015"],
        "executable": "Binaries/TERA.exe",
        "install_notes": "No XIGNCODE3. Classic TERA experience. Good Wine compatibility.",
        "native": False,
        "tested": False
    },

    "tera-novaterra": {
        "name": "TERA - Nova TERA",
        "genre": "Action MMORPG",
        "server": "Nova TERA (Private Server)",
        "population": "Medium-High",
        "description": "Popular TERA private server with custom content.",
        "website": "https://novaterra.eu",
        "client_download_url": "https://novaterra.eu",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2015"],
        "executable": "Binaries/TERA.exe",
        "install_notes": "Custom content and balanced rates. Active community.",
        "native": False,
        "tested": False
    },

    "tera-omni": {
        "name": "TERA - Omni TERA",
        "genre": "Action MMORPG",
        "server": "Omni TERA (Private Server)",
        "population": "Medium",
        "description": "TERA private server with enhanced features.",
        "website": "https://omnitera.com",
        "client_download_url": "https://omnitera.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2015"],
        "executable": "Binaries/TERA.exe",
        "install_notes": "Enhanced features and quality-of-life improvements.",
        "native": False,
        "tested": False
    },

    "tera-starscape": {
        "name": "TERA - Starscape",
        "genre": "Action MMORPG",
        "server": "Starscape (Private Server)",
        "population": "Medium",
        "description": "TERA private server focused on endgame content.",
        "website": "https://starscapetera.com",
        "client_download_url": "https://starscapetera.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2015"],
        "executable": "Binaries/TERA.exe",
        "install_notes": "Endgame-focused with challenging content. No anti-cheat.",
        "native": False,
        "tested": False
    },

    "tera-classic": {
        "name": "TERA - TERA Classic",
        "genre": "Action MMORPG",
        "server": "TERA Classic (Private Server)",
        "population": "Medium-High",
        "description": "Classic TERA experience. Original Island of Dawn and progression.",
        "website": "https://teraclassic.io",
        "client_download_url": "https://teraclassic.io",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2015"],
        "executable": "Binaries/TERA.exe",
        "install_notes": "Classic 2013 experience. Original content and mechanics.",
        "native": False,
        "tested": False
    },

    # === Additional ArcheAge Server ===
    "archeage-classic": {
        "name": "ArcheAge - ArcheAge Classic",
        "genre": "Sandbox MMORPG",
        "server": "ArcheAge Classic (Private Server)",
        "population": "Medium",
        "description": "Classic ArcheAge experience. Pre-Unchained era gameplay.",
        "website": "https://archeageclassic.com",
        "client_download_url": "https://archeageclassic.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging", "d3dx9", "vcrun2015"],
        "executable": "bin64/archeage.exe",
        "install_notes": "Classic pre-Unchained gameplay. Housing, farming, and naval combat.",
        "native": False,
        "tested": False
    },

    # === Additional Star Wars Galaxies Servers ===
    "swg-infinity": {
        "name": "Star Wars Galaxies - Infinity",
        "genre": "Sandbox Sci-Fi MMORPG",
        "server": "SWG Infinity (Private Server)",
        "population": "Medium",
        "description": "SWG private server with custom content and balanced gameplay.",
        "website": "https://swginfinity.com",
        "client_download_url": "https://swginfinity.com",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "dotnet40"],
        "executable": "SWGEmu.exe",
        "install_notes": "Custom content with balanced rates. 32-bit Wine prefix required.",
        "native": False,
        "tested": False
    },

    "swg-beyond": {
        "name": "Star Wars Galaxies - Beyond",
        "genre": "Sandbox Sci-Fi MMORPG",
        "server": "SWG Beyond (Private Server)",
        "population": "Medium",
        "description": "Post-shutdown SWG server with enhanced features.",
        "website": "https://swgbeyond.com",
        "client_download_url": "https://swgbeyond.com",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "dotnet40"],
        "executable": "SWGEmu.exe",
        "install_notes": "Enhanced features and quality-of-life improvements. Lutris compatible.",
        "native": False,
        "tested": False
    },

    "swg-finalizer": {
        "name": "Star Wars Galaxies - Finalizer",
        "genre": "Sandbox Sci-Fi MMORPG",
        "server": "SWG Finalizer (Private Server)",
        "population": "Medium",
        "description": "SWG private server focused on community and player interaction.",
        "website": "https://swgfinalizer.com",
        "client_download_url": "https://swgfinalizer.com",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "dotnet40"],
        "executable": "SWGEmu.exe",
        "install_notes": "Community-focused with regular events. 32-bit prefix with DXVK v1.8.1L.",
        "native": False,
        "tested": False
    },

    "swg-empireinflames": {
        "name": "Star Wars Galaxies - Empire in Flames",
        "genre": "Sandbox Sci-Fi MMORPG",
        "server": "Empire in Flames (Private Server)",
        "population": "Medium-High",
        "description": "Popular SWG server with custom content and active development.",
        "website": "https://empireinflames.com",
        "client_download_url": "https://empireinflames.com",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "dotnet40"],
        "executable": "SWGEmu.exe",
        "install_notes": "Custom content with active development. Good Wine compatibility.",
        "native": False,
        "tested": False
    },

    # === Tibia Private Servers ===
    "tibia-miracle74": {
        "name": "Tibia - Miracle74",
        "genre": "Classic MMORPG",
        "server": "Miracle74 (7.4 OT Server)",
        "population": "Medium",
        "description": "Classic 7.4 Tibia Open Tibia server. Nostalgic gameplay.",
        "website": "https://miracle74.com",
        "client_download_url": "https://miracle74.com",
        "install_type": "manual_download",
        "dependencies": [],
        "executable": "Tibia",
        "install_notes": "Classic 7.4 client. Often has native Linux client or Wine-compatible.",
        "native": True,
        "tested": False
    },

    "tibia-noxious": {
        "name": "Tibia - Noxious OT",
        "genre": "Classic MMORPG",
        "server": "Noxious OT (Custom Server)",
        "population": "Medium",
        "description": "Custom Tibia Open Tibia server with unique features.",
        "website": "https://noxiousot.com",
        "client_download_url": "https://noxiousot.com",
        "install_type": "manual_download",
        "dependencies": [],
        "executable": "Tibia",
        "install_notes": "Custom content and features. Native Linux or Wine compatible.",
        "native": True,
        "tested": False
    },

    "tibia-outcast": {
        "name": "Tibia - Outcast OT",
        "genre": "Classic MMORPG",
        "server": "Outcast OT (Private Server)",
        "population": "Medium",
        "description": "Tibia Open Tibia server with balanced gameplay.",
        "website": "https://outcastot.com",
        "client_download_url": "https://outcastot.com",
        "install_type": "manual_download",
        "dependencies": [],
        "executable": "Tibia",
        "install_notes": "Balanced gameplay with active community. Linux compatible.",
        "native": True,
        "tested": False
    },

    # === Additional WoW Servers ===
    "wow-chromiecraft": {
        "name": "World of Warcraft - ChromieCraft",
        "genre": "Fantasy MMORPG",
        "server": "ChromieCraft (Progressive Vanilla-WotLK)",
        "population": "Very High (1,000+ concurrent)",
        "description": "Progressive 1x server from Vanilla through WotLK. Level-locked content unlocks progressively. Exceptional scripting quality.",
        "website": "https://chromiecraft.com",
        "client_download_url": "https://chromiecraft.com/how-to-connect/",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "Wow.exe",
        "install_notes": "3.3.5a client required. Progressive content unlock. Excellent Wine compatibility.",
        "native": False,
        "tested": True
    },

    "wow-dalaran": {
        "name": "World of Warcraft - Dalaran WoW",
        "genre": "Fantasy MMORPG",
        "server": "Dalaran WoW (WotLK)",
        "population": "High (500-1,000 concurrent)",
        "description": "Long-running WotLK server (2.0x rates). Established since 2010. Progressive PvE content.",
        "website": "https://dalaran-wow.com",
        "client_download_url": "https://www.dalaran-wow.com/forums/downloads/",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "Wow.exe",
        "install_notes": "WotLK 3.3.5a client. 2x rates. Very stable and mature server.",
        "native": False,
        "tested": True
    },

    "wow-sunwell": {
        "name": "World of Warcraft - Sunwell",
        "genre": "Fantasy MMORPG",
        "server": "Sunwell Frosthold (WotLK x2)",
        "population": "Very High (2,000+ concurrent)",
        "description": "High population WotLK x2 server. Excellent scripting and active development.",
        "website": "https://sunwell.pl",
        "client_download_url": "https://sunwell.pl/download",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "Wow.exe",
        "install_notes": "WotLK 3.3.5a client. 2x rates. Very high quality scripting.",
        "native": False,
        "tested": True
    }
}


def get_all_games() -> Dict[str, Dict[str, Any]]:
    """
    Return list of all games.
    
    Returns:
        Dict mapping game IDs to game metadata
    """
    return GAMES_DATABASE


def get_game_by_id(game_id: str) -> Optional[Dict[str, Any]]:
    """
    Get specific game by ID.
    
    Args:
        game_id: Unique identifier for the game
        
    Returns:
        Game metadata dict or None if not found
    """
    return GAMES_DATABASE.get(game_id)


def get_games_by_genre(genre: str) -> Dict[str, Dict[str, Any]]:
    """
    Filter games by genre.
    
    Args:
        genre: Genre name to filter by (case-insensitive partial match)
        
    Returns:
        Dict of games matching the genre
    """
    return {k: v for k, v in GAMES_DATABASE.items() if genre.lower() in v['genre'].lower()}


def get_native_games() -> Dict[str, Dict[str, Any]]:
    """
    Get only native Linux games.
    
    Returns:
        Dict of games with native Linux support
    """
    return {k: v for k, v in GAMES_DATABASE.items() if v['native']}


def get_tested_games() -> Dict[str, Dict[str, Any]]:
    """
    Get only tested/working games.
    
    Returns:
        Dict of games that have been tested and verified
    """
    return {k: v for k, v in GAMES_DATABASE.items() if v['tested']}
