#!/bin/bash

# EverQuest Titanium Auto-Installer for Project 1999
# - Guides the user through registration
# - Mounts Titanium ISO images for installation
# - Applies the latest Project 1999 patch files
# - Launches the game via Launch Titanium.bat

set -e

# Accept game_id parameter from installer (kept for compatibility)
GAME_ID="${1:-everquest-p1999}"

# Detect Downloads folder (handles different languages)
DOWNLOADS_DIR="$HOME/Downloads"
if [ -d "$HOME/Hämtningar" ]; then
    DOWNLOADS_DIR="$HOME/Hämtningar"
elif [ -d "$HOME/Téléchargements" ]; then
    DOWNLOADS_DIR="$HOME/Téléchargements"
elif [ -d "$HOME/Descargas" ]; then
    DOWNLOADS_DIR="$HOME/Descargas"
elif [ -d "$HOME/下载" ]; then
    DOWNLOADS_DIR="$HOME/下载"
fi

TEMP_DIR="/tmp/p99_install"
ISO_DIR="$TEMP_DIR/isos"
MOUNT_BASE="$TEMP_DIR/mounts"
TITANIUM_ZIP="$DOWNLOADS_DIR/EverQuest_Titanium.zip"
REGISTRATION_URL="https://www.project1999.com/account/?Play"
PATCH_FORUM_URL="https://www.project1999.com/forums/forumdisplay.php?f=11"
DEFAULT_PATCH_DIRS=("$DOWNLOADS_DIR" "$HOME/Download" "$HOME")
PATCH_PATTERNS=("P99Files" "Project1999Files")
DRIVE_LETTERS=("d:" "e:" "f:" "g:" "h:")
DEFAULT_TITANIUM_DIRS=(
    "$DOWNLOADS_DIR"
    "$HOME/Download"
    "$HOME"
)
TITANIUM_FILENAMES=(
    "EverQuest_Titanium.zip"
    "EverQuest Titanium.zip"
    "EverQuest-Titanium.zip"
    "EQ_Titanium.zip"
    "EverQuest.zip"
)

DEFAULT_PREFIX="$HOME/Games/umu/everquest-p1999/default"
export WINEPREFIX="${WINEPREFIX:-$DEFAULT_PREFIX}"
export PROTONPATH="${PROTONPATH:-GE-Proton}"
SKIP_INSTALL="${SKIP_INSTALL:-0}"

# Track mounted ISO directories for cleanup
MOUNT_POINTS=()
MOUNT_METHODS=()

cleanup_mounts() {
    for idx in "${!MOUNT_POINTS[@]}"; do
        local mountpoint="${MOUNT_POINTS[$idx]}"
        local method="${MOUNT_METHODS[$idx]}"
        if [ -z "$mountpoint" ]; then
            continue
        fi

        case "$method" in
            fuseiso)
                fuseiso -u "$mountpoint" >/dev/null 2>&1 || fusermount -u "$mountpoint" >/dev/null 2>&1 || true
                ;;
            sudo)
                sudo umount "$mountpoint" >/dev/null 2>&1 || true
                ;;
            root)
                umount "$mountpoint" >/dev/null 2>&1 || true
                ;;
            *)
                umount "$mountpoint" >/dev/null 2>&1 || sudo umount "$mountpoint" >/dev/null 2>&1 || true
                ;;
        esac

        rmdir "$mountpoint" >/dev/null 2>&1 || true
    done

    MOUNT_POINTS=()
    MOUNT_METHODS=()

    # Clean up Wine drive mappings
    if [ -n "${WINEPREFIX:-}" ]; then
        for drive in "${DRIVE_LETTERS[@]}"; do
            rm -f "$WINEPREFIX/dosdevices/$drive" 2>/dev/null || true
        done
    fi
}

