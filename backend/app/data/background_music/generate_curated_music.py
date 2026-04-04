from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path

SAMPLE_RATE_HZ = 24_000
DURATION_SECONDS = 24
MAX_AMPLITUDE = 32_767


def _write_wav(path: Path, samples: array) -> None:
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE_HZ)
        wav_file.writeframes(samples.tobytes())


def _master_envelope(time_seconds: float) -> float:
    fade_duration = 0.8
    fade_in = min(time_seconds / fade_duration, 1.0)
    fade_out = min((DURATION_SECONDS - time_seconds) / fade_duration, 1.0)
    return max(min(fade_in, fade_out), 0.0)


def _sine(frequency_hz: float, time_seconds: float, phase_radians: float = 0.0) -> float:
    return math.sin((2 * math.pi * frequency_hz * time_seconds) + phase_radians)


def _clamp_sample(value: float) -> int:
    return max(min(int(round(value * MAX_AMPLITUDE)), MAX_AMPLITUDE), -MAX_AMPLITUDE)


def _build_lullaby_piano() -> array:
    samples = array("h")
    notes = [220.0, 247.0, 294.0, 330.0, 294.0, 247.0]
    frame_count = SAMPLE_RATE_HZ * DURATION_SECONDS
    for frame in range(frame_count):
        time_seconds = frame / SAMPLE_RATE_HZ
        pattern_time = time_seconds % 6.0
        note_index = int(pattern_time // 1.0) % len(notes)
        note_time = pattern_time % 1.0
        note_frequency = notes[note_index]
        note_envelope = math.exp(-3.2 * note_time)
        note = (
            0.68 * _sine(note_frequency, time_seconds)
            + 0.22 * _sine(note_frequency * 2, time_seconds)
            + 0.10 * _sine(note_frequency * 3, time_seconds)
        )
        drone = 0.18 * _sine(110.0, time_seconds)
        value = (note * note_envelope * 0.22) + (drone * 0.05)
        samples.append(_clamp_sample(value * _master_envelope(time_seconds)))
    return samples


def _build_string_drift() -> array:
    samples = array("h")
    chord_sets = [
        (196.0, 247.0, 294.0),
        (220.0, 277.0, 330.0),
        (196.0, 262.0, 330.0),
        (175.0, 220.0, 262.0),
    ]
    frame_count = SAMPLE_RATE_HZ * DURATION_SECONDS
    for frame in range(frame_count):
        time_seconds = frame / SAMPLE_RATE_HZ
        chord_index = int(time_seconds // 6.0) % len(chord_sets)
        chord = chord_sets[chord_index]
        swirl = 0.5 + (0.5 * _sine(0.08, time_seconds))
        value = (
            0.10 * _sine(chord[0], time_seconds)
            + 0.08 * _sine(chord[1], time_seconds, phase_radians=0.8)
            + 0.07 * _sine(chord[2], time_seconds, phase_radians=1.4)
            + 0.03 * _sine(chord[0] / 2, time_seconds)
        ) * swirl
        samples.append(_clamp_sample(value * _master_envelope(time_seconds)))
    return samples


def _build_night_ambience() -> array:
    samples = array("h")
    twinkle_notes = [523.0, 587.0, 659.0, 698.0]
    frame_count = SAMPLE_RATE_HZ * DURATION_SECONDS
    for frame in range(frame_count):
        time_seconds = frame / SAMPLE_RATE_HZ
        bed = (
            0.08 * _sine(87.0, time_seconds)
            + 0.05 * _sine(131.0, time_seconds, phase_radians=0.6)
            + 0.03 * _sine(173.0, time_seconds, phase_radians=1.2)
        )
        shimmer = 0.015 * _sine(0.13, time_seconds) + 0.015 * _sine(0.07, time_seconds)
        twinkle_value = 0.0
        twinkle_window = time_seconds % 4.0
        if twinkle_window < 0.6:
            twinkle_frequency = twinkle_notes[int(time_seconds // 4.0) % len(twinkle_notes)]
            twinkle_envelope = math.exp(-7.5 * twinkle_window)
            twinkle_value = 0.06 * _sine(twinkle_frequency, time_seconds) * twinkle_envelope
        value = bed + shimmer + twinkle_value
        samples.append(_clamp_sample(value * _master_envelope(time_seconds)))
    return samples


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_wav(output_dir / "lullaby_piano.wav", _build_lullaby_piano())
    _write_wav(output_dir / "string_drift.wav", _build_string_drift())
    _write_wav(output_dir / "night_ambience.wav", _build_night_ambience())


if __name__ == "__main__":
    main()
