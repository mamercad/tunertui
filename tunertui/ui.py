"""
Textual UI for the instrument tuner
"""

from textual.app import ComposeResult, RenderableType
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Header, Footer, Button, Select, Label
from textual.reactive import reactive
from textual.message import Message
import asyncio
from typing import Optional

from tunertui.audio import TunerEngine, FrequencyResult
from tunertui.notes import NoteUtils, InstrumentPresets, Instrument


class TunerDisplay(Static):
    """Displays the main tuner gauge and frequency information"""

    frequency = reactive(0.0)
    note_name = reactive("---")
    cents_off = reactive(0.0)
    confidence = reactive(0.0)
    is_valid = reactive(False)

    def render(self) -> RenderableType:
        """Render the tuner display"""
        # Build the frequency gauge
        gauge_width = 40
        if self.is_valid:
            # Calculate position on gauge (-50 to +50 cents)
            position = max(0, min(gauge_width - 1, int((self.cents_off + 50) / 100 * gauge_width)))
            gauge = "─" * position + "◆" + "─" * (gauge_width - position - 1)
            
            # Determine if sharp or flat
            if self.cents_off > 2:
                tuning_status = "♯ SHARP"
            elif self.cents_off < -2:
                tuning_status = "♭ FLAT"
            else:
                tuning_status = "✓ IN TUNE"
        else:
            gauge = "─" * gauge_width
            tuning_status = "NO SIGNAL"

        output = f"""
╔════════════════════════════════════════════════════════╗
║  TunerTUI - Instrument Tuner                           ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Note:        {self.note_name:>8}                            ║
║  Frequency:   {self.frequency:>8.2f} Hz                      ║
║                                                        ║
║  {gauge}  ║
║                                                        ║
║  Status:      {tuning_status:<28}            ║
║  Cents Off:   {self.cents_off:>8.2f}                          ║
║  Confidence:  {self.confidence:>8.1%}                         ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
"""
        return output.rstrip()


class StringTuner(Static):
    """Widget for tuning individual strings"""

    def __init__(self, string_number: int, note_name: str, target_freq: float, **kwargs):
        super().__init__(**kwargs)
        self.string_number = string_number
        self.note_name = note_name
        self.target_freq = target_freq
        self.detected_freq = 0.0
        self.cents_off = 0.0
        self.is_in_tune = False

    def render(self) -> RenderableType:
        status = "✓ IN TUNE" if self.is_in_tune else "  NOT TUNED"
        if self.detected_freq > 0:
            if self.cents_off > 2:
                sharp_flat = "↑"
            elif self.cents_off < -2:
                sharp_flat = "↓"
            else:
                sharp_flat = " "
        else:
            sharp_flat = "?"

        return (
            f"String {self.string_number}: {self.note_name:>3} "
            f"({self.target_freq:>6.2f}Hz) {sharp_flat} "
            f"{self.detected_freq:>6.2f}Hz {status:>12}"
        )


class InstrumentSelector(Container):
    """Widget for selecting instrument"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_instrument: Optional[Instrument] = None

    def compose(self) -> ComposeResult:
        instrument_names = InstrumentPresets.get_names()
        yield Label("Select Instrument:")
        yield Select(
            ((name, name) for name in instrument_names),
            id="instrument-select"
        )


class StringList(Static):
    """Display list of all strings to tune"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.string_widgets: dict[int, StringTuner] = {}

    def add_strings(self, instrument: Instrument) -> None:
        """Add string widgets for the instrument"""
        self.string_widgets.clear()
        for i, note in enumerate(instrument.get_string_notes(), 1):
            widget = StringTuner(i, note.name, note.frequency)
            self.string_widgets[i] = widget

    def render(self) -> RenderableType:
        if not self.string_widgets:
            return "No strings configured"
        
        lines = ["Strings to tune:\n"]
        for i in sorted(self.string_widgets.keys()):
            widget = self.string_widgets[i]
            lines.append(widget.render())
        
        return "\n".join(lines)

    def update_string(self, string_number: int, detected_freq: float, cents_off: float) -> None:
        """Update a string's tuning status"""
        if string_number in self.string_widgets:
            widget = self.string_widgets[string_number]
            widget.detected_freq = detected_freq
            widget.cents_off = cents_off
            widget.is_in_tune = abs(cents_off) < 3  # Within 3 cents is considered in tune


