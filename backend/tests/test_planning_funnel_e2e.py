from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from app.db import Base
from app.db.session import get_engine, get_session_factory
from app.main import create_app
from app.models import (
    BeatSheetGenerationInvocation,
    BeatSheetGenerationInvocationResult,
    BeatSheetGenerationStructuredOutput,
    BriefNormalizationInvocation,
    BriefNormalizationInvocationResult,
    BriefNormalizationStructuredOutput,
    CharacterGenerationInvocation,
    CharacterGenerationInvocationResult,
    CharacterGenerationStructuredOutput,
    GeneratedBeatSheetBeat,
    GeneratedBeatSheetCandidate,
    GeneratedCharacterProfile,
    GeneratedCharacterSheetCandidate,
    GeneratedPitchCandidate,
    NormalizedBriefPreferences,
    PitchGenerationInvocation,
    PitchGenerationInvocationResult,
    PitchGenerationStructuredOutput,
)
from app.services.catalog import CATALOG_FILE_PATH, load_catalog_document, seed_catalog
from app.settings import get_settings
from fastapi.testclient import TestClient


class PlanningFunnelBriefNormalizationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-flash-lite"

    def normalize(
        self,
        invocation: BriefNormalizationInvocation,
    ) -> BriefNormalizationInvocationResult:
        return BriefNormalizationInvocationResult(
            invocation=invocation,
            structured_output=BriefNormalizationStructuredOutput(
                normalized_summary=(
                    "A harbor bedtime quest where Mira and an otter guardian guide stray "
                    "lanterns home, turning late-night worry into calm belonging."
                ),
                normalized_preferences=NormalizedBriefPreferences(
                    protagonist_type="A child lantern-keeper and an otter guardian",
                    setting="a moonlit harbor with quiet docks and hidden coves",
                    emotional_goal="turn last-minute worry into a restful reunion",
                    constraint_notes=[
                        "End with the harbor settled and Mira safely ready for sleep.",
                        "Keep every discovery emotionally legible for a tired listener.",
                    ],
                    bedtime_safety_concerns=[
                        "Any spike in tension should be brief, named, and quickly soothed.",
                    ],
                    candidate_motifs=[
                        "floating lanterns",
                        "silver harbor water",
                        "soft dock-bell echoes",
                    ],
                ),
            ),
            raw_response={
                "stub": True,
                "usageMetadata": {
                    "promptTokenCount": 268,
                    "candidatesTokenCount": 91,
                    "totalTokenCount": 359,
                },
            },
        )

    def close(self) -> None:
        return None


class PlanningFunnelPitchGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: PitchGenerationInvocation,
    ) -> PitchGenerationInvocationResult:
        return PitchGenerationInvocationResult(
            invocation=invocation,
            structured_output=PitchGenerationStructuredOutput(
                pitches=[
                    GeneratedPitchCandidate(
                        title="Lanterns Over Juniper Cove",
                        hook=(
                            "Mira and a patient otter guardian follow drifting lanterns across "
                            "the harbor so every light can reach home before the last bell."
                        ),
                        central_conflict=(
                            "A hidden cove and one worried missing lantern threaten to stretch "
                            "the bedtime route longer than Mira can manage alone."
                        ),
                        why_it_fits=(
                            "It keeps the quest active while using luminous harbor imagery, "
                            "small-scale stakes, and a visibly restful ending."
                        ),
                    ),
                    GeneratedPitchCandidate(
                        title="The Quiet Map of Lights",
                        hook=(
                            "A path of lantern reflections opens over the water, inviting Mira "
                            "to solve the harbor's gentlest unfinished promise."
                        ),
                        central_conflict=(
                            "To help the harbor settle, Mira must follow the light-map without "
                            "letting uncertainty grow sharper than bedtime can hold."
                        ),
                        why_it_fits=(
                            "It matches the lane with soft mystery, calm discovery, and quick "
                            "emotional repair whenever the mood dips."
                        ),
                    ),
                    GeneratedPitchCandidate(
                        title="Otis and the Last Doorstep",
                        hook=(
                            "When one lantern refuses to land, Mira and Otis make a moonlit tour "
                            "of the docks to learn what kindness the night still needs."
                        ),
                        central_conflict=(
                            "They need to finish the route before the harbor can rest, but each "
                            "stop asks Mira to trade anxious control for steadier trust."
                        ),
                        why_it_fits=(
                            "It supports bedtime pacing by making the conflict internal, "
                            "relational, and safely resolved before sleep."
                        ),
                    ),
                ]
            ),
            raw_response={
                "stub": True,
                "usageMetadata": {
                    "promptTokenCount": 614,
                    "candidatesTokenCount": 244,
                    "totalTokenCount": 858,
                },
            },
        )

    def close(self) -> None:
        return None


class PlanningFunnelCharacterGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: CharacterGenerationInvocation,
    ) -> CharacterGenerationInvocationResult:
        return CharacterGenerationInvocationResult(
            invocation=invocation,
            structured_output=CharacterGenerationStructuredOutput(
                character_sheets=[
                    GeneratedCharacterSheetCandidate(
                        title="Juniper Cove Lantern Crew",
                        summary=(
                            "Mira's cast keeps the harbor story active, intimate, and easy to "
                            "outline around shared rituals, trust, and emotional repair."
                        ),
                        story_function=(
                            "This crew turns the selected pitch into a guided quest where every "
                            "beat can pivot from worry toward visible comfort."
                        ),
                        bedtime_safety_notes=(
                            "Every helper stays physically close, names feelings clearly, and "
                            "buffers the low points before they can feel harsh."
                        ),
                        visual_motifs=[
                            "lantern glow on sleeves",
                            "otter pawprints on dock planks",
                            "soft ripples of harbor light",
                        ],
                        protagonist=GeneratedCharacterProfile(
                            name="Mira",
                            role="lantern-keeper in training",
                            goal="guide the last drifting lanterns home before the harbor sleeps",
                            flaw="tries to carry every worry alone instead of asking for help",
                            comfort_trait="counts dock-bell echoes until her breathing slows",
                            bedtime_safety_notes=(
                                "Mira is never left alone with fear for long; Otis and the harbor "
                                "rituals keep each obstacle readable."
                            ),
                            relationships=[
                                "Trusts Otis to slow the plan down when she rushes.",
                                "Feels responsible for every harbor doorstep.",
                            ],
                            visual_anchors=[
                                "sea-glass satchel",
                                "moon-silver sleeve trim",
                            ],
                        ),
                        supporting_cast=[
                            GeneratedCharacterProfile(
                                name="Otis",
                                role="patient otter harbor guardian",
                                goal="help Mira turn anxious urgency into steady care",
                                flaw="sometimes explains too much instead of letting Mira notice",
                                comfort_trait="grounds scenes with small repeated harbor rituals",
                                bedtime_safety_notes=(
                                    "Otis makes each late-night complication concrete, small, and "
                                    "quickly reassuring."
                                ),
                                relationships=[
                                    "Acts as Mira's calm sounding board and route guide.",
                                ],
                                visual_anchors=[
                                    "tidy rope satchel",
                                    "river-smooth lantern staff",
                                ],
                            )
                        ],
                    ),
                    GeneratedCharacterSheetCandidate(
                        title="Harbor Listener Pair",
                        summary=(
                            "A quieter duo built around observation and conversation, suited to a "
                            "more reflective version of the same harbor quest."
                        ),
                        story_function=(
                            "This option would make the midpoint and low point hinge on dialogue "
                            "and naming feelings rather than movement."
                        ),
                        bedtime_safety_notes=(
                            "Mystery beats stay gentle because every reveal is quickly interpreted "
                            "by a supportive companion."
                        ),
                        visual_motifs=[
                            "still-water reflections",
                            "silver reeds",
                            "sleepy ferry ropes",
                        ],
                        protagonist=GeneratedCharacterProfile(
                            name="Pip",
                            role="quiet shoreline listener",
                            goal="understand what the harbor still needs before bed",
                            flaw="hesitates to speak up when worry first appears",
                            comfort_trait="matches footsteps to the harbor's hush",
                            bedtime_safety_notes=(
                                "Pip's uncertainty is always shared out loud with a helper before "
                                "it grows too heavy."
                            ),
                            relationships=[
                                "Leans on Rowan for clearer language when emotions spike.",
                            ],
                            visual_anchors=["silver pockets", "reed-shadow scarf"],
                        ),
                        supporting_cast=[
                            GeneratedCharacterProfile(
                                name="Rowan",
                                role="older sibling interpreter",
                                goal="translate the harbor's signals into practical kindness",
                                flaw="tries to fix worry before fully listening",
                                comfort_trait="restates feelings in calmer words",
                                bedtime_safety_notes=(
                                    "Rowan keeps the mystery transparent enough for bedtime."
                                ),
                                relationships=[
                                    "Helps Pip name the hidden worry before it lingers.",
                                ],
                                visual_anchors=["striped scarf", "reed basket"],
                            )
                        ],
                    ),
                    GeneratedCharacterSheetCandidate(
                        title="Moonroute Keepers",
                        summary=(
                            "A route-focused cast that emphasizes ritual, maps, and soft teamwork "
                            "while keeping the harbor quest bedtime-safe."
                        ),
                        story_function=(
                            "This version would make the outline more procedural, with each stop "
                            "on the lantern route tied to one practical emotional repair."
                        ),
                        bedtime_safety_notes=(
                            "Each route marker has a helper and a clearly calming purpose."
                        ),
                        visual_motifs=[
                            "mapped lantern ribbons",
                            "quiet knots",
                            "moonlit buoy lights",
                        ],
                        protagonist=GeneratedCharacterProfile(
                            name="Tavi",
                            role="gentle route-maker",
                            goal="lead one stubborn lantern toward its proper harbor home",
                            flaw="overplans and gets rattled when the route changes",
                            comfort_trait="returns to familiar rituals whenever the plan slips",
                            bedtime_safety_notes=(
                                "Tavi's planning worries stay small because the cast keeps the "
                                "next step visible."
                            ),
                            relationships=[
                                "Relies on Ember to reframe surprises as invitations.",
                            ],
                            visual_anchors=["mapped ribbon", "quiet satchel"],
                        ),
                        supporting_cast=[
                            GeneratedCharacterProfile(
                                name="Ember",
                                role="warmhearted harbor mentor",
                                goal="keep the route readable without flattening the wonder",
                                flaw="tries to solve the problem too early",
                                comfort_trait="grounds scenes with a repeated lantern phrase",
                                bedtime_safety_notes=(
                                    "Ember explains each obstacle before it can feel overwhelming."
                                ),
                                relationships=[
                                    "Encourages Tavi to trust the quieter route.",
                                ],
                                visual_anchors=["soft lantern staff", "threaded map"],
                            )
                        ],
                    ),
                ]
            ),
            raw_response={
                "stub": True,
                "usageMetadata": {
                    "promptTokenCount": 702,
                    "candidatesTokenCount": 322,
                    "totalTokenCount": 1024,
                },
            },
        )

    def close(self) -> None:
        return None


class PlanningFunnelBeatSheetGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: BeatSheetGenerationInvocation,
    ) -> BeatSheetGenerationInvocationResult:
        beats = [
            GeneratedBeatSheetBeat(
                key=key,
                label=label,
                summary=summary,
                emotional_intent=emotional_intent,
                bedtime_softening_note=bedtime_softening_note,
            )
            for key, label, summary, emotional_intent, bedtime_softening_note in (
                (
                    "opening_image",
                    "Opening Image",
                    "Mira watches lantern light ripple across the last quiet harbor before bed.",
                    "Begin with stillness, warmth, and visible safety.",
                    "Keep the opening sensory and calm enough to settle the listener immediately.",
                ),
                (
                    "theme_stated",
                    "Theme Stated",
                    (
                        "Otis reminds Mira that every light finds home faster when it is guided "
                        "gently."
                    ),
                    "State the story's trust-over-urgency theme.",
                    "Frame the lesson as a comfort, not a warning.",
                ),
                (
                    "set_up",
                    "Set-Up",
                    "Harbor routines, Mira's sense of duty, and the bedtime route become clear.",
                    "Make the world structured and readable before anything shifts.",
                    "Let familiar rituals anchor the listener before the problem arrives.",
                ),
                (
                    "catalyst",
                    "Catalyst",
                    "One lantern drifts away from the safe route and refuses to land.",
                    "Introduce a gentle problem worth following.",
                    "Keep the problem curious rather than alarming.",
                ),
                (
                    "debate",
                    "Debate",
                    "Mira worries that following the lantern will delay everyone else's rest.",
                    "Let hesitation feel honest but held.",
                    "Give Mira immediate companionship while she hesitates.",
                ),
                (
                    "break_into_two",
                    "Break into Two",
                    (
                        "Mira and Otis leave the dock and follow the lantern into the harbor's "
                        "quieter edges."
                    ),
                    "Turn worry into motion and wonder.",
                    "Make the departure feel purposeful and safe.",
                ),
                (
                    "b_story",
                    "B Story",
                    "Otis teaches Mira a slower way to listen when the harbor feels too large.",
                    "Deepen the relationship that will repair the low point later.",
                    "Keep every lesson actionable and soothing.",
                ),
                (
                    "fun_and_games",
                    "Fun and Games",
                    "The pair follows reflected clues past sleepy boats and glowing doorsteps.",
                    "Let wonder and playful discovery carry the middle stretch.",
                    "Favor delight and small mystery over suspense.",
                ),
                (
                    "midpoint",
                    "Midpoint",
                    (
                        "The missing lantern reveals a hidden cove where the harbor's final "
                        "promise waits."
                    ),
                    "Lift the wonder while widening the emotional stakes.",
                    "Keep the surprise luminous and quickly reassuring.",
                ),
                (
                    "bad_guys_close_in",
                    "Bad Guys Close In",
                    "The tide turns and Mira fears the route home may be slipping away.",
                    "Narrow the path without making the danger harsh.",
                    "Translate pressure into pacing and emotion, not threat.",
                ),
                (
                    "all_is_lost",
                    "All Is Lost",
                    (
                        "The lantern dims for a moment and Mira thinks she has failed the whole "
                        "harbor."
                    ),
                    "Let the low point feel temporary, specific, and emotionally legible.",
                    "Buffer the low point with visible companionship and a quick path to repair.",
                ),
                (
                    "dark_night_of_the_soul",
                    "Dark Night of the Soul",
                    (
                        "Otis helps Mira name the fear beneath her urgency and remember the "
                        "harbor's rhythms."
                    ),
                    "Turn fear into reflection and steadier trust.",
                    "Keep the pause intimate, warm, and brief.",
                ),
                (
                    "break_into_three",
                    "Break into Three",
                    (
                        "Mira chooses a gentler route home that lets the harbor's own lights "
                        "guide them."
                    ),
                    "Shift from anxious control to collaborative confidence.",
                    "Make the solution feel earned through calm, not force.",
                ),
                (
                    "finale",
                    "Finale",
                    (
                        "The lantern reaches its doorstep and the whole harbor settles into a "
                        "shared exhale."
                    ),
                    "Deliver repair, belonging, and visible calm.",
                    "Show everyone safe, connected, and ready for sleep.",
                ),
                (
                    "final_image",
                    "Final Image",
                    (
                        "Mira watches the restored lights shimmer once more before heading home "
                        "to rest."
                    ),
                    "End with softness and sleep-readiness.",
                    "Leave the listener with still water, dim lights, and nothing unresolved.",
                ),
            )
        ]
        return BeatSheetGenerationInvocationResult(
            invocation=invocation,
            structured_output=BeatSheetGenerationStructuredOutput(
                beat_sheet=GeneratedBeatSheetCandidate(
                    summary=(
                        "A harbor Save-the-Cat arc where Mira trades anxious urgency for trust, "
                        "guides each light home, and lets the night settle into belonging."
                    ),
                    bedtime_notes=(
                        "Keep every pressure beat readable, companioned, and brief enough that "
                        "the ending can land noticeably sleepier than the beginning."
                    ),
                    beats=beats,
                )
            ),
            raw_response={
                "stub": True,
                "usageMetadata": {
                    "promptTokenCount": 844,
                    "candidatesTokenCount": 371,
                    "totalTokenCount": 1215,
                },
            },
        )

    def close(self) -> None:
        return None


