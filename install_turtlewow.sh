#!/usr/bin/env bash
set -euo pipefail

# Turtle WoW Native Linux Client Installation Script
# Uses yay (AUR) if available, otherwise downloads AppImage

echo "=========================================="
echo "Turtle WoW Linux Client Installer"
echo "=========================================="
echo ""

# Configuration
GAME_DIR="$HOME/Games/turtlewow"
AUR_PACKAGE="turtle-wow"
APPIMAGE_NAME="TurtleWoW.AppImage"
APPIMAGE_URL="https://cdn.turtle-wow.org/launcher/turtle-wow-launcher-linux.AppImage"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

INSTALL_METHOD=""
CLIENT_EXE=""

# Check if yay is available
if command -v yay &> /dev/null; then
    echo -e "${GREEN}[1/2]${NC} Installing Turtle WoW from AUR..."
    echo "Package: $AUR_PACKAGE"
    echo "Using: yay"
    echo ""

    if yay -S --needed --noconfirm "$AUR_PACKAGE"; then
        echo -e "${GREEN}✓${NC} AUR package installed successfully!"
        INSTALL_METHOD="aur"

        # Find the executable
        if command -v turtle-wow &> /dev/null; then
            CLIENT_EXE=$(which turtle-wow)
        elif [ -f "/usr/bin/turtle-wow" ]; then
            CLIENT_EXE="/usr/bin/turtle-wow"
        fi
    else
        echo -e "${YELLOW}Warning:${NC} AUR installation failed"
        echo "Falling back to AppImage download..."
        echo ""
    fi
fi

# If yay not available or AUR install failed, download AppImage
if [ -z "$INSTALL_METHOD" ]; then
    echo -e "${GREEN}[1/2]${NC} Installing Turtle WoW AppImage..."

    if ! command -v yay &> /dev/null; then
        echo "yay not found - downloading AppImage instead"
        echo ""
    fi

    # Check for FUSE
    if ! command -v fusermount &> /dev/null && ! command -v fusermount3 &> /dev/null; then
        echo -e "${YELLOW}Warning:${NC} FUSE not detected. AppImages require FUSE."
        echo "Install with: sudo pacman -S fuse2"
        echo ""
        read -r -p "Continue anyway? (y/N): " continue_install
        if [[ ! "$continue_install" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Create game directory
    mkdir -p "$GAME_DIR"
    APPIMAGE_PATH="$GAME_DIR/$APPIMAGE_NAME"

    # Check if already downloaded
    if [ -f "$APPIMAGE_PATH" ] && [ -s "$APPIMAGE_PATH" ]; then
        echo "AppImage already exists at: $APPIMAGE_PATH"
        echo "Size: $(du -h "$APPIMAGE_PATH" | cut -f1)"
        echo ""
        chmod +x "$APPIMAGE_PATH"
    else
        # Download AppImage
        echo "Downloading from: $APPIMAGE_URL"
        echo ""

        if command -v wget &> /dev/null; then
            wget -O "$APPIMAGE_PATH" "$APPIMAGE_URL" --progress=bar:force 2>&1
        elif command -v curl &> /dev/null; then
            curl -L -o "$APPIMAGE_PATH" "$APPIMAGE_URL" --progress-bar
        else
            echo -e "${RED}[ERROR]${NC} Neither wget nor curl found"
            exit 1
        fi

        # Verify download
        if [ ! -f "$APPIMAGE_PATH" ] || [ ! -s "$APPIMAGE_PATH" ]; then
            echo -e "${RED}[ERROR]${NC} Download failed or file is empty"
            exit 1
        fi

        chmod +x "$APPIMAGE_PATH"
        echo -e "${GREEN}✓${NC} AppImage downloaded!"
    fi

    INSTALL_METHOD="appimage"
    CLIENT_EXE="$APPIMAGE_PATH"
fi

if [ -z "$CLIENT_EXE" ]; then
    echo -e "${RED}[ERROR]${NC} Could not locate Turtle WoW executable"
    exit 1
fi

# Register with launcher database
if command -v python3 &> /dev/null; then
    echo ""
    echo -e "${GREEN}[2/2]${NC} Registering with Linux MMORPG Launcher..."
    GAME_DIR_PATH="$GAME_DIR" CLIENT_PATH="$CLIENT_EXE" INSTALL_METHOD="$INSTALL_METHOD" python3 - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

game_dir = Path(os.environ.get("GAME_DIR_PATH", ""))
client_exe = os.environ.get("CLIENT_PATH", "")
install_method = os.environ.get("INSTALL_METHOD", "unknown")

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

data["wow-turtle"] = {
    "name": "World of Warcraft - Turtle WoW",
    "path": str(game_dir) if game_dir.exists() else str(Path(client_exe).parent),
    "install_type": "native",
    "install_method": install_method,
    "status": "installed",
    "client_exe": client_exe,
    "native": True,
    "updated_at": datetime.now(timezone.utc).isoformat()
}

installed_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("✓ Registered with launcher")
PY
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo -e "${GREEN}Installation Details:${NC}"
echo "  Method: $INSTALL_METHOD"
echo "  Executable: $CLIENT_EXE"
echo ""

if [ "$INSTALL_METHOD" = "aur" ]; then
    echo -e "${BLUE}Installed via AUR:${NC}"
    echo "  Package: turtle-wow"
    echo "  The launcher is now available system-wide"
    echo ""
elif [ "$INSTALL_METHOD" = "appimage" ]; then
    echo -e "${BLUE}About AppImage:${NC}"
    echo "  AppImages are self-contained Linux apps"
    echo "  Location: $GAME_DIR"
    if ! command -v fusermount &> /dev/null && ! command -v fusermount3 &> /dev/null; then
        echo ""
        echo -e "${YELLOW}Install FUSE for better compatibility:${NC}"
        echo "  sudo pacman -S fuse2"
    fi
    echo ""
fi

echo -e "${GREEN}Launch Turtle WoW:${NC}"
if [ "$INSTALL_METHOD" = "aur" ]; then
    echo "  • Run: turtle-wow"
    echo "  • Or from application menu"
    echo "  • Or use Linux MMORPG Launcher"
else
    echo "  • Run: $CLIENT_EXE"
    echo "  • Or double-click in file manager"
    echo "  • Or use Linux MMORPG Launcher"
fi
echo ""
echo -e "${BLUE}Note:${NC} First launch will download game files (~2-3GB)"
echo ""

# Launch now
read -r -p "Launch Turtle WoW now? (Y/n): " launch_now
if [[ ! "$launch_now" =~ ^[Nn]$ ]]; then
    echo ""
    echo "Launching Turtle WoW..."
    "$CLIENT_EXE" &
    sleep 2
    echo -e "${GREEN}✓${NC} Launcher started!"
fi

echo ""
echo "Installation complete!"
exit 0
