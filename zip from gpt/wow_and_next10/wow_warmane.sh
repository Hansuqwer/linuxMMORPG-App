#!/usr/bin/env bash
set -euo pipefail
# WoW Warmane (WotLK/Cata/MoP) via UMU

PREFIX="$HOME/Games/umu/wow/warmane"
EXE="$HOME/Games/WoW/Warmane/Wow.exe"   # <- update to your client path/exe (3.3.5a etc.)
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
echo "[*] Launching Warmane…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
