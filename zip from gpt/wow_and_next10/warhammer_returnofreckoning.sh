#!/usr/bin/env bash
set -euo pipefail
# Warhammer Online: Return of Reckoning via UMU

PREFIX="$HOME/Games/umu/warhammer/ror"
EXE="$HOME/Games/WarhammerOnline/ReturnOfReckoning.exe" # or RoRLauncher.exe
WINETRICKS="d3dx9 vcrun2008 vcrun2010 corefonts"

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
echo "[*] Launching Warhammer Online: Return of Reckoning…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