@dataclass
class PlanningFunnelJourney:
    session_id: str
    created: dict[str, Any]
    genre: dict[str, Any]
    tone: dict[str, Any]
    brief: dict[str, Any]
    pitches: dict[str, Any]
    pitch_selection: dict[str, Any]
    characters: dict[str, Any]
    character_selection: dict[str, Any]
    beats: dict[str, Any]
    beat_selection: dict[str, Any]
    story_setup: dict[str, Any]
    reloaded_snapshot: dict[str, Any]
    hydrated: dict[str, Any]
    history: dict[str, Any]


@pytest.fixture
def planning_funnel_api_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[TestClient]:
    database_path = tmp_path / "planning-funnel.sqlite3"
    monkeypatch.setenv("STORYTELLER_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    engine = get_engine()
    Base.metadata.create_all(engine)

    app = create_app()
    app.state.brief_normalization_adapter = PlanningFunnelBriefNormalizationAdapter()
    app.state.pitch_generation_adapter = PlanningFunnelPitchGenerationAdapter()
    app.state.character_generation_adapter = PlanningFunnelCharacterGenerationAdapter()
    app.state.beat_sheet_generation_adapter = PlanningFunnelBeatSheetGenerationAdapter()

    db_session = get_session_factory()()
    try:
        seed_catalog(db_session, load_catalog_document(CATALOG_FILE_PATH))
    finally:
        db_session.close()

    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()


def test_planning_funnel_e2e_persists_a_coherent_outline_ready_for_composition(
    planning_funnel_api_client: TestClient,
) -> None:
    journey = _run_planning_funnel(planning_funnel_api_client)

    assert journey.genre["snapshot"]["current_stage"] == "tone"
    assert journey.tone["snapshot"]["current_stage"] == "brief"
    assert journey.brief["snapshot"]["current_stage"] == "pitches"
    assert journey.pitches["snapshot"]["current_stage"] == "pitches"
    assert journey.pitch_selection["snapshot"]["current_stage"] == "characters"
    assert journey.characters["snapshot"]["current_stage"] == "characters"
    assert journey.character_selection["snapshot"]["current_stage"] == "beats"
    assert journey.beats["snapshot"]["current_stage"] == "beats"
    assert journey.beat_selection["snapshot"]["current_stage"] == "story_setup"

    final_snapshot = journey.story_setup["snapshot"]
    reloaded_snapshot = journey.reloaded_snapshot
    hydrated_snapshot = journey.hydrated["snapshot"]
    history = journey.history

    assert final_snapshot["current_stage"] == "composition"
    assert final_snapshot["resume_stage"] == "composition"
    assert final_snapshot["furthest_completed_stage"] == "story_setup"
    assert final_snapshot["overall_status"] == "in_progress"
    assert final_snapshot["progress"] == {
        "total_stages": 10,
        "completed_stages": 7,
        "in_progress_stages": 0,
        "needs_regeneration_stages": 0,
    }
    assert _stage_status(final_snapshot, "genre") == "completed"
    assert _stage_status(final_snapshot, "tone") == "completed"
    assert _stage_status(final_snapshot, "brief") == "completed"
    assert _stage_status(final_snapshot, "pitches") == "completed"
    assert _stage_status(final_snapshot, "characters") == "completed"
    assert _stage_status(final_snapshot, "beats") == "completed"
    assert _stage_status(final_snapshot, "story_setup") == "completed"
    assert _stage_status(final_snapshot, "composition") == "draft"
    assert _stage_status(final_snapshot, "audio") == "draft"
    assert _stage_status(final_snapshot, "finalize") == "draft"

    assert final_snapshot["selected_genre"]["slug"] == "quest-fantasy"
    assert final_snapshot["selected_tone_profile"]["slug"] == "hushed-wonder"
    assert final_snapshot["story_brief"]["normalized_summary"].startswith(
        "A harbor bedtime quest where Mira and an otter guardian guide stray lanterns home"
    )
    assert final_snapshot["selected_pitch"]["title"] == "Lanterns Over Juniper Cove"
    assert final_snapshot["selected_character_sheet"]["title"] == "Juniper Cove Lantern Crew"
    assert final_snapshot["selected_character_sheet"]["protagonist"]["name"] == "Mira"
    assert final_snapshot["selected_beat_sheet"]["revision_number"] == 1
    assert len(final_snapshot["selected_beat_sheet"]["beats"]) == 15

    assert final_snapshot["selected_story_setup"]["revision_number"] == 1
    assert final_snapshot["selected_story_setup"]["target_word_count"] == 2200
    assert final_snapshot["selected_story_setup"]["target_runtime_minutes"] == 14
    assert final_snapshot["selected_story_setup"]["chapter_count"] == 4
    assert final_snapshot["selected_story_setup"]["approximate_scene_count"] == 10
    assert final_snapshot["selected_story_setup"]["chapter_style"] is None
    assert final_snapshot["selected_story_setup"]["guidance_notes"] == (
        "Let each chapter land calmer than it began, and keep the late low point visibly supported."
    )
    assert final_snapshot["selected_story_setup"]["preferences"] == {"source": "workspace"}
    assert final_snapshot["selected_story_setup"]["accepted_at"] is not None

    outline = final_snapshot["selected_story_outline"]
    assert outline["revision_number"] == 1
    assert outline["outline_kind"] == "chapter"
    assert outline["summary"].startswith(
        "4 draftable chapters mapped from the accepted beat sheet."
    )
    assert outline["summary"].endswith("Lane: Quest Fantasy / Hushed Wonder.")
    assert len(outline["cards"]) == 4
    assert [card["position"] for card in outline["cards"]] == [1, 2, 3, 4]
    assert all(card["card_type"] == "chapter" for card in outline["cards"])
    assert all(card["purpose"] for card in outline["cards"])
    assert all(card["drafting_brief"] for card in outline["cards"])
    assert all(card["bedtime_guardrail"] for card in outline["cards"])
    assert all(card["tone_direction"] for card in outline["cards"])
    assert "Quest Fantasy / Hushed Wonder" in outline["cards"][0]["drafting_brief"]
    assert "Let each chapter land calmer than it began" in outline["cards"][0]["drafting_brief"]
    assert sum(card["target_word_count"] or 0 for card in outline["cards"]) == 2200
    assert sum(card["target_runtime_minutes"] or 0 for card in outline["cards"]) == 14
    assert sum(card["target_scene_count"] or 0 for card in outline["cards"]) == 10
    assert _flattened_beat_keys(outline["cards"]) == [
        beat["key"] for beat in final_snapshot["selected_beat_sheet"]["beats"]
    ]

    assert final_snapshot["current_plan_revision"] is not None
    assert final_snapshot["current_plan_revision"]["source_stage"] == "story_setup"
    assert final_snapshot["current_plan_revision"]["changed_artifacts"] == [
        "story_setup",
        "story_outline",
    ]
    assert final_snapshot["current_plan_revision"]["beat_sheet"]["revision_number"] == 1
    assert final_snapshot["current_plan_revision"]["story_setup"]["revision_number"] == 1
    assert final_snapshot["current_plan_revision"]["story_outline"]["revision_number"] == 1
    assert final_snapshot["current_plan_revision"]["story_setup"]["label"] == (
        "~14 min, 4 chapters, 10 scenes"
    )
    assert len(final_snapshot["plan_revisions"]) >= 4
    assert [revision["source_stage"] for revision in final_snapshot["plan_revisions"][:4]] == [
        "story_setup",
        "beats",
        "characters",
        "pitches",
    ]

    planning_usage = next(
        bucket
        for bucket in final_snapshot["usage_summary"]["buckets"]
        if bucket["usage_bucket"] == "planning"
    )
    assert final_snapshot["usage_summary"]["total_calls"] == 4
    assert planning_usage["total_calls"] == 4
    assert planning_usage["succeeded_calls"] == 4
    assert planning_usage["failed_calls"] == 0
    assert planning_usage["fallback_calls"] == 0
    assert set(planning_usage["models_used"]) == {"gemini-3.1-flash-lite", "gemini-3.1-pro"}

    current_plan_revision_id = final_snapshot["current_plan_revision"]["id"]
    assert reloaded_snapshot["id"] == final_snapshot["id"]
    assert reloaded_snapshot["selected_story_outline"]["id"] == outline["id"]
    assert reloaded_snapshot["current_plan_revision"]["id"] == current_plan_revision_id
    assert reloaded_snapshot["usage_summary"]["total_calls"] == 4

    assert hydrated_snapshot["selected_story_outline"]["id"] == outline["id"]
    assert hydrated_snapshot["current_plan_revision"]["id"] == current_plan_revision_id
    assert journey.hydrated["hydration"]["strategy"] == "materialized_only"
    assert (
        journey.hydrated["hydration"]["latest_sequence_number"] == history["latest_sequence_number"]
    )
    assert journey.hydrated["hydration"]["history_event_count"] == len(history["events"])

    assert history["session_id"] == journey.session_id
    assert history["latest_sequence_number"] == len(history["events"])
    assert [event["event_type"] for event in history["events"][:2]] == [
        "session.created",
        "workflow.stage_changed",
    ]
    assert [
        (event["stage"], event["payload"]["selection_kind"])
        for event in history["events"]
        if event["event_type"] == "selection.recorded"
    ] == [
        ("genre", "genre"),
        ("tone", "tone_profile"),
        ("pitches", "pitch"),
        ("characters", "character_sheet"),
        ("beats", "beat_sheet"),
        ("story_setup", "story_setup"),
    ]
    assert [
        (event["stage"], event["payload"]["output_kind"])
        for event in history["events"]
        if event["event_type"] == "ai.output.recorded"
    ] == [
        ("pitches", "pitch_batch"),
        ("characters", "character_sheet"),
        ("beats", "beat_sheet"),
    ]
    assert [
        event["stage"]
        for event in history["events"]
        if event["event_type"] == "content.user_edit.recorded"
    ] == [
        "brief",
        "story_setup",
    ]


def _run_planning_funnel(client: TestClient) -> PlanningFunnelJourney:
    created = _expect_json(
        client.post(
            "/api/v1/sessions",
            json={"working_title": "Planning Funnel E2E"},
        ),
        201,
    )
    session_id = created["id"]

    genre = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/selections/genre",
            json={"genre_slug": "quest-fantasy", "origin": "workspace"},
        )
    )
    tone = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/selections/tone",
            json={"tone_profile_slug": "hushed-wonder", "origin": "workspace"},
        )
    )
    brief = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/story-brief",
            json={
                "story_idea": (
                    "A lantern-keeper in training follows drifting harbor lanterns with an "
                    "otter guardian and learns how to slow down enough to guide them home."
                ),
                "desired_themes": "belonging, gentle courage, trust, and a calmer bedtime rhythm",
                "key_images": (
                    "floating lanterns, silver harbor water, sleepy docks, a hidden cove, "
                    "otter pawprints"
                ),
                "audience_notes": (
                    "Bedtime-safe for children who enjoy wonder, motion, and mystery as long as "
                    "the emotional landing is clear and restful."
                ),
                "must_have_elements": (
                    "End with the harbor settled, Mira feeling safe, and the final lantern back "
                    "where it belongs."
                ),
                "origin": "workspace",
            },
        )
    )
    pitches = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/pitches/generate",
            json={
                "candidate_count": 3,
                "guidance": (
                    "Favor harbor wonder and emotional clarity over suspense, and make sure the "
                    "restful ending is visible in the logline."
                ),
                "origin": "workspace",
            },
        )
    )
    selected_pitch_id = pitches["snapshot"]["pitch_batches"][0]["pitches"][0]["id"]
    pitch_selection = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/selections/pitch",
            json={"pitch_id": selected_pitch_id, "origin": "workspace"},
        )
    )
    characters = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/characters/generate",
            json={
                "candidate_count": 3,
                "guidance": (
                    "Keep the support cast compact and make the protagonist's calming ritual "
                    "easy to carry forward into later beats."
                ),
                "origin": "workspace",
            },
        )
    )
    selected_character_sheet_id = characters["snapshot"]["character_sheet_batches"][0][
        "character_sheets"
    ][0]["id"]
    character_selection = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/selections/character-sheet",
            json={
                "character_sheet_id": selected_character_sheet_id,
                "origin": "workspace",
            },
        )
    )
    beats = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/beats/generate",
            json={
                "guidance": (
                    "Keep the midpoint luminous, the low point brief, and the ending distinctly "
                    "sleepier than the opening."
                ),
                "focus_beats": ["midpoint", "all_is_lost", "finale"],
                "bedtime_goal": "Leave the listener feeling safe, held, and ready to sleep.",
                "origin": "workspace",
            },
        )
    )
    selected_beat_sheet_id = beats["snapshot"]["beat_sheet_revisions"][0]["id"]
    beat_selection = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/selections/beat-sheet",
            json={"beat_sheet_id": selected_beat_sheet_id, "origin": "workspace"},
        )
    )
    story_setup = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/story-setup",
            json={
                "target_word_count": 2200,
                "target_runtime_minutes": 14,
                "chapter_count": 4,
                "approximate_scene_count": 10,
                "guidance_notes": (
                    "Let each chapter land calmer than it began, and keep the late low point "
                    "visibly supported."
                ),
                "origin": "workspace",
            },
        )
    )
    reloaded_snapshot = _expect_json(client.get(f"/api/v1/sessions/{session_id}"))
    hydrated = _expect_json(client.get(f"/api/v1/sessions/{session_id}/hydrate"))
    history = _expect_json(client.get(f"/api/v1/sessions/{session_id}/history"))

    return PlanningFunnelJourney(
        session_id=session_id,
        created=created,
        genre=genre,
        tone=tone,
        brief=brief,
        pitches=pitches,
        pitch_selection=pitch_selection,
        characters=characters,
        character_selection=character_selection,
        beats=beats,
        beat_selection=beat_selection,
        story_setup=story_setup,
        reloaded_snapshot=reloaded_snapshot,
        hydrated=hydrated,
        history=history,
    )


def _expect_json(response, expected_status: int = 200) -> dict[str, Any]:
    assert response.status_code == expected_status, response.text
    return response.json()


def _stage_status(snapshot: dict[str, Any], stage: str) -> str:
    return next(item["status"] for item in snapshot["stage_states"] if item["stage"] == stage)


def _flattened_beat_keys(cards: list[dict[str, Any]]) -> list[str]:
    return [beat_key for card in cards for beat_key in card["beat_keys"]]
