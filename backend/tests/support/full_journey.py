from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

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
from app.services import evaluate_composition_segment_draft
from app.services.composition_jobs import GeneratedCompositionSegmentDraft
from app.storage import ObjectStorageService
from app.worker import JobWorker, build_default_job_handler_registry
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker


class FullJourneyBriefNormalizationAdapter:
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
                    "A harbor bedtime quest where Mira and an otter guardian guide drifting "
                    "lanterns home, turning late worry into calm belonging."
                ),
                normalized_preferences=NormalizedBriefPreferences(
                    protagonist_type="A child lantern-keeper and an otter guardian",
                    setting="a moonlit harbor with quiet docks, coves, and sleeping boats",
                    emotional_goal="turn anxious urgency into a restful return home",
                    constraint_notes=[
                        "End with the harbor settled and Mira safe in bed.",
                        "Keep every discovery easy for a sleepy child to follow.",
                    ],
                    bedtime_safety_concerns=[
                        "Any spike in tension should be brief, named, and soothed quickly.",
                    ],
                    candidate_motifs=[
                        "floating lanterns",
                        "silver harbor water",
                        "dock-bell echoes",
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


class FullJourneyPitchGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: PitchGenerationInvocation,
    ) -> PitchGenerationInvocationResult:
        if invocation.context.generation_goal == "refinement":
            pitches = [
                GeneratedPitchCandidate(
                    title="Lanterns Over Juniper Cove",
                    hook=(
                        "Mira and her otter-like harbor guardian Otis follow drifting lanterns "
                        "across Juniper Cove so every light can reach home before the last bell."
                    ),
                    central_conflict=(
                        "A worried missing lantern keeps asking Mira to trust Otis and share the "
                        "burden of guiding the harbor home."
                    ),
                    why_it_fits=(
                        "It keeps the selected harbor imagery, softens the conflict into shared "
                        "care, and lands the bedtime promise in visible belonging."
                    ),
                )
            ]
        else:
            pitches = [
                GeneratedPitchCandidate(
                    title="Lanterns Over Juniper Cove",
                    hook=(
                        "Mira and a patient otter guardian follow drifting lanterns across the "
                        "harbor so every light can reach home before the last bell."
                    ),
                    central_conflict=(
                        "A hidden cove and one worried missing lantern threaten to stretch the "
                        "bedtime route longer than Mira can manage alone."
                    ),
                    why_it_fits=(
                        "It keeps the quest active while using luminous harbor imagery, "
                        "small-scale stakes, and a visibly restful ending."
                    ),
                ),
                GeneratedPitchCandidate(
                    title="The Quiet Map of Lights",
                    hook=(
                        "A path of lantern reflections opens over the water, inviting Mira to "
                        "solve the harbor's gentlest unfinished promise."
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
                        "When one lantern refuses to land, Mira and Otis make a moonlit tour of "
                        "the docks to learn what kindness the night still needs."
                    ),
                    central_conflict=(
                        "They need to finish the route before the harbor can rest, but each stop "
                        "asks Mira to trade anxious control for steadier trust."
                    ),
                    why_it_fits=(
                        "It supports bedtime pacing by making the conflict internal, relational, "
                        "and safely resolved before sleep."
                    ),
                ),
            ]

        return PitchGenerationInvocationResult(
            invocation=invocation,
            structured_output=PitchGenerationStructuredOutput(pitches=pitches),
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


class FullJourneyCharacterGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: CharacterGenerationInvocation,
    ) -> CharacterGenerationInvocationResult:
        if invocation.context.generation_goal == "refinement":
            character_sheets = [
                GeneratedCharacterSheetCandidate(
                    title="Juniper Cove Lantern Crew",
                    summary=(
                        "Mira and Otis now read as an almost-sibling pair who turn the harbor "
                        "quest into a shared bedtime promise."
                    ),
                    story_function=(
                        "This refinement sharpens their back-and-forth comfort dynamic so later "
                        "beats can show co-regulation instead of lonely strain."
                    ),
                    bedtime_safety_notes=(
                        "Otis stays physically and emotionally close, translating every worry "
                        "into a small, solvable next step."
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
                        flaw="tries to carry every worry alone instead of sharing the route",
                        comfort_trait="counts dock-bell echoes until her breathing slows",
                        bedtime_safety_notes=(
                            "Mira is never left alone with fear for long; Otis and the harbor "
                            "rituals keep each obstacle readable."
                        ),
                        relationships=[
                            "Treats Otis like the steady older sibling she can finally lean on.",
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
                            goal="help Mira trade anxious control for shared trust",
                            flaw="sometimes softens his own needs until Mira asks",
                            comfort_trait="grounds scenes with small repeated harbor rituals",
                            bedtime_safety_notes=(
                                "Otis makes each late-night complication concrete, small, and "
                                "quickly reassuring."
                            ),
                            relationships=[
                                "Shows Mira how sibling-like care can feel calm instead of heavy.",
                            ],
                            visual_anchors=[
                                "tidy rope satchel",
                                "river-smooth lantern staff",
                            ],
                        )
                    ],
                )
            ]
        else:
            character_sheets = [
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
                        "This option would make the midpoint and low point hinge on dialogue and "
                        "naming feelings rather than movement."
                    ),
                    bedtime_safety_notes=(
                        "Mystery beats stay gentle because every reveal is quickly interpreted by "
                        "a supportive companion."
                    ),
                    visual_motifs=[
                        "glowing tide charts",
                        "quiet dock shadows",
                    ],
                    protagonist=GeneratedCharacterProfile(
                        name="Mira",
                        role="harbor listener",
                        goal="understand why one lantern is still roaming",
                        flaw="waits too long to speak when she feels unsure",
                        comfort_trait="matches her breathing to harbor bells",
                        bedtime_safety_notes="She is always paired with a calm interpreter.",
                        relationships=["Learns to say what she needs out loud."],
                        visual_anchors=["knotted charm bracelet"],
                    ),
                    supporting_cast=[
                        GeneratedCharacterProfile(
                            name="Otis",
                            role="harbor guide",
                            goal="help Mira trust what she notices",
                            flaw="can over-protect Mira's feelings",
                            comfort_trait="turns each discovery into a bedtime ritual",
                            bedtime_safety_notes="He turns uncertainty into gentle explanation.",
                            relationships=["Reflects Mira's courage back to her."],
                            visual_anchors=["harbor map satchel"],
                        )
                    ],
                ),
            ]

        return CharacterGenerationInvocationResult(
            invocation=invocation,
            structured_output=CharacterGenerationStructuredOutput(
                character_sheets=character_sheets
            ),
            raw_response={
                "stub": True,
                "usageMetadata": {
                    "promptTokenCount": 711,
                    "candidatesTokenCount": 387,
                    "totalTokenCount": 1098,
                },
            },
        )

    def close(self) -> None:
        return None


class FullJourneyBeatSheetGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: BeatSheetGenerationInvocation,
    ) -> BeatSheetGenerationInvocationResult:
        beat_sheet = GeneratedBeatSheetCandidate(
            summary=(
                "Mira and Otis guide the harbor's last drifting lanterns home, turning anxious "
                "urgency into shared trust and a visibly sleepy return."
            ),
            bedtime_notes=(
                "Keep each low point brief, buffered by companionship, and resolved into a calm "
                "nighttime landing."
            ),
            beats=[
                GeneratedBeatSheetBeat(
                    key=key,
                    label=label,
                    summary=(
                        f"{label} keeps Mira and Otis moving through the harbor with gentle "
                        "stakes, luminous imagery, and a clear step toward rest."
                    ),
                    emotional_intent=(
                        "Let worry become more legible and more supported than the beat before."
                    ),
                    bedtime_softening_note=(
                        "Any uncertainty should stay brief, named clearly, and followed by "
                        "visible comfort."
                    ),
                )
                for key, label in (
                    ("opening_image", "Opening Image"),
                    ("theme_stated", "Theme Stated"),
                    ("set_up", "Set-Up"),
                    ("catalyst", "Catalyst"),
                    ("debate", "Debate"),
                    ("break_into_two", "Break into Two"),
                    ("b_story", "B Story"),
                    ("fun_and_games", "Fun and Games"),
                    ("midpoint", "Midpoint"),
                    ("bad_guys_close_in", "Bad Guys Close In"),
                    ("all_is_lost", "All Is Lost"),
                    ("dark_night_of_the_soul", "Dark Night of the Soul"),
                    ("break_into_three", "Break into Three"),
                    ("finale", "Finale"),
                    ("final_image", "Final Image"),
                )
            ],
        )
        return BeatSheetGenerationInvocationResult(
            invocation=invocation,
            structured_output=BeatSheetGenerationStructuredOutput(beat_sheet=beat_sheet),
            raw_response={
                "stub": True,
                "usageMetadata": {
                    "promptTokenCount": 802,
                    "candidatesTokenCount": 421,
                    "totalTokenCount": 1223,
                },
            },
        )

    def close(self) -> None:
        return None


class FullJourneyCompositionWriter:
    def compose_segment(
        self,
        *,
        segment_payload,
        prior_segments,
        current_partial_text,
        total_segments,
    ) -> GeneratedCompositionSegmentDraft:
        del prior_segments, current_partial_text, total_segments
        prompt = segment_payload["composition_prompt"]
        dynamic_context = prompt["dynamic_context"]
        segment_index = int(dynamic_context["segment_index"])
        protagonist_name = (
            dynamic_context["selected_character_sheet"].get("protagonist_name") or "Mira"
        )
        companion_name = "Otis"
        accepted_text = _build_segment_text(
            segment_index=segment_index,
            protagonist_name=protagonist_name,
            companion_name=companion_name,
        )
        carryover_summary = (
            f"Segment {segment_index} leaves {protagonist_name} calmer, keeps the lantern "
            f"promise active, and sends {companion_name} forward as visible support."
        )
        evaluation = evaluate_composition_segment_draft(
            accepted_text,
            protagonist_name=protagonist_name,
            supporting_character_name=companion_name,
            carryover_summary=carryover_summary,
        )
        paragraphs = tuple(
            paragraph for paragraph in accepted_text.split("\n\n") if paragraph.strip()
        )
        return GeneratedCompositionSegmentDraft(
            raw_text=accepted_text,
            accepted_text=accepted_text,
            carryover_summary=carryover_summary,
            remaining_chunks=paragraphs,
            evaluation=evaluation,
            source="heuristic",
        )


@dataclass(frozen=True)
class FullJourneyPlanningResult:
    session_id: str
    created: dict[str, Any]
    genre: dict[str, Any]
    tone: dict[str, Any]
    brief: dict[str, Any]
    pitches: dict[str, Any]
    refined_pitch: dict[str, Any]
    characters: dict[str, Any]
    selected_character: dict[str, Any]
    refined_character: dict[str, Any]
    beats: dict[str, Any]
    beat_selection: dict[str, Any]
    story_setup: dict[str, Any]


def run_full_journey_planning(client: TestClient) -> FullJourneyPlanningResult:
    created = _expect_json(
        client.post(
            "/api/v1/sessions",
            json={"working_title": "Full Journey E2E"},
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
                    "otter guardian and learns how to share the route home."
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
                    "Favor harbor wonder and emotional clarity over suspense, and keep the "
                    "restful ending visible in the logline."
                ),
                "origin": "workspace",
            },
        )
    )
    source_pitch = pitches["snapshot"]["pitch_batches"][0]["pitches"][1]
    refined_pitch = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/pitches/refine",
            json={
                "pitch_id": source_pitch["id"],
                "instructions": "Make Mira and Otis feel more sibling-like and mutually steadying.",
                "origin": "chat",
            },
        )
    )

    characters = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/characters/generate",
            json={
                "candidate_count": 3,
                "guidance": (
                    "Keep the support cast compact and make Mira's calming ritual easy to carry "
                    "forward into later beats."
                ),
                "origin": "workspace",
            },
        )
    )
    source_character_sheet = characters["snapshot"]["character_sheet_batches"][0][
        "character_sheets"
    ][1]
    selected_character = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/selections/character-sheet",
            json={
                "character_sheet_id": source_character_sheet["id"],
                "origin": "workspace",
            },
        )
    )
    refined_character = _expect_json(
        client.post(
            f"/api/v1/sessions/{session_id}/characters/refine",
            json={
                "character_sheet_id": source_character_sheet["id"],
                "instructions": "Make Mira and Otis feel even more sibling-like and co-regulating.",
                "focus_character_names": ["Mira", "Otis"],
                "change_summary": "Sharpen the mutual comfort dynamic.",
                "change_impact": "major",
                "origin": "chat",
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
                "target_word_count": 2400,
                "target_runtime_minutes": 15,
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

    return FullJourneyPlanningResult(
        session_id=session_id,
        created=created,
        genre=genre,
        tone=tone,
        brief=brief,
        pitches=pitches,
        refined_pitch=refined_pitch,
        characters=characters,
        selected_character=selected_character,
        refined_character=refined_character,
        beats=beats,
        beat_selection=beat_selection,
        story_setup=story_setup,
    )


def build_worker(
    *,
    session_factory: sessionmaker[Session],
    object_storage: ObjectStorageService,
    composition_writer,
    tts_adapter,
) -> JobWorker:
    return JobWorker(
        session_factory=session_factory,
        registry=build_default_job_handler_registry(
            object_storage=object_storage,
            composition_writer=composition_writer,
            tts_adapter=tts_adapter,
        ),
        worker_id="full-journey-worker",
        lease_duration=timedelta(seconds=30),
        poll_interval_seconds=0.01,
    )


def run_worker_until_idle(worker: JobWorker, *, max_jobs: int = 20) -> int:
    processed_jobs = 0
    while worker.run_once():
        processed_jobs += 1
        if processed_jobs >= max_jobs:
            raise AssertionError(f"worker exceeded {max_jobs} jobs without going idle")
    return processed_jobs


def _expect_json(response, expected_status: int = 200) -> dict[str, Any]:
    assert response.status_code == expected_status, response.text
    return response.json()


def _build_segment_text(
    *,
    segment_index: int,
    protagonist_name: str,
    companion_name: str,
) -> str:
    return "\n\n".join(
        [
            (
                f"Segment {segment_index} lets {protagonist_name} follow the silver bell "
                "through a gentle stretch of harbor water while the night stays readable, warm, "
                "and unmistakably safe for bedtime listening."
            ),
            (
                f"{companion_name} stays close enough to steady every surprise, and the prose "
                "keeps the movement soft, patient, visibly cared for, and easy for a sleepy "
                "child to trust."
            ),
            (
                f"The moment lands in calm repair, so {protagonist_name} and {companion_name} "
                "can rest before the next handoff, with the harbor settled, the promise intact, "
                "and the final image quiet."
            ),
        ]
    )
