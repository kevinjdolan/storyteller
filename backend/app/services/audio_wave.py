from __future__ import annotations

import io
import wave


def build_wav_bytes(
    pcm_audio_bytes: bytes,
    *,
    sample_rate_hz: int,
    channel_count: int,
    sample_width_bytes: int,
) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(channel_count)
        wav_file.setsampwidth(sample_width_bytes)
        wav_file.setframerate(sample_rate_hz)
        wav_file.writeframes(pcm_audio_bytes)
    return buffer.getvalue()


def read_wav_bytes(wav_bytes: bytes) -> tuple[bytes, int, int, int]:
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
        sample_rate_hz = wav_file.getframerate()
        channel_count = wav_file.getnchannels()
        sample_width_bytes = wav_file.getsampwidth()
        pcm_audio_bytes = wav_file.readframes(wav_file.getnframes())
    return pcm_audio_bytes, sample_rate_hz, channel_count, sample_width_bytes


def wav_duration_seconds(wav_bytes: bytes) -> float:
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
        frame_count = wav_file.getnframes()
        sample_rate_hz = wav_file.getframerate()
    if sample_rate_hz <= 0:
        raise ValueError("wav bytes must contain a valid sample rate")
    return round(frame_count / sample_rate_hz, 3)


def build_silence_pcm(
    *,
    duration_seconds: int,
    sample_rate_hz: int,
    channel_count: int,
    sample_width_bytes: int,
) -> bytes:
    frame_count = max(int(duration_seconds), 0) * sample_rate_hz
    return b"\x00" * frame_count * channel_count * sample_width_bytes
