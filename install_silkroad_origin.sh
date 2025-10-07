#!/usr/bin/env bash
set -euo pipefail

# Silkroad Origin Installation Helper Script
# This script helps you install Silkroad Origin after manually downloading the client

echo "=========================================="
echo "Silkroad Origin Installation Helper"
echo "=========================================="
echo ""

# Configuration
GAME_DIR="$HOME/Games/silkroad-origin"
PREFIX="$HOME/Games/umu/silkroad/origin"
SEARCH_DIRS=("$HOME" "$HOME/Downloads")

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
echo -e "${GREEN}[1/5]${NC} Creating game directory..."
mkdir -p "$GAME_DIR"
mkdir -p "$PREFIX"

# Look for downloaded installer/client
echo -e "${GREEN}[2/5]${NC} Looking for Silkroad Origin installer..."
echo ""

# Common installer/archive names
INSTALLER_PATTERNS=(
    "Origin_Online_Genesis_Global_v*.exe"
    "Origin_Online_Genesis_Global_*.exe"
    "SilkroadOrigin_Installer.exe"
    "SRO_Origin_Client.exe"
    "Silkroad_Installer.exe"
    "sro_client.exe"
    "*Origin*Installer*.exe"
    "*Silkroad*Installer*.exe"
)

ARCHIVE_PATTERNS=(
    "Origin_Online_Genesis*.zip"
    "SilkroadOrigin.zip"
    "SRO_Origin.zip"
    "Silkroad.zip"
    "*Origin*.zip"
    "SilkroadOrigin.rar"
    "SRO_Origin.rar"
    "*Origin*.rar"
    "SilkroadOrigin.7z"
    "*Origin*.7z"
)

FOUND_INSTALLER=""
FOUND_ARCHIVE=""

# Search for installer EXE in all directories
echo "Searching in: Home folder and Downloads..."
for search_dir in "${SEARCH_DIRS[@]}"; do
    if [ ! -d "$search_dir" ]; then
        continue
    fi

    for pattern in "${INSTALLER_PATTERNS[@]}"; do
        # Search only in the top level of each directory (not recursive to avoid slowness)
        for file in "$search_dir"/$pattern; do
            if [ -f "$file" ]; then
                FOUND_INSTALLER="$file"
                echo -e "${GREEN}✓${NC} Found installer: $(basename "$file")"
                echo "  Location: $file"
                break 3
            fi
        done
    done
done

# Search for archives if no installer found
if [ -z "$FOUND_INSTALLER" ]; then
    for search_dir in "${SEARCH_DIRS[@]}"; do
        if [ ! -d "$search_dir" ]; then
            continue
        fi

        for pattern in "${ARCHIVE_PATTERNS[@]}"; do
            for file in "$search_dir"/$pattern; do
                if [ -f "$file" ]; then
                    FOUND_ARCHIVE="$file"
                    echo -e "${GREEN}✓${NC} Found archive: $(basename "$file")"
                    echo "  Location: $file"
                    break 3
                fi
            done
        done
    done
fi

# If nothing found, ask user for path
if [ -z "$FOUND_INSTALLER" ] && [ -z "$FOUND_ARCHIVE" ]; then
    echo -e "${YELLOW}No installer found automatically.${NC}"
    echo ""
    echo "Please enter the full path to your downloaded Silkroad Origin installer or archive:"
    read -r USER_PATH

    if [ -f "$USER_PATH" ]; then
        if [[ "$USER_PATH" == *.exe ]]; then
            FOUND_INSTALLER="$USER_PATH"
        else
            FOUND_ARCHIVE="$USER_PATH"
        fi
        echo -e "${GREEN}✓${NC} Using: $USER_PATH"
    else
        echo -e "${RED}[ERROR]${NC} File not found: $USER_PATH"
        exit 1
    fi
fi

