"""
GUI module for Linux MMORPG Launcher
Provides a PyQt6-based interface for managing and launching MMO games
"""
import sys
import logging
from hashlib import md5
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QPlainTextEdit,
    QProgressBar,
    QTabWidget,
    QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QFont, QDesktopServices, QPixmap, QPainter, QLinearGradient, QColor

from games_db import get_all_games, get_game_by_id
from game_installer import GameInstaller

# Constants
LOG_FILE = Path("logs/launcher.log")
WINDOW_TITLE = "Linux MMORPG Launcher – Expert Edition"
DEFAULT_WINDOW_SIZE = (1360, 860)
DEFAULT_WINDOW_POS = (100, 100)

# Status badge colors
STATUS_NOT_INSTALLED = ("#39435a", "#f5f8ff")
STATUS_INSTALLED = ("#43a047", "#f5f8ff")
STATUS_MANUAL_REQUIRED = ("#f9a825", "#1b1e27")

# Dependencies to check
DEFAULT_DEPENDENCIES = ["umu-launcher", "wine", "steam", "flatpak", "java"]

# Ensure log directory exists
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

    def __init__(self, installer: GameInstaller, game_id: str, game_data: dict):
        super().__init__()
        self.installer = installer
        self.game_id = game_id
        self.game_data = game_data

    def run(self):
        def progress_callback(msg: str):
            self.progress.emit(msg)

        result = self.installer.install_game(self.game_id, self.game_data, progress_callback)
        self.finished.emit(result)