class TunerApp(Static):
    """Main Textual app for the instrument tuner"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tuner_engine: Optional[TunerEngine] = None
        self.current_instrument: Optional[Instrument] = None
        self.tuner_display: Optional[TunerDisplay] = None
        self.string_list: Optional[StringList] = None
        self.is_running = False

    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header(show_clock=True)
        
        with Vertical():
            with Horizontal():
                self.tuner_display = TunerDisplay(id="tuner-display")
                yield self.tuner_display
                
                with Vertical():
                    yield InstrumentSelector(id="instrument-selector")
                    self.string_list = StringList(id="string-list")
                    yield self.string_list
                    
                    with Horizontal():
                        yield Button("Start", id="btn-start", variant="primary")
                        yield Button("Stop", id="btn-stop")
                        yield Button("Quit", id="btn-quit", variant="error")
        
        yield Footer()

    def on_mount(self) -> None:
        """Initialize when app mounts"""
        try:
            self.tuner_engine = TunerEngine()
            # Set default instrument
            self.current_instrument = InstrumentPresets.GUITAR_STANDARD
            if self.string_list:
                self.string_list.add_strings(self.current_instrument)
                self.string_list.refresh()
        except Exception as e:
            self.notify(f"Error initializing tuner: {e}", severity="error")

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle instrument selection change"""
        if event.control.id == "instrument-select":
            try:
                instrument_name = event.value
                if instrument_name:
                    self.current_instrument = InstrumentPresets.get_by_name(instrument_name)
                    if self.string_list:
                        self.string_list.add_strings(self.current_instrument)
                        self.string_list.refresh()
            except Exception as e:
                self.notify(f"Error changing instrument: {e}", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "btn-start":
            self.start_tuning()
        elif event.button.id == "btn-stop":
            self.stop_tuning()
        elif event.button.id == "btn-quit":
            self.app.exit()

    def start_tuning(self) -> None:
        """Start the tuner"""
        if not self.tuner_engine or self.is_running:
            return
        
        try:
            self.tuner_engine.start()
            self.is_running = True
            self.notify("Tuner started", timeout=2)
            self.app.call_later(self._start_update_loop)
        except Exception as e:
            self.notify(f"Error starting tuner: {e}", severity="error")
    
    def _start_update_loop(self) -> None:
        """Start the update loop"""
        self.app.create_task(self.update_frequency())

    def stop_tuning(self) -> None:
        """Stop the tuner"""
        if not self.tuner_engine or not self.is_running:
            return
        
        try:
            self.tuner_engine.stop()
            self.is_running = False
            self.notify("Tuner stopped", timeout=2)
        except Exception as e:
            self.notify(f"Error stopping tuner: {e}", severity="error")

    async def update_frequency(self) -> None:
        """Continuously update frequency display"""
        while self.is_running and self.tuner_engine:
            try:
                result = self.tuner_engine.get_frequency()
                
                if self.tuner_display:
                    self.tuner_display.frequency = result.frequency
                    self.tuner_display.confidence = result.confidence
                    self.tuner_display.is_valid = result.is_valid
                    
                    note_name, cents_off = NoteUtils.frequency_to_note(result.frequency)
                    self.tuner_display.note_name = note_name
                    self.tuner_display.cents_off = cents_off
                    
                    self.tuner_display.refresh()
                    
                    # Update string list if we have instrument loaded
                    if self.current_instrument and self.string_list:
                        # Check which string is closest to detected frequency
                        strings = self.current_instrument.get_string_notes()
                        if strings:
                            closest_idx = 0
                            min_diff = abs(strings[0].frequency - result.frequency)
                            for i, note in enumerate(strings):
                                diff = abs(note.frequency - result.frequency)
                                if diff < min_diff:
                                    min_diff = diff
                                    closest_idx = i
                            
                            # Only update if reasonably close
                            if min_diff < 500:  # Hz tolerance
                                self.string_list.update_string(
                                    closest_idx + 1,
                                    result.frequency,
                                    cents_off
                                )
                                self.string_list.refresh()
                
                await asyncio.sleep(0.05)  # Update 20 times per second
            except Exception as e:
                self.notify(f"Tuner error: {e}", severity="error")
                self.is_running = False
                break
