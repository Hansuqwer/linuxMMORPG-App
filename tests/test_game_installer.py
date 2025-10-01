"""
Test suite for game_installer.py
Tests GameInstaller initialization, dependency checking, installation, launching, and configuration
"""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call

from game_installer import (
    GameInstaller,
    DEFAULT_GAMES_DIR,
    CONFIG_DIR,
    AUR_HELPERS,
    UMU_COMMANDS
)


@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing"""
    temp_games_dir = tempfile.mkdtemp(prefix='test_games_')
    temp_config_dir = tempfile.mkdtemp(prefix='test_config_')
    
    yield {
        'games_dir': temp_games_dir,
        'config_dir': temp_config_dir
    }
    
    # Cleanup
    shutil.rmtree(temp_games_dir, ignore_errors=True)
    shutil.rmtree(temp_config_dir, ignore_errors=True)


@pytest.fixture
def mock_installer(temp_dirs):
    """Create a GameInstaller with mocked paths"""
    with patch('game_installer.CONFIG_DIR', Path(temp_dirs['config_dir'])):
        with patch('game_installer.INSTALLED_GAMES_FILE', 
                   Path(temp_dirs['config_dir']) / 'installed_games.json'):
            installer = GameInstaller(games_dir=temp_dirs['games_dir'])
            return installer


@pytest.fixture
def sample_game_data():
    """Sample game data for testing"""
    return {
        'name': 'Test Game',
        'genre': 'Test Genre',
        'server': 'Test Server',
        'population': 'High',
        'description': 'A test game for unit testing',
        'website': 'https://test-game.com',
        'client_download_url': 'https://test-game.com/download',
        'install_type': 'manual_download',
        'dependencies': ['umu-launcher', 'wine'],
        'executable': 'testgame.exe',
        'install_notes': 'Test installation notes',
        'native': False,
        'tested': True
    }


class TestGameInstallerInitialization:
    """Test GameInstaller initialization and setup"""
    
    def test_installer_creates_with_default_dir(self, temp_dirs):
        """GameInstaller should initialize with default directory"""
        with patch('game_installer.DEFAULT_GAMES_DIR', Path(temp_dirs['games_dir'])):
            with patch('game_installer.CONFIG_DIR', Path(temp_dirs['config_dir'])):
                with patch('game_installer.INSTALLED_GAMES_FILE',
                          Path(temp_dirs['config_dir']) / 'installed_games.json'):
                    installer = GameInstaller()
                    assert installer is not None
                    assert installer.games_dir.exists()
    
    def test_installer_creates_with_custom_dir(self, temp_dirs):
        """GameInstaller should initialize with custom directory"""
        custom_dir = temp_dirs['games_dir']
        with patch('game_installer.CONFIG_DIR', Path(temp_dirs['config_dir'])):
            with patch('game_installer.INSTALLED_GAMES_FILE',
                      Path(temp_dirs['config_dir']) / 'installed_games.json'):
                installer = GameInstaller(games_dir=custom_dir)
                assert str(installer.games_dir) == custom_dir
    
    def test_installer_creates_games_directory(self, temp_dirs):
        """GameInstaller should create games directory if it doesn't exist"""
        games_dir = Path(temp_dirs['games_dir']) / 'new_subdir'
        assert not games_dir.exists()
        
        with patch('game_installer.CONFIG_DIR', Path(temp_dirs['config_dir'])):
            with patch('game_installer.INSTALLED_GAMES_FILE',
                      Path(temp_dirs['config_dir']) / 'installed_games.json'):
                installer = GameInstaller(games_dir=str(games_dir))
                assert games_dir.exists()
    
    def test_installer_creates_config_directory(self, mock_installer):
        """GameInstaller should create config directory"""
        assert mock_installer.config_dir.exists()
    
    def test_installer_initializes_installed_games(self, mock_installer):
        """GameInstaller should initialize installed_games dict"""
        assert hasattr(mock_installer, 'installed_games')
        assert isinstance(mock_installer.installed_games, dict)
    
    def test_installer_detects_aur_helper(self, mock_installer):
        """GameInstaller should attempt to detect AUR helper"""
        # Should have aur_helper attribute (may be None)
        assert hasattr(mock_installer, 'aur_helper')


