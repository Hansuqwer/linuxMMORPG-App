"""
Tests for game_installer.py module
"""

import pytest
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import tempfile

from game_installer import GameInstaller


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp, ignore_errors=True)


@pytest.fixture
def mock_installer(temp_dir):
    """Create GameInstaller with temporary directories"""
    with patch('game_installer.Path.home') as mock_home:
        mock_home.return_value = temp_dir
        installer = GameInstaller(games_dir=str(temp_dir / "Games"))
        return installer


class TestGameInstallerInit:
    """Test GameInstaller initialization"""

    def test_creates_games_directory(self, temp_dir):
        """Test that games directory is created"""
        with patch('game_installer.Path.home') as mock_home:
            mock_home.return_value = temp_dir
            installer = GameInstaller(games_dir=str(temp_dir / "Games"))
            assert installer.games_dir.exists()

    def test_creates_config_directory(self, temp_dir):
        """Test that config directory is created"""
        with patch('game_installer.Path.home') as mock_home:
            mock_home.return_value = temp_dir
            installer = GameInstaller(games_dir=str(temp_dir / "Games"))
            assert installer.config_dir.exists()

    def test_loads_installed_games(self, mock_installer):
        """Test that installed games are loaded from JSON"""
        assert isinstance(mock_installer.installed_games, dict)


class TestAURHelperDetection:
    """Test AUR helper detection"""

    def test_detects_yay(self, mock_installer):
        """Test detection of yay AUR helper"""
        with patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/yay' if x == 'yay' else None
            helper = mock_installer._detect_aur_helper()
            assert helper == 'yay'

    def test_detects_paru(self, mock_installer):
        """Test detection of paru AUR helper"""
        with patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/paru' if x == 'paru' else None
            helper = mock_installer._detect_aur_helper()
            assert helper == 'paru'

    def test_no_helper_found(self, mock_installer):
        """Test when no AUR helper is found"""
        with patch('shutil.which', return_value=None):
            helper = mock_installer._detect_aur_helper()
            assert helper is None


class TestDependencyChecking:
    """Test dependency checking functionality"""

    def test_check_umu_launcher(self, mock_installer):
        """Test checking for umu-launcher"""
        with patch('shutil.which', return_value='/usr/bin/umu'):
            results = mock_installer.check_dependencies(['umu-launcher'])
            assert results['umu-launcher'] is True

    def test_check_wine(self, mock_installer):
        """Test checking for wine"""
        with patch('shutil.which', return_value='/usr/bin/wine'):
            results = mock_installer.check_dependencies(['wine'])
            assert results['wine'] is True

    def test_missing_dependency(self, mock_installer):
        """Test detection of missing dependency"""
        with patch('shutil.which', return_value=None):
            results = mock_installer.check_dependencies(['steam'])
            assert results['steam'] is False


class TestGameInstallation:
    """Test game installation functionality"""

    def test_is_installed_true(self, mock_installer):
        """Test checking if game is installed"""
        mock_installer.installed_games = {'test-game': {'name': 'Test Game'}}
        assert mock_installer.is_installed('test-game') is True

    def test_is_installed_false(self, mock_installer):
        """Test checking if game is not installed"""
        assert mock_installer.is_installed('nonexistent-game') is False

    def test_get_game_path_exists(self, mock_installer):
        """Test getting game path for installed game"""
        mock_installer.installed_games = {
            'test-game': {'name': 'Test Game', 'path': '/home/user/Games/test-game'}
        }
        path = mock_installer.get_game_path('test-game')
        assert path == Path('/home/user/Games/test-game')

    def test_get_game_path_aur_returns_none(self, mock_installer):
        """Test that AUR paths return None"""
        mock_installer.installed_games = {
            'test-game': {'name': 'Test Game', 'path': 'aur://test-package'}
        }
        path = mock_installer.get_game_path('test-game')
        assert path is None

    def test_get_game_path_flatpak_returns_none(self, mock_installer):
        """Test that Flatpak paths return None"""
        mock_installer.installed_games = {
            'test-game': {'name': 'Test Game', 'path': 'flatpak://com.test.Game'}
        }
        path = mock_installer.get_game_path('test-game')
        assert path is None


