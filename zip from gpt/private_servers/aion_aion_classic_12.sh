#!/usr/bin/env bash
set -euo pipefail
# UMU launcher for Aion - Aion Classic 12
# NOTE: Provide your own game files/client. Update EXE path below.

PREFIX="$HOME/Games/umu/aion/aion_classic_12"
EXE="$HOME/Games/Aion/AionClassic1.2/Launcher.exe"
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
echo "[*] Launching Aion Classic 12…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
