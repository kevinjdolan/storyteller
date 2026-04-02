"""Domain services for the Storyteller backend."""

from app.services.action_policy import (
    SessionActionPolicyService,
    SessionActionPolicyServiceError,
)
from app.services.assets import (
    AssetNotFoundError,
    AssetOwnershipError,
    AssetServiceError,
    AssetSessionNotFoundError,
    SessionAssetService,
)
from app.services.audio_jobs import (
    AUDIO_RUNTIME_JOB_TYPE,
    AudioJobNotFoundError,
    AudioJobService,
    AudioJobServiceError,
    AudioJobStartResult,
    AudioJobStateError,
    build_silence_pcm,
    build_wav_bytes,
    read_wav_bytes,
)
from app.services.beat_sheet_generation import (
    BeatSheetGenerationService,
    build_beat_sheet_model_output,
    evaluate_beat_sheet,
)
from app.services.brief_normalization import (
    BriefNormalizationService,
    apply_brief_normalization_overrides,
    build_brief_model_output,
    build_brief_normalization_result_from_existing,
    synthesize_normalized_summary,
)
from app.services.character_generation import (
    CharacterGenerationService,
    build_character_model_output,
    evaluate_character_sheet_batch,
)
from app.services.composition_jobs import (
    COMPOSITION_RUNTIME_JOB_TYPE,
    CompositionJobNotFoundError,
    CompositionJobService,
    CompositionJobServiceError,
    CompositionJobStateError,
    CompositionSegmentWriter,
    GeminiCompositionSegmentWriter,
    HeuristicCompositionSegmentWriter,
    evaluate_composition_segment_draft,
)
from app.services.composition_prompt_assembly import (
    CompositionPromptAssemblyService,
    CompositionPromptAssemblyServiceError,
)
from app.services.continuity import SessionContinuityService, build_continuity_payload
from app.services.conversation_memory import SessionMemoryService
from app.services.event_log import SessionEventLogService
from app.services.intent_parser import SessionIntentParserService
from app.services.jobs import (
    BackgroundJobLeaseLostError,
    BackgroundJobNotFoundError,
    BackgroundJobRecord,
    BackgroundJobService,
    BackgroundJobServiceError,
    ClaimedBackgroundJob,
)
from app.services.narration_segmentation import (
    NarrationPlanResult,
    NarrationSegmentationError,
    NarrationSegmentationService,
)
from app.services.outline_generation import (
    StoryOutlineGenerationService,
    StoryOutlineGenerationServiceError,
)
from app.services.pitch_generation import (
    PitchGenerationService,
    build_pitch_model_output,
    evaluate_pitch_batch,
)
from app.services.session_hydration import (
    SessionHydrationNotFoundError,
    SessionHydrationService,
    SessionHydrationServiceError,
)
from app.services.sessions import (
    InvalidStageTransitionError,
    SessionNotFoundError,
    SessionService,
    SessionServiceError,
    UnsupportedSessionContextUpdateError,
)
from app.services.story_tools import (
    StoryWorkflowActionRouter,
    StoryWorkflowToolDefinition,
    StoryWorkflowToolRegistry,
    StoryWorkflowToolService,
    StoryWorkflowToolServiceError,
    get_story_workflow_tool_prompt_catalog,
    get_story_workflow_tool_registry,
    get_story_workflow_tool_schema_bundle,
)

__all__ = [
    "AssetNotFoundError",
    "AssetOwnershipError",
    "AssetServiceError",
    "AssetSessionNotFoundError",
    "AUDIO_RUNTIME_JOB_TYPE",
    "AudioJobNotFoundError",
    "AudioJobService",
    "AudioJobServiceError",
    "AudioJobStartResult",
    "AudioJobStateError",
    "BackgroundJobLeaseLostError",
    "BackgroundJobNotFoundError",
    "BackgroundJobRecord",
    "BackgroundJobService",
    "BackgroundJobServiceError",
    "BeatSheetGenerationService",
    "BriefNormalizationService",
    "CharacterGenerationService",
    "ClaimedBackgroundJob",
    "COMPOSITION_RUNTIME_JOB_TYPE",
    "CompositionJobNotFoundError",
    "CompositionJobService",
    "CompositionJobServiceError",
    "CompositionJobStateError",
    "CompositionSegmentWriter",
    "CompositionPromptAssemblyService",
    "CompositionPromptAssemblyServiceError",
    "GeminiCompositionSegmentWriter",
    "SessionContinuityService",
    "InvalidStageTransitionError",
    "NarrationPlanResult",
    "NarrationSegmentationError",
    "NarrationSegmentationService",
    "PitchGenerationService",
    "StoryOutlineGenerationService",
    "StoryOutlineGenerationServiceError",
    "SessionActionPolicyService",
    "SessionActionPolicyServiceError",
    "SessionIntentParserService",
    "SessionMemoryService",
    "SessionNotFoundError",
    "SessionAssetService",
    "SessionEventLogService",
    "SessionHydrationNotFoundError",
    "SessionHydrationService",
    "SessionHydrationServiceError",
    "SessionService",
    "SessionServiceError",
    "StoryWorkflowActionRouter",
    "StoryWorkflowToolDefinition",
    "StoryWorkflowToolRegistry",
    "StoryWorkflowToolService",
    "StoryWorkflowToolServiceError",
    "UnsupportedSessionContextUpdateError",
    "apply_brief_normalization_overrides",
    "build_beat_sheet_model_output",
    "build_brief_model_output",
    "build_silence_pcm",
    "build_wav_bytes",
    "build_character_model_output",
    "build_continuity_payload",
    "build_brief_normalization_result_from_existing",
    "build_pitch_model_output",
    "evaluate_character_sheet_batch",
    "evaluate_composition_segment_draft",
    "evaluate_beat_sheet",
    "evaluate_pitch_batch",
    "get_story_workflow_tool_prompt_catalog",
    "get_story_workflow_tool_registry",
    "get_story_workflow_tool_schema_bundle",
    "read_wav_bytes",
    "synthesize_normalized_summary",
    "HeuristicCompositionSegmentWriter",
]
