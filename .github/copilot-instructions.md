# Copilot Instructions for linuxMMORPG-App

## Project Overview
- This is a professional MMO game launcher for Arch Linux, with a PyQt6 GUI.
- Main files: `gui.py` (UI), `launcher.py` (launch logic), `games_db.py` (game metadata), `game_installer.py` (game install logic), `installer.py` (system integration).
- Game list and config are managed via `config.yaml`.
- Logging is handled in `logs/launcher.log`.
- Packaged for repo-style installation using `PKGBUILD`.

## Architecture & Data Flow
- The launcher reads game data from `config.yaml` and/or `games_db.py`.
- User interacts via the PyQt6 GUI (`gui.py`), which triggers launch/install actions.
- Game launching uses the external tool `umu-run` from `faugus/umu` (see error handling for missing binaries).
- Errors and events are logged to `logs/launcher.log`.
- Installer logic (`installer.py`, `game_installer.py`) handles Flatpak, DEB, and other package types.

## Developer Workflows
- **Build:** Use `makepkg -si` for repo-style install (see README).
- **Run:** Use `mmo-launcher` after install, or run `python launcher.py` for direct execution.
- **Debug:** Check `logs/launcher.log` for error traces. Common issues include missing binaries (e.g., `umu`) and failed package installs (see log for Flatpak/DEB errors).
- **Config:** Edit `config.yaml` to add/remove games or change settings.

## Patterns & Conventions
- All user-facing actions are triggered from the GUI (`gui.py`).
- Game metadata is centralized in `games_db.py` and/or `config.yaml`.
- External dependencies (e.g., `umu`, Flatpak, DEB) are invoked via subprocess and errors are logged.
- Logging uses Python's logging module, outputting to `logs/launcher.log`.
- Error messages are user-friendly and localized (see log for Swedish error strings).
- Packaging uses PKGBUILD for Arch Linux compatibility.

## Integration Points
- **External tools:** `umu-run` from `faugus/umu` (game runner), Flatpak, DEB package manager.
- **Assets:** Located in `assets/`.
- **Logs:** All runtime errors/events in `logs/launcher.log`.

## Examples
- To add a new game, update `config.yaml` and ensure metadata in `games_db.py`.
- To debug a launch failure, check for missing binaries and review `logs/launcher.log` for error details.
- To package for distribution, use `PKGBUILD` and follow Arch Linux repo conventions.

---
For questions about project-specific patterns, see the referenced files above or ask for clarification on any unclear workflow.
