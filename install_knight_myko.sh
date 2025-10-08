#!/usr/bin/env bash
set -euo pipefail

# Knight Online MyKO Installation Helper Script
# This script installs Knight Online from the downloaded client

echo "=========================================="
echo "Knight Online MyKO Installation Helper"
echo "=========================================="
echo ""

# Configuration
GAME_DIR="$HOME/Games/knight-myko"
PREFIX="$HOME/Games/umu/knight-myko/default"

# Common client filenames (case-insensitive match will be handled later)
declare -a KNOWN_CLIENT_FILES=(
    "Client_KOMYKO.zip"
    "client_myko.zip"
    "Client_Myko.zip"
    "Client_KOMYKO.exe"
    "client_myko.exe"
    "Client_KOMYKO.rar"
    "Client_KOMYKO.7z"
)

# Resolve default download location if the expected file exists
DOWNLOAD_FILE=""
USER_OVERRIDE=""
if [ $# -gt 0 ]; then
    # Remove surrounding quotes and expand ~
    ARG_PATH="${1%\"}"
    ARG_PATH="${ARG_PATH#\"}"
    ARG_PATH="${ARG_PATH%\'}"
    ARG_PATH="${ARG_PATH#\'}"
    ARG_PATH="${ARG_PATH/#\~/$HOME}"

    if [ -f "$ARG_PATH" ]; then
        USER_OVERRIDE="$ARG_PATH"
        echo "Using file provided as argument: $ARG_PATH"
    elif [ $# -gt 1 ]; then
        ARG_PATH="${2%\"}"
        ARG_PATH="${ARG_PATH#\"}"
        ARG_PATH="${ARG_PATH%\'}"
        ARG_PATH="${ARG_PATH#\'}"
        ARG_PATH="${ARG_PATH/#\~/$HOME}"
        if [ -f "$ARG_PATH" ]; then
            USER_OVERRIDE="$ARG_PATH"
            echo "Using file provided as argument: $ARG_PATH"
        fi
    fi
fi

for candidate in "${KNOWN_CLIENT_FILES[@]}"; do
    if [ -z "$DOWNLOAD_FILE" ] && [ -f "$HOME/Hämtningar/$candidate" ]; then
        DOWNLOAD_FILE="$HOME/Hämtningar/$candidate"
    elif [ -z "$DOWNLOAD_FILE" ] && [ -f "$HOME/Downloads/$candidate" ]; then
        DOWNLOAD_FILE="$HOME/Downloads/$candidate"
    fi
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if umu-run is available
if ! command -v umu-run &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} umu-run not found. Please install umu-launcher first."
    echo "Install with: yay -S umu-launcher"
    exit 1
fi

# Create game directory
echo -e "${GREEN}[1/4]${NC} Creating game directory..."
mkdir -p "$GAME_DIR"
mkdir -p "$PREFIX"

# Check for downloaded client
echo -e "${GREEN}[2/4]${NC} Looking for Knight Online client..."
echo ""

# Search for Knight Online related files in Downloads folder
FOUND_FILE=""

# Allow user-provided override file
if [ -n "$USER_OVERRIDE" ]; then
    FOUND_FILE="$USER_OVERRIDE"
fi

# First check the specific default location
if [ -z "$FOUND_FILE" ] && [ -n "$DOWNLOAD_FILE" ] && [ -f "$DOWNLOAD_FILE" ]; then
    FOUND_FILE="$DOWNLOAD_FILE"
else
    # Search in Downloads folder for any Knight Online related files
    echo "Searching for Knight Online files in Downloads folder..."

    # Priority 1: Look for KOMYKO/MyKO specific files first
    if [ -z "$FOUND_FILE" ]; then
        for dir in "$HOME/Hämtningar" "$HOME/Downloads"; do
            [ ! -d "$dir" ] && continue
            FOUND_FILE=$(find "$dir" -maxdepth 1 -type f \( -iname "*myko*.zip" -o -iname "*myko*.exe" -o -iname "*myko*.rar" -o -iname "*myko*.7z" \) 2>/dev/null | head -1)
            [ -n "$FOUND_FILE" ] && break
        done
    fi

    # Priority 2: Look for generic Knight Online files (but exclude other games)
    if [ -z "$FOUND_FILE" ]; then
        for dir in "$HOME/Hämtningar" "$HOME/Downloads"; do
            [ ! -d "$dir" ] && continue
            while IFS= read -r -d '' file; do
                basename_lower=$(basename "$file" | tr '[:upper:]' '[:lower:]')
                # Exclude Silkroad and other games explicitly
                if [[ ! "$basename_lower" =~ (silkroad|origin|genesis|seal|legend|zenger|phoenix) ]]; then
                    FOUND_FILE="$file"
                    break 2
                fi
            done < <(find "$dir" -maxdepth 1 -type f \( -iname "*knight*.zip" -o -iname "*knight*.exe" -o -iname "*knight*.rar" -o -iname "*knight*.7z" \) -print0 2>/dev/null)
        done
    fi

    # Priority 3: Look for Client_KO files
    if [ -z "$FOUND_FILE" ]; then
        for dir in "$HOME/Hämtningar" "$HOME/Downloads"; do
            [ ! -d "$dir" ] && continue
            FOUND_FILE=$(find "$dir" -maxdepth 1 -type f \( -iname "client_ko*.zip" -o -iname "client_ko*.exe" -o -iname "client_ko*.rar" -o -iname "client_ko*.7z" \) 2>/dev/null | head -1)
            [ -n "$FOUND_FILE" ] && break
        done
    fi
fi

if [ -z "$FOUND_FILE" ]; then
    echo -e "${RED}[ERROR]${NC} No Knight Online client found in Downloads folder"
    echo ""
    echo "Please download the client from https://ko-myko.com/downloads"
    echo "and save it to your Downloads folder (Hämtningar)"
    echo ""
    echo "Looking for files matching: knight, myko, KO, Client_KOMYKO"
    exit 1
fi

echo -e "${GREEN}✓${NC} Found client: $(basename "$FOUND_FILE")"
echo "  Location: $FOUND_FILE"
echo "  Size: $(du -h "$FOUND_FILE" | cut -f1)"
echo ""
echo "Use this file? (Y/n)"
read -r CONFIRM
if [[ "$CONFIRM" =~ ^[Nn]$ ]]; then
    echo "Please enter the full path to the correct installer:"
    read -r USER_PATH
    # Remove surrounding quotes if present
    USER_PATH="${USER_PATH%\"}"
    USER_PATH="${USER_PATH#\"}"
    USER_PATH="${USER_PATH%\'}"
    USER_PATH="${USER_PATH#\'}"
    # Expand ~ to home directory
    USER_PATH="${USER_PATH/#\~/$HOME}"

    if [ -f "$USER_PATH" ]; then
        FOUND_FILE="$USER_PATH"
        echo -e "${GREEN}✓${NC} Using: $USER_PATH"
    else
        echo -e "${RED}[ERROR]${NC} File not found: $USER_PATH"
        exit 1
    fi
fi

# Extract archive if it's a ZIP/RAR/7z
echo -e "${GREEN}[3/4]${NC} Processing client file..."
if [[ "$FOUND_FILE" == *.zip ]]; then
    if [ -f "$GAME_DIR/Client_KOMYKO.exe" ] || [ -f "$GAME_DIR/KnightOnLine.exe" ]; then
        echo -e "${YELLOW}Note:${NC} Client already extracted, skipping extraction..."
    else
        echo "Extracting ZIP archive..."
        unzip -o -q "$FOUND_FILE" -d "$GAME_DIR"
        echo -e "${GREEN}✓${NC} Client extracted to: $GAME_DIR"
    fi
elif [[ "$FOUND_FILE" == *.rar || "$FOUND_FILE" == *.RAR ]]; then
    if [ -f "$GAME_DIR/Client_KOMYKO.exe" ] || [ -f "$GAME_DIR/KnightOnLine.exe" ]; then
        echo -e "${YELLOW}Note:${NC} Client already extracted, skipping extraction..."
    else
        if command -v unrar &> /dev/null; then
            echo "Extracting RAR archive..."
            unrar x "$FOUND_FILE" "$GAME_DIR/"
            echo -e "${GREEN}✓${NC} Client extracted to: $GAME_DIR"
        else
            echo -e "${RED}[ERROR]${NC} unrar not found. Install with: sudo pacman -S unrar"
            exit 1
        fi
    fi
elif [[ "$FOUND_FILE" == *.7z ]]; then
    if [ -f "$GAME_DIR/Client_KOMYKO.exe" ] || [ -f "$GAME_DIR/KnightOnLine.exe" ]; then
        echo -e "${YELLOW}Note:${NC} Client already extracted, skipping extraction..."
    else
        if command -v 7z &> /dev/null; then
            echo "Extracting 7z archive..."
            7z x "$FOUND_FILE" -o"$GAME_DIR"
            echo -e "${GREEN}✓${NC} Client extracted to: $GAME_DIR"
        else
            echo -e "${RED}[ERROR]${NC} 7z not found. Install with: sudo pacman -S p7zip"
            exit 1
        fi
    fi
elif [[ "$FOUND_FILE" == *.exe ]]; then
    # If it's an EXE, copy it to game directory if not already there
    if [[ "$FOUND_FILE" != "$GAME_DIR"* ]]; then
        echo "Copying installer to game directory..."
        cp "$FOUND_FILE" "$GAME_DIR/"
        echo -e "${GREEN}✓${NC} Installer copied to: $GAME_DIR"
    else
        echo -e "${GREEN}✓${NC} Installer already in game directory"
    fi
fi

# Look for the game executable
echo -e "${GREEN}[4/4]${NC} Looking for game executable..."

# Check if game is already installed (Client_KOMYKO.exe is the actual launcher for MyKO)
GAME_EXE=$(find "$GAME_DIR" -maxdepth 3 -type f \( -iname "KnightOnLine.exe" -o -iname "Client_KOMYKO.exe" \) 2>/dev/null | head -1)

if [ -n "$GAME_EXE" ]; then
    echo -e "${GREEN}✓${NC} Game already installed!"
    echo "  Executable: $GAME_EXE"
    echo ""

    # Register with launcher database
    if command -v python3 &> /dev/null; then
        echo "Registering installation with Linux MMORPG Launcher..."
        GAME_DIR_PATH="$GAME_DIR" CLIENT_PATH="$GAME_EXE" PREFIX_PATH="$PREFIX" python3 - <<'PY'
import json
import os
from datetime import datetime
from pathlib import Path

game_dir = Path(os.environ.get("GAME_DIR_PATH", ""))
client_exe = os.environ.get("CLIENT_PATH", "")
prefix_path = os.environ.get("PREFIX_PATH", "")

config_dir = Path.home() / ".config" / "mmo-launcher"
config_dir.mkdir(parents=True, exist_ok=True)
installed_file = config_dir / "installed_games.json"

try:
    if installed_file.exists():
        data = json.loads(installed_file.read_text(encoding="utf-8"))
    else:
        data = {}
except Exception:
    data = {}

data["knight-myko"] = {
    "name": "Knight Online - MyKO",
    "path": str(game_dir),
    "install_type": "manual_download",
    "auto_detected": True,
    "status": "installed",
    "prefix": prefix_path,
    "client_exe": client_exe,
    "updated_at": datetime.utcnow().isoformat() + "Z"
}

installed_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("✓ Registered with launcher")
PY
    fi

    echo ""
    echo "=========================================="
    echo "Game ready to play!"
    echo "=========================================="
    echo ""
    echo "To launch the game:"
    echo "  1. Use the Linux MMORPG Launcher (auto-detects installed games)"
    echo "  2. Or run manually:"
    echo "     WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$GAME_EXE\""
    echo ""
    exit 0
fi

# No installation needed - Client_KOMYKO.exe is the actual game launcher
# Just need to set up Wine dependencies

echo -e "${GREEN}✓${NC} Client found: Client_KOMYKO.exe"
echo ""
echo "Setting up Wine environment..."

# Install Wine dependencies
echo "Installing Wine dependencies..."
echo "This may take a few minutes..."

# Initialize Wine prefix
echo "Initializing Wine prefix..."
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "" || true
sleep 2

# Install dependencies
echo "Installing DirectX, Visual C++ runtime, and fonts (English + CJK)..."
WINETRICKS="d3dx9 vcrun2008 corefonts liberation cjkfonts"
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run winetricks -q $WINETRICKS || {
    echo -e "${YELLOW}Warning:${NC} Some dependencies may have failed to install."
    echo "Continuing anyway..."
}

echo -e "${GREEN}✓${NC} Dependencies installed"

# Find the game executable
CLIENT_EXE=$(find "$GAME_DIR" -maxdepth 3 -type f \( -iname "Client_KOMYKO.exe" -o -iname "KnightOnLine.exe" \) 2>/dev/null | head -1)

# Verify installation
echo ""
echo "Verifying installation..."

if [ -n "$CLIENT_EXE" ] && [ -f "$CLIENT_EXE" ]; then
    echo -e "${GREEN}✓${NC} Knight Online client found!"
    echo ""
    echo "=========================================="
    echo "Installation successful!"
    echo "=========================================="
    echo ""
    echo "Game directory: $GAME_DIR"
    echo "Wine prefix: $PREFIX"
    echo "Client executable: $CLIENT_EXE"
    echo ""

    # Update launcher database so the game shows as installed
    if command -v python3 &> /dev/null; then
        echo "Registering installation with Linux MMORPG Launcher..."
        GAME_DIR_PATH="$GAME_DIR" CLIENT_PATH="$CLIENT_EXE" PREFIX_PATH="$PREFIX" python3 - <<'PY'
import json
import os
from datetime import datetime
from pathlib import Path

game_dir = Path(os.environ.get("GAME_DIR_PATH", ""))
client_exe = os.environ.get("CLIENT_PATH", "")
prefix_path = os.environ.get("PREFIX_PATH", "")

config_dir = Path.home() / ".config" / "mmo-launcher"
config_dir.mkdir(parents=True, exist_ok=True)
installed_file = config_dir / "installed_games.json"

try:
    if installed_file.exists():
        data = json.loads(installed_file.read_text(encoding="utf-8"))
    else:
        data = {}
except Exception:
    data = {}

data["knight-myko"] = {
    "name": "Knight Online - MyKO",
    "path": str(game_dir),
    "install_type": "manual_download",
    "auto_detected": True,
    "status": "installed",
    "prefix": prefix_path,
    "client_exe": client_exe,
    "updated_at": datetime.utcnow().isoformat() + "Z"
}

installed_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("✓ Registered with launcher")
PY
    fi

    echo ""
    echo "To launch the game:"
    echo "  1. Use the Linux MMORPG Launcher (auto-detects installed games)"
    echo "  2. Or run manually:"
    echo "     WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$CLIENT_EXE\""
    echo ""
    echo "Installation complete! You can now close this window."
    exit 0
else
    echo -e "${YELLOW}Warning:${NC} Game executable (KnightOnLine.exe) not found after installation."
    echo ""
    echo "This usually means the installer didn't complete successfully."
    echo "Please check:"
    echo "  1. The installer may have shown an error"
    echo "  2. You may need to run the installer again"
    echo "  3. Check if the game files are in: $GAME_DIR"
    echo ""
    echo "If you see KnightOnLine.exe in the game directory, you can launch it with:"
    echo "  WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$GAME_DIR/KnightOnLine.exe\""
    echo ""
    exit 1
fi
