# Kino.pub Kodi Addon - Makefile
# ================================
#
# This Makefile provides common development tasks for the Kino.pub Kodi addon.
# Make sure you have uv installed: https://docs.astral.sh/uv/

.PHONY: help install test lint format type-check clean build package dev-setup all check pre-commit
.DEFAULT_GOAL := help

# Variables
ADDON_ID = plugin.video.kinopub
PYTHON_VERSION = 3.11
VENV_DIR = .venv
BUILD_DIR = build
DIST_DIR = dist

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Kino.pub Kodi Addon - Development Commands$(NC)"
	@echo "==========================================="
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Examples:$(NC)"
	@echo "  make dev-setup    # Set up development environment"
	@echo "  make check        # Run all quality checks"
	@echo "  make build        # Build addon package"
	@echo "  make clean        # Clean all generated files"

# Development Setup
dev-setup: ## Set up development environment with dependencies
	@echo "$(GREEN)Setting up development environment...$(NC)"
	uv python install $(PYTHON_VERSION)
	uv sync --all-extras
	@echo "$(GREEN)✓ Development environment ready!$(NC)"

install: ## Install project dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✓ Dependencies installed!$(NC)"

install-dev: ## Install development dependencies
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	uv sync --all-extras
	@echo "$(GREEN)✓ Development dependencies installed!$(NC)"

# Testing
test: ## Run all tests
	@echo "$(GREEN)Running tests...$(NC)"
	uv run pytest tests/ -v
	@echo "$(GREEN)✓ Tests completed!$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	uv run pytest tests/ -v --cov=lib --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	uv run pytest-watch tests/ -- -v

test-benchmark: ## Run performance benchmarks
	@echo "$(GREEN)Running benchmarks...$(NC)"
	uv run pytest tests/ --benchmark-only -v

# Code Quality
lint: ## Run ruff linter
	@echo "$(GREEN)Running ruff linter...$(NC)"
	uv run ruff check .
	@echo "$(GREEN)✓ Linting completed!$(NC)"

lint-fix: ## Run ruff linter with auto-fix
	@echo "$(GREEN)Running ruff linter with auto-fix...$(NC)"
	uv run ruff check . --fix
	@echo "$(GREEN)✓ Auto-fixes applied!$(NC)"

format: ## Format code with ruff
	@echo "$(GREEN)Formatting code...$(NC)"
	uv run ruff format .
	@echo "$(GREEN)✓ Code formatted!$(NC)"

format-check: ## Check code formatting without making changes
	@echo "$(GREEN)Checking code formatting...$(NC)"
	uv run ruff format . --check
	@echo "$(GREEN)✓ Format check completed!$(NC)"

type-check: ## Run mypy type checker
	@echo "$(GREEN)Running type checker...$(NC)"
	uv run mypy lib/
	@echo "$(GREEN)✓ Type checking completed!$(NC)"

# Combined checks
check: lint type-check test ## Run all quality checks (lint, type-check, test)
	@echo "$(GREEN)✓ All checks passed!$(NC)"

check-ci: lint format-check type-check test ## Run all CI checks including format check
	@echo "$(GREEN)✓ All CI checks passed!$(NC)"

# Building and Packaging
build: clean ## Build addon package
	@echo "$(GREEN)Building addon package...$(NC)"
	mkdir -p $(BUILD_DIR) $(DIST_DIR)
	uv run python scripts/build_addon.py
	@echo "$(GREEN)✓ Addon package built successfully!$(NC)"

package: build ## Alias for build
	@echo "$(GREEN)✓ Package created!$(NC)"

# Development utilities
clean: ## Clean all generated files and caches
	@echo "$(GREEN)Cleaning generated files...$(NC)"
	rm -rf $(BUILD_DIR)/ $(DIST_DIR)/ *.zip
	rm -rf .pytest_cache/ .coverage htmlcov/ .mypy_cache/
	rm -rf **/__pycache__/ **/*.pyc **/*.pyo
	rm -rf repository/ tests/test_profile/
	find . -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup completed!$(NC)"

