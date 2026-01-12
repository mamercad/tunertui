# TunerTUI

A modern, terminal-based instrument tuner built with Python and [Textual](https://textual.textualize.io/).

## Features

- **Real-time audio capture** from microphone using `sounddevice`
- **YIN algorithm** for accurate pitch detection
- **Multiple instrument presets**: Guitar, Bass, Ukulele, Banjo, Mandolin, Violin
- **Visual tuning gauge** showing sharp/flat status
- **Per-string tuning display** with visual feedback
- **Confidence meter** showing signal quality
- **Cross-platform** (Linux, macOS, Windows)

## Installation

### Prerequisites

- Python 3.9 or higher
- A working microphone

### From Source

```bash
# Clone or navigate to the project
cd tunertui

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Running

```bash
# Run the tuner
tunertui

# Or run directly from Python
python -m tunertui.cli
```

## Usage

1. **Start the Application**
   ```
   tunertui
   ```

2. **Select an Instrument**
   - Use the instrument selector dropdown
   - Available: Guitar (Standard, Drop D, Open G), Bass, Ukulele, Banjo, Mandolin, Violin

3. **Start Tuning**
   - Click the "Start" button to begin capturing audio
   - Pluck or play a string/note on your instrument
   - The display will show the detected frequency and note

4. **Tune Your Instrument**
   - Watch the gauge to see if you're sharp (↑) or flat (↓)
   - Adjust your instrument until the note is in tune (✓)
   - The display shows individual string tuning status

## How It Works

### Frequency Detection

The application uses the **YIN algorithm** for pitch detection, which is:
- More accurate than FFT-based methods for musical frequencies
- Robust to harmonics and noise
- Computationally efficient enough for real-time processing

### Audio Processing

1. Audio is captured from the microphone at 44.1 kHz
2. A window function is applied to reduce spectral leakage
3. The YIN algorithm processes the audio buffer
4. Detected frequency is compared to standard note frequencies (A4 = 440 Hz)
5. Results show: note name, frequency, cents off, and confidence

### Note Calculation

- Uses equal temperament tuning (12-tone equal temperament)
- References A4 = 440 Hz (international standard)
- Displays deviation in cents (-50 to +50 cents = -1 to +1 semitone)

## Configuration

Currently, presets are hardcoded. You can extend `InstrumentPresets` in `tunertui/notes.py`:

```python
GUITAR_CUSTOM = Instrument(
    "Guitar (Custom)",
    ["D2", "A2", "D3", "G3", "B3", "F4"]  # Custom tuning
)
```

## Troubleshooting

### No signal detected
- Check that your microphone is properly connected
- Verify microphone permissions in system settings
- Try playing louder or closer to the microphone

### Inaccurate detection
- Ensure minimal background noise
- The YIN algorithm works best with frequencies between 50 Hz and 4000 Hz
- Avoid very low frequencies which are harder to detect

### Performance issues
- Close other applications using audio
- Increase the block size in `AudioConfig` if detection is slow

## Architecture

```
tunertui/
├── audio.py      # Audio capture and frequency detection (YIN algorithm)
├── notes.py      # Note definitions and instrument presets
├── ui.py         # Textual UI components
├── cli.py        # CLI entry point
└── __init__.py
```

## Dependencies

- **textual**: Terminal UI framework
- **numpy**: Numerical computations
- **sounddevice**: Audio I/O
- **scipy**: Signal processing (optional, for future enhancements)

## Future Enhancements

- [ ] Calibration mode (set custom reference frequency)
- [ ] Export tuning history
- [ ] Custom instrument definitions
- [ ] Visual waveform display
- [ ] Strobe tuner mode
- [ ] Auto-detection of instrument type
- [ ] Chord detection
- [ ] MIDI support

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## References

- [Textual Documentation](https://textual.textualize.io/)
- [YIN Algorithm](http://audition.lis.uiuc.edu/~alkamal/Papers/alkamalYINAlgorithm.pdf)
- [Equal Temperament Tuning](https://en.wikipedia.org/wiki/Equal_temperament)
