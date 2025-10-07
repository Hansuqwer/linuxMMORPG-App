#!/usr/bin/env bash
set -euo pipefail
# UMU launcher for Archeage - Archeage Classic
# NOTE: Provide your own game files/client. Update EXE path below.

PREFIX="$HOME/Games/umu/archeage/archeage_classic"
EXE="$HOME/Games/ArcheAge/ArcheAgeClassic/Launcher.exe"
WINETRICKS="d3dx9 vcrun2010 vcrun2015 corefonts"

mkdir -p "$PREFIX"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "" || true
if [[ -n "$WINETRICKS" ]]; then
  WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run winetricks -q $WINETRICKS || true
fi
if [[ ! -f "$EXE" ]]; then
  echo "[!] Missing executable: $EXE"
  echo "    Edit this script and set EXE to your installed client/launcher."
  exit 1
fi
echo "[*] Launching Archeage Classic…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
