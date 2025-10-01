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

    "everquest-p1999-green": {
        "name": "EverQuest - Project 1999 Green",
        "genre": "Classic MMORPG",
        "server": "Project 1999 Green (Velious-locked)",
        "population": "Very High (1,000+ concurrent at peak)",
        "description": "Most popular P99 server. Classic 1999-2001 era, locked at Velious expansion. Officially licensed by Daybreak.",
        "website": "https://project1999.com",
        "client_download_url": "https://archive.org/details/EverQuestTitanium",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts"],
        "executable": "eqgame.exe",
        "install_notes": "Titanium client from Internet Archive. Apply P99 patches. Use p99-login-middlemand for Linux. Install to C:\\Everquest (not Program Files). Windowed Mode required, disable Vertex Shaders. Official Linux guide: wiki.project1999.com/EverQuest_in_Linux_Guide",
        "native": False,
        "tested": True
    },

    "everquest-p1999-blue": {
        "name": "EverQuest - Project 1999 Blue",
        "genre": "Classic MMORPG",
        "server": "Project 1999 Blue (Full Classic)",
        "population": "Medium (second most popular P99 server)",
        "description": "Full classic progression through Velious. Established server with mature economy.",
        "website": "https://project1999.com",
        "client_download_url": "https://archive.org/details/EverQuestTitanium",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts"],
        "executable": "eqgame.exe",
        "install_notes": "Same installation as Green server. Titanium client + P99 patches. Use p99-login-middlemand for server list fix. Long load times (5-20 min) normal.",
        "native": False,
        "tested": True
    },

    "everquest-p1999-red": {
        "name": "EverQuest - Project 1999 Red",
        "genre": "Classic MMORPG",
        "server": "Project 1999 Red (PvP)",
        "population": "Low (~50 concurrent average)",
        "description": "PvP-focused classic EverQuest server. Teams, FFA PvP zones, classic ruleset.",
        "website": "https://project1999.com",
        "client_download_url": "https://archive.org/details/EverQuestTitanium",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts"],
        "executable": "eqgame.exe",
        "install_notes": "Same installation as other P99 servers. Titanium client required. Smaller but dedicated PvP community.",
        "native": False,
        "tested": True
    },

    "everquest-quarm": {
        "name": "EverQuest - Project Quarm",
        "genre": "Classic MMORPG",
        "server": "Project Quarm (Time-locked Progression)",
        "population": "High (active, exact numbers undisclosed)",
        "description": "Time-locked progression server stopping at Planes of Power. Classic 1x rates.",
        "website": "https://projectquarm.com",
        "client_download_url": "https://quarm.guide/installing-the-game",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine", "d3dx9_43", "corefonts"],
        "executable": "eqgame.exe",
        "install_notes": "Download TAKP v2.2 client + Quarm files from Discord #server-files. Install to root drive (not Program Files). Uses Titanium client - same Wine setup as P99.",
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
        "client_download_url": "https://uaro.net/",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine"],
        "executable": "Uaro.exe",
        "install_notes": "Works on Linux via Wine/Proton. No anti-cheat blocking. Download client and patch from website.",
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
        "client_download_url": "https://forums.homecomingservers.com/files/file/16-coh-client-installer/",
        "install_type": "auto_installer",
        "dependencies": ["umu-launcher", "wine", "dotnet35", "dinput8"],
        "executable": "cityofheroes.exe",
        "install_notes": "Homecoming Launcher supports Wine. Install dotnet35 and dinput8 via winetricks. Works with win32/win64 prefixes. Often better performance than Windows.",
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
        "client_download_url": "https://evolvedpw.com",
        "install_type": "manual_download",
        "dependencies": ["umu-launcher", "wine-staging"],
        "executable": "elementclient.exe",
        "install_notes": "Lutris installer available. Recent updates transitioned from 32-bit to 64-bit executables.",
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
