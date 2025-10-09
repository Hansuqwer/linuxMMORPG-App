#!/bin/bash

# Project 1999 (Green/Blue/Red) Auto-Installer
# Downloads EverQuest Titanium, mounts ISOs, installs game, and applies P99 patches

set -e

# Accept game_id parameter from installer
GAME_ID="${1:-everquest-p1999}"

GAME_DIR="$HOME/Games/everquest-p1999"
TEMP_DIR="/tmp/p99_install"
# Using combined Titanium + P99 v46 archive (smaller and includes patches)
TITANIUM_P99_URL="https://archive.org/download/EQP99V46/EQ%20P99%20v46.zip"
# Fallback to separate downloads if needed
TITANIUM_URL="https://archive.org/download/EverQuestTitanium/EverQuest%20Titanium.zip"
P99_PATCHES_URL="https://www.project1999.com/files/P99FilesV61.zip"

echo "=== Project 1999 EverQuest Auto-Installer ==="
echo "Supports: Green (PvE), Blue (PvE), Red (PvP)"
echo "Game directory: $GAME_DIR"
echo ""

# Create directories
mkdir -p "$GAME_DIR"
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

if ! command -v fuseiso >/dev/null 2>&1 && ! command -v mount >/dev/null 2>&1; then
    echo "Warning: Neither fuseiso nor mount found. Will try alternative ISO extraction."
fi

if [ -n "$MISSING_TOOLS" ]; then
    echo "Error: Missing required tools:$MISSING_TOOLS"
    echo ""
    echo "Install with: sudo pacman -S p7zip unzip curl fuseiso"
    read -p "Press Enter to exit..."
    exit 1
fi

DOWNLOAD_CMD="wget -O"
if ! command -v wget >/dev/null 2>&1; then
    DOWNLOAD_CMD="curl -L -o"
fi

# Step 1: Download EverQuest Titanium + P99 Combined
echo ""
echo "Step 1/4: Downloading EverQuest Titanium + P99 v46 Combined..."
echo "This is ~1.3GB and may take a while..."
echo "This archive includes both Titanium client and P99 patches!"

if [ ! -f "$TEMP_DIR/p99_combined.zip" ]; then
    $DOWNLOAD_CMD "$TEMP_DIR/p99_combined.zip" "$TITANIUM_P99_URL"
    if [ $? -ne 0 ] || [ ! -s "$TEMP_DIR/p99_combined.zip" ]; then
        echo "Combined archive failed, trying separate Titanium download..."
        $DOWNLOAD_CMD "$TEMP_DIR/titanium.zip" "$TITANIUM_URL"
        USE_SEPARATE=true
    else
        echo "Download complete! File size: $(du -h "$TEMP_DIR/p99_combined.zip" | cut -f1)"
        USE_SEPARATE=false
    fi
else
    echo "Archive already downloaded, skipping..."
    USE_SEPARATE=false
fi

# Step 2: Extract archive
echo ""
echo "Step 2/4: Extracting game files (this may take several minutes)..."

if [ "$USE_SEPARATE" = "true" ]; then
    unzip -q "$TEMP_DIR/titanium.zip" -d "$TEMP_DIR/eq_extracted"
else
    unzip -q "$TEMP_DIR/p99_combined.zip" -d "$TEMP_DIR/eq_extracted"
fi

echo "Extraction complete!"

# Step 3: Copy game files to Wine prefix directory
echo ""
echo "Step 3/4: Installing EverQuest to Wine prefix..."

# Set up Wine prefix
export WINEPREFIX="$HOME/Games/umu/everquest-p1999/default"
export PROTONPATH="GE-Proton"

# Create Wine prefix directory structure
mkdir -p "$WINEPREFIX/drive_c/Program Files"

# Find the EverQuest folder in extracted files
EQ_SOURCE=$(find "$TEMP_DIR/eq_extracted" -type d -iname "everquest" | head -n 1)

if [ -z "$EQ_SOURCE" ]; then
    echo "Warning: Could not find EverQuest folder, checking for alternate structure..."
    # Might be directly in extracted folder
    EQ_SOURCE="$TEMP_DIR/eq_extracted"
fi

EQ_INSTALL_DIR="$WINEPREFIX/drive_c/Program Files/EverQuest"

echo "Copying game files..."
mkdir -p "$EQ_INSTALL_DIR"
cp -r "$EQ_SOURCE"/* "$EQ_INSTALL_DIR/" 2>/dev/null || cp -r "$TEMP_DIR/eq_extracted"/* "$EQ_INSTALL_DIR/"

echo "Game files installed to: $EQ_INSTALL_DIR"

# Step 4: Download and apply latest P99 patches
echo ""
echo "Step 4/5: Downloading latest P99 patch files..."

if [ ! -f "$TEMP_DIR/p99patches.zip" ]; then
    $DOWNLOAD_CMD "$TEMP_DIR/p99patches.zip" "$P99_PATCHES_URL"
    if [ $? -eq 0 ] && [ -s "$TEMP_DIR/p99patches.zip" ]; then
        echo "Latest P99 patches downloaded!"
    else
        echo "Warning: Could not download latest patches. Using patches from archive."
    fi
fi

if [ -f "$TEMP_DIR/p99patches.zip" ]; then
    echo "Applying latest P99 patches to game directory..."
    unzip -o "$TEMP_DIR/p99patches.zip" -d "$EQ_INSTALL_DIR"
    echo "Latest P99 patches applied!"

    # Verify critical files exist (antivirus sometimes deletes dsetup.dll)
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
else
    echo "Using P99 patches from combined archive (may be older version)"
fi

echo ""
echo "CRITICAL: NEVER run 'eqgame.exe' or patch the game!"
echo "ALWAYS use 'Launch Titanium.exe' to start the game!"

# Step 5: Account creation prompt
echo ""
echo "Step 5/5: Account Registration"
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
    echo "  - Green: Most populated, Velious-locked PvE"
    echo "  - Blue: Established economy, full classic progression PvE"
    echo "  - Red: PvP server (~50 players)"
fi

# Cleanup
echo ""
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

# Installation complete - launcher will auto-detect the game
echo ""
echo "Game installation complete!"

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "Installation directory: $EQ_INSTALL_DIR"
echo ""
echo "Return to the launcher and click Play to start!"
echo "Server selection (Green/Blue/Red) is done in the 'Launch Titanium' window."
echo ""
echo "REMEMBER: NEVER run eqgame.exe or patch the game!"
echo "ALWAYS use 'Launch Titanium.bat' to start!"
echo ""
echo "Project 1999 Resources:"
echo "  Website: https://www.project1999.com"
echo "  Wiki: https://wiki.project1999.com"
echo "  Forums: https://www.project1999.com/forums"
echo ""
echo "Installation complete! The launcher will now detect the game."
echo ""
read -p "Press Enter to finish and close this window..."
exit 0
