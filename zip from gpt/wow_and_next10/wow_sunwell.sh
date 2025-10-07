#!/usr/bin/env bash
set -euo pipefail
# WoW Sunwell (WotLK) via UMU

PREFIX="$HOME/Games/umu/wow/sunwell"
EXE="$HOME/Games/WoW/Sunwell/Wow.exe"
WINETRICKS="d3dx9 vcrun2008 corefonts"

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
echo "[*] Launching Sunwell…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
