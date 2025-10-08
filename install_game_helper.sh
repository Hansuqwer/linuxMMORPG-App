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

# Determine keywords that identify the correct installer for this game
declare -a KEYWORDS=()
declare -a PREFERRED_FILES=()
IFS='-' read -r -a NAME_PARTS <<< "$GAME_NAME"
for part in "${NAME_PARTS[@]}"; do
    part_lower="${part,,}"
    if [ -n "$part_lower" ]; then
        KEYWORDS+=("$part_lower")
    fi
done

case "$GAME_NAME" in
    knight-myko)
        KEYWORDS+=("knight" "myko" "komyko" "client_myko" "client_ko")
        PREFERRED_FILES+=(
            "$HOME/Hämtningar/Client_KOMYKO.zip"
            "$HOME/Hämtningar/client_myko.zip"
            "$HOME/Hämtningar/Client_KOMYKO.exe"
            "$HOME/Hämtningar/client_myko.exe"
            "$HOME/Downloads/Client_KOMYKO.zip"
            "$HOME/Downloads/client_myko.zip"
            "$HOME/Downloads/Client_KOMYKO.exe"
            "$HOME/Downloads/client_myko.exe"
        )
        ;;
    silkroad-origin|silkroad-legend|silkroad-zenger|silkroad-phoenix)
        KEYWORDS+=("silkroad" "sro" "origin" "legend" "zenger" "phoenix")
        ;;
    everquest-*)
        KEYWORDS+=("everquest" "eq" "p99" "quarm" "ezserver")
        ;;
esac

