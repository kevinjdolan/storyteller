from __future__ import annotations

from app.ai import render_gemini_tts_prompt
from app.ai.gemini_tts import NarrationSynthesisRequest
from app.models.audio_settings import AudioNarrationStyle, AudioVoiceKey


def test_eval_tts_prompt_keeps_exact_recitation_guardrails() -> None:
    prompt = render_gemini_tts_prompt(
        NarrationSynthesisRequest(
            text="Pip counted the lantern rings until every ripple looked friendly again.",
            voice_key=AudioVoiceKey.STORYKEEPER,
            narration_style=AudioNarrationStyle.CALM,
            playback_speed=1.0,
            guidance_notes=None,
        )
    )

    criteria = {
        "verbatim_instruction_present": "exactly as written" in prompt,
        "no_adlib_guardrail_present": "Do not add titles" in prompt,
        "punctuation_pause_guardrail_present": "Let punctuation shape natural pauses" in prompt,
        "passage_delimited": '"""' in prompt and "friendly again." in prompt,
    }

    assert all(criteria.values()), criteria


def test_eval_tts_prompt_translates_voice_style_speed_and_notes() -> None:
    prompt = render_gemini_tts_prompt(
        NarrationSynthesisRequest(
            text="Mira tucked the last lantern under her arm and smiled at the quiet dock.",
            voice_key=AudioVoiceKey.HEARTHSIDE,
            narration_style=AudioNarrationStyle.WARM,
            playback_speed=0.78,
            guidance_notes="Keep the final smile audible without sounding perky.",
        )
    )

    criteria = {
        "voice_mapping_present": "- Use the Sulafat voice." in prompt,
        "voice_profile_present": "tucked-in" in prompt,
        "style_mapping_present": "warm, reassuring, and softly expressive" in prompt,
        "slow_speed_guidance_present": "Noticeably slower than a typical read-aloud" in prompt,
        "user_notes_preserved": "Keep the final smile audible" in prompt,
    }

    assert all(criteria.values()), criteria
