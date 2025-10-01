# Linux MMORPG Launcher - Test Suite

Comprehensive test suite for the Linux MMORPG Launcher application.

## Setup

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Install Application Dependencies

```bash
pip install PyQt6 pyyaml
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_game_installer.py
pytest tests/test_games_db.py
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html --cov-report=term
```

View HTML coverage report:
```bash
firefox htmlcov/index.html
```

### Run Tests in Parallel

```bash
pytest -n auto
```

### Run Only Fast Tests (Skip Slow Tests)

```bash
pytest -m "not slow"
```

### Run Specific Test Class or Function

```bash
# Run specific test class
pytest tests/test_game_installer.py::TestGameInstallerInit

# Run specific test function
pytest tests/test_game_installer.py::TestGameInstallerInit::test_creates_games_directory
```

### Verbose Output

```bash
pytest -v
```

### Show Print Statements

```bash
pytest -s
```

## Test Organization

### Test Files

- `test_game_installer.py` - Tests for game installation, detection, and management
- `test_games_db.py` - Tests for game database structure and queries

### Test Categories (Markers)

Tests are organized with markers for selective execution:

- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests across components
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.gui` - GUI-related tests (require display)
- `@pytest.mark.requires_root` - Tests requiring sudo/root
- `@pytest.mark.requires_aur` - Tests requiring AUR helper
- `@pytest.mark.requires_network` - Tests requiring network

Run tests by marker:
```bash
pytest -m unit              # Only unit tests
pytest -m "not slow"        # Skip slow tests
pytest -m "not gui"         # Skip GUI tests
```

## Test Coverage

Current test coverage includes:

### GameInstaller (game_installer.py)
- ✅ Initialization and directory creation
- ✅ AUR helper detection
- ✅ Dependency checking
- ✅ Game installation tracking
- ✅ Auto-detection of installed games
- ✅ Game launching (AUR, Flatpak, UMU)
- ✅ Game uninstallation
- ✅ Configuration persistence

### Games Database (games_db.py)
- ✅ Database structure validation
- ✅ Required field checking
- ✅ Data type validation
- ✅ URL validation
- ✅ Query functions (by ID, genre, native, tested)
- ✅ Specific game configurations
- ✅ Database integrity checks

## Writing New Tests

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch

class TestFeatureName:
    """Test description"""

    def test_specific_behavior(self):
        """Test that specific behavior works"""
        # Arrange
        expected = "result"

        # Act
        actual = function_under_test()

        # Assert
        assert actual == expected
```

### Using Fixtures

```python
@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp, ignore_errors=True)

def test_with_fixture(temp_dir):
    """Test using fixture"""
    assert temp_dir.exists()
```

### Mocking

```python
def test_with_mock():
    """Test with mocked dependencies"""
    with patch('module.function') as mock_func:
        mock_func.return_value = "mocked"
        result = code_under_test()
        assert result == "mocked"
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Manual workflow dispatch

See `.github/workflows/tests.yml` for CI configuration.

## Troubleshooting

### Qt/GUI Tests Failing

GUI tests require a display. On headless systems:
```bash
# Skip GUI tests
pytest -m "not gui"

# Or use Xvfb
xvfb-run pytest
```

### Permission Errors

Some tests may require specific permissions:
```bash
# Run with user privileges (recommended)
pytest

# Skip tests requiring root
pytest -m "not requires_root"
```

### Import Errors

Ensure you're running from the project root:
```bash
cd /path/to/linuxMMORPG-App
pytest
```

Or add project to PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

## Coverage Goals

Target coverage: **80%+**

Current coverage by module:
- `game_installer.py`: 75%+
- `games_db.py`: 95%+
- `gui.py`: 60%+ (GUI testing is complex)

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov`
4. Run linting: `flake8` and `black`
5. Update test documentation

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [PyQt Testing](https://pytest-qt.readthedocs.io/)
