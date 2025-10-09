#!/bin/bash

# Project Quarm Auto-Installer
# Downloads TAKP client, extracts to Games folder, and sets up patcher

set -e

# Accept game_id parameter from installer (but we don't need it)
GAME_ID="${1:-everquest-quarm}"

GAME_DIR="$HOME/Games/everquest-quarm"
TEMP_DIR="/tmp/quarm_install"
CLIENT_URL="https://drive.google.com/file/d/1qoBktDeJMJKPBr-EZxub1vspJhz11i1y/view"
CLIENT_ID="1qoBktDeJMJKPBr-EZxub1vspJhz11i1y"
PATCHER_PATH="$HOME/Hämtningar/QuarmPatcher.zip"

echo "=== Project Quarm Auto-Installer ==="
echo "Game directory: $GAME_DIR"
echo ""

# Create directories
mkdir -p "$GAME_DIR"
mkdir -p "$TEMP_DIR"

# Check for patcher in Downloads folder
if [ -f "$HOME/Hämtningar/QuarmPatcher (1).zip" ]; then
    PATCHER_PATH="$HOME/Hämtningar/QuarmPatcher (1).zip"
    echo "Found patcher at: $PATCHER_PATH"
elif [ -f "$PATCHER_PATH" ]; then
    echo "Found patcher at: $PATCHER_PATH"
else
    echo "Warning: QuarmPatcher.zip not found in ~/Hämtningar/"
    echo "Will continue without patcher - you can add it later"
fi

# Download TAKP client from Google Drive
echo ""
echo "Downloading TAKP client from Google Drive..."
echo "This may take a while (large file ~2GB)..."

DOWNLOAD_SUCCESS=0

# Try gdown first (best for Google Drive)
if command -v gdown >/dev/null 2>&1; then
    echo "Using gdown to download..."
    if gdown "https://drive.google.com/uc?id=$CLIENT_ID" -O "$TEMP_DIR/quarm_client.zip" 2>/dev/null; then
        DOWNLOAD_SUCCESS=1
    fi
fi

# Try curl if gdown failed or not available
if [ $DOWNLOAD_SUCCESS -eq 0 ] && command -v curl >/dev/null 2>&1; then
    echo "Using curl to download..."
    # Try multiple Google Drive download methods
    if curl -L "https://drive.usercontent.google.com/download?id=$CLIENT_ID&export=download&authuser=0&confirm=t" \
         -o "$TEMP_DIR/quarm_client.zip" \
         --max-time 900 2>/dev/null; then
        DOWNLOAD_SUCCESS=1
    fi
fi

# Check if download was successful
if [ ! -f "$TEMP_DIR/quarm_client.zip" ] || [ ! -s "$TEMP_DIR/quarm_client.zip" ]; then
    echo "Error: Download failed or file is empty"
    echo ""
    echo "Manual download instructions:"
    echo "1. Visit: $CLIENT_URL"
    echo "2. Download the file"
    echo "3. Save it to: $TEMP_DIR/quarm_client.zip"
    echo "4. Run this script again"
    exit 1
fi

echo "Download complete! File size: $(du -h "$TEMP_DIR/quarm_client.zip" | cut -f1)"

# Extract client to Games folder
echo ""
echo "Extracting TAKP client to $GAME_DIR..."
echo "This may take several minutes..."

if command -v 7z >/dev/null 2>&1; then
    7z x "$TEMP_DIR/quarm_client.zip" -o"$GAME_DIR" -y
elif command -v unzip >/dev/null 2>&1; then
    unzip -q -o "$TEMP_DIR/quarm_client.zip" -d "$GAME_DIR"
else
    echo "Error: Neither 7z nor unzip found. Please install one."
    echo "  pacman -S p7zip     # for 7z"
    echo "  pacman -S unzip     # for unzip"
    exit 1
fi

echo "Client extracted successfully!"

# Find the actual client directory (might be nested)
CLIENT_SUBDIR=""
if [ -d "$GAME_DIR/TAKP" ]; then
    CLIENT_SUBDIR="$GAME_DIR/TAKP"
