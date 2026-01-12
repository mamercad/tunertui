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
        tau_min = int(self.sample_rate / 500)  # min frequency ~500 Hz
        tau_max = int(self.sample_rate / 50)   # max frequency ~50 Hz

        # Calculate autocorrelation difference
        yin = self._yin_diff(windowed, tau_min, tau_max)

        # Find threshold crossings
        tau = self._find_tau(yin)

        if tau is None:
            return FrequencyResult(
                frequency=0.0,
                confidence=0.0,
                is_valid=False
            )

        frequency = self.sample_rate / tau
        confidence = 1.0 - yin[tau]

        is_valid = confidence >= self.confidence_threshold

        return FrequencyResult(
            frequency=frequency,
            confidence=confidence,
            is_valid=is_valid
        )

    def _yin_diff(self, audio: np.ndarray, tau_min: int, tau_max: int) -> np.ndarray:
        """Calculate YIN difference function"""
        yin = np.zeros(tau_max)

        for tau in range(tau_min, tau_max):
            for i in range(len(audio) - tau):
                yin[tau] += (audio[i] - audio[i + tau]) ** 2

        # Cumulative mean normalized difference
        cumsum = np.cumsum(yin)
        for tau in range(tau_min, tau_max):
            if cumsum[tau] == 0:
                yin[tau] = 1
            else:
                yin[tau] = tau * yin[tau] / cumsum[tau]

        return yin

    def _find_tau(self, yin: np.ndarray, threshold: float = 0.1) -> Optional[float]:
        """Find period tau using threshold"""
        for tau in range(len(yin)):
            if yin[tau] < threshold:
                # Do parabolic interpolation for finer resolution
                if 0 < tau < len(yin) - 1:
                    a = yin[tau - 1]
                    b = yin[tau]
                    c = yin[tau + 1]
                    # Parabolic interpolation
                    shift = (c - a) / (2 * (2 * b - a - c))
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
