# TunerTUI Architecture

## Overview

TunerTUI is a modular instrument tuning application built with Python. It captures audio from a microphone, detects the dominant frequency using the YIN algorithm, and displays real-time tuning feedback through a Textual TUI.

```
┌─────────────────┐
│   Microphone    │
└────────┬────────┘
         │ Audio Stream
         ↓
┌─────────────────────────────┐
│   sounddevice (InputStream) │  ← Audio Capture
└────────┬────────────────────┘
         │ Raw Audio Data
         ↓
┌─────────────────────────────┐
│   YIN Algorithm             │  ← Frequency Detection
│  (FrequencyDetector)        │
└────────┬────────────────────┘
         │ Detected Frequency
         ↓
┌─────────────────────────────┐
│   NoteUtils                 │  ← Frequency → Note
│  (Frequency Converter)      │
└────────┬────────────────────┘
         │ Note + Cents Off
         ↓
┌─────────────────────────────┐
│   Textual TUI               │  ← Visual Feedback
│  (Display & Controls)       │
└─────────────────────────────┘
```

## Module Structure

### 1. `audio.py` - Audio Processing
**Responsibilities:**
- Real-time audio capture from microphone
- Frequency detection using YIN algorithm
- Audio signal processing

**Key Classes:**
- `AudioConfig`: Configuration for audio capture (sample rate, block size, etc.)
- `AudioCapture`: Manages microphone stream (start/stop, read audio data)
- `FrequencyResult`: Data class for detection results (frequency, confidence, validity)
- `FrequencyDetector`: Implements YIN algorithm for pitch detection
- `TunerEngine`: Main engine orchestrating audio capture and detection

**Algorithm Details (YIN):**
```
1. Read audio buffer from microphone
2. Apply window function (Hanning) to reduce spectral leakage
3. Calculate autocorrelation difference function
4. Cumulative mean normalize
5. Find threshold crossing for minimum tau
6. Use parabolic interpolation for fine resolution
7. Convert tau (period) to frequency
8. Calculate confidence based on normalized difference
```

### 2. `notes.py` - Musical Note System
**Responsibilities:**
- Note definitions and frequency calculations
- Instrument preset configurations
- Frequency-to-note conversion with cent calculation

**Key Classes:**
- `Note`: Represents a musical note (name, frequency, octave)
- `NoteUtils`: Static utilities for note/frequency conversions
  - `frequency_to_note()`: Detect note name and cents off
  - `note_to_frequency()`: Convert note name to frequency
  - `get_notes_in_range()`: Find all notes in frequency range
- `Instrument`: Represents an instrument with multiple strings
- `InstrumentPresets`: Collection of common instrument tunings

**Supported Instruments:**
- Guitar: Standard, Drop D, Open G
- Bass: 4-string, 5-string
- Ukulele: Soprano
- Banjo: 5-string
- Mandolin
- Violin

**Tuning System:**
- Reference: A4 = 440 Hz (international standard)
- Equal temperament tuning (12-tone)
- Frequency ratio per semitone: 2^(1/12) ≈ 1.0595

### 3. `ui.py` - Textual User Interface
**Responsibilities:**
- Terminal UI rendering and interaction
- Real-time display updates
- User input handling (button clicks, dropdown selection)

**Key Classes:**
- `TunerDisplay`: Shows frequency, note, tuning gauge, cents, confidence
- `StringTuner`: Widget for displaying individual string tuning status
- `InstrumentSelector`: Dropdown for instrument selection
- `StringList`: List of all strings for current instrument
- `TunerApp`: Main application widget

**UI Components:**
```
┌─────────────────────────────────────────────┐
│ Header (Clock)                              │
├─────────────────────────────────────────────┤
│                                             │
│ ┌──────────────────┐  ┌──────────────────┐ │
│ │ Tuner Display    │  │ Instrument       │ │
│ │ • Note           │  │ Selector         │ │
│ │ • Frequency      │  │ • Dropdown       │ │
│ │ • Gauge          │  ├──────────────────┤ │
│ │ • Status         │  │ String List      │ │
│ │ • Confidence     │  │ • String 1: E2   │ │
│ │                  │  │ • String 2: A2   │ │
│ │                  │  │ • String 3: D3   │ │
│ │                  │  ├──────────────────┤ │
│ │                  │  │ [Start] [Stop]   │ │
│ │                  │  │ [Quit]           │ │
│ └──────────────────┘  └──────────────────┘ │
│                                             │
├─────────────────────────────────────────────┤
│ Footer (Help Text)                          │
└─────────────────────────────────────────────┘
```

### 4. `cli.py` - Command-Line Interface
**Responsibilities:**
- Application entry point
- Textual app initialization
- CSS styling

## Data Flow

### Tuning Process

