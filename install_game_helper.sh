#!/usr/bin/env bash
set -euo pipefail

# Generic MMORPG Game Installation Helper Script
# Works for any game - searches home folder for installers/archives

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Linux MMORPG Game Installation Helper"
echo "=========================================="
echo ""

# Check if game name provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <game-name>"
    echo ""
    echo "Examples:"
    echo "  $0 silkroad-origin"
    echo "  $0 knight-myko"
    echo "  $0 ragnarok-uaro"
    echo ""
    exit 1
fi

GAME_NAME="$1"
GAME_DIR="$HOME/Games/$GAME_NAME"
PREFIX="$HOME/Games/umu/$GAME_NAME/default"
SEARCH_DIRS=("$HOME" "$HOME/Downloads")

echo -e "${BLUE}Game:${NC} $GAME_NAME"
echo -e "${BLUE}Install location:${NC} $GAME_DIR"
echo ""

# Check if umu-run is available
if ! command -v umu-run &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} umu-run not found. Please install umu-launcher first."
    echo "Install with: yay -S umu-launcher"
    exit 1
fi

# Create directories
echo -e "${GREEN}[1/5]${NC} Creating game directory..."
mkdir -p "$GAME_DIR"
mkdir -p "$PREFIX"

# Search for installers/archives
echo -e "${GREEN}[2/5]${NC} Searching for game installer/archive..."
echo "Searching in: Home folder and Downloads folder..."
echo ""

FOUND_FILE=""
FOUND_TYPE=""

# Search for any EXE files (installers)
for search_dir in "${SEARCH_DIRS[@]}"; do
    if [ ! -d "$search_dir" ]; then
        continue
    fi

    # Find .exe files
    while IFS= read -r -d '' file; do
        echo -e "  Found: $(basename "$file")"
        if [ -z "$FOUND_FILE" ]; then
            FOUND_FILE="$file"
            FOUND_TYPE="exe"
        fi
    done < <(find "$search_dir" -maxdepth 1 -type f -iname "*.exe" -print0 2>/dev/null)
done

# Search for archives if no EXE found
if [ -z "$FOUND_FILE" ]; then
    for search_dir in "${SEARCH_DIRS[@]}"; do
        if [ ! -d "$search_dir" ]; then
            continue
        fi

        # Find archive files
        while IFS= read -r -d '' file; do
            echo -e "  Found: $(basename "$file")"
            if [ -z "$FOUND_FILE" ]; then
                FOUND_FILE="$file"
                FOUND_TYPE="archive"
            fi
        done < <(find "$search_dir" -maxdepth 1 -type f \( -iname "*.zip" -o -iname "*.rar" -o -iname "*.7z" -o -iname "*.tar.gz" \) -print0 2>/dev/null)
    done
fi

echo ""

# If nothing found, ask user
if [ -z "$FOUND_FILE" ]; then
    echo -e "${YELLOW}No installer found automatically.${NC}"
    echo ""
    echo "Please enter the full path to your downloaded game installer or archive:"
    read -r USER_PATH

    if [ -f "$USER_PATH" ]; then
        FOUND_FILE="$USER_PATH"
        if [[ "$USER_PATH" == *.exe ]]; then
            FOUND_TYPE="exe"
        else
            FOUND_TYPE="archive"
        fi
        echo -e "${GREEN}✓${NC} Using: $USER_PATH"
    else
        echo -e "${RED}[ERROR]${NC} File not found: $USER_PATH"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Found: $(basename "$FOUND_FILE")"
    echo ""
    echo "Use this file? (Y/n)"
    read -r CONFIRM
    if [[ "$CONFIRM" =~ ^[Nn]$ ]]; then
        echo "Please enter the full path to the correct installer:"
        read -r USER_PATH
        if [ -f "$USER_PATH" ]; then
            FOUND_FILE="$USER_PATH"
            if [[ "$USER_PATH" == *.exe ]]; then
                FOUND_TYPE="exe"
            else
                FOUND_TYPE="archive"
            fi
        else
            echo -e "${RED}[ERROR]${NC} File not found: $USER_PATH"
            exit 1
        fi
    fi
fi