if [ ${#KEYWORDS[@]} -eq 0 ]; then
    KEYWORDS+=("${GAME_NAME,,}")
fi

matches_keywords() {
    local filename_lower="${1,,}"
    for keyword in "${KEYWORDS[@]}"; do
        if [[ "$filename_lower" == *"$keyword"* ]]; then
            return 0
        fi
    done
    return 1
}

# Detect Downloads folder (handles different languages)
DOWNLOADS_DIR="$HOME/Downloads"
if [ -d "$HOME/Hämtningar" ]; then
    DOWNLOADS_DIR="$HOME/Hämtningar"
elif [ -d "$HOME/Téléchargements" ]; then
    DOWNLOADS_DIR="$HOME/Téléchargements"
elif [ -d "$HOME/Descargas" ]; then
    DOWNLOADS_DIR="$HOME/Descargas"
fi

SEARCH_DIRS=("$HOME" "$DOWNLOADS_DIR")

echo -e "${BLUE}Game:${NC} $GAME_NAME"
echo -e "${BLUE}Install location:${NC} $GAME_DIR"
echo ""

# Check preferred filenames first
FOUND_FILE=""
FOUND_TYPE=""
for candidate in "${PREFERRED_FILES[@]}"; do
    if [ -f "$candidate" ]; then
        FOUND_FILE="$candidate"
        if [[ "$candidate" == *.exe || "$candidate" == *.EXE ]]; then
            FOUND_TYPE="exe"
        else
            FOUND_TYPE="archive"
        fi
        echo -e "${GREEN}✓${NC} Found preferred file: $(basename "$FOUND_FILE")"
        break
    fi
done

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

if [ -z "$FOUND_FILE" ]; then
    declare -a EXE_MATCHES=()
    declare -a EXE_CANDIDATES=()
    declare -a ARCHIVE_MATCHES=()
    declare -a ARCHIVE_CANDIDATES=()

    # Search for any EXE files (installers)
    for search_dir in "${SEARCH_DIRS[@]}"; do
        if [ ! -d "$search_dir" ]; then
            continue
        fi

        # Find .exe files
        while IFS= read -r -d '' file; do
            base_name="$(basename "$file")"
            if matches_keywords "$base_name"; then
                EXE_MATCHES+=("$file")
                echo -e "  [match] $base_name"
            else
                EXE_CANDIDATES+=("$file")
                echo -e "  [other] $base_name"
            fi
        done < <(find "$search_dir" -maxdepth 1 -type f -iname "*.exe" -print0 2>/dev/null)
    done

    # Search for archives if no EXE matches found
    if [ -z "$FOUND_FILE" ] && [ ${#EXE_MATCHES[@]} -eq 0 ]; then
        for search_dir in "${SEARCH_DIRS[@]}"; do
            if [ ! -d "$search_dir" ]; then
                continue
            fi

            # Find archive files
            while IFS= read -r -d '' file; do
                base_name="$(basename "$file")"
                if matches_keywords "$base_name"; then
                    ARCHIVE_MATCHES+=("$file")
                    echo -e "  [match] $base_name"
                else
                    ARCHIVE_CANDIDATES+=("$file")
                    echo -e "  [other] $base_name"
                fi
            done < <(find "$search_dir" -maxdepth 1 -type f \( -iname "*.zip" -o -iname "*.rar" -o -iname "*.7z" -o -iname "*.tar.gz" \) -print0 2>/dev/null)
        done
    fi

    if [ -z "$FOUND_FILE" ]; then
        if [ ${#EXE_MATCHES[@]} -gt 0 ]; then
            FOUND_FILE="${EXE_MATCHES[0]}"
            FOUND_TYPE="exe"
        elif [ ${#ARCHIVE_MATCHES[@]} -gt 0 ]; then
            FOUND_FILE="${ARCHIVE_MATCHES[0]}"
            FOUND_TYPE="archive"
        fi
    fi
fi

echo ""

# If nothing found, ask user
if [ -z "$FOUND_FILE" ]; then
    echo -e "${YELLOW}No installer found automatically.${NC}"
    echo ""
    echo "Please enter the full path to your downloaded game installer or archive:"
    echo "(You can drag and drop the file here)"
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
        if [[ "$USER_PATH" == *.exe ]]; then
            FOUND_TYPE="exe"
        else
            FOUND_TYPE="archive"
        fi
        echo -e "${GREEN}✓${NC} Using: $USER_PATH"
    else
        echo -e "${RED}[ERROR]${NC} File not found: $USER_PATH"
        echo "Searched for: $USER_PATH"
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

# Track whether we should run the detected executable as an installer
SHOULD_RUN_INSTALLER=false

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
        mapfile -d '' CANDIDATE_EXES < <(find "$GAME_DIR" -maxdepth 3 -type f -iname "*.exe" -print0 2>/dev/null)
        if [ ${#CANDIDATE_EXES[@]} -gt 0 ]; then
            # Prefer executables that look like the actual game client, not the installer
            CLIENT=""
            for exe in "${CANDIDATE_EXES[@]}"; do
                lower_name="$(basename "$exe" | tr '[:upper:]' '[:lower:]')"
                case "$lower_name" in
                    knightonline.exe|*-game*.exe|*gameclient*.exe|*main.exe)
                        CLIENT="$exe"
                        break
                        ;;
                esac
            done
            # If we didn't match a preferred name, fall back to the first candidate
            if [ -z "$CLIENT" ]; then
                CLIENT="${CANDIDATE_EXES[0]}"
            fi

            echo -e "${GREEN}✓${NC} Found executable in extracted files: $(basename "$CLIENT")"
            echo "Continuing with dependency setup and installation..."
            FOUND_FILE="$CLIENT"
            FOUND_TYPE="exe"
        fi
    fi
fi

# Decide if the executable should be run as an installer
if [ "$FOUND_TYPE" == "exe" ]; then
    exe_name_lower="$(basename "$FOUND_FILE" | tr '[:upper:]' '[:lower:]')"
    if [[ "$exe_name_lower" == *"install"* || "$exe_name_lower" == *"setup"* || "$exe_name_lower" == *"installer"* || "$exe_name_lower" == *"client"* ]]; then
        SHOULD_RUN_INSTALLER=true
    fi
fi

# Install Wine dependencies
echo -e "${GREEN}[4/5]${NC} Installing Wine dependencies..."
echo "This may take a few minutes..."
WINETRICKS="d3dx9 vcrun2008 corefonts liberation cjkfonts"

# Initialize Wine prefix
echo "Initializing Wine prefix..."
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run "" || true
sleep 2

# Install dependencies
echo "Installing DirectX, Visual C++ runtime, and fonts (English + CJK)..."
WINEPREFIX="$PREFIX" PROTONPATH="GE-Proton" umu-run winetricks -q $WINETRICKS || {
    echo -e "${YELLOW}Warning:${NC} Some dependencies may have failed to install."
    echo "Continuing anyway..."
}

echo -e "${GREEN}✓${NC} Dependencies installed"

# Run installer if we have one
if [ "$FOUND_TYPE" == "exe" ] && [ "$SHOULD_RUN_INSTALLER" = true ]; then
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
elif [ "$FOUND_TYPE" == "exe" ]; then
    echo -e "${YELLOW}Note:${NC} Detected executable appears to be the game client."
    echo "Skipping automatic installer launch. You can start it later via the launcher."
fi

# Verify installation
echo ""
echo "Verifying installation..."
mapfile -d '' VERIFY_EXES < <(find "$GAME_DIR" -maxdepth 4 -type f -iname "*.exe" -print0 2>/dev/null)
CLIENT=""
if [ ${#VERIFY_EXES[@]} -gt 0 ]; then
    for exe in "${VERIFY_EXES[@]}"; do
        lower_name="$(basename "$exe" | tr '[:upper:]' '[:lower:]')"
        case "$lower_name" in
            knightonline.exe|*gameclient*.exe|*launch*.exe|*main.exe)
                CLIENT="$exe"
                break
                ;;
        esac
        if [[ "$lower_name" == *"$GAME_NAME"* ]]; then
            CLIENT="$exe"
            break
        fi
    done
    if [ -z "$CLIENT" ]; then
        CLIENT="${VERIFY_EXES[0]}"
    fi
fi

if [ -n "$CLIENT" ] && [ -f "$CLIENT" ]; then
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