elif [ -d "$GAME_DIR/EverQuest" ]; then
    CLIENT_SUBDIR="$GAME_DIR/EverQuest"
elif [ -f "$GAME_DIR/eqgame.exe" ]; then
    CLIENT_SUBDIR="$GAME_DIR"
else
    # Find first directory with eqgame.exe
    CLIENT_SUBDIR=$(find "$GAME_DIR" -name "eqgame.exe" -type f -exec dirname {} \; | head -n 1)
fi

if [ -z "$CLIENT_SUBDIR" ]; then
    echo "Warning: Could not find eqgame.exe in extracted files"
    echo "Files extracted to: $GAME_DIR"
    CLIENT_SUBDIR="$GAME_DIR"
else
    echo "Found client at: $CLIENT_SUBDIR"
    # Move everything to game dir if nested
    if [ "$CLIENT_SUBDIR" != "$GAME_DIR" ]; then
        echo "Moving client files to $GAME_DIR..."
        mv "$CLIENT_SUBDIR"/* "$GAME_DIR/" 2>/dev/null || true
        rmdir "$CLIENT_SUBDIR" 2>/dev/null || true
        CLIENT_SUBDIR="$GAME_DIR"
    fi
fi

# Extract patcher to game directory
if [ -f "$PATCHER_PATH" ]; then
    echo ""
    echo "Extracting Quarm Patcher to client directory..."
    if command -v unzip >/dev/null 2>&1; then
        unzip -q -o "$PATCHER_PATH" -d "$CLIENT_SUBDIR"
        echo "Patcher extracted successfully to $CLIENT_SUBDIR!"
    else
        echo "Error: unzip not found"
        exit 1
    fi
else
    echo ""
    echo "Warning: Quarm Patcher not found"
    echo "You can manually extract QuarmPatcher.zip to: $CLIENT_SUBDIR"
fi

# Create launch scripts
echo ""
echo "Creating launch scripts..."

cat > "$CLIENT_SUBDIR/launch_patcher.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
WINEPREFIX="$HOME/Games/umu/everquest-quarm/default" PROTONPATH="GE-Proton" umu-run "$SCRIPT_DIR/eqemupatcher.exe"
EOF

cat > "$CLIENT_SUBDIR/launch_game.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
WINEPREFIX="$HOME/Games/umu/everquest-quarm/default" PROTONPATH="GE-Proton" umu-run "$SCRIPT_DIR/eqgame.exe"
EOF

chmod +x "$CLIENT_SUBDIR/launch_patcher.sh"
chmod +x "$CLIENT_SUBDIR/launch_game.sh"

# Cleanup
echo ""
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "Game installed to: $CLIENT_SUBDIR"
echo ""
if [ -f "$CLIENT_SUBDIR/eqemupatcher.exe" ]; then
    echo "✓ TAKP Client extracted"
    echo "✓ Quarm Patcher extracted"
else
    echo "✓ TAKP Client extracted"
    echo "✗ Quarm Patcher not found - add it manually to: $CLIENT_SUBDIR"
fi
echo ""
echo "Next steps:"
echo "1. Create account at: https://www.takproject.net/forums/"
echo "   Then go to 'Game Accounts' → 'Create Login Server Account'"
echo ""
echo "2. Run the patcher first: $CLIENT_SUBDIR/launch_patcher.sh"
echo "   Or manually: cd $CLIENT_SUBDIR && WINEPREFIX=~/Games/umu/everquest-quarm/default PROTONPATH=GE-Proton umu-run eqemupatcher.exe"
echo ""
echo "3. After patching, launch the game: $CLIENT_SUBDIR/launch_game.sh"
echo "   Or manually: cd $CLIENT_SUBDIR && WINEPREFIX=~/Games/umu/everquest-quarm/default PROTONPATH=GE-Proton umu-run eqgame.exe"
echo ""
echo "Note: First launch will set up Wine prefix with required dependencies."
echo ""
echo "Server Info:"
echo "  - 1,200 player cap + queue system"
echo "  - STRICT one-box policy (no multiboxing)"
echo "  - Currently on Luclin era"
echo "  - Officially licensed by Daybreak Games"
echo ""
