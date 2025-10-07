#!/bin/bash

# Project Quarm Downloader Script
# This script downloads the necessary files for Project Quarm (EverQuest private server)

set -e

INSTALL_DIR="${1:-$HOME/Games/ProjectQuarm}"
TEMP_DIR="/tmp/quarm_download"

echo "=== Project Quarm Downloader ==="
echo "Install directory: $INSTALL_DIR"
echo ""

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$TEMP_DIR"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
if ! command_exists wget && ! command_exists curl; then
    echo "Error: Either wget or curl is required"
    exit 1
fi

DOWNLOAD_CMD="wget -O"
if ! command_exists wget; then
    DOWNLOAD_CMD="curl -L -o"
fi

# Download Windows Client (Google Drive)
echo "Downloading Project Quarm Windows Client..."
echo "Note: Google Drive links require manual download or gdown tool"
if command_exists gdown; then
    gdown "https://drive.google.com/uc?id=1qoBktDeJMJKPBr-EZxub1vspJhz11i1y" -O "$TEMP_DIR/quarm_client.zip"
else
    echo "Warning: 'gdown' not found. Please install with: pip install gdown"
    echo "Then manually download from: https://drive.google.com/file/d/1qoBktDeJMJKPBr-EZxub1vspJhz11i1y/edit"
    echo "Save to: $TEMP_DIR/quarm_client.zip"
    read -p "Press Enter once downloaded, or Ctrl+C to cancel..."
fi

# Extract client
if [ -f "$TEMP_DIR/quarm_client.zip" ]; then
    echo "Extracting client files..."
    unzip -q "$TEMP_DIR/quarm_client.zip" -d "$INSTALL_DIR"
    echo "Client extracted to $INSTALL_DIR"
fi

# Download Zeal (latest release)
echo ""
echo "Downloading Zeal..."
ZEAL_URL=$(curl -s https://api.github.com/repos/CoastalRedwood/Zeal/releases/latest | grep "browser_download_url.*zip" | cut -d '"' -f 4)
if [ -n "$ZEAL_URL" ]; then
    $DOWNLOAD_CMD "$TEMP_DIR/zeal.zip" "$ZEAL_URL"
    echo "Extracting Zeal..."
    unzip -q "$TEMP_DIR/zeal.zip" -d "$INSTALL_DIR/Zeal"
    echo "Zeal installed"
fi

# Download dgVoodoo config
echo ""
echo "Downloading dgVoodoo configuration..."
$DOWNLOAD_CMD "$INSTALL_DIR/dgVoodoo.conf" "https://www.dropbox.com/scl/fi/ltqgx3prylelv74q0zu30/dgVoodoo.conf?rlkey=any&dl=1"

# Instructions for Discord files
echo ""
echo "=== Additional Steps Required ==="
echo "1. Join Project Quarm Discord: https://projectquarm.com/"
echo "2. Navigate to #server-files channel"
echo "3. Download the following files:"
echo "   - pq_files_[date].zip (latest patch files)"
echo "   - QuarmPatcher.zip"
echo "4. Extract these files to: $INSTALL_DIR"
echo ""
echo "=== Installation Summary ==="
echo "Install directory: $INSTALL_DIR"
echo "Client files: Downloaded"
echo "Zeal: Downloaded"
echo "dgVoodoo config: Downloaded"
echo ""
echo "Next steps:"
echo "1. Complete Discord file downloads (see above)"
echo "2. Run with Wine/Proton or configure in Lutris"
echo "3. Launch eqgame.exe"
echo ""
echo "Temp files location: $TEMP_DIR"
echo "Run 'rm -rf $TEMP_DIR' to clean up temporary files"
