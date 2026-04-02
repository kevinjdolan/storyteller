from __future__ import annotations

import shlex
import subprocess
import tempfile
import wave
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from app.services.audio_music import AudioMixPlan, get_background_music_track


class AudioMixingError(Exception):
    """Raised when the background music mixing pipeline fails."""


@dataclass(frozen=True)
class AudioMixResult:
    mixed_wav_bytes: bytes
    output_duration_seconds: float
    ffmpeg_command: str | None = None


class FfmpegAudioMixer:
    def __init__(
        self,
        *,
        ffmpeg_binary: str = "ffmpeg",
        runner=subprocess.run,
    ) -> None:
        self._ffmpeg_binary = ffmpeg_binary
        self._runner = runner

    def mix(self, narration_wav_bytes: bytes, *, plan: AudioMixPlan) -> AudioMixResult:
        if not plan.should_mix:
            return AudioMixResult(
                mixed_wav_bytes=narration_wav_bytes,
                output_duration_seconds=_wav_duration_seconds(narration_wav_bytes),
                ffmpeg_command=None,
            )

        if plan.music_profile is None:
            raise AudioMixingError("audio mix plan is missing a music_profile")

        track = get_background_music_track(plan.music_profile)
        if not track.asset_path.is_file():
            raise AudioMixingError(
                f"background music asset {track.asset_file_name!r} is missing from the catalog",
            )

        with wave.open(BytesIO(narration_wav_bytes), "rb") as wav_file:
            sample_rate_hz = wav_file.getframerate()
            channel_count = wav_file.getnchannels()
        narration_duration_seconds = _wav_duration_seconds(narration_wav_bytes)
        channel_layout = _channel_layout_for_count(channel_count)
        filter_complex = _build_filter_complex(
            plan=plan,
            sample_rate_hz=sample_rate_hz,
            channel_layout=channel_layout,
            narration_duration_seconds=narration_duration_seconds,
        )

        with tempfile.TemporaryDirectory(prefix="storyteller-audio-mix-") as temp_dir:
            working_dir = Path(temp_dir)
            narration_path = working_dir / "narration.wav"
            mixed_path = working_dir / "mixed.wav"
            narration_path.write_bytes(narration_wav_bytes)

            command = [
                self._ffmpeg_binary,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-stream_loop",
                "-1",
                "-i",
                str(track.asset_path),
                "-i",
                str(narration_path),
                "-filter_complex",
                filter_complex,
                "-map",
                "[out]",
                "-c:a",
                "pcm_s16le",
                str(mixed_path),
            ]

            try:
                completed = self._runner(
                    command,
                    capture_output=True,
                    check=False,
                    text=False,
                )
            except FileNotFoundError as exc:
                raise AudioMixingError(
                    "ffmpeg is not installed or not available on PATH",
                ) from exc

            if completed.returncode != 0:
                stderr = completed.stderr.decode("utf-8", errors="replace").strip()
                stdout = completed.stdout.decode("utf-8", errors="replace").strip()
                detail = stderr or stdout or "ffmpeg returned a non-zero exit status"
                raise AudioMixingError(f"ffmpeg mixing failed: {detail}")

            mixed_wav_bytes = mixed_path.read_bytes()

        return AudioMixResult(
            mixed_wav_bytes=mixed_wav_bytes,
            output_duration_seconds=_wav_duration_seconds(mixed_wav_bytes),
            ffmpeg_command=" ".join(shlex.quote(part) for part in command),
        )


def _wav_duration_seconds(wav_bytes: bytes) -> float:
    with wave.open(BytesIO(wav_bytes), "rb") as wav_file:
        sample_rate_hz = wav_file.getframerate()
        channel_count = wav_file.getnchannels()
        sample_width_bytes = wav_file.getsampwidth()
        frame_count = wav_file.getnframes()
    if sample_rate_hz <= 0 or channel_count <= 0 or sample_width_bytes <= 0:
        raise AudioMixingError("wav input must have valid sample metadata")
    return round(frame_count / sample_rate_hz, 3)


def _channel_layout_for_count(channel_count: int) -> str:
    if channel_count == 1:
        return "mono"
    if channel_count == 2:
        return "stereo"
    raise AudioMixingError(
        "background music mixing only supports mono or stereo narration masters",
    )


def _build_filter_complex(
    *,
    plan: AudioMixPlan,
    sample_rate_hz: int,
    channel_layout: str,
    narration_duration_seconds: float,
) -> str:
    if plan.music_gain_db is None:
        raise AudioMixingError("audio mix plan is missing music_gain_db")
    if plan.ducking_ratio is None:
        raise AudioMixingError("audio mix plan is missing ducking_ratio")
    if plan.ducking_threshold is None:
        raise AudioMixingError("audio mix plan is missing ducking_threshold")

    fade_out_seconds = max(int(plan.fade_out_seconds or 0), 0)
    fade_start_seconds = max(narration_duration_seconds - fade_out_seconds, 0)
    fade_fragment = (
        f",afade=t=out:st={fade_start_seconds:.3f}:d={fade_out_seconds}"
        if fade_out_seconds > 0
        else ""
    )
    attack_ms = max(int(plan.ducking_attack_ms or 30), 1)
    release_ms = max(int(plan.ducking_release_ms or 300), 1)

    return (
        f"[0:a]aresample={sample_rate_hz},"
        f"aformat=sample_fmts=s16:channel_layouts={channel_layout},"
        f"atrim=0:{narration_duration_seconds:.3f},"
        f"volume={plan.music_gain_db:.1f}dB"
        f"{fade_fragment}[music];"
        f"[1:a]aresample={sample_rate_hz},"
        f"aformat=sample_fmts=s16:channel_layouts={channel_layout},"
        f"volume={plan.narration_gain_db:.1f}dB,"
        f"asplit=2[voice_mix][voice_sidechain];"
        f"[music][voice_sidechain]sidechaincompress="
        f"threshold={plan.ducking_threshold:.3f}:"
        f"ratio={plan.ducking_ratio:.1f}:"
        f"attack={attack_ms}:"
        f"release={release_ms}"
        f"[ducked];"
        f"[voice_mix][ducked]amix=inputs=2:duration=first:dropout_transition=0,"
        f"atrim=0:{narration_duration_seconds:.3f}[out]"
    )