# Extract archive if needed
if [ "$FOUND_TYPE" == "archive" ]; then
    echo -e "${GREEN}[3/5]${NC} Extracting archive..."

    if [[ "$FOUND_FILE" == *.zip ]]; then
        unzip -q "$FOUND_FILE" -d "$GAME_DIR"
        echo -e "${GREEN}✓${NC} Extracted ZIP archive"
    elif [[ "$FOUND_FILE" == *.rar || "$FOUND_FILE" == *.RAR ]]; then
        if command -v unrar &> /dev/null; then
            unrar x "$FOUND_FILE" "$GAME_DIR/"
            echo -e "${GREEN}✓${NC} Extracted RAR archive"
        else
            echo -e "${RED}[ERROR]${NC} unrar not found. Install with: sudo pacman -S unrar"
            exit 1
        fi
    elif [[ "$FOUND_FILE" == *.7z ]]; then
        if command -v 7z &> /dev/null; then
            7z x "$FOUND_FILE" -o"$GAME_DIR"
            echo -e "${GREEN}✓${NC} Extracted 7z archive"
        else
            echo -e "${RED}[ERROR]${NC} 7z not found. Install with: sudo pacman -S p7zip"
            exit 1
        fi
    elif [[ "$FOUND_FILE" == *.tar.gz ]]; then
        tar -xzf "$FOUND_FILE" -C "$GAME_DIR"
        echo -e "${GREEN}✓${NC} Extracted tar.gz archive"
    fi

    # Find installer in extracted files
    INSTALLER=$(find "$GAME_DIR" -maxdepth 2 -type f -iname "*install*.exe" -o -iname "setup*.exe" -o -iname "*launcher*.exe" | head -1)

    if [ -n "$INSTALLER" ]; then
        FOUND_FILE="$INSTALLER"
        FOUND_TYPE="exe"
        echo -e "${GREEN}✓${NC} Found installer in archive: $(basename "$INSTALLER")"
    else
        # Check if client is already extracted
        CLIENT=$(find "$GAME_DIR" -maxdepth 2 -type f -iname "*.exe" | head -1)
        if [ -n "$CLIENT" ]; then
            echo -e "${GREEN}✓${NC} Game client already extracted!"
            echo ""
            echo "Client location: $GAME_DIR"
            echo "Main executable: $CLIENT"
            echo ""
            echo "The Linux MMORPG Launcher will auto-detect this game."
            echo "Or launch manually with:"
            echo "  WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$CLIENT\""
            exit 0
        fi
    fi
fi

# Install Wine dependencies
echo -e "${GREEN}[4/5]${NC} Installing Wine dependencies..."
WINETRICKS="d3dx9 vcrun2008 corefonts"

WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "" || true
sleep 2
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run winetricks -q $WINETRICKS || true

echo -e "${GREEN}✓${NC} Dependencies installed"

# Run installer if we have one
if [ "$FOUND_TYPE" == "exe" ]; then
    echo -e "${GREEN}[5/5]${NC} Running installer..."
    echo ""
    echo "The installer window will open. Please:"
    echo "  1. Install to: $GAME_DIR"
    echo "  2. Complete the installation"
    echo "  3. Close the installer when done"
    echo ""
    read -p "Press Enter to start the installer..."

    # Copy installer to game dir if not already there
    if [[ "$FOUND_FILE" != "$GAME_DIR"* ]]; then
        cp "$FOUND_FILE" "$GAME_DIR/"
        FOUND_FILE="$GAME_DIR/$(basename "$FOUND_FILE")"
    fi

    WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "$FOUND_FILE"

    echo ""
    echo -e "${GREEN}✓${NC} Installation complete!"
fi

# Verify installation
echo ""
echo "Verifying installation..."
CLIENT=$(find "$GAME_DIR" -maxdepth 3 -type f -iname "*.exe" | head -1)

if [ -n "$CLIENT" ]; then
    echo -e "${GREEN}✓${NC} Game client found!"
    echo ""
    echo "=========================================="
    echo "Installation successful!"
    echo "=========================================="
    echo ""
    echo "Game: $GAME_NAME"
    echo "Directory: $GAME_DIR"
    echo "Wine prefix: $PREFIX"
    echo "Client: $(basename "$CLIENT")"
    echo ""
    echo "To launch the game:"
    echo "  1. Use the Linux MMORPG Launcher (auto-detects installed games)"
    echo "  2. Or run manually:"
    echo "     WINEPREFIX=\"$PREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$CLIENT\""
    echo ""
else
    echo -e "${YELLOW}Warning:${NC} Game executable not found."
    echo "Check $GAME_DIR for the game files."
fi

echo ""
echo "Done!"
