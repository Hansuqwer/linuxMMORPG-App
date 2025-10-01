# Copilot Instructions for linuxMMORPG-App

## Project Overview
- This is a professional MMO game launcher for Arch Linux, with a PyQt6 GUI.
- Main files: `gui.py` (UI), `launcher.py` (launch logic), `games_db.py` (game metadata), `game_installer.py` (game install logic), `installer.py` (system integration), `preview_gui.py` (UI preview generator).
- Game list and config are managed via `config.yaml`.
- Logging is handled in `logs/launcher.log` and `logs/installer.log`.
- Packaged for repo-style installation using `PKGBUILD`.

## Architecture & Data Flow
- The launcher reads game data from `config.yaml` and/or `games_db.py`.
- User interacts via the PyQt6 GUI (`gui.py`), which triggers launch/install actions.
- Game launching uses the external tool `umu-run` from `faugus/umu` (see error handling for missing binaries).
- Errors and events are logged to `logs/launcher.log` and `logs/installer.log`.
- Installer logic (`installer.py`, `game_installer.py`) handles Flatpak, AUR, DEB, Steam, and manual download types.
- Game installation state is tracked in `~/.config/mmo-launcher/installed_games.json`.

## Dependencies & Prerequisites
- **Required Python packages:** PyQt6, PyYAML (standard library: subprocess, logging, json, pathlib, urllib)
- **System tools:** 
  - `umu-run` or `umu` (from faugus/umu) - for running Windows games
  - AUR helpers (optional): `yay`, `paru`, `pikaur`, or `trizen` - for AUR package installation
  - `wine`, `wine-staging` - Windows compatibility layer
  - `steam` - for Steam-based games
  - `flatpak` - for Flatpak-based games
- **Install on Arch Linux:** `makepkg -si` in project root
- **Run directly (development):** `python gui.py` or `python launcher.py`

## Developer Workflows
- **Build:** Use `makepkg -si` for repo-style install (see README).
- **Run:** Use `mmo-launcher` after install, or run `python gui.py` for direct execution.
- **Debug:** Check `logs/launcher.log` and `logs/installer.log` for error traces. Common issues include missing binaries (e.g., `umu`) and failed package installs (see log for Flatpak/DEB errors).
- **Config:** Edit `config.yaml` to add/remove games or change settings.
- **Preview UI:** Run `python preview_gui.py` to generate UI screenshots in `assets/previews/`.

## Code Style & Conventions
- **Python Style:** Follow PEP 8 conventions. Use descriptive variable names and docstrings for classes and complex functions.
- **Imports:** Standard library first, then third-party (PyQt6, yaml), then local imports.
- **Error Handling:** All subprocess calls and file operations should have try-except blocks with logging.
- **Logging:** Use `logging.info()` for normal operations, `logging.error()` for errors, `logging.warning()` for warnings.
- **UI Components:** PyQt6 widgets follow camelCase for methods (Qt convention) and snake_case for custom methods.
- **Constants:** Define at module level in UPPER_CASE (e.g., `DEFAULT_GAMES_DIR`, `LOG_FILE`).

## Patterns & Conventions
- All user-facing actions are triggered from the GUI (`gui.py`).
- Game metadata is centralized in `games_db.py` and/or `config.yaml`.
- External dependencies (e.g., `umu`, Flatpak, DEB) are invoked via subprocess and errors are logged.
- Logging uses Python's logging module, outputting to `logs/launcher.log` and `logs/installer.log`.
- Error messages are user-friendly and localized (see log for Swedish error strings).
- Packaging uses PKGBUILD for Arch Linux compatibility.
- Background operations (installation, downloads) use QThread to avoid blocking the UI.

## Integration Points
- **External tools:** `umu-run` from `faugus/umu` (game runner), Flatpak, DEB package manager, AUR helpers.
- **Assets:** Located in `assets/` (UI previews in `assets/previews/`).
- **Logs:** Runtime errors/events in `logs/launcher.log` and `logs/installer.log`.
- **Config:** User configuration in `~/.config/mmo-launcher/` (installed games list).
- **Game installs:** Default location `~/Games/` (configurable in `game_installer.py`).

## Testing Strategy
- **No automated tests currently exist** - changes should be manually tested.
- **Manual testing checklist:**
  - Launch GUI: `python gui.py` should open without errors
  - Game list loads: Check that games from `games_db.py` appear in the library
  - Game details: Select a game and verify all metadata displays correctly
  - UI previews: Run `python preview_gui.py` to ensure screenshots are generated
  - Logging: Check `logs/` directory for proper log file creation
- **Common issues to test:**
  - Missing `umu-run` binary (should show appropriate error)
  - Invalid game paths in `config.yaml` (should handle gracefully)
  - Installation failures (check installer logs for proper error handling)

## Common Pitfalls & Troubleshooting
- **Missing umu binary:** Game launch fails if `umu-run` or `umu` not in PATH. Check with `which umu-run`.
- **PyQt6 display issues:** Set `QT_QPA_PLATFORM=offscreen` for headless environments (used in `preview_gui.py`).
- **Log directory permissions:** `logs/` directory must be writable. Created automatically but may fail in restricted environments.
- **Config file location:** `config.yaml` must be in the project root for direct execution.
- **Game database structure:** Each game in `games_db.py` requires: name, genre, server, population, description, website, client_download_url, install_type, dependencies, executable, install_notes, native, tested.

## Examples
- To add a new game, update `config.yaml` and ensure metadata in `games_db.py`.
- To debug a launch failure, check for missing binaries and review `logs/launcher.log` for error details.
- To package for distribution, use `PKGBUILD` and follow Arch Linux repo conventions.
- To add a new install type, extend the `install_game()` method in `game_installer.py` and add corresponding UI handling in `gui.py`.

---
For questions about project-specific patterns, see the referenced files above or ask for clarification on any unclear workflow.
