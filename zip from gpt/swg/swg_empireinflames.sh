#!/usr/bin/env bash
set -euo pipefail
# Star Wars Galaxies Empire in Flames via UMU
# NOTE: Provide your own game files/client. Update EXE path below.

PREFIX="$HOME/Games/umu/swg/empireinflames"
EXE="$HOME/Games/SWG/EmpireInFlames/SwgClient_r.exe"
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
echo "[*] Launching SWG Empire in Flames…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
