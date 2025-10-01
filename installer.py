import subprocess
import logging

def install_dependencies():
    logging.info("Installing dependencies...")
    try:
        subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "python-pyqt6", "faugus", "umu"], check=True)
        logging.info("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Installation failed: {e}")

if __name__ == "__main__":
    install_dependencies()
