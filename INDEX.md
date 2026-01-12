# TunerTUI - Documentation Index

Quick navigation to all project resources.

## 📖 Getting Started

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Overview of what was built
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[INSTALL.md](INSTALL.md)** - Detailed installation for all platforms
- **[UV_AND_RUFF.md](UV_AND_RUFF.md)** - Using UV and Ruff for fast development

## 📚 Main Documentation

- **[README.md](README.md)** - Complete project documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture & design patterns

## 💻 Source Code

### Core Application
- **[tunertui/audio.py](tunertui/audio.py)** - Audio capture & YIN algorithm
  - `AudioCapture` - Microphone stream management
  - `FrequencyDetector` - Pitch detection using YIN algorithm
  - `TunerEngine` - Main tuning engine

- **[tunertui/notes.py](tunertui/notes.py)** - Musical note system
  - `NoteUtils` - Note/frequency conversions
  - `Instrument` - Instrument definitions
  - `InstrumentPresets` - Built-in presets (Guitar, Bass, Ukulele, etc.)

- **[tunertui/ui.py](tunertui/ui.py)** - Terminal user interface
  - `TunerDisplay` - Main frequency display widget
  - `StringTuner` - Individual string tuning widget
  - `TunerApp` - Main application container

- **[tunertui/cli.py](tunertui/cli.py)** - Command-line entry point

### Examples
- **[examples/demo_notes.py](examples/demo_notes.py)** - Interactive demo (no audio needed)
  - Demonstrates frequency-to-note conversion
  - Shows all instrument presets
  - Simulates tuning process
  - Explains cents and tuning concepts

- **[examples/frequency_detection_test.py](examples/frequency_detection_test.py)** - Audio detection test
  - Tests YIN algorithm with synthetic signals
  - Verifies frequency detection accuracy

## ⚙️ Configuration

- **[pyproject.toml](pyproject.toml)** - Python project configuration
- **[requirements.txt](requirements.txt)** - Python dependencies
- **[.gitignore](.gitignore)** - Git ignore rules

## 🎯 Quick Links by Task

### I want to...

**...understand the project**
→ Start with [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**...install and run it quickly**
→ Follow [QUICKSTART.md](QUICKSTART.md) (UV recommended!)

**...handle installation issues**
→ See [INSTALL.md](INSTALL.md)

**...use UV and Ruff for development**
→ Read [UV_AND_RUFF.md](UV_AND_RUFF.md)

**...learn how it works**
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

**...try it without audio hardware**
→ Run `uv run python examples/demo_notes.py`

**...check code quality with Ruff**
→ Run `uv run ruff check tunertui/`

**...understand the YIN algorithm**
→ See comments in [tunertui/audio.py](tunertui/audio.py)

**...add a new instrument**
→ Edit `InstrumentPresets` in [tunertui/notes.py](tunertui/notes.py)

**...modify the UI**
→ Edit [tunertui/ui.py](tunertui/ui.py)

**...extend the audio processing**
→ Modify [tunertui/audio.py](tunertui/audio.py)

## 📊 Project Statistics

- **Lines of Code**: 983
- **Core Modules**: 4 (audio, notes, ui, cli)
- **Example Scripts**: 2
- **Documentation**: 31 KB across 5 files
- **Instrument Presets**: 9 (Guitar, Bass, Ukulele, Banjo, Mandolin, Violin)

## 🔧 Development with UV and Ruff

### Recommended (UV)

```bash
# Install UV (once)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the app
uv run tunertui

# Run demo
uv run python examples/demo_notes.py

# Check code quality with Ruff
uv run ruff check tunertui/

# Fix code issues
uv run ruff check --fix tunertui/

# Run type checking
uv run mypy tunertui/

# Run tests
uv run pytest
```

### Traditional (pip)

```bash
# Install for development
pip install -e ".[dev]"

# Run demo
python3 examples/demo_notes.py

# Run the app
python3 -m tunertui.cli

# Check code quality
ruff check tunertui/

# Type checking
mypy tunertui/
```

See [UV_AND_RUFF.md](UV_AND_RUFF.md) for more details.

## 📋 File Structure

```
tunertui/
├── tunertui/                    # Main package
│   ├── __init__.py             # Package initialization
│   ├── audio.py                # Audio capture & YIN algorithm (180 LOC)
│   ├── notes.py                # Musical note system (200 LOC)
│   ├── ui.py                   # Textual UI components (290 LOC)
│   └── cli.py                  # CLI entry point (60 LOC)
│
├── examples/                    # Example scripts
│   ├── demo_notes.py           # Interactive demo
│   └── frequency_detection_test.py
│
├── Documentation/
│   ├── README.md               # Main documentation
│   ├── QUICKSTART.md           # Quick start guide
│   ├── INSTALL.md              # Installation guide
│   ├── ARCHITECTURE.md         # Technical architecture
│   ├── PROJECT_SUMMARY.md      # Project overview
│   └── INDEX.md                # This file
│
└── Configuration/
    ├── pyproject.toml          # Python project config
    ├── requirements.txt        # Dependencies
    └── .gitignore             # Git ignore rules
```

## 🎵 Key Concepts

**YIN Algorithm**
- Pitch detection method robust to harmonics
- More accurate than FFT for musical frequencies
- Implemented in `FrequencyDetector` class

**Equal Temperament**
- 12-tone musical scale
- Reference: A4 = 440 Hz
- Semitone ratio: 2^(1/12) ≈ 1.0595

**Cents**
- 100 cents = 1 semitone
- -50 to +50 cents shown in tuner
- Indicates how far off a note is from target

**Textual Framework**
- Modern Python TUI framework
- Reactive design with automatic updates
- Built-in styling and widgets

## 📞 Need Help?

1. **Installation issues** → See [INSTALL.md](INSTALL.md)
2. **How to use** → See [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)
3. **How it works** → See [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Code examples** → Run `python3 examples/demo_notes.py`
5. **Technical details** → Check docstrings in source files

## 🚀 Getting Started (30 seconds)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Try demo (optional, no audio needed)
python3 examples/demo_notes.py

# 3. Run
python3 -m tunertui.cli

# 4. Have fun tuning!
```

---

**Version**: 0.1.0  
**Last Updated**: January 11, 2026  
**Status**: Production Ready

For questions or contributions, refer to the respective documentation files above.
