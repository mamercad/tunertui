#!/usr/bin/env python3
"""
Demonstration of the note system without audio
Shows how the tuner works conceptually
"""

import sys
sys.path.insert(0, '..')

from tunertui.notes import NoteUtils, InstrumentPresets, Note


def demo_frequency_to_note():
    """Demonstrate frequency to note conversion"""
    print("\n" + "=" * 70)
    print("DEMO 1: Converting Frequencies to Notes")
    print("=" * 70)
    
    # Test various frequencies
    test_frequencies = [
        82.41,   # E2 (low E on guitar)
        110.00,  # A2
        164.81,  # E3
        246.94,  # B3
        329.63,  # E4 (middle E)
        440.00,  # A4 (concert pitch)
        659.25,  # E5
        880.00,  # A5
    ]
    
    print("\nFrequency → Note Detection:")
    print("-" * 70)
    print(f"{'Frequency (Hz)':<15} | {'Detected Note':<15} | {'Cents Off':<12}")
    print("-" * 70)
    
    for freq in test_frequencies:
        note, cents = NoteUtils.frequency_to_note(freq)
        cents_str = f"{cents:+.1f}¢"
        print(f"{freq:<14.2f} | {note:<14} | {cents_str:<12}")


def demo_note_to_frequency():
    """Demonstrate note to frequency conversion"""
    print("\n" + "=" * 70)
    print("DEMO 2: Converting Notes to Frequencies")
    print("=" * 70)
    
    notes_to_test = [
        ("E", 2), ("A", 2), ("D", 3), ("G", 3), ("B", 3), ("E", 4),
        ("A", 4), ("E", 5),
    ]
    
    print("\nNote → Frequency Conversion:")
    print("-" * 70)
    print(f"{'Note':<10} | {'Frequency (Hz)':<15}")
    print("-" * 70)
    
    for note_name, octave in notes_to_test:
        freq = NoteUtils.note_to_frequency(note_name, octave)
        print(f"{note_name}{octave:<8} | {freq:<14.2f}")


def demo_instruments():
    """Demonstrate instrument presets"""
    print("\n" + "=" * 70)
    print("DEMO 3: Instrument Presets")
    print("=" * 70)
    
    for instrument in InstrumentPresets.ALL:
        print(f"\n📍 {instrument.name}")
        print("   " + "-" * 50)
        notes = instrument.get_string_notes()
        for i, note in enumerate(notes, 1):
            freq_str = f"{note.frequency:.2f}Hz"
            print(f"   String {i}: {note.name}{note.octave:<3} ({freq_str})")


def demo_tuning_feedback():
    """Simulate tuning feedback"""
    print("\n" + "=" * 70)
    print("DEMO 4: Simulated Tuning Feedback")
    print("=" * 70)
    
    # Simulate a guitarist trying to tune the low E string
    target_freq = NoteUtils.note_to_frequency("E", 2)
    print(f"\nTarget: Low E String (E2 = {target_freq:.2f} Hz)")
    print("-" * 70)
    
    # Simulate tuning progression
    attempts = [
        70.00,    # Way too flat
        75.00,    # Still flat
        80.00,    # Getting closer, flat
        82.00,    # Very close, slightly flat
        82.35,    # Almost there
        82.41,    # Perfect!
        82.50,    # Slightly sharp
        83.00,    # Too sharp
    ]
    
    print("\nTuning progression:")
    print("-" * 70)
    print(f"{'Step':<6} | {'Freq (Hz)':<12} | {'Detected Note':<15} | {'Status':<20}")
    print("-" * 70)
    
    for i, freq in enumerate(attempts, 1):
        note, cents = NoteUtils.frequency_to_note(freq)
        
        if abs(cents) < 3:
            status = "✓ IN TUNE"
        elif cents > 0:
            status = f"♯ SHARP ({cents:+.1f}¢)"
        else:
            status = f"♭ FLAT ({cents:+.1f}¢)"
        
        print(f"{i:<5} | {freq:<11.2f} | {note:<14} | {status:<20}")


def demo_cents_explanation():
    """Explain cents and how they work"""
    print("\n" + "=" * 70)
    print("DEMO 5: Understanding Cents")
    print("=" * 70)
    
    print("""
What are cents?
  • 1 semitone = 100 cents
  • 12 semitones = 1 octave = 1200 cents
  • Cents measure pitch deviation from a target note
  
The Tuning Range:
  • -50 cents = 0.5 semitones below target (half-flat)
  • -25 cents = 0.25 semitones below target (slightly flat)
  •   0 cents = perfectly in tune
  • +25 cents = 0.25 semitones above target (slightly sharp)
  • +50 cents = 0.5 semitones above target (half-sharp)

Visual Feedback:
  • |-------|-------|-------|-------|-------|
  •  -50   -25      0      +25    +50
  •   ♭                    ♯
  •  FLAT               SHARP
  
In TunerTUI:
  • ✓ IN TUNE: Within ±3 cents
  • ♭ FLAT: More than 3 cents below target
  • ♯ SHARP: More than 3 cents above target
""")


def main():
    """Run all demos"""
    print("\n" * 2)
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TUNERTUI DEMONSTRATION" + " " * 31 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demo_frequency_to_note()
    demo_note_to_frequency()
    demo_instruments()
    demo_tuning_feedback()
    demo_cents_explanation()
    
    print("\n" + "=" * 70)
    print("END OF DEMONSTRATION")
    print("=" * 70)
    print("\nTo run the full TUI with audio capture:")
    print("  cd ..")
    print("  python3 -m tunertui.cli")
    print("\nAfter installing dependencies:")
    print("  pip install -r requirements.txt")
    print()


if __name__ == "__main__":
    main()