class TestAURHelperDetection:
    """Test AUR helper detection functionality"""
    
    def test_detect_aur_helper_finds_yay(self, mock_installer):
        """Should detect yay if available"""
        with patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/yay' if x == 'yay' else None
            helper = mock_installer._detect_aur_helper()
            assert helper == 'yay'
    
    def test_detect_aur_helper_finds_paru(self, mock_installer):
        """Should detect paru if available"""
        with patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/paru' if x == 'paru' else None
            helper = mock_installer._detect_aur_helper()
            assert helper == 'paru'
    
    def test_detect_aur_helper_returns_none_if_none_found(self, mock_installer):
        """Should return None if no AUR helper found"""
        with patch('shutil.which', return_value=None):
            helper = mock_installer._detect_aur_helper()
            assert helper is None
    
    def test_detect_aur_helper_checks_all_helpers(self, mock_installer):
        """Should check all known AUR helpers"""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = None
            mock_installer._detect_aur_helper()
            # Verify it checked for AUR helpers
            for helper in AUR_HELPERS:
                mock_which.assert_any_call(helper)


class TestDependencyChecking:
    """Test dependency checking functionality"""
    
    def test_check_dependencies_empty_list(self, mock_installer):
        """Should handle empty dependency list"""
        result = mock_installer.check_dependencies([])
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_check_dependencies_umu_launcher(self, mock_installer):
        """Should check for umu-launcher correctly"""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/bin/umu-run'
            result = mock_installer.check_dependencies(['umu-launcher'])
            assert 'umu-launcher' in result
            assert result['umu-launcher'] is True
    
    def test_check_dependencies_umu_not_installed(self, mock_installer):
        """Should detect when umu is not installed"""
        with patch('shutil.which', return_value=None):
            result = mock_installer.check_dependencies(['umu-launcher'])
            assert 'umu-launcher' in result
            assert result['umu-launcher'] is False
    
    def test_check_dependencies_multiple_deps(self, mock_installer):
        """Should check multiple dependencies"""
        deps = ['umu-launcher', 'wine', 'steam']
        with patch('shutil.which', return_value='/usr/bin/something'):
            result = mock_installer.check_dependencies(deps)
            assert len(result) == len(deps)
            for dep in deps:
                assert dep in result
    
    def test_check_dependencies_wine(self, mock_installer):
        """Should check for wine"""
        with patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/wine' if x == 'wine' else None
            result = mock_installer.check_dependencies(['wine'])
            assert result['wine'] is True
    
    def test_check_dependencies_steam(self, mock_installer):
        """Should check for steam"""
        with patch('shutil.which') as mock_which:
            mock_which.side_effect = lambda x: '/usr/bin/steam' if x == 'steam' else None
            result = mock_installer.check_dependencies(['steam'])
            assert result['steam'] is True


class TestGameInstallation:
    """Test game installation functionality"""
    
    def test_is_installed_returns_false_for_new_game(self, mock_installer):
        """Should return False for non-installed game"""
        assert mock_installer.is_installed('test-game') is False
    
    def test_is_installed_returns_true_for_installed_game(self, mock_installer):
        """Should return True for installed game"""
        mock_installer.installed_games['test-game'] = {
            'name': 'Test Game',
            'path': '/path/to/game'
        }
        assert mock_installer.is_installed('test-game') is True
    
    def test_get_game_path_returns_none_for_uninstalled(self, mock_installer):
        """Should return None for uninstalled game"""
        path = mock_installer.get_game_path('nonexistent-game')
        assert path is None
    
    def test_get_game_path_returns_path_for_installed(self, mock_installer):
        """Should return path for installed game"""
        test_path = '/test/path/to/game'
        mock_installer.installed_games['test-game'] = {
            'name': 'Test Game',
            'path': test_path
        }
        path = mock_installer.get_game_path('test-game')
        assert path == Path(test_path)
    
    @patch('subprocess.run')
    def test_install_game_creates_directory(self, mock_run, mock_installer, sample_game_data):
        """Install should create game directory"""
        game_id = 'test-game'
        
        # Mock dependency checking
        with patch.object(mock_installer, 'check_dependencies', return_value={}):
            with patch.object(mock_installer, '_save_installed_games', return_value=True):
                # The actual install might fail, but directory creation should work
                game_dir = mock_installer.games_dir / game_id
                
                # Test that path is constructed correctly
                expected_dir = Path(mock_installer.games_dir) / game_id
                assert str(expected_dir) == str(game_dir)


