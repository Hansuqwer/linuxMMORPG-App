"""
System dependency installer module
Handles installation of system-level dependencies
"""
import subprocess
import logging
from pathlib import Path

# Constants
LOG_FILE = Path("logs/installer.log")
REQUIRED_PACKAGES = ["python-pyqt6", "umu"]

# Ensure log directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def install_dependencies() -> bool:
    """
    Install required system dependencies via pacman.
    
    Returns:
        bool: True if installation was successful, False otherwise
    """
    logging.info("Installing dependencies...")
    try:
        subprocess.run(
            ["sudo", "pacman", "-S", "--noconfirm"] + REQUIRED_PACKAGES,
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Installation failed with return code {e.returncode}: {e.stderr}")
        return False
    except FileNotFoundError:
        logging.error("pacman not found - this script requires Arch Linux")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during installation: {e}")
        return False


if __name__ == "__main__":
    success = install_dependencies()
    exit(0 if success else 1)
