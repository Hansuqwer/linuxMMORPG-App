import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QMessageBox, QScrollArea, QTextEdit,
                             QGroupBox, QComboBox, QProgressBar, QTabWidget, QListWidget,
                             QListWidgetItem, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from games_db import get_all_games, get_game_by_id
from game_installer import GameInstaller

LOG_FILE = Path("logs/launcher.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class InstallThread(QThread):
    """Background thread for game installation"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, installer, game_id, game_data):
        super().__init__()
        self.installer = installer
        self.game_id = game_id
        self.game_data = game_data

    def run(self):
        def progress_callback(msg):
            self.progress.emit(msg)

        result = self.installer.install_game(self.game_id, self.game_data, progress_callback)
        self.finished.emit(result)


class GameCard(QGroupBox):
    """Widget representing a single game"""
    def __init__(self, game_id, game_data, installer, parent=None):
        super().__init__(parent)
        self.game_id = game_id
        self.game_data = game_data
        self.installer = installer
        self.is_installed = installer.is_installed(game_id)

        self.setTitle(game_data['name'])
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Game info
        info_label = QLabel(f"<b>Genre:</b> {self.game_data['genre']}<br>"
                           f"<b>Server:</b> {self.game_data['server']}<br>"
                           f"<b>Population:</b> {self.game_data['population']}<br>"
                           f"<b>Native:</b> {'Yes' if self.game_data['native'] else 'No (via Wine/Proton)'}")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Description
        desc_label = QLabel(self.game_data['description'])
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(desc_label)

        # Buttons
        button_layout = QHBoxLayout()

        if self.is_installed:
            self.launch_btn = QPushButton("Launch")
            self.launch_btn.clicked.connect(self.launch_game)
            self.launch_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
            button_layout.addWidget(self.launch_btn)

            self.uninstall_btn = QPushButton("Uninstall")
            self.uninstall_btn.clicked.connect(self.uninstall_game)
            self.uninstall_btn.setStyleSheet("background-color: #f44336; color: white;")
            button_layout.addWidget(self.uninstall_btn)
        else:
            self.install_btn = QPushButton("Install")
            self.install_btn.clicked.connect(self.install_game)
            self.install_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
            button_layout.addWidget(self.install_btn)

        self.info_btn = QPushButton("Info")
        self.info_btn.clicked.connect(self.show_info)
        button_layout.addWidget(self.info_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def launch_game(self):
        if self.installer.launch_game(self.game_id, self.game_data):
            QMessageBox.information(self, "Success", f"{self.game_data['name']} launched!")
        else:
            QMessageBox.critical(self, "Error", f"Failed to launch {self.game_data['name']}")

    def install_game(self):
        reply = QMessageBox.question(self, 'Install Game',
                                     f"Install {self.game_data['name']}?\n\n"
                                     f"Dependencies: {', '.join(self.game_data['dependencies'])}",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Show progress dialog
            progress_dialog = QMessageBox(self)
            progress_dialog.setWindowTitle("Installing...")
            progress_dialog.setText(f"Installing {self.game_data['name']}")
            progress_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
            progress_dialog.show()

            # Start installation in background thread
            self.install_thread = InstallThread(self.installer, self.game_id, self.game_data)
            self.install_thread.progress.connect(lambda msg: progress_dialog.setText(msg))
            self.install_thread.finished.connect(lambda success: self.installation_finished(success, progress_dialog))
            self.install_thread.start()

    def installation_finished(self, success, dialog):
        dialog.close()
        if success:
            QMessageBox.information(self, "Success", f"{self.game_data['name']} installed successfully!")
            self.is_installed = True
            # Refresh the card
            self.setup_ui()
        else:
            QMessageBox.warning(self, "Installation",
                              f"{self.game_data['name']} installation requires manual steps.\n\n"
                              f"Please check the info panel for instructions.")

    def uninstall_game(self):
        reply = QMessageBox.question(self, 'Uninstall Game',
                                     f"Are you sure you want to uninstall {self.game_data['name']}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if self.installer.uninstall_game(self.game_id):
                QMessageBox.information(self, "Success", f"{self.game_data['name']} uninstalled!")
                self.is_installed = False
                self.setup_ui()
            else:
                QMessageBox.critical(self, "Error", "Failed to uninstall game")

    def show_info(self):
        info_text = f"""
<h2>{self.game_data['name']}</h2>
<p><b>Genre:</b> {self.game_data['genre']}</p>
<p><b>Server:</b> {self.game_data['server']}</p>
<p><b>Population:</b> {self.game_data['population']}</p>
<p><b>Website:</b> <a href="{self.game_data['website']}">{self.game_data['website']}</a></p>
<p><b>Native Linux:</b> {'Yes' if self.game_data['native'] else 'No'}</p>
<p><b>Tested:</b> {'Yes' if self.game_data['tested'] else 'No'}</p>

<h3>Description</h3>
<p>{self.game_data['description']}</p>

<h3>Installation Type</h3>
<p>{self.game_data['install_type']}</p>

<h3>Dependencies</h3>
<p>{', '.join(self.game_data['dependencies']) if self.game_data['dependencies'] else 'None'}</p>

<h3>Installation Notes</h3>
<p>{self.game_data['install_notes']}</p>

<h3>Download URL</h3>
<p><a href="{self.game_data['client_download_url']}">{self.game_data['client_download_url']}</a></p>
        """

        msg = QMessageBox(self)
        msg.setWindowTitle(f"Game Info - {self.game_data['name']}")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(info_text)
        msg.setStandardButtons(QMessageBox.StandardButton.Close)
        msg.exec()


class LauncherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux MMORPG Launcher")
        self.setGeometry(100, 100, 1200, 800)

        self.installer = GameInstaller()
        self.games_db = get_all_games()

        self.setup_ui()

    def setup_ui(self):
        # Menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Refresh", self.refresh_games)
        file_menu.addAction("Exit", self.close)

        tools_menu = menu.addMenu("Tools")
        tools_menu.addAction("Check Dependencies", self.check_dependencies)
        tools_menu.addAction("View Logs", self.view_logs)

        help_menu = menu.addMenu("Help")
        help_menu.addAction("About", self.show_about)

        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Filter/Search bar
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter:"))

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Games", "Installed", "Not Installed", "Native Linux", "Tested"])
        self.filter_combo.currentTextChanged.connect(self.filter_games)
        filter_layout.addWidget(self.filter_combo)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Scroll area for game cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.games_container = QWidget()
        self.games_layout = QVBoxLayout()
        self.games_container.setLayout(self.games_layout)
        scroll.setWidget(self.games_container)

        main_layout.addWidget(scroll)

        # Status bar
        self.statusBar().showMessage("Ready")

        central_widget.setLayout(main_layout)

        # Load games
        self.load_games()

    def load_games(self, filter_type="All Games"):
        # Clear existing games
        while self.games_layout.count():
            child = self.games_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Filter games
        games_to_show = {}

        for game_id, game_data in self.games_db.items():
            if filter_type == "All Games":
                games_to_show[game_id] = game_data
            elif filter_type == "Installed" and self.installer.is_installed(game_id):
                games_to_show[game_id] = game_data
            elif filter_type == "Not Installed" and not self.installer.is_installed(game_id):
                games_to_show[game_id] = game_data
            elif filter_type == "Native Linux" and game_data['native']:
                games_to_show[game_id] = game_data
            elif filter_type == "Tested" and game_data['tested']:
                games_to_show[game_id] = game_data

        # Add game cards
        for game_id, game_data in games_to_show.items():
            card = GameCard(game_id, game_data, self.installer)
            self.games_layout.addWidget(card)

        self.games_layout.addStretch()

        # Update status
        installed_count = len([g for g in self.games_db.keys() if self.installer.is_installed(g)])
        total_count = len(self.games_db)
        self.statusBar().showMessage(f"Showing {len(games_to_show)} games | {installed_count}/{total_count} installed")

    def filter_games(self, filter_type):
        self.load_games(filter_type)

    def refresh_games(self):
        self.installer = GameInstaller()
        self.load_games(self.filter_combo.currentText())
        QMessageBox.information(self, "Refresh", "Games list refreshed!")

    def check_dependencies(self):
        deps = ["umu-launcher", "wine", "steam", "flatpak", "java"]
        results = self.installer.check_dependencies(deps)

        msg = "Dependency Check:\n\n"
        for dep, installed in results.items():
            status = "✓ Installed" if installed else "✗ Not Installed"
            msg += f"{dep}: {status}\n"

        QMessageBox.information(self, "Dependencies", msg)

    def view_logs(self):
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r') as f:
                logs = f.read()

            dialog = QMessageBox(self)
            dialog.setWindowTitle("Launcher Logs")
            dialog.setText("Recent log entries:")
            dialog.setDetailedText(logs)
            dialog.exec()
        else:
            QMessageBox.information(self, "Logs", "No logs found")

    def show_about(self):
        QMessageBox.information(self, "About",
                               "Linux MMORPG Launcher\n\n"
                               "A professional MMO game launcher for Linux\n"
                               "Powered by PyQt6 + UMU\n\n"
                               "Features:\n"
                               "• 30+ MMORPG support\n"
                               "• One-click installation\n"
                               "• UMU launcher integration\n"
                               "• Native Linux games support")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherApp()
    window.show()
    sys.exit(app.exec())
