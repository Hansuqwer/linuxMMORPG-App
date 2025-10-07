#!/usr/bin/env bash
set -euo pipefail
# TERA (private) via UMU — official service ended; private launchers vary

PREFIX="$HOME/Games/umu/tera/default"
EXE="$HOME/Games/TERA/Tera-Launcher.exe"  # or Client/Tera.exe depending on server
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
echo "[*] Launching TERA…"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$EXE"
