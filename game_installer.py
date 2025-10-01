"""
Game installer module
Handles downloading, installing, and configuring MMORPGs with UMU launcher
"""

import os
import subprocess
import logging
import json
from pathlib import Path
from typing import Optional, Callable
import urllib.request
import shutil

class GameInstaller:
    def __init__(self, games_dir: str = None):
        """Initialize game installer"""
        self.games_dir = Path(games_dir) if games_dir else Path.home() / "Games"
        self.games_dir.mkdir(parents=True, exist_ok=True)

        self.config_dir = Path.home() / ".config" / "mmo-launcher"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.installed_games_file = self.config_dir / "installed_games.json"
        self.installed_games = self._load_installed_games()

        # Detect AUR helper
        self.aur_helper = self._detect_aur_helper()

        # Setup logging
        self.log_file = Path("logs/installer.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _detect_aur_helper(self) -> Optional[str]:
        """Detect available AUR helper"""
        for helper in ["yay", "paru", "pikaur", "trizen"]:
            if shutil.which(helper):
                logging.info(f"Detected AUR helper: {helper}")
                return helper
        return None

    def _load_installed_games(self) -> dict:
        """Load list of installed games from config"""
        if self.installed_games_file.exists():
            with open(self.installed_games_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_installed_games(self):
        """Save installed games to config"""
        with open(self.installed_games_file, 'w') as f:
            json.dump(self.installed_games, f, indent=2)

    def is_installed(self, game_id: str) -> bool:
        """Check if game is installed"""
        return game_id in self.installed_games

    def get_game_path(self, game_id: str) -> Optional[Path]:
        """Get installation path for a game"""
        if game_id in self.installed_games:
            return Path(self.installed_games[game_id]['path'])
        return None

    def check_dependencies(self, dependencies: list) -> dict:
        """Check if required dependencies are installed"""
        results = {}

        for dep in dependencies:
            if dep == "umu-launcher":
                results[dep] = shutil.which("umu") is not None or shutil.which("umu-run") is not None
            elif dep == "wine" or dep == "wine-staging":
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

    def download_file(self, url: str, dest: Path, progress_callback: Callable = None):
        """Download a file with progress tracking"""
        if progress_callback:
            progress_callback(f"Downloading from {url}")

        try:
            urllib.request.urlretrieve(url, dest)
            logging.info(f"Downloaded {url} to {dest}")
            if progress_callback:
                progress_callback(f"Download complete: {dest.name}")
            return True
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
                    terminals = ['konsole', 'gnome-terminal', 'xfce4-terminal', 'alacritty', 'kitty', 'xterm']
                    term_cmd = None
                    for term in terminals:
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
                    if progress_callback:
                        progress_callback(f"Installing via Flatpak: {flatpak_id}")

                    result = subprocess.run(
                        ["flatpak", "install", "-y", "flathub", flatpak_id],
                        capture_output=True,
                        text=True
                    )

                    if result.returncode == 0:
                        self.installed_games[game_id] = {
                            'name': game_data['name'],
                            'path': f"flatpak://{flatpak_id}",
                            'install_type': 'flatpak'
                        }
                        self._save_installed_games()
                        return True
                    else:
                        logging.error(f"Flatpak install failed: {result.stderr}")
                        return False
                return False

            elif install_type == "flatpak":
                flatpak_id = game_data['client_download_url'].replace("flatpak://", "")
                if progress_callback:
                    progress_callback(f"Installing via Flatpak: {flatpak_id}")

                result = subprocess.run(
                    ["flatpak", "install", "-y", "flathub", flatpak_id],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    self.installed_games[game_id] = {
                        'name': game_data['name'],
                        'path': f"flatpak://{flatpak_id}",
                        'install_type': 'flatpak'
                    }
                    self._save_installed_games()
                    return True
                else:
                    logging.error(f"Flatpak install failed: {result.stderr}")
                    return False

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
                # Check for umu-run or umu
                umu_cmd = "umu-run" if shutil.which("umu-run") else "umu"

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
                if self.aur_helper:
                    subprocess.run([self.aur_helper, "-R", "--noconfirm", aur_pkg], check=True)
                else:
                    subprocess.run(["sudo", "pacman", "-R", "--noconfirm", aur_pkg], check=True)
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
