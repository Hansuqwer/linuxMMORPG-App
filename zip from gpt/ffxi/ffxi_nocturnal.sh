#!/usr/bin/env bash
set -euo pipefail
# FFXI Nocturnal Souls via UMU
# NOTE: Provide your own game files/client. Update EXE path below.

PREFIX="$HOME/Games/umu/ffxi/nocturnal"
EXE="$HOME/Games/FFXI/NocturnalSouls/pol.exe"
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
echo "[*] Launching FFXI Nocturnal Souls…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