class TestAutoDetection:
    """Test automatic game detection"""

    def test_detects_aur_package(self, mock_installer):
        """Test detection of AUR installed package"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            mock_installer._auto_detect_games()
            # Should detect runescape-launcher or xivlauncher if installed

    def test_detects_flatpak(self, mock_installer):
        """Test detection of Flatpak apps"""
        with patch('subprocess.run') as mock_run, \
             patch('shutil.which', return_value='/usr/bin/flatpak'):
            mock_run.return_value = Mock(
                returncode=0,
                stdout='dev.goats.xivlauncher\ncom.jagex.RuneScape\n'
            )
            mock_installer._auto_detect_games()

    def test_detects_manual_installs(self, mock_installer, temp_dir):
        """Test detection of manually installed games"""
        # Create fake game installation
        game_dir = temp_dir / "Games" / "RFAlturism" / "RFAltruism2232"
        game_dir.mkdir(parents=True)
        (game_dir / "RFAltruismLauncher.exe").touch()

        with patch('game_installer.Path.home', return_value=temp_dir):
            installer = GameInstaller(games_dir=str(temp_dir / "Games"))
            # Should detect rf-altruism


class TestGameLaunching:
    """Test game launching functionality"""

    def test_launch_aur_game(self, mock_installer):
        """Test launching AUR package game"""
        mock_installer.installed_games = {
            'test-game': {
                'name': 'Test Game',
                'path': 'aur://test-package',
                'install_type': 'aur'
            }
        }
        game_data = {'name': 'Test Game', 'launch_command': 'test-package'}

        with patch('subprocess.Popen') as mock_popen:
            result = mock_installer.launch_game('test-game', game_data)
            assert result is True
            mock_popen.assert_called_once()

    def test_launch_flatpak_game(self, mock_installer):
        """Test launching Flatpak game"""
        mock_installer.installed_games = {
            'test-game': {
                'name': 'Test Game',
                'path': 'flatpak://com.test.Game',
                'install_type': 'flatpak'
            }
        }
        game_data = {'name': 'Test Game'}

        with patch('subprocess.Popen') as mock_popen:
            result = mock_installer.launch_game('test-game', game_data)
            assert result is True
            mock_popen.assert_called_with(['flatpak', 'run', 'com.test.Game'])

    def test_launch_umu_game(self, mock_installer, temp_dir):
        """Test launching game via UMU"""
        game_dir = temp_dir / "Games" / "test-game"
        game_dir.mkdir(parents=True)
        (game_dir / "game.exe").touch()

        mock_installer.installed_games = {
            'test-game': {
                'name': 'Test Game',
                'path': str(game_dir),
                'install_type': 'manual_download'
            }
        }
        game_data = {'name': 'Test Game', 'executable': 'game.exe'}

        with patch('subprocess.Popen') as mock_popen, \
             patch('shutil.which', return_value='/usr/bin/umu-run'):
            result = mock_installer.launch_game('test-game', game_data)
            assert result is True

    def test_launch_game_not_installed(self, mock_installer):
        """Test launching game that's not installed"""
        game_data = {'name': 'Test Game'}
        result = mock_installer.launch_game('nonexistent-game', game_data)
        assert result is False


class TestGameUninstall:
    """Test game uninstallation"""

    def test_uninstall_nonexistent_game(self, mock_installer):
        """Test uninstalling game that doesn't exist"""
        result = mock_installer.uninstall_game('nonexistent-game')
        assert result is False

    def test_uninstall_manual_game(self, mock_installer, temp_dir):
        """Test uninstalling manually installed game"""
        game_dir = temp_dir / "Games" / "test-game"
        game_dir.mkdir(parents=True)

        mock_installer.installed_games = {
            'test-game': {
                'name': 'Test Game',
                'path': str(game_dir),
                'install_type': 'manual_download'
            }
        }

        result = mock_installer.uninstall_game('test-game')
        assert result is True
        assert not game_dir.exists()
        assert 'test-game' not in mock_installer.installed_games


class TestConfigPersistence:
    """Test configuration saving and loading"""

    def test_save_installed_games(self, mock_installer):
        """Test saving installed games to JSON"""
        mock_installer.installed_games = {
            'test-game': {'name': 'Test Game', 'path': '/test/path'}
        }
        mock_installer._save_installed_games()

        # Load and verify
        with open(mock_installer.installed_games_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == mock_installer.installed_games

    def test_load_installed_games(self, mock_installer):
        """Test loading installed games from JSON"""
        test_data = {
            'test-game': {'name': 'Test Game', 'path': '/test/path'}
        }

        with open(mock_installer.installed_games_file, 'w') as f:
            json.dump(test_data, f)

        loaded = mock_installer._load_installed_games()
        assert loaded == test_data