cleanup() {
    cleanup_mounts
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

prompt_open_registration() {
    echo ""
    echo "You must create both a forum account and a login server account before playing."
    read -r -p "Open the Project 1999 account registration page in your browser now? [y/N]: " open_reg
    if [[ "$open_reg" =~ ^[Yy]$ ]]; then
        if command -v xdg-open >/dev/null 2>&1; then
            xdg-open "$REGISTRATION_URL" >/dev/null 2>&1 &
            echo "Opened $REGISTRATION_URL in your default browser."
        else
            echo "Please open $REGISTRATION_URL manually to create your account."
        fi
    fi
}

auto_detect_patch() {
    local newest_file=""
    local newest_mtime=0

    shopt -s nullglob
    for directory in "${DEFAULT_PATCH_DIRS[@]}"; do
        [ -d "$directory" ] || continue

        for pattern in "${PATCH_PATTERNS[@]}"; do
            for candidate in "$directory"/${pattern}*.zip; do
                [ -f "$candidate" ] || continue

                local mtime
                mtime=$(stat -c %Y "$candidate" 2>/dev/null || stat -f %m "$candidate" 2>/dev/null || echo 0)

                if [ "$mtime" -gt "$newest_mtime" ]; then
                    newest_mtime="$mtime"
                    newest_file="$candidate"
                fi
            done
        done
    done
    shopt -u nullglob

    echo "$newest_file"
}

check_patch_url() {
    local url="$1"
    if command -v curl >/dev/null 2>&1; then
        if curl -sI -H "User-Agent: Mozilla/5.0" "$url" | head -n 1 | grep -q "200"; then
            return 0
        fi
    elif command -v wget >/dev/null 2>&1; then
        if wget --spider -q "$url"; then
            return 0
        fi
    fi
    return 1
}

download_latest_patch() {
    local dest=""
    local versions=$(seq 120 -1 40)
    local url_base="https://www.project1999.com/files"
    local patterns=("P99FilesV%02d.zip" "P99Filesv%02d.zip" "Project1999FilesV%02d.zip" "Project1999Filesv%02d.zip")

    for version in $versions; do
        for pattern in "${patterns[@]}"; do
            local filename
            filename=$(printf "$pattern" "$version")
            local url="$url_base/$filename"
            if check_patch_url "$url"; then
                echo "Found Project 1999 patch archive: $filename"
                dest="$TEMP_DIR/$filename"
                if [ -f "$dest" ] && [ -s "$dest" ]; then
                    echo "Using previously downloaded patch: $dest"
                    echo "$dest"
                    return 0
                fi
                echo "Downloading latest Project 1999 patch (version $version)..."
                if $DOWNLOAD_CMD "$dest" "$url"; then
                    echo "Patch downloaded to: $dest"
                    echo "$dest"
                    return 0
                else
                    echo "Warning: Failed to download $filename"
                fi
            fi
        done
    done

    return 1
}

find_existing_titanium_zip() {
    for directory in "${DEFAULT_TITANIUM_DIRS[@]}"; do
        [ -d "$directory" ] || continue
        for filename in "${TITANIUM_FILENAMES[@]}"; do
            local candidate="$directory/$filename"
            if [ -f "$candidate" ] && [ -s "$candidate" ]; then
                echo "$candidate"
                return 0
            fi
        done
    done

    local temp_candidate="$TEMP_DIR/EverQuest_Titanium.zip"
    if [ -f "$temp_candidate" ] && [ -s "$temp_candidate" ]; then
        echo "$temp_candidate"
        return 0
    fi

    echo ""
    return 1
}

install_with_package_manager() {
    local package="$1"
    local sudo_cmd="sudo"

    if [ "$(id -u)" -eq 0 ]; then
        sudo_cmd=""
    elif ! command -v sudo >/dev/null 2>&1; then
        echo "sudo not found. Please run this script as root to install packages automatically."
        return 1
    fi

    if command -v pacman >/dev/null 2>&1; then
        $sudo_cmd pacman -S --noconfirm "$package"
    elif command -v yay >/dev/null 2>&1; then
        yay -S --noconfirm "$package"
    elif command -v paru >/dev/null 2>&1; then
        paru -S --noconfirm "$package"
    elif command -v apt-get >/dev/null 2>&1; then
        $sudo_cmd apt-get update
        $sudo_cmd apt-get install -y "$package"
    elif command -v dnf >/dev/null 2>&1; then
        $sudo_cmd dnf install -y "$package"
    elif command -v zypper >/dev/null 2>&1; then
        $sudo_cmd zypper install -y "$package"
    else
        return 1
    fi

    return 0
}

ensure_fuseiso() {
    if command -v fuseiso >/dev/null 2>&1; then
        return 0
    fi

    echo ""
    echo "fuseiso not detected. It is required to continue with the Project 1999 installation."
    read -r -p "Install fuseiso now? [y/N]: " install_fuseiso
    if [[ ! "$install_fuseiso" =~ ^[Yy]$ ]]; then
        echo "Cannot continue without fuseiso. Please install it manually and re-run this script."
        exit 1
    fi

    echo "Attempting to install fuseiso..."
    if install_with_package_manager "fuseiso"; then
        if command -v fuseiso >/dev/null 2>&1; then
            echo "fuseiso installed successfully."
            return 0
        fi
    fi

    echo "Failed to install fuseiso automatically. Please install it manually and re-run the script."
    exit 1
}

mount_iso() {
    local iso="$1"
    local target="$2"

    mkdir -p "$target"

    fuseiso -p "$iso" "$target"
    MOUNT_POINTS+=("$target")
    MOUNT_METHODS+=("fuseiso")
    return 0
}

detect_eq_dir() {
    # Check standard locations without using slow find commands
    local default_dir="$WINEPREFIX/drive_c/EverQuest"
    if [ -d "$default_dir" ]; then
        echo "$default_dir"
        return 0
    fi

    # Check Program Files locations
    if [ -d "$WINEPREFIX/drive_c/Program Files/EverQuest" ]; then
        echo "$WINEPREFIX/drive_c/Program Files/EverQuest"
        return 0
    fi

    if [ -d "$WINEPREFIX/drive_c/Program Files (x86)/EverQuest" ]; then
        echo "$WINEPREFIX/drive_c/Program Files (x86)/EverQuest"
        return 0
    fi

    echo ""
    return 1
}

find_eqgame_exe() {
    local search_root="$1"
    local candidate=""

    # Check common locations directly without slow find
    if [ -f "$search_root/eqgame.exe" ]; then
        echo "$search_root/eqgame.exe"
        return 0
    fi

    if [ -f "$search_root/EQLite/eqgame.exe" ]; then
        echo "$search_root/EQLite/eqgame.exe"
        return 0
    fi

    # If not found, do a quick limited find in the EQ directory only
    if [ -d "$search_root" ]; then
        candidate=$(find "$search_root" -maxdepth 3 -type f -iname "eqgame.exe" 2>/dev/null | head -n 1)
        if [ -n "$candidate" ]; then
            echo "$candidate"
            return 0
        fi
    fi

    echo ""
}

echo "=== Project 1999 EverQuest Titanium Auto-Installer ==="
echo ""

mkdir -p "$ISO_DIR" "$MOUNT_BASE"

echo "Checking for required tools..."
MISSING_TOOLS=""

if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
    MISSING_TOOLS="$MISSING_TOOLS curl/wget"
fi

if ! command -v unzip >/dev/null 2>&1; then
    MISSING_TOOLS="$MISSING_TOOLS unzip"
fi

if [ -n "$MISSING_TOOLS" ]; then
    echo "Error: Missing required tools:$MISSING_TOOLS"
    echo ""
    echo "Install with: sudo pacman -S unzip curl  # or your distro equivalents"
    read -p "Press Enter to exit..."
    exit 1
fi

if [ "$SKIP_INSTALL" != "1" ]; then
    ensure_fuseiso
fi

DOWNLOAD_CMD="wget -O"
if ! command -v wget >/dev/null 2>&1; then
    DOWNLOAD_CMD="curl -L -o"
fi

if [ "$SKIP_INSTALL" != "1" ]; then
    prompt_open_registration

    echo ""
    echo "Step 1/6: Locating EverQuest Titanium archive..."
    if [ ! -f "$TITANIUM_ZIP" ]; then
        detected_zip="$(find_existing_titanium_zip)"
        if [ -n "$detected_zip" ]; then
            TITANIUM_ZIP="$detected_zip"
            echo "Found existing EverQuest Titanium archive at: $TITANIUM_ZIP"
        fi
    fi

    if [ ! -f "$TITANIUM_ZIP" ]; then
        echo ""
        echo "EverQuest Titanium ZIP not found at: $TITANIUM_ZIP"
        read -r -p "Enter path to EverQuest_Titanium.zip (or press Enter to download automatically): " user_path

        if [ -n "$user_path" ] && [ -f "$user_path" ]; then
            TITANIUM_ZIP="$user_path"
        else
            echo ""
            DOWNLOAD_TARGET="$TEMP_DIR/EverQuest_Titanium.zip"
            if [ -f "$DOWNLOAD_TARGET" ] && [ -s "$DOWNLOAD_TARGET" ]; then
                echo "Found existing EverQuest Titanium download at: $DOWNLOAD_TARGET"
                echo "Skipping download step."
            else
                echo "Downloading EverQuest Titanium (approximately 3.4 GB)..."
                echo "This can take a while depending on your connection."
                $DOWNLOAD_CMD "$DOWNLOAD_TARGET" "https://archive.org/download/EverQuestTitanium/EverQuest%20Titanium.zip"
                echo "Download complete."
            fi
            TITANIUM_ZIP="$DOWNLOAD_TARGET"
        fi
    fi

    echo "Using Titanium archive: $TITANIUM_ZIP"

    echo ""
    echo "Step 2/6: Extracting ISO images..."
    unzip -j "$TITANIUM_ZIP" "*.iso" -d "$ISO_DIR"
    echo "Extracted ISO files:"
    ls "$ISO_DIR"

    echo ""
    echo "Step 3/6: Mounting ISOs to loop devices..."
    for i in 1 2 3 4 5; do
        iso_path="$ISO_DIR/EQ_TITANIUM_CD${i}.iso"
        if [ ! -f "$iso_path" ]; then
            echo "Error: Missing $iso_path. Ensure the Titanium archive is complete."
            exit 1
        fi

        mount_point="$MOUNT_BASE/cd$i"
        echo "Mounting CD$i..."
        mount_iso "$iso_path" "$mount_point"
    done

    echo ""
    echo "Step 4/6: Mapping mounted CDs to Wine drive letters..."

    mkdir -p "$WINEPREFIX/dosdevices"

    for i in 1 2 3 4 5; do
        idx=$((i - 1))
        drive="${DRIVE_LETTERS[$idx]}"
        mount_point="$MOUNT_BASE/cd$i"

        rm -f "$WINEPREFIX/dosdevices/$drive"
        ln -s "$mount_point" "$WINEPREFIX/dosdevices/$drive"
        echo "  CD$i mounted at $drive"
    done

    echo ""
    echo "Step 5/6: Launching EverQuest Titanium installer..."
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                        IMPORTANT!                              ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║  Install Location: C:\\EverQuest                               ║"
    echo "║                                                                ║"
    echo "║  DO NOT install to:                                            ║"
    echo "║    - C:\\Program Files\\...                                    ║"
    echo "║    - C:\\Program Files (x86)\\...                              ║"
    echo "║                                                                ║"
    echo "║  Use EXACTLY: C:\\EverQuest                                    ║"
    echo "║                                                                ║"
    echo "║  Mounted CD drives:                                            ║"
    echo "║    D: -> CD1  |  E: -> CD2  |  F: -> CD3                       ║"
    echo "║    G: -> CD4  |  H: -> CD5                                     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    read -p "Press Enter to start setup.exe from CD1..."

    (cd "$MOUNT_BASE/cd1" && WINEPREFIX="$WINEPREFIX" PROTONPATH="$PROTONPATH" umu-run setup.exe)

    echo ""
    echo "Installation process completed. ISOs remain mounted for verification."
    echo ""
    read -p "Press Enter to continue to patch download..."
else
    echo ""
    echo "Skip flag detected (SKIP_INSTALL=1). Reusing existing EverQuest installation."
fi

EQ_DIR="$(detect_eq_dir)"
while [ -z "$EQ_DIR" ]; do
    echo ""
    echo "Could not automatically locate your EverQuest installation."
    read -r -p "Enter the full path to your EverQuest directory (inside the Wine prefix): " manual_eq_dir
    if [ -d "$manual_eq_dir" ]; then
        EQ_DIR="$manual_eq_dir"
    else
        echo "Directory not found: $manual_eq_dir"
    fi
done

EQ_GAME_EXE="$(find_eqgame_exe "$EQ_DIR")"
if [ -z "$EQ_GAME_EXE" ]; then
    echo "Error: Could not locate eqgame.exe inside the Wine prefix."
    echo "Verify that EverQuest Titanium was installed correctly and try again."
    exit 1
fi
EQ_GAME_DIR="$(dirname "$EQ_GAME_EXE")"
export EQ_BASE="$EQ_DIR"
export EQ_TARGET="$EQ_GAME_EXE"

if [[ "$EQ_GAME_EXE" == "$EQ_DIR/"* ]]; then
    EQ_GAME_RELATIVE="${EQ_GAME_EXE#$EQ_DIR/}"
else
    EQ_GAME_RELATIVE=$(python3 - <<'PY' 2>/dev/null || true
import os
import sys
base = os.environ.get("EQ_BASE", "")
target = os.environ.get("EQ_TARGET", "")
if base and target:
    try:
        rel = os.path.relpath(target, base)
        if rel == ".":
            rel = os.path.basename(target)
        sys.stdout.write(rel)
    except Exception:
        pass
PY
)
fi
if [ -z "$EQ_GAME_RELATIVE" ] || [ "$EQ_GAME_RELATIVE" = "$EQ_GAME_EXE" ]; then
    EQ_GAME_RELATIVE="$(basename "$EQ_GAME_EXE")"
fi
EQ_GAME_REL_WIN=$(printf '%s\n' "$EQ_GAME_RELATIVE" | sed 's#/#\\#g')
EQ_GAME_NAME="$(basename "$EQ_GAME_EXE")"
EQ_GAME_REL_DIR=""
EQ_GAME_REL_DIR_WIN=""

if [[ "$EQ_GAME_RELATIVE" == */* ]]; then
    EQ_GAME_REL_DIR="${EQ_GAME_RELATIVE%/*}"
    EQ_GAME_REL_DIR_WIN=$(printf '%s\n' "$EQ_GAME_REL_DIR" | sed 's#/#\\#g')
fi
unset EQ_BASE EQ_TARGET

echo ""
echo "Step 6/6: Applying latest Project 1999 patch files..."
PATCH_ZIP="$(auto_detect_patch)"

if [ -z "$PATCH_ZIP" ]; then
    PATCH_ZIP="$(download_latest_patch || true)"
fi

if [ -n "$PATCH_ZIP" ]; then
    read -r -p "Use detected patch archive '$PATCH_ZIP'? [Y/n]: " use_detected
    if [[ "$use_detected" =~ ^[Nn]$ ]]; then
        PATCH_ZIP=""
    fi
fi

while [ -z "$PATCH_ZIP" ]; do
    echo ""
    echo "Download the latest patch from: $PATCH_FORUM_URL"
    read -r -p "Enter path to the Project 1999 patch zip (P99Files*.zip) or press Enter to auto-download: " patch_input
    if [ -z "$patch_input" ]; then
        PATCH_ZIP="$(download_latest_patch || true)"
        if [ -n "$PATCH_ZIP" ]; then
            echo "Using downloaded patch: $PATCH_ZIP"
        else
            echo "Auto-download failed. Please provide a local patch archive."
        fi
    elif [ -f "$patch_input" ]; then
        PATCH_ZIP="$patch_input"
    else
        echo "File not found: $patch_input"
    fi
done

echo ""
echo "Extracting patch archive to $EQ_DIR ..."
if unzip -o "$PATCH_ZIP" -d "$EQ_DIR" >/dev/null; then
    echo "Patch files applied successfully to $EQ_DIR."
    if [ "$EQ_GAME_DIR" != "$EQ_DIR" ]; then
        echo "Mirroring patch files into active game directory ($EQ_GAME_DIR)..."
        if unzip -o "$PATCH_ZIP" -d "$EQ_GAME_DIR" >/dev/null; then
            echo "Patch files applied successfully to $EQ_GAME_DIR."
        else
            echo "Warning: Failed to apply patch files inside $EQ_GAME_DIR."
        fi
    fi
else
    echo "Failed to apply patch files from $PATCH_ZIP"
    exit 1
fi

echo ""
echo "Removing obsolete live files required by Project 1999..."
for extra in arena.eqg arena_EnvironmentEmitters.txt lavastorm.eqg nektulos.eqg Nektulos_EnvironmentEmitters.txt; do
    rm -f "$EQ_DIR/$extra" 2>/dev/null || true
    if [ "$EQ_GAME_DIR" != "$EQ_DIR" ]; then
        rm -f "$EQ_GAME_DIR/$extra" 2>/dev/null || true
    fi
done

echo "Ensuring Windows-compatible casing for critical files..."
for target_dir in "$EQ_DIR" "$EQ_GAME_DIR"; do
    [ -d "$target_dir" ] || continue
    if [ -f "$target_dir/dsetup.dll" ]; then
        mv -f "$target_dir/dsetup.dll" "$target_dir/DSETUP.dll"
        echo "  Renamed $target_dir/dsetup.dll -> DSETUP.dll"
    fi
done

echo ""
echo "Updating Launch Titanium.bat to ensure patchme flag..."
LAUNCH_BAT="$EQ_DIR/Launch Titanium.bat"
cat <<EOF > "$LAUNCH_BAT"
@echo off
cd /d "%~dp0"
EOF

if [ -n "$EQ_GAME_REL_DIR_WIN" ]; then
    cat <<EOF >> "$LAUNCH_BAT"
IF EXIST "%~dp0\$EQ_GAME_REL_WIN" (
    start "" /d "%~dp0\$EQ_GAME_REL_DIR_WIN" "$EQ_GAME_NAME" patchme
) ELSE (
    start "" "$EQ_GAME_REL_WIN" patchme
)
EOF
else
    cat <<EOF >> "$LAUNCH_BAT"
start "" "$EQ_GAME_NAME" patchme
EOF
fi

echo "Creating Linux helper launcher (launch_p99.sh)..."
LINUX_LAUNCHER="$EQ_DIR/launch_p99.sh"
EQ_GAME_EXE_PATH="$EQ_GAME_EXE"
EQ_WINEPREFIX_PATH="$WINEPREFIX"
python3 - <<'PY'
import os
from pathlib import Path

launcher_path = Path(os.environ['LINUX_LAUNCHER'])
game_exe = os.environ['EQ_GAME_EXE_PATH']
wineprefix = os.environ['EQ_WINEPREFIX_PATH']
content = f"""#!/bin/bash
set -e
GAME_EXE="{game_exe}"
GAME_DIR="$(cd "$(dirname "$GAME_EXE")" && pwd)"
if command -v umu-run >/dev/null 2>&1; then
    LAUNCH_CMD="umu-run"
elif command -v umu >/dev/null 2>&1; then
    LAUNCH_CMD="umu"
else
    LAUNCH_CMD="wine"
fi
export WINEPREFIX="{wineprefix}"
export PROTONPATH="GE-Proton"
cd "$GAME_DIR"
exec "$LAUNCH_CMD" "$GAME_EXE" patchme
"""
launcher_path.write_text(content, encoding="utf-8")
PY
chmod +x "$LINUX_LAUNCHER"

echo "Registering installation with Linux MMORPG Launcher..."
if command -v python3 >/dev/null 2>&1; then
    GAME_DIR_PATH="$EQ_DIR" CLIENT_PATH="$LINUX_LAUNCHER" WINDOWS_LAUNCHER="$LAUNCH_BAT" PREFIX_PATH="$WINEPREFIX" CLIENT_DIR_PATH="$EQ_GAME_DIR" CLIENT_EXEC_PATH="$EQ_GAME_EXE" python3 - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

game_dir = Path(os.environ.get("GAME_DIR_PATH", ""))
client_path = os.environ.get("CLIENT_PATH", "")
prefix_path = os.environ.get("PREFIX_PATH", "")
windows_launcher = os.environ.get("WINDOWS_LAUNCHER", "")
client_dir_env = os.environ.get("CLIENT_DIR_PATH", "")
client_dir = Path(client_dir_env) if client_dir_env else game_dir
game_executable = os.environ.get("CLIENT_EXEC_PATH", "")

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

data["everquest-p1999"] = {
    "name": "EverQuest - Project 1999",
    "path": str(game_dir),
    "install_type": "manual_download",
    "status": "installed",
    "prefix": prefix_path,
    "client_exe": client_path,
    "client_dir": str(client_dir),
    "game_executable": game_executable,
    "windows_launcher": windows_launcher,
    "updated_at": datetime.now(timezone.utc).isoformat()
}

installed_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("✓ Registered installation metadata")
PY
else
    echo "Python3 not found; skipping launcher registration."
fi

echo ""
echo "Optional: launch Project 1999 now using patchme."
read -r -p "Launch EverQuest Titanium now? [y/N]: " launch_now
if [[ "$launch_now" =~ ^[Yy]$ ]]; then
    echo "Starting EverQuest with patchme argument..."
    if ! (cd "$EQ_GAME_DIR" && WINEPREFIX="$WINEPREFIX" PROTONPATH="$PROTONPATH" umu-run "$EQ_GAME_EXE" patchme); then
        echo ""
        echo "Launch failed. Try running:"
        echo "  WINEPREFIX=\"$WINEPREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$EQ_GAME_EXE\" patchme"
    fi
fi

echo ""
echo "=== Installation Complete! ==="
echo "Launch options:"
echo "  • Use the Linux launcher (auto-detected entry)."
echo "  • Run directly: $LINUX_LAUNCHER"
echo "  • Or run in Windows prefix: WINEPREFIX=\"$WINEPREFIX\" PROTONPATH=\"GE-Proton\" umu-run \"$EQ_GAME_EXE\" patchme"
echo ""
read -p "Press Enter to finish and close this window..."
exit 0
