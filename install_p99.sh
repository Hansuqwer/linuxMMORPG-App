#!/bin/bash

# Project 1999 (Green/Blue/Red) Auto-Installer
# Installs EverQuest Titanium from ISOs and applies P99 patches

set -e

# Accept game_id parameter from installer
GAME_ID="${1:-everquest-p1999}"

TEMP_DIR="/tmp/p99_install"
TITANIUM_ZIP="$HOME/Hämtningar/EverQuest_Titanium.zip"
P99_PATCHES_URL="https://www.project1999.com/files/P99FilesV61.zip"

echo "=== Project 1999 EverQuest Auto-Installer ==="
echo "Supports: Green (PvE), Blue (PvE), Red (PvP)"
echo ""

# Create temp directory
mkdir -p "$TEMP_DIR"

# Check for required tools
echo "Checking for required tools..."
MISSING_TOOLS=""

if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
    MISSING_TOOLS="$MISSING_TOOLS curl/wget"
fi

if ! command -v 7z >/dev/null 2>&1; then
    MISSING_TOOLS="$MISSING_TOOLS 7z"
fi

if ! command -v unzip >/dev/null 2>&1; then
    MISSING_TOOLS="$MISSING_TOOLS unzip"
fi

if [ -n "$MISSING_TOOLS" ]; then
    echo "Error: Missing required tools:$MISSING_TOOLS"
    echo ""
    echo "Install with: sudo pacman -S p7zip unzip curl"
    read -p "Press Enter to exit..."
    exit 1
fi

DOWNLOAD_CMD="wget -O"
if ! command -v wget >/dev/null 2>&1; then
    DOWNLOAD_CMD="curl -L -o"
fi

# Step 1: Check for Titanium ZIP
echo ""
echo "Step 1/5: Locating EverQuest Titanium files..."

if [ ! -f "$TITANIUM_ZIP" ]; then
    echo ""
    echo "EverQuest Titanium ZIP not found at: $TITANIUM_ZIP"
    echo ""
    read -p "Enter path to EverQuest Titanium.zip (or press Enter to download): " USER_PATH

    if [ -n "$USER_PATH" ] && [ -f "$USER_PATH" ]; then
        TITANIUM_ZIP="$USER_PATH"
        echo "Using: $TITANIUM_ZIP"
    else
        echo ""
        echo "Downloading EverQuest Titanium (3.4GB)..."
        echo "This will take a while..."
        $DOWNLOAD_CMD "$TEMP_DIR/EverQuest_Titanium.zip" "https://archive.org/download/EverQuestTitanium/EverQuest%20Titanium.zip"
        TITANIUM_ZIP="$TEMP_DIR/EverQuest_Titanium.zip"
        echo "Download complete!"
    fi
fi

echo "Using Titanium ZIP: $TITANIUM_ZIP"

# Step 2: Extract ISOs
echo ""
echo "Step 2/5: Extracting Titanium ISO files..."
mkdir -p "$TEMP_DIR/isos"
unzip -j "$TITANIUM_ZIP" "*.iso" -d "$TEMP_DIR/isos"
echo "ISOs extracted!"

# Step 3: Extract game files from ISOs
echo ""
echo "Step 3/5: Extracting game files from Titanium CDs..."
echo "This may take several minutes..."

mkdir -p "$TEMP_DIR/game_files"

