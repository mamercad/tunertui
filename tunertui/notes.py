"""
Note definitions and frequency utilities
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import math


@dataclass
class Note:
    """Represents a musical note"""
    name: str
    frequency: float
    octave: int

    def __str__(self) -> str:
        return f"{self.name}{self.octave}"

    def __repr__(self) -> str:
        return f"Note({self.name}{self.octave}, {self.frequency:.2f}Hz)"


# Reference: A4 = 440 Hz
A4_FREQUENCY = 440
SEMITONE_RATIO = 2 ** (1 / 12)  # 12th root of 2


class NoteUtils:
    """Utilities for working with musical notes"""

    # Standard note names in one octave
    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    NOTE_INDICES = {note: i for i, note in enumerate(NOTES)}

    @staticmethod
    def frequency_to_note(frequency: float) -> Tuple[str, float]:
        """
        Convert frequency to nearest note
        
        Returns:
            Tuple of (note_name, cents_off) where cents_off is -50 to +50
        """
        if frequency <= 0:
            return "---", 0.0

        # Calculate semitones from A4
        semitones_from_a4 = 12 * math.log2(frequency / A4_FREQUENCY)
        
        # Round to nearest semitone
        nearest_semitone = round(semitones_from_a4)
        
        # Calculate cents (100 cents = 1 semitone)
        cents_off = (semitones_from_a4 - nearest_semitone) * 100

        # Calculate which note this is
        # A4 is at index 9 (A) in octave 4
        note_index = (9 + nearest_semitone) % 12
        octave = 4 + (9 + nearest_semitone) // 12

        note_name = NoteUtils.NOTES[note_index]

        return f"{note_name}{octave}", cents_off

    @staticmethod
    def note_to_frequency(note_name: str, octave: int) -> float:
        """Convert note name and octave to frequency"""
        if note_name not in NoteUtils.NOTE_INDICES:
            raise ValueError(f"Unknown note: {note_name}")

        # A4 is at index 9
        note_idx = NoteUtils.NOTE_INDICES[note_name]
        semitones_from_a4 = (octave - 4) * 12 + (note_idx - 9)

        return A4_FREQUENCY * (SEMITONE_RATIO ** semitones_from_a4)

    @staticmethod
    def get_notes_in_range(min_freq: float, max_freq: float) -> List[Note]:
        """Get all notes within frequency range"""
        notes = []
        
        for octave in range(0, 9):
            for note_name in NoteUtils.NOTES:
                freq = NoteUtils.note_to_frequency(note_name, octave)
                if min_freq <= freq <= max_freq:
                    notes.append(Note(note_name, freq, octave))
        
        return sorted(notes, key=lambda n: n.frequency)


class Instrument:
    """Represents an instrument with tuning notes"""

    def __init__(self, name: str, tuning: List[str]):
        """
        Args:
            name: Instrument name
            tuning: List of note strings like ["E2", "A2", "D3", "G3", "B3", "E4"]
        """
        self.name = name
        self.tuning_notes = tuning
        self.strings = self._parse_tuning(tuning)

    def _parse_tuning(self, tuning: List[str]) -> List[Note]:
        """Parse tuning strings to Note objects"""
        notes = []
        for note_str in tuning:
            # Parse "E4" format
            note_name = note_str[:-1]
            octave = int(note_str[-1])
            frequency = NoteUtils.note_to_frequency(note_name, octave)
            notes.append(Note(note_name, frequency, octave))
        return notes

    def get_string_notes(self) -> List[Note]:
        """Get tuning notes for all strings"""
        return self.strings


class InstrumentPresets:
    """Predefined instrument tunings"""

    GUITAR_STANDARD = Instrument(
        "Guitar (Standard)",
        ["E2", "A2", "D3", "G3", "B3", "E4"]
    )

    GUITAR_DROP_D = Instrument(
        "Guitar (Drop D)",
        ["D2", "A2", "D3", "G3", "B3", "E4"]
    )

    GUITAR_OPEN_G = Instrument(
        "Guitar (Open G)",
        ["D2", "G2", "D3", "G3", "B3", "D4"]
    )

    BASS_STANDARD = Instrument(
        "Bass (Standard)",
        ["E1", "A1", "D2", "G2"]
    )

    BASS_5_STRING = Instrument(
        "Bass (5-String)",
        ["B0", "E1", "A1", "D2", "G2"]
    )

    UKULELE_SOPRANO = Instrument(
        "Ukulele (Soprano)",
        ["G4", "C4", "E4", "A4"]
    )

    BANJO_5_STRING = Instrument(
        "Banjo (5-String)",
        ["D2", "B2", "F#3", "D3", "D4"]
    )

    MANDOLIN = Instrument(
        "Mandolin",
        ["G3", "D4", "A4", "E5"]
    )

    VIOLIN = Instrument(
        "Violin",
        ["G3", "D4", "A4", "E5"]
    )

    ALL = [
        GUITAR_STANDARD,
        GUITAR_DROP_D,
        GUITAR_OPEN_G,
        BASS_STANDARD,
        BASS_5_STRING,
        UKULELE_SOPRANO,
        BANJO_5_STRING,
        MANDOLIN,
        VIOLIN,
    ]

    @classmethod
    def get_by_name(cls, name: str) -> Instrument:
        """Get instrument by name"""
        for instrument in cls.ALL:
            if instrument.name.lower() == name.lower():
                return instrument
        raise ValueError(f"Unknown instrument: {name}")

    @classmethod
    def get_names(cls) -> List[str]:
        """Get list of all instrument names"""
        return [inst.name for inst in cls.ALL]
