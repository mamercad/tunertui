#!/usr/bin/env python3
"""
Simple test script to verify frequency detection without GUI
"""

import sys
sys.path.insert(0, '..')

from tunertui.notes import NoteUtils, InstrumentPresets
import numpy as np

# Test frequency detection
print("=" * 60)
print("Frequency Detection Test")
print("=" * 60)

# Test some known frequencies
test_cases = [
    (440, "A4"),     # A4
    (330, "E4"),     # E4
    (220, "A3"),     # A3
    (82.41, "E2"),   # Low E string on guitar
    (123.47, "B2"),  # B2
]

print("\nNote-to-Frequency Detection:")
print("-" * 60)

for freq, expected_note in test_cases:
    note, cents = NoteUtils.frequency_to_note(freq)
    status = "✓" if note.startswith(expected_note[0]) else "✗"
    print(f"{status} Freq: {freq:>7.2f}Hz → {note:>3} ({cents:>+6.2f} cents) [expected: {expected_note}]")

print("\n" + "=" * 60)
print("Instrument Presets")
print("=" * 60)

for instrument in InstrumentPresets.ALL:
    print(f"\n{instrument.name}:")
    for i, note in enumerate(instrument.get_string_notes(), 1):
        print(f"  String {i}: {note.name}{note.octave} ({note.frequency:>7.2f}Hz)")

print("\n" + "=" * 60)
print("YIN Algorithm Simulation")
print("=" * 60)

from tunertui.audio import FrequencyDetector

# Create detector
detector = FrequencyDetector(sample_rate=44100)

# Generate a test signal (sine wave at 440 Hz)
sample_rate = 44100
duration = 0.1  # 100ms
freq = 440  # A4
t = np.arange(int(sample_rate * duration)) / sample_rate
signal = np.sin(2 * np.pi * freq * t)

# Add some noise
noise = np.random.normal(0, 0.1, signal.shape)
noisy_signal = signal + noise

# Detect
result = detector.detect(noisy_signal)
print(f"\nGenerated signal: 440 Hz sine wave")
print(f"Detected: {result.frequency:.2f} Hz")
print(f"Confidence: {result.confidence:.1%}")
print(f"Valid: {result.is_valid}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