# Extract all 5 CDs
for i in 1 2 3 4 5; do
    ISO_FILE="$TEMP_DIR/isos/EQ_TITANIUM_CD${i}.iso"
    if [ -f "$ISO_FILE" ]; then
        echo "Extracting CD${i}..."
        7z x "$ISO_FILE" -o"$TEMP_DIR/cd${i}" -y >/dev/null 2>&1

        # Copy files to game directory (skip duplicates)
        if [ $i -eq 1 ]; then
            # CD1 has the main structure
            cp -r "$TEMP_DIR/cd${i}"/* "$TEMP_DIR/game_files/" 2>/dev/null || true
        else
            # Subsequent CDs contain additional data files
            cp -r "$TEMP_DIR/cd${i}"/* "$TEMP_DIR/game_files/" 2>/dev/null || true
        fi
    fi
done

echo "Game files extracted!"

# Step 4: Install to Wine prefix
echo ""
echo "Step 4/5: Installing EverQuest to Wine prefix..."

export WINEPREFIX="$HOME/Games/umu/everquest-p1999/default"
export PROTONPATH="GE-Proton"

# Create Wine prefix directory structure
mkdir -p "$WINEPREFIX/drive_c/EverQuest"
EQ_INSTALL_DIR="$WINEPREFIX/drive_c/EverQuest"

echo "Copying game files to: $EQ_INSTALL_DIR"

# Copy all extracted files
cp -r "$TEMP_DIR/game_files"/* "$EQ_INSTALL_DIR/" 2>/dev/null || true

echo "Game files installed!"

# Remove conflicting Titanium files
echo ""
echo "Removing conflicting Titanium files for P99 compatibility..."
cd "$EQ_INSTALL_DIR"
rm -f arena.eqg arena_EnvironmentEmitters.txt lavastorm.eqg nektulos.eqg Nektulos_EnvironmentEmitters.txt 2>/dev/null || true
echo "Conflicting files removed."

# Step 5: Download and apply P99 patches
echo ""
echo "Step 5/5: Downloading and applying P99 patches (V61)..."

if [ ! -f "$TEMP_DIR/p99patches.zip" ]; then
    $DOWNLOAD_CMD "$TEMP_DIR/p99patches.zip" "$P99_PATCHES_URL"
    if [ $? -eq 0 ] && [ -s "$TEMP_DIR/p99patches.zip" ]; then
        echo "P99 patches downloaded!"
    else
        echo "Error: Could not download P99 patches"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "Applying P99 patches to game directory..."
unzip -o "$TEMP_DIR/p99patches.zip" -d "$EQ_INSTALL_DIR"
echo "P99 patches applied!"

# Verify critical files exist (antivirus sometimes deletes dsetup.dll)
echo ""
echo "Verifying critical game files..."
if [ ! -f "$EQ_INSTALL_DIR/dsetup.dll" ]; then
    echo ""
    echo "WARNING: dsetup.dll is missing!"
    echo "This file is often deleted by antivirus software (false positive)."
    echo ""
    echo "To fix this:"
    echo "1. Add '$EQ_INSTALL_DIR' to your antivirus exclusions/whitelist"
    echo "2. Re-run this installer, or manually extract P99FilesV61.zip to:"
    echo "   $EQ_INSTALL_DIR"
    echo ""
    echo "The game may not launch correctly without this file!"
    echo ""
    read -p "Press Enter to acknowledge and continue..."
else
    echo "All critical files verified!"
fi

# Run patchme to configure client for P99 servers
echo ""
echo "Configuring client for Project 1999 servers..."
echo "Running eqgame.exe patchme..."
cd "$EQ_INSTALL_DIR"
WINEPREFIX="$WINEPREFIX" PROTONPATH="$PROTONPATH" umu-run "$EQ_INSTALL_DIR/eqgame.exe" patchme &
PATCHME_PID=$!

echo "Waiting for patchme to complete (this usually takes a few seconds)..."
sleep 5

# Check if patchme is still running
if ps -p $PATCHME_PID > /dev/null 2>&1; then
    echo "Patchme is running. Waiting for it to finish..."
    wait $PATCHME_PID 2>/dev/null || true
fi

echo "Client configured for P99 servers!"

# Cleanup
echo ""
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

# Account creation prompt
echo ""
echo "=== Installation Complete! ==="
echo ""
echo "Installation directory: $EQ_INSTALL_DIR"
echo ""
read -p "Would you like to register a Project 1999 account now? (y/n): " REGISTER_ACCOUNT

if [[ "$REGISTER_ACCOUNT" =~ ^[Yy]$ ]]; then
    echo "Opening P99 registration page..."
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "https://www.project1999.com/account/?Play" &
    elif command -v firefox >/dev/null 2>&1; then
        firefox "https://www.project1999.com/account/?Play" &
    elif command -v chromium >/dev/null 2>&1; then
        chromium "https://www.project1999.com/account/?Play" &
    else
        echo "Could not open browser automatically."
        echo "Please visit: https://www.project1999.com/account/?Play"
    fi
    echo ""
    echo "After registering, you can choose which server to play on:"
    echo "  - Green: Most populated, Velious-locked PvE (1200+ players)"
    echo "  - Blue: Established economy, full classic progression PvE (500+ players)"
    echo "  - Red: PvP server (~50 players)"
fi

echo ""
echo "IMPORTANT: Launch the game from the launcher!"
echo "Server selection (Green/Blue/Red) is done in the 'Launch Titanium' window."
echo ""
echo "CRITICAL: NEVER run eqgame.exe directly or patch the game!"
echo "ALWAYS use 'Launch Titanium.bat' to start!"
echo ""
echo "Project 1999 Resources:"
echo "  Website: https://www.project1999.com"
echo "  Wiki: https://wiki.project1999.com"
echo "  Forums: https://www.project1999.com/forums"
echo ""
echo "Installation complete! Return to the launcher and click Play."
echo ""
read -p "Press Enter to finish and close this window..."
exit 0
