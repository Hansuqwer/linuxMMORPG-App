#!/usr/bin/env bash
set -euo pipefail
# Star Wars: The Old Republic via UMU (standalone launcher)

PREFIX="$HOME/Games/umu/swtor/default"
EXE="$HOME/Games/SWTOR/Launcher.exe"   # if using Steam, point to swtor.exe inside steamapps
WINETRICKS="vcrun2010 vcrun2015 corefonts"

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
echo "[*] Launching Star Wars: The Old Republic…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
