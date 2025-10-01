#!/bin/bash
# Test runner script for Linux MMORPG Launcher

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Linux MMORPG Launcher - Test Runner${NC}"
echo "======================================="
echo

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest not found${NC}"
    echo "Install test dependencies with: pip install -r requirements-test.txt"
    exit 1
fi

# Parse arguments
COVERAGE=false
PARALLEL=false
VERBOSE=false
MARKERS=""
TEST_PATH="tests/"

while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -m|--markers)
            MARKERS="$2"
            shift 2
            ;;
        -f|--file)
            TEST_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo
            echo "Options:"
            echo "  -c, --coverage     Run with coverage report"
            echo "  -p, --parallel     Run tests in parallel"
            echo "  -v, --verbose      Verbose output"
            echo "  -m, --markers      Run tests with specific markers (e.g., 'unit', 'not slow')"
            echo "  -f, --file         Run specific test file"
            echo "  -h, --help         Show this help message"
            echo
            echo "Examples:"
            echo "  $0                              # Run all tests"
            echo "  $0 -c                           # Run with coverage"
            echo "  $0 -p                           # Run in parallel"
            echo "  $0 -m 'not slow'                # Skip slow tests"
            echo "  $0 -f tests/test_games_db.py    # Run specific file"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [ "$PARALLEL" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
fi

if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=. --cov-report=html --cov-report=term"
fi

if [ -n "$MARKERS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m '$MARKERS'"
fi

PYTEST_CMD="$PYTEST_CMD $TEST_PATH"

# Run tests
echo -e "${YELLOW}Running: $PYTEST_CMD${NC}"
echo

eval $PYTEST_CMD
TEST_RESULT=$?

echo
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"

    if [ "$COVERAGE" = true ]; then
        echo
        echo -e "${YELLOW}Coverage report generated in htmlcov/index.html${NC}"
        echo "View with: firefox htmlcov/index.html"
    fi
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi

exit 0
