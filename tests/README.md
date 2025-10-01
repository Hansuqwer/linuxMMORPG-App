# Test Suite for Linux MMORPG Launcher

This directory contains comprehensive tests for the Linux MMORPG Launcher application.

## Overview

The test suite covers:
- **Game Database Validation** - Verifies all 42+ games in the database
- **Installation Logic** - Tests game installation and dependency checking
- **Auto-Detection** - Tests for auto-detecting installed games (RF Altruism, uaRO, etc.)
- **AUR/Flatpak/UMU** - Tests package manager and launcher integration
- **Configuration Persistence** - Tests saving and loading game configurations

## Test Files

### `test_games_db.py` (390 lines)
Comprehensive tests for the game database (`games_db.py`):
- Database structure validation
- Query function tests (by ID, genre, native, tested)
- Specific game configuration tests
- Data integrity checks
- Tests for all games in database

### `test_game_installer.py` (270 lines)
Tests for the game installer (`game_installer.py`):
- GameInstaller initialization
- AUR helper detection tests
- Dependency checking tests
- Game installation/uninstallation tests
- Auto-detection tests
- Game launching tests
- Configuration persistence tests

## Running Tests

### Quick Start

```bash
# Run all tests
./run_tests.sh

# Or use pytest directly
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_games_db.py

# Run specific test class
pytest tests/test_games_db.py::TestDatabaseStructure

# Run specific test
pytest tests/test_games_db.py::TestDatabaseStructure::test_database_exists
```

### Using Test Markers

Tests are organized with markers for easy filtering:

```bash
# Run only database tests
pytest -m database

# Run only installer tests
pytest -m installer

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"

# Run auto-detection tests
pytest -m auto_detect
```

## Requirements

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Required packages:
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- pytest-mock >= 3.11.1
- pytest-timeout >= 2.1.0

## Test Configuration

Tests are configured via `pytest.ini` in the root directory:
- Minimum pytest version: 6.0
- Test discovery: `tests/` directory
- Verbose output enabled
- Strict marker mode enabled

## Coverage

To generate coverage reports:

```bash
# HTML report (opens in browser)
pytest --cov=. --cov-report=html
xdg-open htmlcov/index.html

# Terminal report
pytest --cov=. --cov-report=term

# XML report (for CI)
pytest --cov=. --cov-report=xml
```

## CI/CD Integration

Tests run automatically on GitHub Actions via `.github/workflows/tests.yml`:
- Triggers on push and pull requests
- Tests on Python 3.10+
- Generates coverage reports
- Uploads artifacts

## Writing New Tests

### Test Structure

Follow existing patterns:

```python
import pytest
from module_to_test import function_to_test

class TestFeatureName:
    """Test description"""
    
    def test_specific_behavior(self):
        """Should do something specific"""
        result = function_to_test()
        assert result == expected_value
```

### Using Fixtures

```python
@pytest.fixture
def sample_data():
    """Provide test data"""
    return {'key': 'value'}

def test_with_fixture(sample_data):
    """Test using fixture"""
    assert 'key' in sample_data
```

### Mocking

```python
from unittest.mock import Mock, patch

@patch('module.external_function')
def test_with_mock(mock_func):
    """Test with mocked function"""
    mock_func.return_value = 'mocked'
    result = function_that_calls_external()
    assert result == 'mocked'
```

## Database Tests

### Structure Tests
Verify all games have required fields:
- name, genre, server, population
- description, website, client_download_url
- install_type, dependencies, executable
- install_notes, native, tested

### Query Tests
Test all query functions:
- `get_all_games()` - Returns complete database
- `get_game_by_id(game_id)` - Returns specific game
- `get_games_by_genre(genre)` - Filters by genre
- `get_native_games()` - Returns Linux native games
- `get_tested_games()` - Returns tested games

### Data Integrity Tests
- No duplicate game names
- Valid URLs for website and downloads
- Non-empty dependencies for non-native games
- Proper install_type values
- Meaningful descriptions and notes

## Installer Tests

### Initialization Tests
- Creates game directory
- Creates config directory
- Loads existing configurations
- Detects AUR helper

### Dependency Tests
- Checks for umu-launcher
- Checks for Wine variants
- Checks for Steam
- Checks for Flatpak
- Handles missing dependencies

### Installation Tests
- Installs manual download games
- Installs AUR packages
- Installs Flatpak applications
- Handles Steam games
- Auto-detects existing installations

### Persistence Tests
- Saves installed games to JSON
- Loads installed games from JSON
- Handles corrupt JSON gracefully
- Updates configuration after install/uninstall

## Known Issues

### Test Environment Limitations

1. **Package Manager Tests**: Some tests requiring `pacman`, `yay`, or `flatpak` may fail if not available
2. **Permission Tests**: Tests requiring `sudo` are mocked to avoid permission issues
3. **Network Tests**: Download tests use mocks to avoid network dependencies

### Skipped Tests

Some tests may be skipped based on environment:
- AUR helper tests (requires Arch Linux)
- Flatpak tests (requires Flatpak installed)
- Steam tests (requires Steam installed)

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure you're in the project root
cd /path/to/linuxMMORPG-App
python -m pytest
```

**Module Not Found**
```bash
# Add project root to PYTHONPATH
export PYTHONPATH=/path/to/linuxMMORPG-App:$PYTHONPATH
pytest
```

**Permission Errors**
```bash
# Tests shouldn't require sudo, use mocks instead
# If you see permission errors, check test isolation
```

**Fixture Errors**
```bash
# Make sure pytest is properly installed
pip install -r requirements-test.txt
```

## Contributing

When adding new tests:

1. Follow existing naming conventions
2. Use descriptive test names starting with `test_`
3. Group related tests in classes
4. Add docstrings to test classes and functions
5. Use appropriate markers (`@pytest.mark.unit`, etc.)
6. Mock external dependencies
7. Keep tests independent and isolated
8. Update this README with new test categories

## Test Statistics

Current test coverage:
- **Database Tests**: 40+ tests covering all games and queries
- **Installer Tests**: 30+ tests covering installation workflows
- **Total Lines**: 660+ lines of test code
- **Coverage Target**: 80%+ for core modules

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## License

Same as main project - see LICENSE file in root directory.
