"""
Audio capture and frequency detection module using YIN algorithm
"""

import numpy as np
import sounddevice as sd
from typing import Optional, Tuple, Union
from dataclasses import dataclass


@dataclass
class AudioConfig:
    """Audio recording configuration"""

    sample_rate: int = 44100
    block_size: int = 4096
    channels: int = 1
    dtype: str = "float32"


@dataclass
class FrequencyResult:
    """Result from frequency detection"""

    frequency: float  # in Hz
    confidence: float  # 0.0 to 1.0
    is_valid: bool  # confidence above threshold


class AudioCapture:
    """Handles real-time audio capture from microphone"""

    def __init__(self, config: Optional[AudioConfig] = None):
        self.config = config or AudioConfig()
        self.stream: Optional[sd.InputStream] = None
        self.buffer = np.zeros(self.config.block_size, dtype=self.config.dtype)

    def start(self) -> None:
        """Start audio capture stream"""
        if self.stream is not None:
            return
        self.stream = sd.InputStream(
            channels=self.config.channels,
            samplerate=self.config.sample_rate,
            blocksize=self.config.block_size,
            dtype=self.config.dtype,
            latency="low",
        )
        self.stream.start()

    def stop(self) -> None:
        """Stop audio capture stream"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def read(self) -> np.ndarray:
        """Read audio buffer from stream"""
        if not self.stream:
            raise RuntimeError("Stream not started")
        data, _ = self.stream.read(self.config.block_size)
        return data.flatten()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


class FrequencyDetector:
    """Detects dominant frequency using YIN algorithm"""

    def __init__(self, sample_rate: int = 44100, confidence_threshold: float = 0.1):
        self.sample_rate = sample_rate
        self.confidence_threshold = confidence_threshold

    def detect(self, audio_data: np.ndarray) -> FrequencyResult:
        """
        Detect frequency using YIN algorithm

        Args:
            audio_data: Audio samples as numpy array

        Returns:
            FrequencyResult with detected frequency and confidence
        """
        # Ensure audio is 1D
        audio_data = audio_data.flatten()

        # Apply window function to reduce spectral leakage
        windowed = audio_data * np.hanning(len(audio_data))

        # YIN algorithm
        # tau relates to period: smaller tau = higher frequency, larger tau = lower frequency
        # Search range: 40 Hz to 1000 Hz (covers guitar, bass, and test cases)
        # tau_min = smallest tau (highest frequency to search for)
        # tau_max = largest tau (lowest frequency to search for)
        tau_min = int(self.sample_rate / 1000)  # smallest tau for ~1000 Hz
        tau_max = int(self.sample_rate / 40)  # largest tau for ~40 Hz

        # Calculate autocorrelation difference
        yin = self._yin_diff(windowed, tau_max)

        # Find threshold crossings
        tau = self._find_tau(yin, tau_min, tau_max)

        if tau is None or tau == 0:
            return FrequencyResult(frequency=0.0, confidence=0.0, is_valid=False)

        frequency = self.sample_rate / tau
        confidence = 1.0 - yin[int(tau)]

        is_valid = bool(confidence >= self.confidence_threshold)

        # If confidence is too low, return 0 frequency
        if not is_valid:
            return FrequencyResult(frequency=0.0, confidence=float(confidence), is_valid=False)

        return FrequencyResult(
            frequency=float(frequency), confidence=float(confidence), is_valid=is_valid
        )

    def _yin_diff(
        self, audio: np.ndarray, tau_min_or_max: Optional[int] = None, tau_max: Optional[int] = None
    ) -> np.ndarray:
        """Calculate YIN difference function

        Can be called as:
        - _yin_diff(audio, tau_max) - new signature
        - _yin_diff(audio, tau_min, tau_max) - old test signature
        """
        # Handle both old and new signatures
        if tau_max is not None:
            # Old signature: _yin_diff(audio, tau_min, tau_max)
            actual_tau_max = tau_max
        else:
            # New signature: _yin_diff(audio, tau_max)
            actual_tau_max = tau_min_or_max or 882

        yin = np.zeros(actual_tau_max)

        # Calculate autocorrelation difference
        for tau in range(1, actual_tau_max):
            for i in range(len(audio) - tau):
                yin[tau] += (audio[i] - audio[i + tau]) ** 2

        # Cumulative mean normalized difference
        cumsum = np.cumsum(yin)
        cumsum[0] = 1  # Avoid division by zero

        for tau in range(1, actual_tau_max):
            if cumsum[tau] > 0:
                yin[tau] = tau * yin[tau] / cumsum[tau]
            else:
                yin[tau] = 1.0

        return yin

    def _find_tau(
        self,
        yin: np.ndarray,
        tau_min: Optional[int] = None,
        tau_max: Optional[int] = None,
        threshold: float = 0.1,
    ) -> Optional[float]:
        """Find period tau using threshold

        Can be called as:
        - _find_tau(yin, threshold=0.1) - old test signature
        - _find_tau(yin, tau_min, tau_max) - new signature
        """
        # Handle both old and new signatures
        if tau_min is None and tau_max is None:
            # Old test signature: search whole array
            actual_tau_min = 1
            actual_tau_max = len(yin)
        elif isinstance(tau_min, (int, float)) and tau_max is not None:
            # New signature with both bounds
            actual_tau_min = tau_min
            actual_tau_max = tau_max
        else:
            # Fallback
            actual_tau_min = 1
            actual_tau_max = len(yin)

        # First pass: find the global minimum in the range (most reliable)
        search_range = min(actual_tau_max, len(yin))
        if search_range > 1:
            min_idx = np.argmin(yin[1:search_range]) + 1

            # Verify it passes the threshold
            if yin[min_idx] < threshold:
                # Do parabolic interpolation for finer resolution
                if 0 < min_idx < len(yin) - 1:
                    a = yin[min_idx - 1]
                    b = yin[min_idx]
                    c = yin[min_idx + 1]
                    # Parabolic interpolation
                    denom = 2 * (2 * b - a - c)
                    if denom != 0:
                        shift = (c - a) / denom
                        return float(min_idx + shift)
                return float(min_idx)

        # Second pass: search for first threshold crossing (fallback)
        for tau in range(actual_tau_min, min(actual_tau_max, len(yin))):
            if yin[tau] < threshold:
                # Do parabolic interpolation for finer resolution
                if 0 < tau < len(yin) - 1:
                    a = yin[tau - 1]
                    b = yin[tau]
                    c = yin[tau + 1]
                    # Parabolic interpolation
                    denom = 2 * (2 * b - a - c)
                    if denom != 0:
                        shift = (c - a) / denom
                        return float(tau + shift)
                return float(tau)

        return None


class TunerEngine:
    """Main engine combining audio capture and frequency detection"""

    def __init__(self, sample_rate: int = 44100):
        self.config = AudioConfig(sample_rate=sample_rate)
        self.capture = AudioCapture(self.config)
        self.detector = FrequencyDetector(sample_rate)
        self.is_running = False

    def start(self) -> None:
        """Start the tuner"""
        self.capture.start()
        self.is_running = True

    def stop(self) -> None:
        """Stop the tuner"""
        self.capture.stop()
        self.is_running = False

    def get_frequency(self) -> FrequencyResult:
        """Get current detected frequency"""
        if not self.is_running:
            raise RuntimeError("Tuner not running")
        audio_data = self.capture.read()
        return self.detector.detect(audio_data)
