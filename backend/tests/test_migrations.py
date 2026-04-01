from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

BACKEND_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TABLES = {
    "audio_jobs",
    "beat_sheets",
    "character_sheets",
    "composition_jobs",
    "composition_segments",
    "event_log_entries",
    "export_assets",
    "genres",
    "pitches",
    "story_briefs",
    "story_sessions",
    "story_setups",
    "tone_profiles",
    "workflow_stage_states",
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


def test_alembic_can_upgrade_from_zero_to_head_and_back(tmp_path) -> None:
    database_path = tmp_path / "storyteller-migrations.db"
    database_url = f"sqlite:///{database_path}"
    config = _build_alembic_config(database_url)

    command.upgrade(config, "head")
    assert EXPECTED_TABLES <= _get_table_names(database_url)

    command.downgrade(config, "base")
    assert not (EXPECTED_TABLES & _get_table_names(database_url))

    command.upgrade(config, "head")
    assert EXPECTED_TABLES <= _get_table_names(database_url)
