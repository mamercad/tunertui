# Installation and Setup Guide

## System Requirements

- Python 3.9 or higher
- A working microphone
- Terminal that supports Unicode (most modern terminals)
- For Linux: may need to install audio libraries

## Quick Start

### Option A: Using UV (Recommended) ⚡

UV is a fast, modern Python package manager:

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# On macOS with Homebrew:
brew install uv

# 2. Run the tuner (dependencies are installed automatically)
uv run tunertui
```

**That's it!** Dependencies are installed automatically. See [UV_AND_RUFF.md](UV_AND_RUFF.md) for more features.

### Option B: Using pip (Traditional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
tunertui
```

### Option C: Using pyproject.toml

```bash
pip install -e .
tunertui
```

### Option D: Manual Installation

```bash
pip install textual>=0.30.0
pip install numpy>=1.23.0
pip install sounddevice>=0.4.5
pip install scipy>=1.9.0
tunertui
```

## Platform-Specific Instructions

### macOS
```bash
# Install dependencies (if using Homebrew)
brew install portaudio

# Install Python packages
pip install -r requirements.txt

# Run
tunertui
```

### Linux (Ubuntu/Debian)
```bash
# Install audio libraries
sudo apt-get install libportaudio2 portaudio19-dev
sudo apt-get install libasound2-dev

# Install Python packages
pip install -r requirements.txt

# Run
tunertui
```

### Windows
```bash
# Install Python packages (usually straightforward on Windows)
pip install -r requirements.txt

# Run
tunertui
```

## Troubleshooting Installation

### "ModuleNotFoundError: No module named 'sounddevice'"
```bash
pip install --upgrade sounddevice
```

### "ModuleNotFoundError: No module named 'textual'"
```bash
pip install --upgrade textual
```

### "ModuleNotFoundError: No module named 'numpy'"
```bash
pip install --upgrade numpy
```

### macOS: "OSError: cannot load library"
This usually means portaudio isn't installed:
```bash
brew install portaudio
pip install --upgrade sounddevice
```

### Linux: "libasound.so.2: cannot open shared object file"
Install ALSA libraries:
```bash
sudo apt-get install libasound2-dev
```

### Windows: Audio device not found
1. Check Control Panel → Sound Settings
2. Ensure microphone is set as default input
3. Try running as Administrator
4. Update audio drivers

## Verify Installation

Run the included demo script:
```bash
cd examples
python3 demo_notes.py
```

This will show:
- Frequency-to-note conversions
- All instrument presets
- Simulated tuning feedback
- Explanation of cents

No microphone or audio libraries needed for this demo.

## Development Setup

For contributing or modifying the code:

### Install with Dev Dependencies
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Format Code
```bash
black tunertui/
ruff check tunertui/
```

### Type Checking
```bash
mypy tunertui/
```

## Using Different Audio Devices

TunerTUI automatically uses the system's default microphone. To use a different device:

### List Available Devices
```python
import sounddevice as sd
print(sd.query_devices())
```

### Modify Audio Configuration
Edit the `AudioConfig` in `tunertui/audio.py` or create a custom config:
```python
from tunertui.audio import AudioConfig, TunerEngine

config = AudioConfig(
    sample_rate=44100,
    block_size=4096,
    # Add device parameter if needed
)
engine = TunerEngine()
```

## Next Steps

1. **Try the Demo**: `python3 examples/demo_notes.py`
2. **Run the Tuner**: `tunertui`
3. **Select an Instrument**: Choose from the dropdown
4. **Start Tuning**: Click Start and play a note
5. **Tune**: Adjust your instrument based on visual feedback

## Getting Help

### Check the Documentation
- `README.md` - Full project documentation
- `QUICKSTART.md` - Quick usage guide
- `ARCHITECTURE.md` - Technical architecture details

### Verify Your Setup
```bash
# Test notes system (no audio needed)
python3 -c "from tunertui.notes import InstrumentPresets; print('Notes system OK'); print([i.name for i in InstrumentPresets.ALL])"

# Test audio (requires microphone)
python3 examples/frequency_detection_test.py
```

### Common Issues

**TUI not rendering correctly**: Update textual
```bash
pip install --upgrade textual
```

**Audio latency too high**: Reduce block size in AudioConfig
```python
AudioConfig(block_size=2048)  # Instead of 4096
```

**Inaccurate detection**: Try test frequencies in frequency_detection_test.py

## Uninstalling

```bash
# If installed with pip
pip uninstall tunertui textual numpy sounddevice scipy

# If installed from source
pip uninstall -e .
```

## Additional Resources

- [Textual Documentation](https://textual.textualize.io/)
- [SoundDevice Documentation](https://python-sounddevice.readthedocs.io/)
- [NumPy Documentation](https://numpy.org/doc/)
- [YIN Algorithm Paper](http://audition.lis.uiuc.edu/~alkamal/Papers/alkamalYINAlgorithm.pdf)

Enjoy tuning! 🎸🎵
