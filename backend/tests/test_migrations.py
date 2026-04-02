from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

BACKEND_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TABLES = {
    "audio_jobs",
    "background_jobs",
    "beat_sheets",
    "character_sheets",
    "composition_jobs",
    "composition_segments",
    "continuity_bibles",
    "event_log_entries",
    "genres",
    "pitches",
    "session_memory_snapshots",
    "session_assets",
    "story_briefs",
    "story_outlines",
    "story_sessions",
    "story_setups",
    "tone_profiles",
    "workflow_stage_states",
}
EXPECTED_TONE_PROFILE_COLUMNS = {
    "id",
    "genre_id",
    "slug",
    "label",
    "description",
    "bedtime_notes",
    "descriptors",
    "default_planning_hints",
    "sort_order",
    "is_active",
    "created_at",
    "updated_at",
}
EXPECTED_BACKGROUND_JOB_COLUMNS = {
    "id",
    "session_id",
    "job_type",
    "status",
    "payload",
    "result_summary",
    "attempt_count",
    "lease_owner",
    "lease_token",
    "lease_expires_at",
    "claimed_at",
    "heartbeat_at",
    "started_at",
    "completed_at",
    "failed_at",
    "error_message",
    "created_at",
    "updated_at",
}
EXPECTED_SESSION_MEMORY_COLUMNS = {
    "id",
    "session_id",
    "trigger_event_id",
    "trigger_event_type",
    "trigger_event_sequence_number",
    "summary_text",
    "summary_data",
    "created_at",
}
EXPECTED_CONTINUITY_BIBLE_COLUMNS = {
    "id",
    "session_id",
    "revision_number",
    "source_stage",
    "source_summary",
    "summary_text",
    "summary_data",
    "is_selected",
    "created_at",
    "updated_at",
}
EXPECTED_STORY_BRIEF_COLUMNS = {
    "id",
    "session_id",
    "revision_number",
    "story_idea",
    "desired_themes",
    "key_images",
    "audience_notes",
    "must_have_elements",
    "raw_brief",
    "normalized_summary",
    "normalized_preferences",
    "planning_notes",
    "model_output",
    "is_active",
    "accepted_at",
    "created_at",
    "updated_at",
}
EXPECTED_STORY_SETUP_COLUMNS = {
    "id",
    "session_id",
    "beat_sheet_id",
    "revision_number",
    "target_word_count",
    "target_runtime_minutes",
    "chapter_count",
    "approximate_scene_count",
    "chapter_style",
    "guidance_notes",
    "preferences",
    "is_selected",
    "accepted_at",
    "created_at",
    "updated_at",
}
EXPECTED_STORY_OUTLINE_COLUMNS = {
    "id",
    "session_id",
    "beat_sheet_id",
    "story_setup_id",
    "revision_number",
    "outline_kind",
    "summary",
    "cards",
    "metadata_json",
    "is_selected",
    "accepted_at",
    "created_at",
    "updated_at",
}


def _build_alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "migrations"))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _get_table_names(database_url: str) -> set[str]:
    engine = create_engine(database_url)

    try:
        return set(inspect(engine).get_table_names())
    finally:
        engine.dispose()


def _get_column_names(database_url: str, table_name: str) -> set[str]:
    engine = create_engine(database_url)

    try:
        return {column["name"] for column in inspect(engine).get_columns(table_name)}
    finally:
        engine.dispose()


def test_alembic_can_upgrade_from_zero_to_head_and_back(tmp_path) -> None:
    database_path = tmp_path / "storyteller-migrations.db"
    database_url = f"sqlite:///{database_path}"
    config = _build_alembic_config(database_url)

    command.upgrade(config, "head")
    assert EXPECTED_TABLES <= _get_table_names(database_url)
    assert EXPECTED_TONE_PROFILE_COLUMNS <= _get_column_names(database_url, "tone_profiles")
    assert EXPECTED_BACKGROUND_JOB_COLUMNS <= _get_column_names(database_url, "background_jobs")
    assert EXPECTED_STORY_BRIEF_COLUMNS <= _get_column_names(database_url, "story_briefs")
    assert EXPECTED_STORY_OUTLINE_COLUMNS <= _get_column_names(database_url, "story_outlines")
    assert EXPECTED_STORY_SETUP_COLUMNS <= _get_column_names(database_url, "story_setups")
    assert EXPECTED_SESSION_MEMORY_COLUMNS <= _get_column_names(
        database_url,
        "session_memory_snapshots",
    )
    assert EXPECTED_CONTINUITY_BIBLE_COLUMNS <= _get_column_names(
        database_url,
        "continuity_bibles",
    )

    command.downgrade(config, "base")
    assert not (EXPECTED_TABLES & _get_table_names(database_url))

    command.upgrade(config, "head")
    assert EXPECTED_TABLES <= _get_table_names(database_url)
    assert EXPECTED_TONE_PROFILE_COLUMNS <= _get_column_names(database_url, "tone_profiles")
    assert EXPECTED_BACKGROUND_JOB_COLUMNS <= _get_column_names(database_url, "background_jobs")
    assert EXPECTED_STORY_BRIEF_COLUMNS <= _get_column_names(database_url, "story_briefs")
    assert EXPECTED_STORY_OUTLINE_COLUMNS <= _get_column_names(database_url, "story_outlines")
    assert EXPECTED_STORY_SETUP_COLUMNS <= _get_column_names(database_url, "story_setups")
    assert EXPECTED_SESSION_MEMORY_COLUMNS <= _get_column_names(
        database_url,
        "session_memory_snapshots",
    )
    assert EXPECTED_CONTINUITY_BIBLE_COLUMNS <= _get_column_names(
        database_url,
        "continuity_bibles",
    )
