"""
Game launcher module
Handles game launching with proper error handling
"""
import subprocess
import yaml
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Constants
CONFIG_FILE = Path("config.yaml")
LOG_FILE = Path("logs/launcher.log")
UMU_COMMANDS = ["umu-run", "umu"]

# Ensure log directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config() -> Optional[Dict[str, Any]]:
    """Load configuration from YAML file with error handling."""
    try:
        if not CONFIG_FILE.exists():
            logging.error(f"Configuration file not found: {CONFIG_FILE}")
            return None
        
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if not config or "games" not in config:
                logging.error("Invalid configuration: missing 'games' key")
                return None
            return config
    except yaml.YAMLError as e:
        logging.error(f"Failed to parse configuration file: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error loading configuration: {e}")
        return None


def find_umu_executable() -> Optional[str]:
    """Find available UMU executable."""
    import shutil
    for cmd in UMU_COMMANDS:
        if shutil.which(cmd):
            return cmd
    return None


def launch_game(name: str) -> bool:
    """
    Launch a game by name.
    
    Args:
        name: Name of the game to launch
        
    Returns:
        bool: True if launch was successful, False otherwise
    """
    config = load_config()
    if not config:
        return False
    
    game = next((g for g in config["games"] if g["name"] == name), None)
    if not game:
        logging.error(f"Game '{name}' not found in configuration")
        return False
    
    if "path" not in game:
        logging.error(f"Game '{name}' missing 'path' in configuration")
        return False
    
    umu_cmd = find_umu_executable()
    if not umu_cmd:
        logging.error("UMU launcher not found. Please install 'umu' or 'umu-run'")
        return False
    
    try:
        subprocess.Popen([umu_cmd, game["path"]])
        logging.info(f"Launched {game['name']} from {game['path']}")
        return True
    except FileNotFoundError:
        logging.error(f"Game executable not found: {game['path']}")
        return False
    except Exception as e:
        logging.error(f"Failed to launch {game['name']}: {e}")
        return False
