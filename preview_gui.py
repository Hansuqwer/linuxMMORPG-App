"""Capture static previews of the Launcher UI without needing a running display."""

import os
from pathlib import Path

# Ensure we can render without a window server (CI/terminal environments)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import sys
from PyQt6.QtWidgets import QApplication

from gui import LauncherApp


def capture_state(window: LauncherApp, dest: Path):
    pixmap = window.grab()
    pixmap.save(str(dest))


def main() -> int:
    app = QApplication(sys.argv)
    window = LauncherApp()
    window.show()
    for _ in range(3):
        app.processEvents()

    output_dir = Path("assets/previews")
    output_dir.mkdir(parents=True, exist_ok=True)

    capture_state(window, output_dir / "expert_launcher_library.png")

    if window.games_list.count():
        window.games_list.setCurrentRow(0)
        for _ in range(2):
            app.processEvents()
        capture_state(window, output_dir / "expert_launcher_detail.png")

        window.detail_panel.tabs.setCurrentIndex(1)
        for _ in range(2):
            app.processEvents()
        capture_state(window, output_dir / "expert_launcher_installation.png")

        window.detail_panel.tabs.setCurrentIndex(2)
        for _ in range(2):
            app.processEvents()
        capture_state(window, output_dir / "expert_launcher_activity.png")

    window.close()
    app.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
