#!/bin/bash
# Convenient test runner script for Linux MMORPG Launcher
# Run tests with various options

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Function to print colored output
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if pytest is installed
check_dependencies() {
    print_header "Checking Dependencies"
    
    if ! command -v pytest &> /dev/null; then
        print_error "pytest not found!"
        echo "Install test dependencies with:"
        echo "  pip install -r requirements-test.txt"
        exit 1
    fi
    
    print_success "pytest found: $(pytest --version)"
    
    # Check for other dependencies
    python3 -c "import pytest_cov" 2>/dev/null && print_success "pytest-cov available" || print_warning "pytest-cov not found (coverage disabled)"
    python3 -c "import pytest_mock" 2>/dev/null && print_success "pytest-mock available" || print_warning "pytest-mock not found"
    
    echo
}

# Show usage
show_usage() {
    echo "Usage: $0 [option]"
    echo
    echo "Options:"
    echo "  all          Run all tests (default)"
    echo "  db           Run database tests only"
    echo "  installer    Run installer tests only"
    echo "  unit         Run unit tests only"
    echo "  integration  Run integration tests only"
    echo "  coverage     Run tests with coverage report"
    echo "  verbose      Run tests with verbose output"
    echo "  quick        Run tests without slow tests"
    echo "  watch        Run tests in watch mode"
    echo "  help         Show this help message"
    echo
    echo "Examples:"
    echo "  ./run_tests.sh                # Run all tests"
    echo "  ./run_tests.sh db             # Run database tests only"
    echo "  ./run_tests.sh coverage       # Run with coverage"
    echo "  ./run_tests.sh verbose        # Verbose output"
}

# Main test execution
run_tests() {
    local test_option="${1:-all}"
    
    case "$test_option" in
        all)
            print_header "Running All Tests"
            pytest -v --tb=short
            ;;
        
        db|database)
            print_header "Running Database Tests"
            pytest tests/test_games_db.py -v --tb=short
            ;;
        
        installer)
            print_header "Running Installer Tests"
            pytest tests/test_game_installer.py -v --tb=short
            ;;
        
        unit)
            print_header "Running Unit Tests"
            pytest -m unit -v --tb=short
            ;;
        
        integration)
            print_header "Running Integration Tests"
            pytest -m integration -v --tb=short
            ;;
        
        coverage)
            print_header "Running Tests with Coverage"
            pytest --cov=. --cov-report=html --cov-report=term -v
            print_success "Coverage report generated in htmlcov/"
            echo "Open htmlcov/index.html in your browser to view the report"
            ;;
        
        verbose)
            print_header "Running Tests (Verbose)"
            pytest -vv --tb=long
            ;;
        
        quick)
            print_header "Running Quick Tests (excluding slow)"
            pytest -m "not slow" -v --tb=short
            ;;
        
        watch)
            print_header "Running Tests in Watch Mode"
            if command -v pytest-watch &> /dev/null; then
                pytest-watch
            else
                print_warning "pytest-watch not installed"
                echo "Install with: pip install pytest-watch"
                echo "Running tests once instead..."
                pytest -v --tb=short
            fi
            ;;
        
        help|-h|--help)
            show_usage
            exit 0
            ;;
        
        *)
            print_error "Unknown option: $test_option"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Main script
main() {
    print_header "Linux MMORPG Launcher - Test Runner"
    echo
    
    check_dependencies
    run_tests "$@"
    
    echo
    print_success "Test run completed!"
}

# Run main function
main "$@"
