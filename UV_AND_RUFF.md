# UV and Ruff Setup

This project is configured to work with [uv](https://github.com/astral-sh/uv) - a fast Python package installer and resolver, and [ruff](https://github.com/astral-sh/ruff) - a fast Python linter and formatter.

## Quick Start with UV

### Install UV

```bash
# On macOS
brew install uv

# On Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Running TunerTUI with UV

The easiest way to run TunerTUI with uv:

```bash
# Run the tuner directly
uv run tunertui

# Or run a Python script
uv run python3 examples/demo_notes.py
```

This automatically:
- Creates a virtual environment if needed
- Installs dependencies from pyproject.toml
- Runs the command

### Install Dependencies with UV

```bash
# Install main dependencies
uv sync

# Install with dev dependencies
uv sync --all-extras

# Or just install without creating lock file
uv pip install -e .
```

### Using UV with Virtual Environments

```bash
# Create venv and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Run with venv active
tunertui
```

## Ruff Configuration

Ruff is configured in `pyproject.toml` for fast linting and code quality checks.

### Ruff Rules

The project is configured to check:
- **E** - PEP 8 errors
- **F** - PyFlakes (undefined names, unused imports)
- **W** - PEP 8 warnings
- **I** - isort (import sorting)

### Running Ruff

```bash
# Check code quality
uv run ruff check tunertui/

# Format imports (isort integration)
uv run ruff check --fix tunertui/

# Check specific file
uv run ruff check tunertui/audio.py

# Show detailed output
uv run ruff check --show-source tunertui/
```

### Ruff Configuration in pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

[tool.ruff.lint.isort]
known-first-party = ["tunertui"]
```

## Complete Development Workflow with UV and Ruff

### 1. Install and Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the project
git clone https://github.com/mamercad/tunertui.git
cd tunertui

# Create virtual environment and install dependencies
uv sync --all-extras
```

### 2. Run the Application

```bash
# Option A: Direct uv run
uv run tunertui

# Option B: With virtual environment
uv venv
source .venv/bin/activate
tunertui
```

### 3. Check Code Quality

```bash
# Run ruff checks
uv run ruff check tunertui/

# Fix fixable issues
uv run ruff check --fix tunertui/

# Show detailed results
uv run ruff check --show-source tunertui/
```

### 4. Run Tests

```bash
# Run pytest
uv run pytest

# Run with coverage
uv run pytest --cov=tunertui
```

### 5. Type Checking

```bash
# Run mypy
uv run mypy tunertui/
```

## UV Advanced Features

### Using UV with Different Python Versions

```bash
# Specify Python version
uv run --python 3.10 python demo.py

# List available Python versions
uv python list

# Install specific Python version
uv python install 3.10
```

### Creating a Lock File

```bash
# Create uv.lock (recommended for reproducible installs)
uv lock

# Update lock file
uv lock --upgrade

# Install from lock file
uv sync --frozen
```

### UV Workspace Support

For monorepo projects:

```toml
[tool.uv]
workspaces = ["packages/*"]
```

### Development Dependencies

Development dependencies are specified in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.3.0",
    "mypy>=1.0.0",
]
```

Install with:
```bash
uv sync --all-extras
```

## Ruff Advanced Usage

### Configuration Options

```toml
[tool.ruff]
# Maximum line length
line-length = 100

# Target Python version
target-version = "py39"

# Exclude files
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "dist",
    "build",
]

# Extend select (add more checks)
extend-select = ["UP"]  # pyupgrade checks

[tool.ruff.lint]
# Per-file ignores
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Ignore unused imports
```

### Fixing Code Automatically

```bash
# Fix all auto-fixable issues
uv run ruff check --fix tunertui/

# Preview changes without applying
uv run ruff check --fix --diff tunertui/

# Only check, don't fix
uv run ruff check tunertui/
```

## Integration with IDEs

### VS Code

Install the Ruff extension:
1. Open VS Code
2. Go to Extensions
3. Search for "Ruff"
4. Install the official Ruff extension

The extension will automatically use the project's ruff configuration.

### PyCharm

1. Install ruff: `uv pip install ruff`
2. Go to Settings → Tools → Python Integrated Tools
3. Set "Default linter" to "Ruff"
4. Set "Default formatter" to "Ruff"

## Pre-commit Integration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Install pre-commit hook:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## CI/CD with GitHub Actions

Example `.github/workflows/lint.yml`:

```yaml
name: Lint

on: [push, pull_request]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: astral-sh/setup-uv@v1
      - run: uv run ruff check tunertui/
      - run: uv run mypy tunertui/
```

## Common Commands

```bash
# Install
uv sync --all-extras

# Run app
uv run tunertui

# Run tests
uv run pytest

# Check code quality
uv run ruff check tunertui/

# Fix code
uv run ruff check --fix tunertui/

# Type checking
uv run mypy tunertui/

# Run demo
uv run python examples/demo_notes.py
```

## Troubleshooting

### UV not found

Make sure uv is installed and in your PATH:

```bash
uv --version
```

If not installed, follow the [installation guide](#install-uv).

### Ruff not finding files

Make sure you're running from the project root:

```bash
cd /path/to/tunertui
uv run ruff check tunertui/
```

### Virtual environment issues

Remove and recreate:

```bash
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Benefits of UV and Ruff

### UV Benefits
- ⚡ 10-100x faster than pip
- 🔒 Deterministic installs (lock files)
- 📦 Single tool for dependency management
- 🐍 Built-in Python management
- 💾 Minimal download sizes

### Ruff Benefits
- 🚀 10-100x faster than other linters
- 🎯 Catch bugs and code issues quickly
- 📏 Automatic import sorting (isort)
- ✨ Consistent code style
- 🔧 Auto-fix capabilities

## References

- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rules](https://docs.astral.sh/ruff/rules/)
- [Python Project Configuration](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

## Next Steps

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Run the tuner: `uv run tunertui`
3. Check code quality: `uv run ruff check tunertui/`
4. Fix issues: `uv run ruff check --fix tunertui/`

Enjoy fast, reliable Python development! 🚀