# Extract archive if found
if [ -n "$FOUND_ARCHIVE" ]; then
    echo -e "${GREEN}[3/5]${NC} Extracting archive..."

    if [[ "$FOUND_ARCHIVE" == *.zip ]]; then
        unzip -q "$FOUND_ARCHIVE" -d "$GAME_DIR"
        echo -e "${GREEN}✓${NC} Extracted ZIP archive"
    elif [[ "$FOUND_ARCHIVE" == *.rar || "$FOUND_ARCHIVE" == *.RAR ]]; then
        if command -v unrar &> /dev/null; then
            unrar x "$FOUND_ARCHIVE" "$GAME_DIR/"
            echo -e "${GREEN}✓${NC} Extracted RAR archive"
        else
            echo -e "${RED}[ERROR]${NC} unrar not found. Install with: sudo pacman -S unrar"
            exit 1
        fi
    elif [[ "$FOUND_ARCHIVE" == *.7z ]]; then
        if command -v 7z &> /dev/null; then
            7z x "$FOUND_ARCHIVE" -o"$GAME_DIR"
            echo -e "${GREEN}✓${NC} Extracted 7z archive"
        else
            echo -e "${RED}[ERROR]${NC} 7z not found. Install with: sudo pacman -S p7zip"
            exit 1
        fi
    fi

    # Look for installer or client in extracted files
    FOUND_INSTALLER=$(find "$GAME_DIR" -name "*installer*.exe" -o -name "sro_client.exe" -o -name "Launcher.exe" | head -1)

    if [ -z "$FOUND_INSTALLER" ]; then
        echo -e "${YELLOW}Warning:${NC} No installer EXE found in archive. Checking for client..."
        CLIENT_EXE=$(find "$GAME_DIR" -name "sro_client.exe" | head -1)
        if [ -n "$CLIENT_EXE" ]; then
            echo -e "${GREEN}✓${NC} Found client executable: $(basename "$CLIENT_EXE")"
            echo -e "${GREEN}[DONE]${NC} Client is already extracted and ready!"
            echo ""
            echo "Client location: $GAME_DIR"
            echo "To launch the game, use the Linux MMORPG Launcher or run:"
            echo "  WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$CLIENT_EXE\""
            exit 0
        fi
    fi
fi

# Install dependencies via winetricks
echo -e "${GREEN}[4/5]${NC} Installing Wine dependencies..."
WINETRICKS="d3dx9 vcrun2008 corefonts"

WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "" || true
sleep 2
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run winetricks -q $WINETRICKS || true

echo -e "${GREEN}✓${NC} Dependencies installed"

# Run installer
if [ -n "$FOUND_INSTALLER" ]; then
    echo -e "${GREEN}[5/5]${NC} Running installer..."
    echo ""
    echo "The installer window will open. Please:"
    echo "  1. Install to: $GAME_DIR"
    echo "  2. Complete the installation"
    echo "  3. Close the installer when done"
    echo ""
    read -p "Press Enter to start the installer..."

    # Copy installer to game dir if not already there
    if [[ "$FOUND_INSTALLER" != "$GAME_DIR"* ]]; then
        cp "$FOUND_INSTALLER" "$GAME_DIR/"
        FOUND_INSTALLER="$GAME_DIR/$(basename "$FOUND_INSTALLER")"
    fi

    WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$FOUND_INSTALLER"

    echo ""
    echo -e "${GREEN}✓${NC} Installation complete!"
else
    echo -e "${YELLOW}[SKIP]${NC} No installer to run"
fi

# Verify installation
echo ""
echo "Verifying installation..."
CLIENT_EXE=$(find "$GAME_DIR" -name "sro_client.exe" | head -1)

if [ -n "$CLIENT_EXE" ]; then
    echo -e "${GREEN}✓${NC} Silkroad Origin client found!"
    echo ""
    echo "=========================================="
    echo "Installation successful!"
    echo "=========================================="
    echo ""
    echo "Game directory: $GAME_DIR"
    echo "Wine prefix: $PREFIX"
    echo "Client executable: $CLIENT_EXE"
    echo ""
    echo "To launch the game:"
    echo "  1. Use the Linux MMORPG Launcher (it will auto-detect the game)"
    echo "  2. Or run manually:"
    echo "     WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$CLIENT_EXE\""
    echo ""
else
    echo -e "${YELLOW}Warning:${NC} sro_client.exe not found."
    echo "You may need to manually launch the patcher or client."
    echo ""
    echo "Game directory: $GAME_DIR"
    echo "Check this directory for the game executable."
fi

echo ""
echo "Done!"
