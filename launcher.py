"""Entry point for the Linux MMORPG launcher."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

import yaml
from PyQt6.QtWidgets import QApplication

from gui import LauncherApp

CONFIG_FILE = Path("config.yaml")
LOG_FILE = Path("logs/launcher.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def launch_game(name: str) -> None:
    config = load_config()
    games = config.get("games", [])
    game = next((g for g in games if g["name"].lower() == name.lower()), None)
    if not game:
        logging.error("Game %s not found in config", name)
        raise SystemExit(f"Game '{name}' not found in config.yaml")

    try:
        subprocess.Popen(["umu-run", game["path"]])
        logging.info("Launched %s from %s", game["name"], game["path"])
    except Exception as exc:  # pragma: no cover - subprocess failure path
        logging.exception("Failed to launch %s", game["name"])
        raise SystemExit(f"Failed to launch {game['name']}: {exc}")


def run_gui() -> int:
    app = QApplication(sys.argv)
    window = LauncherApp()
    window.show()
    return app.exec()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Linux MMORPG launcher")
    parser.add_argument(
        "game",
        nargs="?",
        help="Launch a game directly by name (uses config.yaml). If omitted, starts the GUI."
    )
    args = parser.parse_args(argv)

    if args.game:
        launch_game(args.game)
        return 0

    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())
