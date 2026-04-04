from __future__ import annotations

import subprocess
from pathlib import Path

from app.models.audio_settings import AudioMusicProfile, AudioSettingsView
from app.services.audio_jobs import build_wav_bytes
from app.services.audio_mixing import AudioMixingError, FfmpegAudioMixer
from app.services.audio_music import build_audio_mix_plan


def _build_narration_wav_bytes() -> bytes:
    pcm_audio = (b"\x01\x00" * 2400) + (b"\x02\x00" * 2400)
    return build_wav_bytes(
        pcm_audio,
        sample_rate_hz=24_000,
        channel_count=1,
        sample_width_bytes=2,
    )


def test_ffmpeg_audio_mixer_builds_loop_and_duck_mix_command() -> None:
    seen_command: list[str] = []
    narration_wav_bytes = _build_narration_wav_bytes()
    mixed_wav_bytes = narration_wav_bytes

    def runner(command, capture_output, check, text):
        del capture_output, check, text
        seen_command.extend(command)
        output_path = Path(command[-1])
        output_path.write_bytes(mixed_wav_bytes)
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    plan = build_audio_mix_plan(
        AudioSettingsView(
            include_background_music=True,
            music_profile=AudioMusicProfile.LULLABY_PIANO,
            narration_volume=92,
            music_volume=24,
        )
    )
    mixer = FfmpegAudioMixer(ffmpeg_binary="ffmpeg-test", runner=runner)

    result = mixer.mix(narration_wav_bytes, plan=plan)

    assert seen_command[0] == "ffmpeg-test"
    assert "-stream_loop" in seen_command
    assert "-filter_complex" in seen_command
    filter_complex = seen_command[seen_command.index("-filter_complex") + 1]
    assert "sidechaincompress=" in filter_complex
    assert "amix=inputs=2" in filter_complex
    assert "duration=first" in filter_complex
    assert "asplit=2" in filter_complex
    assert "volume=" in filter_complex
    assert result.mixed_wav_bytes == mixed_wav_bytes
    assert result.ffmpeg_command is not None and "ffmpeg-test" in result.ffmpeg_command


def test_ffmpeg_audio_mixer_raises_clear_error_when_binary_is_missing() -> None:
    narration_wav_bytes = _build_narration_wav_bytes()
    plan = build_audio_mix_plan(
        AudioSettingsView(
            include_background_music=True,
            music_profile=AudioMusicProfile.STRING_DRIFT,
            narration_volume=90,
            music_volume=20,
        )
    )

    def runner(*_args, **_kwargs):
        raise FileNotFoundError("ffmpeg")

    mixer = FfmpegAudioMixer(runner=runner)

    try:
        mixer.mix(narration_wav_bytes, plan=plan)
    except AudioMixingError as exc:
        assert "ffmpeg is not installed" in str(exc)
    else:
        raise AssertionError("expected AudioMixingError when ffmpeg is unavailable")