```
User plays a note
      ↓
Microphone captures sound → AudioCapture.read()
      ↓
Raw audio buffer (numpy array)
      ↓
FrequencyDetector.detect(audio)
      ├─ Apply window function
      ├─ YIN algorithm
      ├─ Calculate confidence
      └─ Return FrequencyResult
      ↓
NoteUtils.frequency_to_note(frequency)
      ├─ Calculate semitones from A4
      ├─ Round to nearest note
      ├─ Calculate cents off (0-100 per semitone)
      └─ Return (note_name, cents_off)
      ↓
TunerDisplay.update()
      ├─ Update frequency text
      ├─ Update note display
      ├─ Calculate and render gauge
      ├─ Determine status (in tune / sharp / flat)
      └─ Refresh display
      ↓
User sees visual feedback and adjusts instrument
```

## Key Design Patterns

### 1. Separation of Concerns
- Audio processing (audio.py) separate from UI (ui.py)
- Note system (notes.py) independent of audio/UI
- Each module can be tested independently

### 2. Reactive UI
- Textual's `@reactive` decorator for automatic display updates
- Changes to `frequency`, `note_name`, `cents_off` trigger re-renders
- Asynchronous update loop for continuous monitoring

### 3. Configuration Objects
- `AudioConfig` for tuning audio parameters
- `InstrumentPresets` for instrument definitions
- Easy to extend without modifying core logic

### 4. Error Handling
- Graceful fallbacks for missing audio
- Confidence threshold to filter unreliable detections
- User notifications for errors

## Performance Considerations

### Audio Processing
- Block size: 4096 samples (≈93ms at 44.1kHz)
- Sample rate: 44.1 kHz (optimal for frequency detection)
- YIN algorithm: O(N²) but highly optimized
- Update frequency: 20 Hz (50ms between updates)

### Optimization Tips
1. **Larger block size** → Less frequent updates but lower CPU
2. **Lower sample rate** → Better for low frequencies, lower CPU
3. **Threshold tuning** → Balance between responsiveness and noise rejection

## Extension Points

### Adding New Instruments
Edit `InstrumentPresets` in `notes.py`:
```python
GUITAR_CUSTOM = Instrument(
    "Guitar (Custom)",
    ["D2", "A2", "D3", "G3", "B3", "F4"]
)
```

### Custom Frequency Ranges
Modify `AudioConfig` in `audio.py`:
```python
AudioConfig(
    sample_rate=48000,  # Higher sample rate for higher frequencies
    block_size=2048,    # Smaller block for faster response
)
```

### Alternative Frequency Detection
Replace `FrequencyDetector` with alternative algorithm:
- FFT-based detection
- Autocorrelation-based detection
- Machine learning models

## Dependencies

```
┌─────────────────────────────────────────┐
│         TunerTUI Application            │
├─────────────────────────────────────────┤
│                                         │
│ ┌──────────────┐  ┌────────────────┐  │
│ │   textual    │  │   sounddevice  │  │
│ │ (UI/TUI)     │  │  (Audio I/O)   │  │
│ └──────────────┘  └────────────────┘  │
│                                         │
│ ┌──────────────┐  ┌────────────────┐  │
│ │    numpy     │  │     scipy      │  │
│ │ (Signal Proc)│  │  (Signal Proc) │  │
│ └──────────────┘  └────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

- **textual**: Modern TUI framework
- **sounddevice**: Cross-platform audio I/O
- **numpy**: Efficient numerical computations
- **scipy**: Scientific computing (optional for enhancements)

## Testing Strategy

### Unit Tests
- Note conversion accuracy
- Frequency calculation correctness
- Instrument preset validation

### Integration Tests
- Audio capture → Detection → Display
- UI component interaction
- State management

### Manual Tests
- Real instrument tuning
- Microphone input validation
- Cross-platform compatibility

## Future Enhancements

1. **Advanced Features**
   - Calibration mode (custom reference frequency)
   - Strobe tuner visualization
   - Chord detection
   - Polyphonic tuning

2. **UI Improvements**
   - Waveform display
   - Tuning history graph
   - Custom color themes
   - Dark mode

3. **Audio Processing**
   - Multiple frequency detection (chords)
   - Noise reduction
   - Harmonic analysis
   - Filter-based pitch detection

4. **Data Management**
   - Export tuning history
   - Custom instrument definitions
   - Settings persistence
   - MIDI support

## Troubleshooting

### Audio Issues
- Check microphone permissions
- Verify audio device selection
- Test with system audio tools first

### Detection Issues
- Frequencies 50Hz-4000Hz work best
- Avoid strong background noise
- Adjust confidence threshold

### UI Issues
- Ensure terminal supports Unicode
- Check terminal size (minimum 80x24)
- Update textual library