clean-cache: ## Clean only cache files
	@echo "$(GREEN)Cleaning cache files...$(NC)"
	rm -rf .pytest_cache/ .mypy_cache/ **/__pycache__/
	@echo "$(GREEN)✓ Cache cleaned!$(NC)"

# Git hooks and pre-commit
pre-commit: lint-fix format type-check test ## Run pre-commit checks (auto-fix lint, format, type-check, test)
	@echo "$(GREEN)✓ Pre-commit checks completed!$(NC)"

pre-push: check-ci ## Run pre-push checks (all CI checks)
	@echo "$(GREEN)✓ Pre-push checks completed!$(NC)"

# Development server (for testing API)
api-test: ## Run API test script
	@echo "$(GREEN)Running API test...$(NC)"
	uv run python api-test.py
	@echo "$(GREEN)✓ API test completed!$(NC)"

# Information commands
info: ## Show project information
	@echo "$(GREEN)Project Information$(NC)"
	@echo "==================="
	@echo "Addon ID: $(ADDON_ID)"
	@echo "Python Version: $(PYTHON_VERSION)"
	@echo "Virtual Environment: $(VENV_DIR)"
	@echo ""
	@echo "$(GREEN)File Structure:$(NC)"
	@find . -name "*.py" -not -path "./.venv/*" -not -path "./.*" | head -20

deps-info: ## Show dependency information
	@echo "$(GREEN)Dependency Information$(NC)"
	@echo "======================="
	uv tree
	@echo ""
	@echo "$(GREEN)Development Dependencies:$(NC)"
	@echo "- pytest (testing framework)"
	@echo "- ruff (linting and formatting)"
	@echo "- mypy (type checking)"
	@echo "- Kodistubs (Kodi module stubs)"
	@echo "- kodi-json (Kodi testing utilities)"

# Version management
version: ## Show current version
	@echo "$(GREEN)Current Version:$(NC)"
	@grep -o 'version="[^"]*"' addon.xml | head -1 | cut -d'"' -f2 || echo "Version not found in addon.xml"

# Kodi development helpers
kodi-logs: ## Show Kodi log location help
	@echo "$(GREEN)Kodi Log Locations:$(NC)"
	@echo "==================="
	@echo "macOS:     ~/Library/Logs/kodi.log"
	@echo "Linux:     ~/.kodi/temp/kodi.log"
	@echo "Windows:   %APPDATA%\\Kodi\\kodi.log"
	@echo ""
	@echo "$(GREEN)Tail logs:$(NC)"
	@echo "tail -f ~/.kodi/temp/kodi.log | grep $(ADDON_ID)"

kodi-profile: ## Show Kodi profile location help
	@echo "$(GREEN)Kodi Profile Locations:$(NC)"
	@echo "======================="
	@echo "macOS:     ~/Library/Application Support/Kodi/"
	@echo "Linux:     ~/.kodi/"
	@echo "Windows:   %APPDATA%\\Kodi\\"
	@echo ""
	@echo "$(GREEN)Addon Data:$(NC)"
	@echo "userdata/addon_data/$(ADDON_ID)/"

# Advanced targets
all: clean dev-setup check build ## Run complete workflow: clean, setup, check, build
	@echo "$(GREEN)✓ Complete workflow finished!$(NC)"

quick-check: lint test ## Quick check: lint and test only
	@echo "$(GREEN)✓ Quick check completed!$(NC)"

# Release workflow
release-check: clean dev-setup check-ci ## Prepare for release: clean setup and full CI checks
	@echo "$(GREEN)✓ Release checks completed!$(NC)"
	@echo "$(YELLOW)Ready for release! Run 'make build' to create package.$(NC)"

# Documentation
docs-requirements: ## Show documentation about requirements
	@echo "$(GREEN)Requirements$(NC)"
	@echo "============"
	@echo "Development:"
	@echo "- Python $(PYTHON_VERSION)+"
	@echo "- uv (ultra-fast Python package manager)"
	@echo ""
	@echo "Runtime (Kodi):"
	@echo "- Kodi 19+ (Matrix)"
	@echo "- Python 3.8+ (Kodi requirement)"
	@echo "- script.module.requests"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