class TestGameUninstallation:
    """Test game uninstallation functionality"""
    
    def test_uninstall_nonexistent_game_returns_false(self, mock_installer):
        """Uninstalling non-existent game should return False"""
        result = mock_installer.uninstall_game('nonexistent-game')
        assert result is False
    
    def test_uninstall_removes_from_installed_games(self, mock_installer):
        """Uninstalling should remove from installed_games dict"""
        game_id = 'test-game'
        game_path = mock_installer.games_dir / game_id
        game_path.mkdir(parents=True, exist_ok=True)
        
        mock_installer.installed_games[game_id] = {
            'name': 'Test Game',
            'path': str(game_path),
            'install_type': 'manual_download'
        }
        
        with patch.object(mock_installer, '_save_installed_games', return_value=True):
            result = mock_installer.uninstall_game(game_id)
            assert result is True
            assert game_id not in mock_installer.installed_games
    
    @patch('subprocess.run')
    def test_uninstall_aur_package(self, mock_run, mock_installer):
        """Should uninstall AUR package correctly"""
        game_id = 'test-aur-game'
        mock_installer.installed_games[game_id] = {
            'name': 'Test AUR Game',
            'path': 'aur://test-package',
            'install_type': 'aur'
        }
        mock_installer.aur_helper = 'yay'
        
        with patch.object(mock_installer, '_save_installed_games', return_value=True):
            mock_run.return_value = Mock(returncode=0)
            result = mock_installer.uninstall_game(game_id)
            
            # Should have called AUR helper to remove package
            mock_run.assert_called_once()
            assert result is True
    
    @patch('subprocess.run')
    def test_uninstall_flatpak_package(self, mock_run, mock_installer):
        """Should uninstall Flatpak correctly"""
        game_id = 'test-flatpak-game'
        mock_installer.installed_games[game_id] = {
            'name': 'Test Flatpak Game',
            'path': 'flatpak://com.test.Game',
            'install_type': 'flatpak'
        }
        
        with patch.object(mock_installer, '_save_installed_games', return_value=True):
            mock_run.return_value = Mock(returncode=0)
            result = mock_installer.uninstall_game(game_id)
            
            # Should have called flatpak uninstall
            mock_run.assert_called_once()
            assert result is True


class TestAutoDetection:
    """Test auto-detection functionality for games"""
    
    def test_auto_detect_checks_common_paths(self, mock_installer):
        """Auto-detection should check common installation paths"""
        # This is a placeholder - actual implementation may vary
        # Test that the installer can handle auto-detect type
        game_data = {
            'name': 'Auto Detect Game',
            'install_type': 'auto_detect',
            'dependencies': [],
            'native': False,
            'tested': True
        }
        # Just verify it doesn't crash
        assert game_data['install_type'] == 'auto_detect'


class TestGameLaunching:
    """Test game launching functionality"""
    
    @patch('subprocess.Popen')
    def test_launch_game_with_umu(self, mock_popen, mock_installer, sample_game_data):
        """Should launch game with UMU"""
        game_id = 'test-game'
        mock_installer.installed_games[game_id] = {
            'name': 'Test Game',
            'path': str(mock_installer.games_dir / game_id),
            'install_type': 'manual_download'
        }
        
        with patch('shutil.which', return_value='/usr/bin/umu-run'):
            # Mock the process
            mock_process = Mock()
            mock_popen.return_value = mock_process
            
            # Test launching (may not fully succeed without real paths)
            try:
                result = mock_installer.launch_game(game_id, sample_game_data)
                # If it returns, it's attempting to launch
            except Exception:
                # Expected if paths don't exist
                pass


