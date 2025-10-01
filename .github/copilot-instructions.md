# Copilot Instructions for linuxMMORPG-App

## Project Overview
This is a professional MMO game launcher for Arch Linux with a PyQt6 GUI. The launcher helps users manage, install, and launch various MMORPGs on Linux using compatibility tools.

**Key Technologies:**
- **GUI:** PyQt6 (Python Qt bindings)
- **Game Runtime:** `umu-run` from `faugus/umu` (Universal Mod Utility)
- **Packaging:** PKGBUILD for Arch Linux
- **Language:** Python 3.x

**Main Components:**
- `gui.py` - PyQt6 GUI with split-view library explorer and detailed game panels
- `launcher.py` - Game launch logic with error handling
- `games_db.py` - Comprehensive game metadata database (30+ MMORPGs)
- `game_installer.py` - Game installation logic (Flatpak, DEB, AUR, manual)
- `installer.py` - System-level dependency installer
- `config.yaml` - User-specific game configuration
- `preview_gui.py` - UI screenshot generator for documentation

## Directory Structure
```
linuxMMORPG-App/
├── .github/
│   └── copilot-instructions.md    # This file
├── assets/
│   └── previews/                  # UI screenshots
├── logs/                          # Runtime logs (gitignored)
│   ├── launcher.log
│   └── installer.log
├── gui.py                         # Main GUI application
├── launcher.py                    # Launch logic
├── game_installer.py              # Installation logic
├── games_db.py                    # Game metadata
├── installer.py                   # System installer
├── config.yaml                    # User config (example)
├── preview_gui.py                 # Screenshot tool
├── PKGBUILD                       # Arch package definition
└── README.md
```

## Architecture & Data Flow

**Game Data Sources:**
1. `games_db.py` contains static metadata for 30+ MMORPGs (name, genre, server, install type, dependencies)
2. `config.yaml` contains user-specific paths and configurations
3. Installed games tracked in `~/.config/mmo-launcher/installed_games.json`

**Application Flow:**
1. User launches `mmo-launcher` (entry point → `gui.py`)
2. GUI loads game list from `games_db.py` and user config
3. User selects a game → details displayed in right panel (3 tabs: Overview, Installation, Activity)
4. User actions (Install/Launch/Uninstall) → delegated to `game_installer.py`
5. Game launch uses `umu-run <executable>` via subprocess
6. All operations logged to `logs/launcher.log` and `logs/installer.log`

**Threading Model:**
- GUI runs on main thread
- Game installation runs in background thread (`InstallThread` class)
- Progress updates via Qt signals/slots

## Developer Workflows

### Quick Start
```bash
# Clone repository
git clone https://github.com/Hansuqwer/linuxMMORPG-App.git
cd linuxMMORPG-App

# Run directly (for development)
python gui.py

# Or run via launcher module
python launcher.py
```

### Build & Install
```bash
# Build and install system-wide (Arch Linux)
makepkg -si

# Run installed version
mmo-launcher
```

### Development & Testing
```bash
# Generate UI previews
python preview_gui.py

# Check logs
tail -f logs/launcher.log
tail -f logs/installer.log

# Test with specific game
python -c "from launcher import launch_game; launch_game('World of Warcraft - Warmane')"
```

### Common Workflows
- **Add new game:** Update `games_db.py` with game metadata (see existing entries for structure)
- **Modify UI:** Edit `gui.py` → run `python gui.py` to test → regenerate previews with `preview_gui.py`
- **Debug install issues:** Check `logs/installer.log` for detailed error traces
- **Update dependencies:** Modify `dependencies` list in game metadata (handles AUR, Flatpak, system packages)

## Patterns & Conventions

### Code Style
- **Python:** Follow PEP 8 conventions
- **Imports:** Group by standard library, third-party, local (separated by blank lines)
- **Docstrings:** Use triple-quoted strings for functions/classes
- **Comments:** Minimal inline comments; prefer self-documenting code
- **Constants:** UPPER_CASE at module level
- **Class names:** PascalCase (e.g., `GameDetailPanel`, `InstallThread`)
- **Function names:** snake_case (e.g., `load_config`, `launch_game`)

### Logging
- Use Python's `logging` module (never print statements for errors)
- Format: `"%(asctime)s - %(levelname)s - %(message)s"`
- Levels: INFO for operations, ERROR for failures, WARNING for recoverable issues
- All logs go to `logs/launcher.log` or `logs/installer.log`

### Error Handling
- Always use try-except blocks for external operations (subprocess, file I/O, network)
- Log errors with context: `logging.error(f"Failed to X because Y: {error}")`
- Return False from functions on failure (not exceptions in user-facing code)
- Show user-friendly error dialogs via `QMessageBox` in GUI

