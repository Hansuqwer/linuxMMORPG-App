#!/usr/bin/env bash
set -euo pipefail
# ArcheAge (private) via UMU

PREFIX="$HOME/Games/umu/archeage/default"
EXE="$HOME/Games/ArcheAge/ArcheAgeLauncher.exe"  # or AA.bin from custom packs
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
echo "[*] Launching ArcheAge…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
