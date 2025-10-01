import subprocess
import yaml
import logging
from pathlib import Path

CONFIG_FILE = Path("config.yaml")
LOG_FILE = Path("logs/launcher.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def launch_game(name):
    config = load_config()
    game = next((g for g in config["games"] if g["name"] == name), None)
    if not game:
        logging.error(f"Game {name} not found in config")
        return
    try:
        subprocess.Popen(["umu-run", game["path"]])
        logging.info(f"Launched {game['name']} from {game['path']}")
    except Exception as e:
        logging.error(f"Failed to launch {game['name']}: {e}")