### Game Metadata Structure
Each game in `games_db.py` has these fields:
- `name`: Display name
- `genre`: Game category
- `server`: Official/Private server info
- `population`: Player count estimate
- `description`: Brief description
- `website`: Official URL
- `client_download_url`: Where to download (URL, steam://, flatpak://)
- `install_type`: `native`, `steam`, `flatpak`, `aur`, `manual_download`
- `dependencies`: List of required packages
- `executable`: Main executable path (relative to install dir)
- `install_notes`: Important setup instructions
- `native`: Boolean (true for native Linux games)
- `tested`: Boolean (true if verified working)

### Threading & Async
- Never block the GUI thread with long operations
- Use `QThread` for background tasks (installation, downloads)
- Emit Qt signals for progress updates
- Use `pyqtSignal` for cross-thread communication

### External Tool Integration
- **umu-run:** Check availability with `shutil.which()` before use
- **Package managers:** Detect available tools (yay, paru, flatpak) at runtime
- **Terminal emulators:** Support multiple (konsole, gnome-terminal, etc.)
- Always check tool availability and provide user-friendly error messages

## Integration Points

### External Dependencies
- **Required:** `python-pyqt6`, `faugus/umu` (or `umu-run`)
- **Optional:** `yay`/`paru` (AUR helpers), `flatpak`, `steam`, `wine`, `wine-staging`
- Game-specific: Listed in each game's `dependencies` field

### File System
- **User config:** `~/.config/mmo-launcher/`
- **Installed games:** `~/Games/` (default, configurable)
- **Logs:** `./logs/` (relative to launch directory)
- **Assets:** `./assets/previews/` (UI screenshots)

### External Tools
- **umu-run:** Game runner (handles Wine, Proton, native)
- **Flatpak:** For games like XIVLauncher
- **Steam:** For Steam games (steam:// URLs)
- **AUR helpers:** For AUR packages (xivlauncher, etc.)
- **Wine/Proton:** Managed by umu-run

## Troubleshooting

### Common Issues

**"UMU launcher not found"**
- Install umu: `yay -S umu` or `paru -S umu`
- Check PATH includes umu location
- Verify with: `which umu-run`

**Game won't launch**
- Check `logs/launcher.log` for error details
- Verify game path in config.yaml is correct
- Ensure game dependencies installed (check game's `dependencies` field)
- Test umu directly: `umu-run /path/to/game.exe`

**Installation fails**
- Check `logs/installer.log` for detailed trace
- For Flatpak: Ensure flatpak runtime installed
- For AUR: Ensure AUR helper (yay/paru) installed
- For manual downloads: Check network connectivity

**GUI doesn't start**
- Verify PyQt6 installed: `python -c "import PyQt6"`
- Check Python version: `python --version` (need 3.x)
- Run with debug: `python gui.py 2>&1 | tee debug.log`

### Debug Mode
```bash
# Enable verbose logging (edit gui.py temporarily)
logging.basicConfig(level=logging.DEBUG)

# Run with stdout/stderr capture
python gui.py 2>&1 | tee debug.log
```

## Examples & Common Tasks

### Add a New Game
1. Edit `games_db.py`:
```python
"my_game": {
    "name": "My Game Title",
    "genre": "MMORPG",
    "server": "Official",
    "population": "High",
    "description": "Brief description",
    "website": "https://example.com",
    "client_download_url": "https://example.com/download",
    "install_type": "manual_download",
    "dependencies": ["umu-launcher", "wine"],
    "executable": "game.exe",
    "install_notes": "Setup instructions here",
    "native": False,
    "tested": True
}
```
2. Restart launcher to see new game

### Modify UI Theme/Colors
Status badge colors defined in `gui.py`:
```python
STATUS_NOT_INSTALLED = ("#39435a", "#f5f8ff")
STATUS_INSTALLED = ("#43a047", "#f5f8ff")
STATUS_MANUAL_REQUIRED = ("#f9a825", "#1b1e27")
```

### Test Installation Flow
```python
from game_installer import GameInstaller
from games_db import get_game_by_id

installer = GameInstaller()
game_data = get_game_by_id("tibia")  # Use any game ID
success = installer.install_game("tibia", game_data)
```

### Generate UI Screenshots
```bash
python preview_gui.py
# Output: assets/previews/*.png
```

---

## Quick Reference
- **Logs:** `logs/launcher.log`, `logs/installer.log`
- **User config:** `~/.config/mmo-launcher/installed_games.json`
- **Game database:** `games_db.py` (30+ games)
- **Entry point:** `gui.py` or `mmo-launcher` command
- **Package:** PKGBUILD for Arch Linux

For questions about project-specific patterns, refer to the sections above or ask for clarification.
