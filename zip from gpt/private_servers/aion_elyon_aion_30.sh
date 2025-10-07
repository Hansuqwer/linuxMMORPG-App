#!/usr/bin/env bash
set -euo pipefail
# UMU launcher for Aion - Elyon Aion 30
# NOTE: Provide your own game files/client. Update EXE path below.

PREFIX="$HOME/Games/umu/aion/elyon_aion_30"
EXE="$HOME/Games/Aion/ElyonAion3.0/Launcher.exe"
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
echo "[*] Launching Elyon Aion 30…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
