.PHONY: check format test clean

# Default Python interpreter
PYTHON = python3

# Virtual environment
VENV = env
VENV_PYTHON = $(VENV)/bin/python
VENV_UV = uv

# Source directories
SRC_DIRS = src tests

# Install development dependencies
install-dev:
	$(VENV_UV) pip install -e ".[dev]"

# Check code with ruff
check-ruff:
	$(VENV_PYTHON) -m ruff check $(SRC_DIRS)

# Check code with black (no changes)
check-black:
	$(VENV_PYTHON) -m black --check $(SRC_DIRS)

# Check code with isort (no changes)
check-isort:
	$(VENV_PYTHON) -m isort --check-only $(SRC_DIRS)

# Run all checks
check: check-ruff check-black check-isort

# Format code with black
format-black:
	$(VENV_PYTHON) -m black $(SRC_DIRS)

# Format code with isort
format-isort:
	$(VENV_PYTHON) -m isort $(SRC_DIRS)

# Format code with ruff (auto-fix)
format-ruff:
	$(VENV_PYTHON) -m ruff check --fix $(SRC_DIRS)

# Run all formatters
format: format-black format-isort format-ruff

# Run tests with pytest
test:
	$(VENV_PYTHON) -m pytest

# Run tests with coverage
test-cov:
	$(VENV_PYTHON) -m pytest --cov=blokus

# Clean up cache files
clean:
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete