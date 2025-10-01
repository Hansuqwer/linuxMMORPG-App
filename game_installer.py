"""
Game installer module
Handles downloading, installing, and configuring MMORPGs with UMU launcher
"""

import os
import subprocess
import logging
import json
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import urllib.request
import shutil

# Constants
DEFAULT_GAMES_DIR = Path.home() / "Games"
CONFIG_DIR = Path.home() / ".config" / "mmo-launcher"
INSTALLED_GAMES_FILE = CONFIG_DIR / "installed_games.json"
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "installer.log"

AUR_HELPERS = ["yay", "paru", "pikaur", "trizen"]
TERMINAL_EMULATORS = ["konsole", "gnome-terminal", "xfce4-terminal", "alacritty", "kitty", "xterm"]
UMU_COMMANDS = ["umu-run", "umu"]


class GameInstaller:
    def __init__(self, games_dir: str = None):
        """Initialize game installer"""
        self.games_dir = Path(games_dir) if games_dir else DEFAULT_GAMES_DIR
        self.games_dir.mkdir(parents=True, exist_ok=True)

        self.config_dir = CONFIG_DIR
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.installed_games_file = INSTALLED_GAMES_FILE
        self.installed_games = self._load_installed_games()

        # Detect AUR helper
        self.aur_helper = self._detect_aur_helper()

        # Setup logging
        self.log_file = LOG_FILE
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Auto-detect installed games
        self._auto_detect_games()

    def _detect_aur_helper(self) -> Optional[str]:
        """Detect available AUR helper"""
        for helper in AUR_HELPERS:
            if shutil.which(helper):
                logging.info(f"Detected AUR helper: {helper}")
                return helper
        return None

    def _load_installed_games(self) -> Dict[str, Any]:
        """Load list of installed games from config"""
        if self.installed_games_file.exists():
            try:
                with open(self.installed_games_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse installed games file: {e}")
                return {}
            except Exception as e:
                logging.error(f"Error loading installed games: {e}")
                return {}
        return {}

    def _save_installed_games(self) -> bool:
        """Save installed games to config"""
        try:
            with open(self.installed_games_file, 'w', encoding='utf-8') as f:
                json.dump(self.installed_games, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Failed to save installed games: {e}")
            return False

    def _auto_detect_games(self):
        """Auto-detect installed games in common directories"""
        # Don't re-import games_db at module level to avoid circular dependency
        # We'll import it here when needed
        from games_db import GAMES_DATABASE

        detected_count = 0

        # Check AUR/system packages
        aur_packages = {
            'xivlauncher': 'ffxiv',
            'runescape-launcher': 'rs3',
        }

        for pkg_name, game_id in aur_packages.items():
            if game_id not in self.installed_games:
                # Check if package is installed
                result = subprocess.run(['pacman', '-Q', pkg_name], capture_output=True, text=True)
                if result.returncode == 0:
                    if game_id in GAMES_DATABASE:
                        self.installed_games[game_id] = {
                            'name': GAMES_DATABASE[game_id]['name'],
                            'path': f'aur://{pkg_name}',
                            'install_type': 'aur',
                            'auto_detected': True
                        }
                        detected_count += 1
                        logging.info(f"Auto-detected AUR package: {pkg_name} -> {game_id}")

        # Check flatpak apps
        flatpak_apps = {
            'dev.goats.xivlauncher': 'ffxiv',
            'com.jagex.RuneScape': 'rs3',
        }

        if shutil.which('flatpak'):
            result = subprocess.run(['flatpak', 'list', '--app', '--columns=application'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                installed_flatpaks = result.stdout.strip().split('\n')
                for app_id, game_id in flatpak_apps.items():
                    if game_id not in self.installed_games and app_id in installed_flatpaks:
                        if game_id in GAMES_DATABASE:
                            self.installed_games[game_id] = {
                                'name': GAMES_DATABASE[game_id]['name'],
                                'path': f'flatpak://{app_id}',
                                'install_type': 'flatpak',
                                'auto_detected': True
                            }
                            detected_count += 1
                            logging.info(f"Auto-detected Flatpak: {app_id} -> {game_id}")

        # Scan common game directories for manual installs
        search_dirs = [
            self.games_dir,
            Path.home() / "Games",
            Path.home() / ".wine" / "drive_c" / "Program Files",
            Path.home() / ".wine" / "drive_c" / "Program Files (x86)",
            Path.home() / ".local" / "share" / "bottles",
        ]

        # Define patterns to detect specific games
        # Format: game_id: [primary_exe_pattern, optional_path_marker]
        game_patterns = {
            'rf-altruism': ['RFAltruismLauncher.exe', 'altruism'],
            'rf-haunting': ['RF.exe', 'haunting'],
            'ragnarok-uaro': ['Uaro.exe', 'uaro'],
            'ragnarok-revivalro': ['RevivalRO.exe'],
            'ragnarok-talonro': ['tRO.exe'],
            'ragnarok-originsro': ['Ragnarok.exe', 'origins'],
            'lineage1-l15': ['lineage.exe'],
            'lineage1-l1justice': ['jLauncher.exe'],
            'l2-reborn': ['L2.exe', 'reborn'],
            'l2-classic-club': ['L2.exe', 'classic'],
            'l2-essence': ['L2.exe', 'essence'],
            'everquest-p1999-green': ['eqgame.exe', 'p1999'],
            'everquest-p1999-blue': ['eqgame.exe', 'p1999'],
            'everquest-quarm': ['eqgame.exe', 'quarm'],
            'everquest-ezserver': ['eqgame.exe', 'ezserver'],
        }

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            # Search up to 3 levels deep only
            for game_id, patterns in game_patterns.items():
                if game_id in self.installed_games:
                    continue  # Already tracked

                try:
                    # Limit search depth to 3 levels to avoid scanning entire filesystem
                    found = False
                    for depth in range(4):  # 0, 1, 2, 3 levels
                        if found:
                            break
                        pattern_path = "/".join(["*"] * depth) + "/" + patterns[0] if depth > 0 else patterns[0]

                        for item in search_dir.glob(pattern_path):
                            if item.is_file():
                                # Check if additional pattern markers are present
                                match = True
                                if len(patterns) > 1:
                                    parent_str = str(item.parent).lower()
                                    if not any(p.lower() in parent_str for p in patterns[1:]):
                                        match = False

                                if match and game_id in GAMES_DATABASE:
                                    self.installed_games[game_id] = {
                                        'name': GAMES_DATABASE[game_id]['name'],
                                        'path': str(item.parent),
                                        'install_type': 'manual_download',
                                        'auto_detected': True
                                    }
                                    detected_count += 1
                                    logging.info(f"Auto-detected game: {game_id} at {item.parent}")
                                    found = True
                                    break  # Found this game, move to next
                except Exception as e:
                    logging.debug(f"Error scanning {search_dir}: {e}")
                    continue

        if detected_count > 0:
            self._save_installed_games()
            logging.info(f"Auto-detected {detected_count} games total")

    def is_installed(self, game_id: str) -> bool:
        """Check if game is installed"""
        return game_id in self.installed_games

    def get_game_path(self, game_id: str) -> Optional[Path]:
        """Get installation path for a game"""
        if game_id in self.installed_games:
            path_str = self.installed_games[game_id]['path']
            # Don't return Path for AUR/Flatpak pseudo-paths
            if path_str.startswith('aur://') or path_str.startswith('flatpak://'):
                return None
            return Path(path_str)
        return None

    def check_dependencies(self, dependencies: list) -> dict:
        """Check if required dependencies are installed"""
        results = {}

        for dep in dependencies:
            if dep == "umu-launcher":
                results[dep] = any(shutil.which(cmd) for cmd in UMU_COMMANDS)
            elif dep in ("wine", "wine-staging"):
                results[dep] = shutil.which("wine") is not None
            elif dep == "steam":
                results[dep] = shutil.which("steam") is not None
            elif dep == "flatpak":
                results[dep] = shutil.which("flatpak") is not None
            elif dep == "java":
                results[dep] = shutil.which("java") is not None
            else:
                # For winetricks components, assume they can be installed
                results[dep] = True

        return results

    def _install_flatpak_game(self, game_id: str, flatpak_id: str, game_name: str, 
                              progress_callback: Callable = None) -> bool:
        """
        Helper method to install a game via Flatpak.
        
        Args:
            game_id: Unique game identifier
            flatpak_id: Flatpak application ID
            game_name: Human-readable game name
            progress_callback: Optional callback for progress updates
            
        Returns:
            bool: True if installation was successful
        """
        if progress_callback:
            progress_callback(f"Installing via Flatpak: {flatpak_id}")

        try:
            result = subprocess.run(
                ["flatpak", "install", "-y", "flathub", flatpak_id],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                self.installed_games[game_id] = {
                    'name': game_name,
                    'path': f"flatpak://{flatpak_id}",
                    'install_type': 'flatpak'
                }
                self._save_installed_games()
                if progress_callback:
                    progress_callback("Installation complete!")
                logging.info(f"Installed {game_name} via Flatpak")
                return True
            else:
                logging.error(f"Flatpak install failed: {result.stderr}")
                if progress_callback:
                    progress_callback(f"Flatpak installation failed: {result.stderr}")
                return False
        except FileNotFoundError:
            logging.error("Flatpak not found on system")
            if progress_callback:
                progress_callback("Error: Flatpak is not installed")
            return False
        except Exception as e:
            logging.error(f"Unexpected error installing Flatpak: {e}")
            if progress_callback:
                progress_callback(f"Installation error: {e}")
            return False

    def install_dependencies(self, dependencies: list, progress_callback: Callable = None):
        """Install missing dependencies"""
        missing = []
        dep_check = self.check_dependencies(dependencies)

        for dep, installed in dep_check.items():
            if not installed:
                missing.append(dep)

        if not missing:
            if progress_callback:
                progress_callback("All dependencies already installed")
            return True

        if progress_callback:
            progress_callback(f"Installing dependencies: {', '.join(missing)}")

        # Detect package manager
        if shutil.which("pacman"):
            pkg_manager = "pacman"
        elif shutil.which("apt"):
            pkg_manager = "apt"
        elif shutil.which("dnf"):
            pkg_manager = "dnf"
        else:
            logging.error("No supported package manager found")
            return False

        # Map dependencies to package names
        pkg_map = {
            "pacman": {
                "umu-launcher": "umu",
                "wine": "wine",
                "wine-staging": "wine-staging",
                "steam": "steam",
                "flatpak": "flatpak",
                "java": "jre-openjdk"
            },
            "apt": {
                "umu-launcher": None,  # Needs manual install
                "wine": "wine",
                "wine-staging": "wine-staging",
                "steam": "steam",
                "flatpak": "flatpak",
                "java": "default-jre"
            },
            "dnf": {
                "umu-launcher": None,  # Needs manual install
                "wine": "wine",
                "wine-staging": "wine",
                "steam": "steam",
                "flatpak": "flatpak",
                "java": "java-latest-openjdk"
            }
        }

        packages = []
        for dep in missing:
            if dep in pkg_map[pkg_manager]:
                pkg = pkg_map[pkg_manager][dep]
                if pkg:
                    packages.append(pkg)

        if packages:
            try:
                if pkg_manager == "pacman":
                    cmd = ["sudo", "pacman", "-S", "--noconfirm"] + packages
                elif pkg_manager == "apt":
                    cmd = ["sudo", "apt", "install", "-y"] + packages
                elif pkg_manager == "dnf":
                    cmd = ["sudo", "dnf", "install", "-y"] + packages

                if progress_callback:
                    progress_callback(f"Running: {' '.join(cmd)}")

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    logging.info(f"Dependencies installed: {', '.join(packages)}")
                    if progress_callback:
                        progress_callback("Dependencies installed successfully")
                    return True
                else:
                    logging.error(f"Failed to install dependencies: {result.stderr}")
                    return False

            except Exception as e:
                logging.error(f"Error installing dependencies: {e}")
                return False

        return True

    def download_file(self, url: str, dest: Path, progress_callback: Callable = None) -> bool:
        """
        Download a file with progress tracking.
        
        Args:
            url: URL to download from
            dest: Destination path for the downloaded file
            progress_callback: Optional callback for progress updates
            
        Returns:
            bool: True if download was successful
        """
        if not url or not isinstance(url, str):
            logging.error("Invalid URL provided for download")
            return False
        
        if not url.startswith(('http://', 'https://', 'ftp://')):
            logging.error(f"Invalid URL scheme: {url}")
            if progress_callback:
                progress_callback(f"Invalid URL: {url}")
            return False
        
        if progress_callback:
            progress_callback(f"Downloading from {url}")

        try:
            urllib.request.urlretrieve(url, dest)
            logging.info(f"Downloaded {url} to {dest}")
            if progress_callback:
                progress_callback(f"Download complete: {dest.name}")
            return True
        except urllib.error.URLError as e:
            logging.error(f"URL error downloading {url}: {e}")
            if progress_callback:
                progress_callback(f"Download failed: Network error")
            return False
        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")
            if progress_callback:
                progress_callback(f"Download failed: {e}")
            return False

    def install_game(self, game_id: str, game_data: dict, progress_callback: Callable = None) -> bool:
        """
        Install a game

        Args:
            game_id: Unique game identifier
            game_data: Game metadata from games_db
            progress_callback: Function to call with progress updates
        """
        try:
            if progress_callback:
                progress_callback(f"Starting installation of {game_data['name']}")

            # Check dependencies
            if progress_callback:
                progress_callback("Checking dependencies...")

            dep_results = self.check_dependencies(game_data['dependencies'])
            missing_deps = [dep for dep, installed in dep_results.items() if not installed]

            if missing_deps:
                if progress_callback:
                    progress_callback(f"Installing missing dependencies: {', '.join(missing_deps)}")

                if not self.install_dependencies(game_data['dependencies'], progress_callback):
                    return False

            # Create game directory
            game_dir = self.games_dir / game_id
            game_dir.mkdir(parents=True, exist_ok=True)

            install_type = game_data['install_type']

            if install_type == "native":
                if progress_callback:
                    progress_callback("Native Linux game - please download from official website")
                    progress_callback(f"Download URL: {game_data['client_download_url']}")
                return False

            elif install_type == "steam":
                if progress_callback:
                    progress_callback("Steam game - please install via Steam client")
                    progress_callback(f"Steam URL: {game_data['client_download_url']}")
                return False

            elif install_type == "aur":
                # Try AUR first if on Arch Linux
                if self.aur_helper and 'aur_package' in game_data:
                    aur_pkg = game_data['aur_package']
                    if progress_callback:
                        progress_callback(f"Installing via AUR ({self.aur_helper}): {aur_pkg}")
                        progress_callback("Opening terminal for AUR installation...")

                    # Try to detect available terminal emulator
                    term_cmd = None
                    for term in TERMINAL_EMULATORS:
                        if shutil.which(term):
                            term_cmd = term
                            break

                    if term_cmd:
                        # Open terminal and run AUR install with auto-close
                        if term_cmd == 'konsole':
                            cmd = [term_cmd, '--noclose', '-e', 'sh', '-c', f'{self.aur_helper} -S {aur_pkg}; echo "\nPress Enter to close..."; read']
                        elif term_cmd == 'gnome-terminal':
                            cmd = [term_cmd, '--', 'sh', '-c', f'{self.aur_helper} -S {aur_pkg}; echo "\nPress Enter to close..."; read']
                        elif term_cmd == 'xterm':
                            cmd = [term_cmd, '-hold', '-e', f'{self.aur_helper} -S {aur_pkg}']
                        else:
                            cmd = [term_cmd, '-e', 'sh', '-c', f'{self.aur_helper} -S {aur_pkg}; echo "\nPress Enter to close..."; read']

                        result = subprocess.run(cmd, capture_output=True, text=True)

                        if result.returncode == 0:
                            self.installed_games[game_id] = {
                                'name': game_data['name'],
                                'path': f"aur://{aur_pkg}",
                                'install_type': 'aur'
                            }
                            self._save_installed_games()
                            if progress_callback:
                                progress_callback("Installation complete!")
                            return True
                        else:
                            logging.error(f"AUR install failed in terminal: {result.stderr}")
                            if progress_callback:
                                progress_callback(f"AUR installation cancelled or failed: {result.stderr}\nTrying Flatpak...")
                            # Fall through to Flatpak
                    else:
                        logging.error("No terminal emulator found for AUR installation")
                        if progress_callback:
                            progress_callback("No terminal found, trying Flatpak...")
                        # Fall through to Flatpak
                else:
                    if progress_callback:
                        progress_callback("AUR not available, using Flatpak...")

                # Fallback to Flatpak
                if 'client_download_url' in game_data and game_data['client_download_url'].startswith("flatpak://"):
                    flatpak_id = game_data['client_download_url'].replace("flatpak://", "")
                    return self._install_flatpak_game(game_id, flatpak_id, game_data['name'], progress_callback)
                return False

            elif install_type == "flatpak":
                flatpak_id = game_data['client_download_url'].replace("flatpak://", "")
                return self._install_flatpak_game(game_id, flatpak_id, game_data['name'], progress_callback)

            elif install_type == "manual_download":
                if progress_callback:
                    progress_callback("Manual download required")
                    progress_callback(f"Please download client from: {game_data['client_download_url']}")
                    progress_callback(f"Then extract to: {game_dir}")
                    progress_callback("Installation instructions:")
                    progress_callback(game_data['install_notes'])

                # Save as "pending manual installation"
                self.installed_games[game_id] = {
                    'name': game_data['name'],
                    'path': str(game_dir),
                    'install_type': 'manual_download',
                    'status': 'pending_manual'
                }
                self._save_installed_games()
                return False

            elif install_type == "auto_installer":
                if progress_callback:
                    progress_callback("Downloading game installer...")

                installer_file = game_dir / "installer.exe"

                # Download installer
                if self.download_file(game_data['client_download_url'], installer_file, progress_callback):
                    if progress_callback:
                        progress_callback("Running installer via Wine...")

                    # Run installer with Wine
                    result = subprocess.run(
                        ["wine", str(installer_file)],
                        cwd=game_dir,
                        capture_output=True,
                        text=True
                    )

                    if result.returncode == 0:
                        self.installed_games[game_id] = {
                            'name': game_data['name'],
                            'path': str(game_dir),
                            'install_type': 'auto_installer'
                        }
                        self._save_installed_games()

                        if progress_callback:
                            progress_callback("Installation complete!")
                        return True
                    else:
                        logging.error(f"Installer failed: {result.stderr}")
                        return False

            return False

        except Exception as e:
            logging.error(f"Installation error for {game_id}: {e}")
            if progress_callback:
                progress_callback(f"Installation error: {e}")
            return False

    def launch_game(self, game_id: str, game_data: dict) -> bool:
        """Launch a game using UMU"""
        if game_id not in self.installed_games:
            logging.error(f"Game {game_id} not installed")
            return False

        game_info = self.installed_games[game_id]

        if game_info['install_type'] == 'aur':
            # AUR packages typically install desktop entries or binaries
            # Try to find and launch the executable
            aur_pkg = game_info['path'].replace("aur://", "")
            try:
                # Check if game has a launch command
                if 'launch_command' in game_data:
                    launch_cmd = game_data['launch_command']
                    subprocess.Popen(launch_cmd, shell=True)
                    logging.info(f"Launched {game_data['name']} via AUR package")
                    return True
                else:
                    # Try common executable names
                    if shutil.which(aur_pkg):
                        subprocess.Popen([aur_pkg])
                        logging.info(f"Launched {game_data['name']} via AUR package")
                        return True
                    else:
                        logging.error(f"Executable not found for AUR package: {aur_pkg}")
                        return False
            except Exception as e:
                logging.error(f"Failed to launch AUR package: {e}")
                return False

        elif game_info['install_type'] == 'flatpak':
            flatpak_id = game_info['path'].replace("flatpak://", "")
            try:
                subprocess.Popen(["flatpak", "run", flatpak_id])
                logging.info(f"Launched {game_data['name']} via Flatpak")
                return True
            except Exception as e:
                logging.error(f"Failed to launch via Flatpak: {e}")
                return False

        else:
            # Use UMU to launch
            game_path = Path(game_info['path']) / game_data['executable']

            if not game_path.exists():
                logging.error(f"Game executable not found: {game_path}")
                return False

            try:
                # Find available UMU command
                umu_cmd = None
                for cmd in UMU_COMMANDS:
                    if shutil.which(cmd):
                        umu_cmd = cmd
                        break
                
                if not umu_cmd:
                    logging.error("UMU launcher not found on system")
                    return False

                subprocess.Popen([umu_cmd, str(game_path)])
                logging.info(f"Launched {game_data['name']} via UMU")
                return True
            except Exception as e:
                logging.error(f"Failed to launch via UMU: {e}")
                return False

    def uninstall_game(self, game_id: str) -> bool:
        """Uninstall a game"""
        if game_id not in self.installed_games:
            return False

        game_info = self.installed_games[game_id]

        if game_info['install_type'] == 'aur':
            aur_pkg = game_info['path'].replace("aur://", "")
            try:
                # Open terminal for user to confirm uninstall
                terminals = ['konsole', 'gnome-terminal', 'xfce4-terminal', 'alacritty', 'kitty', 'xterm']
                term_cmd = None
                for term in terminals:
                    if shutil.which(term):
                        term_cmd = term
                        break

                if term_cmd:
                    # Open terminal and run uninstall
                    helper = self.aur_helper or "sudo pacman"
                    if term_cmd == 'konsole':
                        cmd = [term_cmd, '-e', 'sh', '-c', f'{helper} -R {aur_pkg}; echo "\nPress Enter to close..."; read; exit']
                    elif term_cmd == 'gnome-terminal':
                        cmd = [term_cmd, '--', 'sh', '-c', f'{helper} -R {aur_pkg}; echo "\nPress Enter to close..."; read; exit']
                    elif term_cmd == 'xterm':
                        cmd = [term_cmd, '-e', 'sh', '-c', f'{helper} -R {aur_pkg}; echo "\nPress Enter to close..."; read; exit']
                    else:
                        cmd = [term_cmd, '-e', 'sh', '-c', f'{helper} -R {aur_pkg}; echo "\nPress Enter to close..."; read; exit']

                    result = subprocess.run(cmd)

                    # Check if package was actually removed
                    check = subprocess.run(['pacman', '-Q', aur_pkg], capture_output=True)
                    if check.returncode != 0:
                        # Package not found, so it was uninstalled
                        del self.installed_games[game_id]
                        self._save_installed_games()
                        logging.info(f"Uninstalled AUR package: {game_id}")
                        return True
                    else:
                        logging.info(f"AUR uninstall cancelled by user: {game_id}")
                        return False
                else:
                    logging.error("No terminal emulator found for AUR uninstall")
                    return False
            except Exception as e:
                logging.error(f"Failed to uninstall AUR package: {e}")
                return False

        elif game_info['install_type'] == 'flatpak':
            flatpak_id = game_info['path'].replace("flatpak://", "")
            try:
                subprocess.run(["flatpak", "uninstall", "-y", flatpak_id], check=True)
            except Exception as e:
                logging.error(f"Failed to uninstall Flatpak: {e}")
                return False
        else:
            # Remove game directory
            game_path = Path(game_info['path'])
            if game_path.exists():
                shutil.rmtree(game_path)

        # Remove from installed games
        del self.installed_games[game_id]
        self._save_installed_games()

        logging.info(f"Uninstalled game: {game_id}")
        return True
