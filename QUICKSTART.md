# Quick Start Guide

## Installation

### Option A: Using UV (Recommended) ⚡

Fast, reliable Python package management:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the tuner (dependencies installed automatically)
uv run tunertui
```

That's it! UV handles everything automatically.

### Option B: Using pip directly

```bash
pip install -r requirements.txt
```

### Option C: Using the pyproject.toml

```bash
pip install -e .
```

## Run the Tuner

### With UV (Fastest Way)
```bash
# Run directly
uv run tunertui

# Run with a specific Python version
uv run --python 3.10 tunertui
```

### With Traditional Python
```bash
# Using the CLI
tunertui

# Or directly with Python
python3 -m tunertui.cli

# Run examples
python3 examples/demo_notes.py  # Test without audio
```

### 2. Run the Tuner

```bash
# Using the CLI
tunertui

# Or directly with Python
python3 -m tunertui.cli

# Or from the examples directory
cd examples
python3 frequency_detection_test.py  # Test without audio
```

## What You'll See

When you run `tunertui`, you'll see:

```
╔════════════════════════════════════════════════════════╗
║  TunerTUI - Instrument Tuner                           ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Note:              E4                                 ║
║  Frequency:       329.63 Hz                            ║
║                                                        ║
║  ─────────────────◆────────────────────────────────── ║
║                                                        ║
║  Status:           ✓ IN TUNE                           ║
║  Cents Off:         +0.05                              ║
║  Confidence:        85.3%                              ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

## Using the Tuner

1. **Select Instrument** - Choose from the dropdown (Guitar, Bass, Ukulele, etc.)
2. **Click Start** - Begin capturing audio from your microphone
3. **Play/Tune** - Play a string or note on your instrument
4. **Watch the Display** - See real-time feedback:
   - `✓ IN TUNE` - You're in tune!
   - `♯ SHARP` - Play a lower note
   - `♭ FLAT` - Play a higher note
5. **Adjust** - Tune until the note is in tune
6. **Repeat** - Go through each string

## Keyboard Controls

- `Ctrl+C` - Exit the application
- `Tab` - Navigate between controls
- `Space` - Activate buttons

## Troubleshooting

**"No module named 'sounddevice'"**
```bash
pip install sounddevice
```

**"No module named 'textual'"**
```bash
pip install textual
```

**Microphone not working**
- Check microphone permissions
- Try playing louder
- Ensure no other apps are using the mic

**Inaccurate detection**
- Use the notes that are closer to middle frequencies (avoid very low/high notes)
- Minimize background noise
- Test with the example script: `python3 examples/frequency_detection_test.py`

## Architecture Overview

```
Audio Input (Microphone)
         ↓
AudioCapture (sounddevice)
         ↓
FrequencyDetector (YIN Algorithm)
         ↓
NoteUtils (Frequency → Note conversion)
         ↓
TUI Display (Textual)
         ↓
Visual Feedback
```

## Next Steps

- Try different instruments in the preset list
- Experiment with different audio devices
- Check the examples for testing frequency detection
- Customize instrument tunings in `tunertui/notes.py`

## Contributing

Found a bug? Have a feature idea? Check the main README.md for contribution guidelines!
