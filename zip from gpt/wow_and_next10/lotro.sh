#!/usr/bin/env bash
set -euo pipefail
# Lord of the Rings Online via UMU

PREFIX="$HOME/Games/umu/lotro/default"
EXE="$HOME/Games/LOTRO/lotrolive.exe"  # or lotroclient64.exe depending on install
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
echo "[*] Launching Lord of the Rings Online…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