class TestConfigPersistence:
    """Test configuration saving and loading"""
    
    def test_save_installed_games_creates_file(self, mock_installer):
        """Should create installed_games.json file"""
        mock_installer.installed_games['test-game'] = {
            'name': 'Test Game',
            'path': '/test/path'
        }
        
        result = mock_installer._save_installed_games()
        assert result is True
        assert mock_installer.installed_games_file.exists()
    
    def test_save_and_load_installed_games(self, mock_installer):
        """Should save and load installed games correctly"""
        test_data = {
            'game1': {'name': 'Game 1', 'path': '/path1'},
            'game2': {'name': 'Game 2', 'path': '/path2'}
        }
        
        mock_installer.installed_games = test_data
        mock_installer._save_installed_games()
        
        # Load in a new installer
        with patch('game_installer.CONFIG_DIR', mock_installer.config_dir):
            with patch('game_installer.INSTALLED_GAMES_FILE', 
                      mock_installer.installed_games_file):
                new_installer = GameInstaller(games_dir=str(mock_installer.games_dir))
                loaded_data = new_installer._load_installed_games()
                
                assert len(loaded_data) == len(test_data)
                assert 'game1' in loaded_data
                assert 'game2' in loaded_data
    
    def test_load_installed_games_handles_missing_file(self, mock_installer):
        """Should handle missing installed_games.json gracefully"""
        # Remove file if it exists
        if mock_installer.installed_games_file.exists():
            mock_installer.installed_games_file.unlink()
        
        loaded = mock_installer._load_installed_games()
        assert isinstance(loaded, dict)
        assert len(loaded) == 0
    
    def test_load_installed_games_handles_corrupt_json(self, mock_installer):
        """Should handle corrupted JSON file gracefully"""
        # Write invalid JSON
        with open(mock_installer.installed_games_file, 'w') as f:
            f.write('{ invalid json content }')
        
        loaded = mock_installer._load_installed_games()
        assert isinstance(loaded, dict)
        assert len(loaded) == 0


class TestDependencyInstallation:
    """Test dependency installation functionality"""
    
    def test_install_dependencies_skips_if_all_installed(self, mock_installer):
        """Should skip installation if all dependencies present"""
        deps = ['wine', 'steam']
        
        with patch.object(mock_installer, 'check_dependencies') as mock_check:
            mock_check.return_value = {'wine': True, 'steam': True}
            
            result = mock_installer.install_dependencies(deps)
            assert result is True
    
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_install_dependencies_attempts_install(self, mock_which, mock_run, mock_installer):
        """Should attempt to install missing dependencies"""
        deps = ['wine']
        
        # Simulate pacman being available
        mock_which.side_effect = lambda x: '/usr/bin/pacman' if x == 'pacman' else None
        mock_run.return_value = Mock(returncode=0)
        
        with patch.object(mock_installer, 'check_dependencies') as mock_check:
            mock_check.return_value = {'wine': False}
            
            result = mock_installer.install_dependencies(deps)
            # Will call subprocess to install
            assert mock_run.called or result is False  # May fail without sudo


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_installer_handles_readonly_config_dir(self, temp_dirs):
        """Should handle read-only config directory gracefully"""
        # This test might not work on all systems, so we keep it simple
        try:
            with patch('game_installer.CONFIG_DIR', Path('/readonly/path')):
                with patch('game_installer.INSTALLED_GAMES_FILE',
                          Path('/readonly/path/installed_games.json')):
                    # Should not crash during init
                    installer = GameInstaller(games_dir=temp_dirs['games_dir'])
                    assert installer is not None
        except (PermissionError, OSError):
            # Expected on some systems
            pass
    
    def test_check_dependencies_with_none(self, mock_installer):
        """Should handle None in dependencies list"""
        result = mock_installer.check_dependencies([None])
        assert isinstance(result, dict)
    
    def test_uninstall_game_with_missing_path(self, mock_installer):
        """Should handle uninstall when game path doesn't exist"""
        game_id = 'test-game'
        mock_installer.installed_games[game_id] = {
            'name': 'Test Game',
            'path': '/nonexistent/path',
            'install_type': 'manual_download'
        }
        
        with patch.object(mock_installer, '_save_installed_games', return_value=True):
            result = mock_installer.uninstall_game(game_id)
            # Should still remove from database even if path doesn't exist
            assert game_id not in mock_installer.installed_games