class GameDetailPanel(QWidget):
    """Detailed view for selected game with expert controls."""

    install_requested = pyqtSignal(str)
    uninstall_requested = pyqtSignal(str)
    launch_requested = pyqtSignal(str)
    open_site_requested = pyqtSignal(str)
    open_folder_requested = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.current_game_id: Optional[str] = None
        self.current_game_data: Optional[dict] = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.placeholder = QLabel("Select a game from the list to inspect details.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: #7a8193; font-size: 15px;")
        layout.addWidget(self.placeholder)

        self.content = QWidget()
        self.content.hide()
        content_layout = QVBoxLayout(self.content)
        content_layout.setSpacing(14)

        # Header with title and status badge
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        self.icon_label.setObjectName("DetailIcon")
        self.icon_label.setFixedSize(80, 80)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.hide()
        header_layout.addWidget(self.icon_label)

        title_container = QVBoxLayout()
        title_container.setContentsMargins(0, 0, 0, 0)
        title_container.setSpacing(6)

        self.title_label = QLabel()
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setFont(QFont("Sans Serif", 20, QFont.Weight.Bold))
        title_container.addWidget(self.title_label)

        self.status_badge = QLabel("Not installed")
        self.status_badge.setObjectName("StatusBadge")
        self.status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_badge.setMinimumWidth(160)
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.addWidget(self.status_badge, alignment=Qt.AlignmentFlag.AlignLeft)
        title_container.addLayout(status_layout)

        header_layout.addLayout(title_container, stretch=1)
        content_layout.addLayout(header_layout)

        # Action buttons row
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        self.install_btn = QPushButton("Install")
        self.install_btn.setProperty("kind", "primary")
        self.install_btn.clicked.connect(self._emit_install)
        action_layout.addWidget(self.install_btn)

        self.launch_btn = QPushButton("Launch")
        self.launch_btn.setProperty("kind", "success")
        self.launch_btn.clicked.connect(self._emit_launch)
        action_layout.addWidget(self.launch_btn)

        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.setProperty("kind", "danger")
        self.uninstall_btn.clicked.connect(self._emit_uninstall)
        action_layout.addWidget(self.uninstall_btn)

        action_layout.addStretch()

        self.open_site_btn = QPushButton("Open Website")
        self.open_site_btn.clicked.connect(self._emit_open_site)
        action_layout.addWidget(self.open_site_btn)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.clicked.connect(self._emit_open_folder)
        action_layout.addWidget(self.open_folder_btn)

        content_layout.addLayout(action_layout)

        # Tabs for overview, installation, and activity
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Overview tab
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        overview_layout.setSpacing(10)

        overview_form = QFormLayout()
        overview_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        overview_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft)

        self.genre_value = QLabel()
        overview_form.addRow("Genre:", self.genre_value)

        self.server_value = QLabel()
        overview_form.addRow("Server:", self.server_value)

        self.population_value = QLabel()
        overview_form.addRow("Population:", self.population_value)

        self.native_value = QLabel()
        overview_form.addRow("Native Linux:", self.native_value)

        self.tested_value = QLabel()
        overview_form.addRow("Tested:", self.tested_value)

        self.install_type_value = QLabel()
        overview_form.addRow("Install Type:", self.install_type_value)

        overview_layout.addLayout(overview_form)

        self.description_field = QPlainTextEdit()
        self.description_field.setReadOnly(True)
        self.description_field.setMaximumBlockCount(1000)
        self.description_field.setMinimumHeight(120)
        overview_layout.addWidget(QLabel("Description:"))
        overview_layout.addWidget(self.description_field)

        self.tabs.addTab(overview_tab, "Overview")

        # Installation tab
        install_tab = QWidget()
        install_layout = QVBoxLayout(install_tab)
        install_layout.setSpacing(10)

        install_form = QFormLayout()
        install_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        install_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft)

        self.dependencies_value = QLabel()
        self.dependencies_value.setWordWrap(True)
        install_form.addRow("Dependencies:", self.dependencies_value)

        self.path_value = QLabel("-")
        self.path_value.setWordWrap(True)
        install_form.addRow("Install Path:", self.path_value)

        install_layout.addLayout(install_form)

        self.notes_field = QPlainTextEdit()
        self.notes_field.setReadOnly(True)
        self.notes_field.setMaximumBlockCount(2000)
        self.notes_field.setMinimumHeight(180)
        install_layout.addWidget(QLabel("Installation Notes:"))
        install_layout.addWidget(self.notes_field)

        self.tabs.addTab(install_tab, "Installation")

        # Activity tab
        activity_tab = QWidget()
        activity_layout = QVBoxLayout(activity_tab)
        activity_layout.setSpacing(10)

        self.activity_label = QLabel("No active tasks")
        self.activity_label.setStyleSheet("color: #adb3c7;")
        activity_layout.addWidget(self.activity_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        activity_layout.addWidget(self.progress_bar)

        self.log_field = QPlainTextEdit()
        self.log_field.setReadOnly(True)
        self.log_field.setMaximumBlockCount(3000)
        self.log_field.setMinimumHeight(250)
        self.log_field.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 12px;
                border: 1px solid #3a3f51;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.log_field.setPlaceholderText("Installation output will appear here...")
        activity_layout.addWidget(self.log_field)

        self.tabs.addTab(activity_tab, "Activity & Logs")

        content_layout.addWidget(self.tabs)
        layout.addWidget(self.content)

    # --- Helpers ---------------------------------------------------------
    def clear_display(self):
        """Clear the detail panel display."""
        self.current_game_id = None
        self.current_game_data = None
        self.content.hide()
        self.placeholder.show()
        bg_color, text_color = STATUS_NOT_INSTALLED
        self._set_status_badge("Not installed", bg_color, text_color)
        self.clear_activity()
        self.set_game_icon(None)

    def display_game(self, game_id: str, game_data: Dict[str, Any], install_info: Optional[Dict[str, Any]]):
        """Display game details in the panel."""
        self.current_game_id = game_id
        self.current_game_data = game_data

        self.set_game_icon(None)

        if self.placeholder.isVisible():
            self.placeholder.hide()
            self.content.show()

        self.title_label.setText(game_data['name'])
        self.genre_value.setText(game_data['genre'])
        self.server_value.setText(game_data['server'])
        self.population_value.setText(game_data['population'])
        self.native_value.setText('Yes' if game_data['native'] else 'No (Wine/Proton)')
        self.tested_value.setText('Yes' if game_data['tested'] else 'Not verified')
        self.install_type_value.setText(game_data['install_type'].replace('_', ' ').title())

        self.description_field.setPlainText(game_data['description'])
        self.notes_field.setPlainText(game_data['install_notes'])

        deps = game_data['dependencies'] or []
        self.dependencies_value.setText(', '.join(deps) if deps else 'None')

        if install_info and install_info.get('path'):
            self.path_value.setText(install_info['path'])
        else:
            self.path_value.setText('Not installed')

        pending_manual = bool(install_info and install_info.get('status') == 'pending_manual')

        if install_info:
            if pending_manual:
                bg_color, text_color = STATUS_MANUAL_REQUIRED
                self._set_status_badge('Manual steps required', bg_color, text_color)
            else:
                bg_color, text_color = STATUS_INSTALLED
                self._set_status_badge('Installed', bg_color, text_color)
        else:
            bg_color, text_color = STATUS_NOT_INSTALLED
            self._set_status_badge('Not installed', bg_color, text_color)

        self.install_btn.setEnabled(install_info is None or pending_manual)
        self.install_btn.setText('Install' if install_info is None else 'Review Manual Steps')
        self.launch_btn.setEnabled(bool(install_info) and not pending_manual)
        self.uninstall_btn.setEnabled(bool(install_info))

        # Only enable "Open Folder" for filesystem-based installs (not AUR/Flatpak)
        has_filesystem_path = False
        if install_info and install_info.get('path'):
            path_str = install_info.get('path')
            has_filesystem_path = not (path_str.startswith('aur://') or path_str.startswith('flatpak://'))
        self.open_folder_btn.setEnabled(has_filesystem_path)

        self.clear_activity()

    def _set_status_badge(self, text: str, background: str, text_color: str = '#f5f8ff'):
        """Set the status badge appearance."""
        self.status_badge.setText(text)
        self.status_badge.setStyleSheet(
            f"padding: 6px 12px; border-radius: 12px; background-color: {background}; color: {text_color};"
        )

    def set_game_icon(self, pixmap: Optional[QPixmap]):
        """Assign the hero icon shown for the current game."""
        if pixmap:
            scaled = pixmap.scaled(
                self.icon_label.width(),
                self.icon_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.icon_label.setPixmap(scaled)
            self.icon_label.show()
        else:
            self.icon_label.clear()
            self.icon_label.hide()

    def clear_activity(self):
        self.activity_label.setText("No active tasks")
        self.log_field.clear()
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

    def begin_activity(self, header: str):
        self.activity_label.setText(header)
        self.log_field.clear()
        self.log_field.appendPlainText(f"=== {header} ===\n")
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Busy indicator
        # Auto-switch to Activity tab to show progress
        self.tabs.setCurrentIndex(2)  # Index 2 is Activity & Logs tab

    def end_activity(self, footer: str = "Finished"):
        self.activity_label.setText(footer)
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

    def update_activity(self, message: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_label.setText(message)
        self.log_field.appendPlainText(f"[{timestamp}] {message}")
        cursor = self.log_field.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_field.setTextCursor(cursor)
        # Ensure the log scrolls to show latest message
        self.log_field.ensureCursorVisible()

    # --- Signal emitters -------------------------------------------------
    def _emit_install(self):
        if self.current_game_id:
            self.install_requested.emit(self.current_game_id)

    def _emit_uninstall(self):
        if self.current_game_id:
            self.uninstall_requested.emit(self.current_game_id)

    def _emit_launch(self):
        if self.current_game_id:
            self.launch_requested.emit(self.current_game_id)

    def _emit_open_site(self):
        if self.current_game_id:
            self.open_site_requested.emit(self.current_game_id)

    def _emit_open_folder(self):
        if self.current_game_id:
            self.open_folder_requested.emit(self.current_game_id)


class LauncherApp(QMainWindow):
    """Primary window presenting expert launcher UI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        x, y = DEFAULT_WINDOW_POS
        width, height = DEFAULT_WINDOW_SIZE
        self.setGeometry(x, y, width, height)

        self.installer = GameInstaller()
        self.games_db = get_all_games()
        self.install_thread: Optional[InstallThread] = None
        self.active_install_game: Optional[str] = None
        self.summary_labels: Dict[str, QLabel] = {}
        self.icon_cache: Dict[str, QPixmap] = {}

        self._setup_ui()
        self._apply_style()
        self.refresh_game_list()

    # --- UI assembly -----------------------------------------------------
    def _setup_ui(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Refresh Library", self.refresh_games_database)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        tools_menu = menu.addMenu("Tools")
        tools_menu.addAction("Check Dependencies", self.check_dependencies)
        tools_menu.addAction("View Logs", self.view_logs)

        help_menu = menu.addMenu("Help")
        help_menu.addAction("About", self.show_about)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(12, 12, 12, 12)
        central_layout.setSpacing(12)

        # Summary metrics row
        summary_frame = QFrame()
        summary_frame.setObjectName("SummaryFrame")
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(0, 0, 0, 0)
        summary_layout.setSpacing(12)

        summary_cards = [
            ("total", "Library", "Total titles"),
            ("installed", "Installed", "Ready to launch"),
            ("manual", "Follow-up", "Need manual steps"),
            ("verified", "Verified", "QA-checked"),
            ("filtered", "Shown", "Matching filters"),
        ]

        for key, title, caption in summary_cards:
            card, value_label = self._create_summary_card(title, caption)
            summary_layout.addWidget(card)
            self.summary_labels[key] = value_label

        summary_layout.addStretch(1)
        central_layout.addWidget(summary_frame)

        # Filters row
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, description, or server...")
        self.search_input.textChanged.connect(self.refresh_game_list)
        filters_layout.addWidget(QLabel("Search:"))
        filters_layout.addWidget(self.search_input, stretch=2)

        self.status_filter = QComboBox()
        self.status_filter.addItem("All statuses", "all")
        self.status_filter.addItem("Installed", "installed")
        self.status_filter.addItem("Not installed", "not_installed")
        self.status_filter.addItem("Manual follow-up", "manual")
        self.status_filter.currentIndexChanged.connect(self.refresh_game_list)
        filters_layout.addWidget(QLabel("Status:"))
        filters_layout.addWidget(self.status_filter)

        genres = sorted({data['genre'] for data in self.games_db.values()})
        self.genre_filter = QComboBox()
        self.genre_filter.addItem("All genres", "all")
        for genre in genres:
            self.genre_filter.addItem(genre, genre)
        self.genre_filter.currentIndexChanged.connect(self.refresh_game_list)
        filters_layout.addWidget(QLabel("Genre:"))
        filters_layout.addWidget(self.genre_filter)

        self.tested_filter = QComboBox()
        self.tested_filter.addItem("Any testing status", "all")
        self.tested_filter.addItem("Verified", "tested")
        self.tested_filter.addItem("Not verified", "untested")
        self.tested_filter.currentIndexChanged.connect(self.refresh_game_list)
        filters_layout.addWidget(QLabel("QA:"))
        filters_layout.addWidget(self.tested_filter)

        filters_layout.addStretch()
        central_layout.addLayout(filters_layout)

        # Main splitter with list and detail panel
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        list_panel = QWidget()
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        self.list_summary = QLabel("0 games")
        self.list_summary.setStyleSheet("color: #7a8193;")
        list_layout.addWidget(self.list_summary)

        self.games_list = QListWidget()
        self.games_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.games_list.setSpacing(8)
        self.games_list.setUniformItemSizes(False)
        self.games_list.setAlternatingRowColors(False)
        self.games_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.games_list.itemSelectionChanged.connect(self.on_game_selected)
        list_layout.addWidget(self.games_list)

        splitter.addWidget(list_panel)

        self.detail_panel = GameDetailPanel()
        self.detail_panel.install_requested.connect(self.handle_install_request)
        self.detail_panel.uninstall_requested.connect(self.handle_uninstall_request)
        self.detail_panel.launch_requested.connect(self.handle_launch_request)
        self.detail_panel.open_site_requested.connect(self.handle_open_site_request)
        self.detail_panel.open_folder_requested.connect(self.handle_open_folder_request)
        splitter.addWidget(self.detail_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        central_layout.addWidget(splitter)
        self.setCentralWidget(central)

        self.statusBar().showMessage("Ready")

    def _create_summary_card(self, title: str, caption: str) -> Tuple[QFrame, QLabel]:
        """Create a stylized summary card with title, value, and caption."""
        card = QFrame()
        card.setObjectName("SummaryCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        title_label = QLabel(title.upper())
        title_label.setObjectName("SummaryTitle")
        layout.addWidget(title_label)

        value_label = QLabel("0")
        value_label.setObjectName("SummaryValue")
        layout.addWidget(value_label)

        caption_label = QLabel(caption)
        caption_label.setObjectName("SummaryCaption")
        layout.addWidget(caption_label)

        return card, value_label

    def _color_from_string(self, text: str) -> QColor:
        """Derive a deterministic vibrant QColor from a string."""
        digest = md5(text.encode('utf-8')).hexdigest()
        hue = int(digest[:2], 16) % 360
        saturation = 180 + (int(digest[2:4], 16) % 60)
        value = 200 + (int(digest[4:6], 16) % 40)
        return QColor.fromHsv(hue, min(saturation, 255), min(value, 255))

    def _get_game_icon(self, game_id: str, game_data: Dict[str, Any]) -> QPixmap:
        """Return a cached gradient icon for a game, generating if necessary."""
        if game_id in self.icon_cache:
            return self.icon_cache[game_id]

        size = 96
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        base_color = self._color_from_string(game_id)
        highlight_color = QColor(base_color)
        highlight_color = highlight_color.lighter(140)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        gradient = QLinearGradient(0, 0, size, size)
        gradient.setColorAt(0.0, base_color)
        gradient.setColorAt(1.0, highlight_color)

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, size, size, 18, 18)

        words = [part for part in game_data['name'].split() if part]
        initials = ''.join(word[0] for word in words[:2]).upper()
        if not initials:
            initials = game_id[:2].upper()

        painter.setPen(QColor('#f5f8ff'))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(28)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), int(Qt.AlignmentFlag.AlignCenter), initials)
        painter.end()

        self.icon_cache[game_id] = pixmap
        return pixmap

    def _build_status_pill(self, text: str, status: str) -> QLabel:
        """Create a pill-style label used for game metadata badges."""
        pill = QLabel(text)
        pill.setObjectName("GameStatusPill")
        pill.setProperty("status", status)
        pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return pill

    def _resolve_install_status(self, install_info: Optional[Dict[str, Any]]) -> Tuple[str, str]:
        """Determine text and style key for installation status badge."""
        if install_info:
            if install_info.get('status') == 'pending_manual':
                return "Manual steps", "manual"
            return "Installed", "installed"
        return "Not installed", "available"

    def _create_game_list_widget(self, game_id: str, game_data: Dict[str, Any], install_info: Optional[Dict[str, Any]]) -> QFrame:
        """Build the richer list card for a game entry."""
        card = QFrame()
        card.setObjectName("GameListCard")
        card.setProperty("selected", False)

        outer_layout = QHBoxLayout(card)
        outer_layout.setContentsMargins(14, 12, 14, 12)
        outer_layout.setSpacing(12)

        icon_label = QLabel()
        icon_label.setObjectName("GameCardIcon")
        icon_label.setFixedSize(60, 60)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_pixmap = self._get_game_icon(game_id, game_data)
        icon_label.setPixmap(
            icon_pixmap.scaled(
                icon_label.width(),
                icon_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        outer_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignTop)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        title_label = QLabel(game_data['name'])
        title_label.setObjectName("GameListTitle")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, stretch=1)

        status_text, status_key = self._resolve_install_status(install_info)
        status_pill = self._build_status_pill(status_text, status_key)
        header_layout.addWidget(status_pill, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(header_layout)

        subtitle_label = QLabel(game_data['server'])
        subtitle_label.setObjectName("GameListSubtitle")
        subtitle_label.setWordWrap(True)
        layout.addWidget(subtitle_label)

        info_bits = [game_data['genre']]
        population = game_data.get('population')
        if population:
            info_bits.append(population)
        info_label = QLabel(" • ".join(info_bits))
        info_label.setObjectName("GameListSubtitle")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        tags_layout = QHBoxLayout()
        tags_layout.setContentsMargins(0, 4, 0, 0)
        tags_layout.setSpacing(6)

        compatibility_text = "Native" if game_data['native'] else "Wine/Proton"
        compatibility_key = "native" if game_data['native'] else "available"
        tags_layout.addWidget(self._build_status_pill(compatibility_text, compatibility_key))

        if game_data.get('tested'):
            tags_layout.addWidget(self._build_status_pill("QA Verified", "tested"))
        else:
            tags_layout.addWidget(self._build_status_pill("Untested", "untested"))

        tags_layout.addStretch(1)
        layout.addLayout(tags_layout)

        outer_layout.addLayout(layout, stretch=1)

        return card

    def _refresh_selection_styles(self):
        """Ensure list card widgets reflect QListWidget selection state."""
        for row in range(self.games_list.count()):
            item = self.games_list.item(row)
            widget = self.games_list.itemWidget(item)
            if not widget:
                continue
            widget.setProperty("selected", item.isSelected())
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    def _update_summary_metrics(self, filtered_games: List[Tuple[str, Dict[str, Any], Optional[Dict[str, Any]]]]):
        """Update summary cards with current library statistics."""
        total_games = len(self.games_db)
        installed_games = sum(1 for info in self.installer.installed_games.values() if info)
        manual_games = sum(1 for info in self.installer.installed_games.values() if info.get('status') == 'pending_manual')
        verified_games = sum(1 for data in self.games_db.values() if data.get('tested'))
        filtered_count = len(filtered_games)

        metrics = {
            'total': f"{total_games}",
            'installed': f"{installed_games}",
            'manual': f"{manual_games}",
            'verified': f"{verified_games}",
            'filtered': f"{filtered_count}",
        }

        for key, value in metrics.items():
            label = self.summary_labels.get(key)
            if label:
                label.setText(value)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QMainWindow { background-color: #161923; color: #e8ecff; }
            QLabel { color: #dce3ff; }
            QLabel#TitleLabel { font-size: 22px; color: #f5f8ff; }
            QLabel#StatusBadge { font-weight: bold; }
            QFrame#SummaryFrame { background-color: transparent; }
            QFrame#SummaryCard { background-color: #1e2330; border: 1px solid #2d3244; border-radius: 10px; }
            QLabel#SummaryTitle { font-size: 10px; letter-spacing: 1px; color: #7a8193; }
            QLabel#SummaryValue { font-size: 24px; font-weight: 600; color: #f5f8ff; }
            QLabel#SummaryCaption { color: #a6adc6; font-size: 11px; }
            QLineEdit, QComboBox { background-color: #1e2330; color: #f1f4ff; border: 1px solid #2b3142; border-radius: 6px; padding: 8px; }
            QListWidget { background-color: #181d27; color: #f1f4ff; border: none; border-radius: 8px; padding: 4px; }
            QListWidget::item { margin: 6px 2px; padding: 0; }
            QListWidget::item:selected { background-color: transparent; }
            QFrame#GameListCard { background-color: #1b1f2c; border: 1px solid transparent; border-radius: 10px; padding: 10px 14px; }
            QFrame#GameListCard[selected="true"] { border-color: #2e7dff; background-color: #23314a; }
            QLabel#GameCardIcon { border-radius: 16px; background-color: #111521; }
            QLabel#DetailIcon { border-radius: 20px; background-color: #111521; }
            QLabel#GameListTitle { font-size: 15px; font-weight: 600; color: #f7f9ff; }
            QLabel#GameListSubtitle { color: #9aa3bd; font-size: 12px; }
            QLabel#GameStatusPill { border-radius: 10px; padding: 2px 8px; font-size: 11px; font-weight: 600; }
            QLabel#GameStatusPill[status="installed"] { background-color: #204d36; color: #7be5a2; }
            QLabel#GameStatusPill[status="manual"] { background-color: #473818; color: #f4c770; }
            QLabel#GameStatusPill[status="available"] { background-color: #2d3140; color: #aab3ce; }
            QLabel#GameStatusPill[status="native"] { background-color: #21445d; color: #7fb6ff; }
            QLabel#GameStatusPill[status="tested"] { background-color: #2c3c2a; color: #9fe08c; }
            QLabel#GameStatusPill[status="untested"] { background-color: #432833; color: #f499b0; }
            QPushButton { background-color: #2b3142; color: #f1f4ff; border: 1px solid #384056; border-radius: 6px; padding: 8px 14px; }
            QPushButton[kind="primary"] { background-color: #2e7dff; border-color: #3270ff; }
            QPushButton[kind="success"] { background-color: #43a047; border-color: #2e7d32; }
            QPushButton[kind="danger"] { background-color: #d84343; border-color: #c62828; }
            QPushButton:disabled { background-color: #262c3a; color: #7a8193; border-color: #262c3a; }
            QTabWidget::pane { border: 1px solid #2b3142; border-radius: 6px; }
            QTabBar::tab { background: #1e2330; color: #d7dcf5; padding: 8px 14px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #2b3142; }
            QPlainTextEdit { background-color: #141824; color: #f1f4ff; border: 1px solid #2b3142; border-radius: 6px; }
            QProgressBar { border: 1px solid #2b3142; border-radius: 6px; background: #1e2330; }
            QProgressBar::chunk { background-color: #2e7dff; border-radius: 6px; }
            """
        )

    # --- Data / filtering ------------------------------------------------
    def refresh_game_list(self):
        search_term = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentData()
        genre_filter = self.genre_filter.currentData()
        tested_filter = self.tested_filter.currentData()

        current_selection = None
        selected_items = self.games_list.selectedItems()
        if selected_items:
            current_selection = selected_items[0].data(Qt.ItemDataRole.UserRole)
        elif self.detail_panel.current_game_id:
            current_selection = self.detail_panel.current_game_id

        self.games_list.blockSignals(True)
        self.games_list.clear()

        filtered_games = []

        for game_id, game_data in sorted(self.games_db.items(), key=lambda item: item[1]['name']):
            name = game_data['name']
            description = game_data['description']
            server = game_data['server']

            if search_term and search_term not in name.lower() and search_term not in description.lower() and search_term not in server.lower():
                continue

            install_info = self.installer.installed_games.get(game_id)
            is_installed = install_info is not None
            pending_manual = bool(install_info and install_info.get('status') == 'pending_manual')

            if status_filter == 'installed' and not is_installed:
                continue
            if status_filter == 'not_installed' and is_installed:
                continue
            if status_filter == 'manual' and not pending_manual:
                continue
            if status_filter not in ('all', 'manual') and pending_manual:
                # Exclude pending manual from installed filter when not explicitly requested
                if status_filter == 'installed':
                    continue

            if genre_filter != 'all' and game_data['genre'] != genre_filter:
                continue

            if tested_filter == 'tested' and not game_data['tested']:
                continue
            if tested_filter == 'untested' and game_data['tested']:
                continue

            filtered_games.append((game_id, game_data, install_info))

        for game_id, game_data, install_info in filtered_games:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, game_id)
            card = self._create_game_list_widget(game_id, game_data, install_info)
            item.setSizeHint(card.sizeHint())
            self.games_list.addItem(item)
            self.games_list.setItemWidget(item, card)

        self.games_list.blockSignals(False)

        self._update_summary_metrics(filtered_games)

        count_text = f"Showing {len(filtered_games)} of {len(self.games_db)} games"
        self.list_summary.setText(count_text)
        self.statusBar().showMessage(f"Filtered {len(filtered_games)} titles")

        if not filtered_games:
            self.detail_panel.clear_display()
            self._refresh_selection_styles()
            return

        # Restore selection or select first item
        restored = False
        if current_selection:
            for row in range(self.games_list.count()):
                item = self.games_list.item(row)
                if item.data(Qt.ItemDataRole.UserRole) == current_selection:
                    self.games_list.setCurrentRow(row)
                    restored = True
                    break

        if not restored:
            self.games_list.setCurrentRow(0)

        self._refresh_selection_styles()

    def on_game_selected(self):
        items = self.games_list.selectedItems()
        if not items:
            self.detail_panel.clear_display()
            return

        item = items[0]
        game_id = item.data(Qt.ItemDataRole.UserRole)
        game_data = self.games_db.get(game_id)
        if not game_data:
            return

        install_info = self.installer.installed_games.get(game_id)
        self.detail_panel.display_game(game_id, game_data, install_info)
        self.detail_panel.set_game_icon(self._get_game_icon(game_id, game_data))
        self.statusBar().showMessage(f"Selected: {game_data['name']}")
        self._refresh_selection_styles()

    # --- Actions ---------------------------------------------------------
    def refresh_games_database(self):
        self.installer = GameInstaller()
        self.games_db = get_all_games()
        self.detail_panel.clear_display()
        self.refresh_game_list()
        QMessageBox.information(self, "Game Library", "Game definitions reloaded. Installer refreshed.")

    def handle_install_request(self, game_id: str):
        if self.install_thread and self.install_thread.isRunning():
            QMessageBox.information(self, "Installation in progress", "Please wait for the current installation to finish before starting another.")
            return

        game_data = get_game_by_id(game_id)
        if not game_data:
            QMessageBox.warning(self, "Game not found", "Unable to locate the selected game in the database.")
            return

        deps = ', '.join(game_data['dependencies']) if game_data['dependencies'] else 'None'
        reply = QMessageBox.question(
            self,
            "Install Game",
            f"Install {game_data['name']}?\n\nDependencies: {deps}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.active_install_game = game_id
        self.detail_panel.begin_activity(f"Installing {game_data['name']}...")

        self.install_thread = InstallThread(self.installer, game_id, game_data)
        self.install_thread.progress.connect(lambda msg, gid=game_id: self.on_install_progress(gid, msg))
        self.install_thread.finished.connect(lambda success, gid=game_id: self.on_install_finished(gid, success))
        self.install_thread.start()

    def on_install_progress(self, game_id: str, message: str):
        if self.detail_panel.current_game_id == game_id:
            self.detail_panel.update_activity(message)
        logging.info(f"{game_id}: {message}")

    def on_install_finished(self, game_id: str, success: bool):
        if self.install_thread:
            self.install_thread.deleteLater()
            self.install_thread = None

        install_info = self.installer.installed_games.get(game_id)
        pending_manual = bool(install_info and install_info.get('status') == 'pending_manual')

        if self.detail_panel.current_game_id == game_id:
            footer = "Installation complete" if success else "Installation finished with notes"
            if pending_manual:
                footer = "Manual steps still required"
            elif not success and not install_info:
                footer = "Installation failed"

            self.detail_panel.end_activity(footer)
            game_data = self.games_db[game_id]
            self.detail_panel.display_game(game_id, game_data, install_info)
            self.detail_panel.set_game_icon(self._get_game_icon(game_id, game_data))

        self.refresh_game_list()

        if success:
            QMessageBox.information(self, "Installation", f"{self.games_db[game_id]['name']} installed successfully.")
        else:
            if pending_manual:
                QMessageBox.warning(
                    self,
                    "Manual Steps Required",
                    "Installation requires manual follow-up. Review the installation notes in the detail panel."
                )
            elif install_info:
                QMessageBox.information(
                    self,
                    "Installation",
                    "Installation completed with warnings. Review the logs for details."
                )
            else:
                QMessageBox.critical(self, "Installation failed", "The game could not be installed. Check the activity log for details.")

        self.active_install_game = None

    def handle_uninstall_request(self, game_id: str):
        game_data = get_game_by_id(game_id)
        if not game_data:
            QMessageBox.warning(self, "Game not found", "Unable to locate the selected game in the database.")
            return

        reply = QMessageBox.question(
            self,
            "Uninstall Game",
            f"Are you sure you want to uninstall {game_data['name']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        result = self.installer.uninstall_game(game_id)

        # Refresh installer to check actual package status
        self.installer = GameInstaller()

        # Refresh UI
        self.refresh_game_list()

        # Check if actually uninstalled
        if game_id not in self.installer.installed_games:
            self.detail_panel.end_activity("Game removed")
            self.detail_panel.display_game(game_id, game_data, None)
            self.detail_panel.set_game_icon(self._get_game_icon(game_id, game_data))
            QMessageBox.information(self, "Uninstall", f"{game_data['name']} has been removed.")
        else:
            if result:
                QMessageBox.information(self, "Uninstall", "Uninstall completed or cancelled.")
            else:
                QMessageBox.critical(self, "Uninstall", "Failed to remove the game. Check permissions and try again.")

    def handle_launch_request(self, game_id: str):
        game_data = get_game_by_id(game_id)
        if not game_data:
            QMessageBox.warning(self, "Game not found", "Unable to locate the selected game in the database.")
            return

        if self.installer.launch_game(game_id, game_data):
            self.statusBar().showMessage(f"Launching {game_data['name']}...")
            self.detail_panel.update_activity("Launch command executed")
        else:
            QMessageBox.critical(self, "Launch failed", "Unable to launch the game. Verify installation and configuration.")

    def handle_open_site_request(self, game_id: str):
        """Open the game's website in the default browser."""
        game_data = get_game_by_id(game_id)
        if not game_data:
            QMessageBox.warning(self, "Open Website", "Game information not found.")
            return
        
        url = game_data.get('website')
        if url:
            try:
                QDesktopServices.openUrl(QUrl(url))
                logging.info(f"Opened website for {game_data.get('name', game_id)}: {url}")
            except Exception as e:
                logging.error(f"Failed to open website {url}: {e}")
                QMessageBox.warning(self, "Open Website", f"Failed to open website: {e}")
        else:
            QMessageBox.information(self, "Open Website", "No website URL available for this game.")

    def handle_open_folder_request(self, game_id: str):
        """Open the game's installation folder in the file manager."""
        path = self.installer.get_game_path(game_id)
        if not path:
            QMessageBox.information(self, "Open Folder", "No installation path recorded for this title.")
            return

        if not path.exists():
            QMessageBox.warning(self, "Open Folder", "The recorded installation path no longer exists.")
            return

        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
            logging.info(f"Opened folder for {game_id}: {path}")
        except Exception as e:
            logging.error(f"Failed to open folder {path}: {e}")
            QMessageBox.warning(self, "Open Folder", f"Failed to open folder: {e}")

    def refresh_games(self):
        self.refresh_game_list()

    def check_dependencies(self):
        """Check system dependencies and display results."""
        results = self.installer.check_dependencies(DEFAULT_DEPENDENCIES)

        summary_lines = []
        for dep, installed in results.items():
            status = "✓ OK" if installed else "✗ Missing"
            summary_lines.append(f"{dep}: {status}")

        QMessageBox.information(self, "Dependency Check", "\n".join(summary_lines))

    def view_logs(self):
        """View launcher log file contents."""
        if LOG_FILE.exists():
            try:
                content = LOG_FILE.read_text(encoding='utf-8')
            except Exception as exc:
                QMessageBox.warning(self, "Logs", f"Failed to read log file: {exc}")
                return

            dialog = QMessageBox(self)
            dialog.setWindowTitle("Launcher Logs")
            dialog.setText("Recent log entries:")
            dialog.setDetailedText(content)
            dialog.exec()
        else:
            QMessageBox.information(self, "Logs", "No log entries recorded yet.")

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            "Linux MMORPG Launcher – Expert Edition\n\n"
            "Enhanced interface for power users.\n"
            "Features:\n"
            "• Split-view library explorer\n"
            "• Detailed install & activity tracking\n"
            "• Quick access to game resources"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherApp()
    window.show()
    sys.exit(app.exec())
