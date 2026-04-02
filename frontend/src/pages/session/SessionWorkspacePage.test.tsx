import { fireEvent, screen, within } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type {
  SessionCharacterSheetGenerationResponse,
  SessionHydration,
  SessionHistory,
  SessionPitchGenerationResponse,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import { SessionWorkspacePage } from './SessionWorkspacePage.tsx'

const sampleSnapshot: SessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  working_title: 'Lanterns Over Juniper Lake',
  current_stage: 'beats',
  resume_stage: 'beats',
  furthest_completed_stage: 'characters',
  overall_status: 'in_progress',
  created_at: '2026-04-01T03:00:00Z',
  updated_at: '2026-04-01T05:15:00Z',
  completed_at: null,
  selected_genre: {
    id: 'genre-1',
    slug: 'quest-fantasy',
    label: 'Quest Fantasy',
  },
  selected_tone_profile: {
    id: 'tone-1',
    slug: 'hushed-wonder',
    label: 'Hushed Wonder',
  },
  progress: {
    total_stages: 10,
    completed_stages: 5,
    in_progress_stages: 1,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'genre',
      label: 'Genre',
      description:
        'Choose the overall bedtime-story lane before the rest of the plan is shaped.',
      status: 'completed',
      detail: 'Accepted quest fantasy.',
    },
    {
      stage: 'tone',
      label: 'Tone',
      description:
        'Choose the emotional texture and bedtime-safety posture for the session.',
      status: 'completed',
      detail: 'Selected a soft adventurous tone.',
    },
    {
      stage: 'brief',
      label: 'Story brief',
      description:
        "Capture the user's free-form idea and any normalized planning summary derived from it.",
      status: 'completed',
      detail: 'Accepted normalized brief.',
    },
    {
      stage: 'pitches',
      label: 'Pitches',
      description:
        'Generate, compare, refine, and accept candidate story directions.',
      status: 'completed',
      detail: 'Accepted the harbor lantern pitch.',
    },
    {
      stage: 'characters',
      label: 'Characters',
      description:
        'Define the accepted character sheet that later planning and writing will reference.',
      status: 'completed',
      detail: 'Locked the character sheet.',
    },
    {
      stage: 'beats',
      label: 'Beat sheet',
      description:
        'Store the accepted Save-the-Cat beat sheet for the session.',
      status: 'in_progress',
      detail: 'Midpoint needs one more bedtime-soft pass.',
    },
    {
      stage: 'story_setup',
      label: 'Story setup',
      description:
        'Store soft planning targets such as word count, runtime, and chapter structure.',
      status: 'draft',
      detail: null,
    },
    {
      stage: 'composition',
      label: 'Composition',
      description:
        'Write the story durably in segments, with room for interruption and targeted rewrites.',
      status: 'draft',
      detail: null,
    },
    {
      stage: 'audio',
      label: 'Audio',
      description:
        'Configure narration settings and generate resumable audio artifacts.',
      status: 'draft',
      detail: null,
    },
    {
      stage: 'finalize',
      label: 'Finalize',
      description: 'Read, listen, review final assets, and download exports.',
      status: 'draft',
      detail: null,
    },
  ],
  story_brief: {
    id: 'brief-1',
    revision_number: 1,
    story_idea:
      'A child follows floating lanterns across a harbor and helps a shy otter guardian bring them home.',
    desired_themes: 'Belonging, gentle courage, and a calm return home.',
    key_images: 'Lanterns on dark water, otter paws, and moonlit docks.',
    audience_notes:
      'For an early-elementary read-aloud that stays cozy instead of suspenseful.',
    must_have_elements: 'A harbor reunion and a restful ending.',
    raw_brief:
      'A child follows floating lanterns across a harbor and helps a shy otter guardian bring them home.',
    normalized_summary:
      'A harbor bedtime quest where floating lanterns guide a child and an otter toward a calm reunion.',
    normalized_preferences: {
      protagonist_type: 'A child and an otter guardian',
      setting: 'a moonlit harbor',
      emotional_goal: 'belonging, gentle courage, and a calm reunion',
      constraint_notes: ['Keep the ending restful.'],
      bedtime_safety_concerns: ['Let any mystery resolve gently.'],
      candidate_motifs: ['floating lanterns', 'moonlit docks', 'otter paws'],
    },
    updated_at: '2026-04-01T05:14:00Z',
  },
  pitch_batches: [
    {
      generation_key: 'batch-1',
      candidate_count: 2,
      created_at: '2026-04-01T05:13:00Z',
      pitches: [
        {
          id: 'pitch-1',
          generation_key: 'batch-1',
          pitch_index: 1,
          title: 'Lanterns Over Juniper Lake',
          hook: 'A child and an otter guardian follow drifting lanterns across the harbor to return each light before bedtime.',
          central_conflict:
            'They need to help each lantern find the right doorstep before one frightened pause turns the calm journey into a longer night.',
          why_it_fits:
            'It fits Quest Fantasy and Hushed Wonder by keeping the movement gentle, the imagery luminous, and the ending clearly restful.',
          logline:
            'A child and an otter guardian follow drifting lanterns across the harbor to return each light before bedtime.',
          summary:
            'They need to help each lantern find the right doorstep before one frightened pause turns the calm journey into a longer night.',
          bedtime_notes:
            'It fits Quest Fantasy and Hushed Wonder by keeping the movement gentle, the imagery luminous, and the ending clearly restful.',
          is_selected: true,
          accepted_at: '2026-04-01T05:13:30Z',
          created_at: '2026-04-01T05:13:00Z',
          updated_at: '2026-04-01T05:13:30Z',
        },
        {
          id: 'pitch-2',
          generation_key: 'batch-1',
          pitch_index: 2,
          title: 'The Otter Who Counted the Lights',
          hook: 'A harbor child helps a shy otter guardian count the last awake lanterns before the docks can finally settle.',
          central_conflict:
            'Each lantern reveals one lingering nighttime worry, and the pair must answer all of them before anyone can relax into sleep.',
          why_it_fits:
            'It fits the brief by turning the harbor imagery into a calmer bedside mystery with clear emotional repair.',
          logline:
            'A harbor child helps a shy otter guardian count the last awake lanterns before the docks can finally settle.',
          summary:
            'Each lantern reveals one lingering nighttime worry, and the pair must answer all of them before anyone can relax into sleep.',
          bedtime_notes:
            'It fits the brief by turning the harbor imagery into a calmer bedside mystery with clear emotional repair.',
          is_selected: false,
          accepted_at: null,
          created_at: '2026-04-01T05:13:01Z',
          updated_at: '2026-04-01T05:13:01Z',
        },
      ],
    },
  ],
  selected_pitch: {
    id: 'pitch-1',
    generation_key: 'batch-1',
    pitch_index: 1,
    title: 'Lanterns Over Juniper Lake',
    hook: 'A child and an otter guardian follow drifting lanterns across the harbor to return each light before bedtime.',
    central_conflict:
      'They need to help each lantern find the right doorstep before one frightened pause turns the calm journey into a longer night.',
    why_it_fits:
      'It fits Quest Fantasy and Hushed Wonder by keeping the movement gentle, the imagery luminous, and the ending clearly restful.',
    logline:
      'A child and an otter guardian follow drifting lanterns across the harbor to return each light before bedtime.',
    summary:
      'They need to help each lantern find the right doorstep before one frightened pause turns the calm journey into a longer night.',
    bedtime_notes:
      'It fits Quest Fantasy and Hushed Wonder by keeping the movement gentle, the imagery luminous, and the ending clearly restful.',
    is_selected: true,
    accepted_at: '2026-04-01T05:13:30Z',
    created_at: '2026-04-01T05:13:00Z',
    updated_at: '2026-04-01T05:13:30Z',
  },
  selected_character_sheet: null,
  selected_story_setup: {
    id: 'setup-1',
    revision_number: 1,
    target_word_count: 1500,
    target_runtime_minutes: 12,
    chapter_count: 4,
    chapter_style: 'short',
  },
  active_composition_job: null,
  active_audio_job: null,
  latest_story_asset: null,
  latest_audio_asset: null,
}

const sampleHistory: SessionHistory = {
  session_id: 'moonlit-harbor',
  latest_sequence_number: 4,
  events: [
    {
      id: 'event-1',
      session_id: 'moonlit-harbor',
      sequence_number: 1,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'session.created',
      stage: null,
      summary: 'Created session: Lanterns Over Juniper Lake.',
      payload: {
        schema_version: 1,
        working_title: 'Lanterns Over Juniper Lake',
      },
      created_at: '2026-04-01T03:00:00Z',
    },
    {
      id: 'event-2',
      session_id: 'moonlit-harbor',
      sequence_number: 2,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'genre',
      summary: 'Selected genre: Quest Fantasy.',
      payload: {
        schema_version: 1,
        selection_kind: 'genre',
        label: 'Quest Fantasy',
        accepted: true,
        source: 'ui',
      },
      created_at: '2026-04-01T03:01:00Z',
    },
    {
      id: 'event-3',
      session_id: 'moonlit-harbor',
      sequence_number: 3,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'tone',
      summary: 'Selected tone profile: Hushed Wonder.',
      payload: {
        schema_version: 1,
        selection_kind: 'tone_profile',
        label: 'Hushed Wonder',
        accepted: true,
        source: 'ui',
      },
      created_at: '2026-04-01T03:02:00Z',
    },
    {
      id: 'event-4',
      session_id: 'moonlit-harbor',
      sequence_number: 4,
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      event_type: 'chat.message.recorded',
      stage: 'beats',
      summary: 'Recorded assistant chat message.',
      payload: {
        schema_version: 1,
        message_role: 'assistant',
        content_preview:
          'The current focus is softening the midpoint before composition starts.',
        content_length: 71,
        source: 'intent_parser',
      },
      created_at: '2026-04-01T03:03:00Z',
    },
  ],
}

const sampleHydration: SessionHydration = {
  snapshot: sampleSnapshot,
  recent_history: sampleHistory,
  hydration: {
    strategy: 'materialized_only',
    materialized_through_sequence_number: 4,
    replay_from_sequence_number: null,
    replayed_event_count: 0,
    latest_sequence_number: 4,
    history_event_count: 4,
    history_window_truncated: false,
  },
}

const sampleGenreCatalog = [
  {
    id: 'genre-1',
    slug: 'quest-fantasy',
    label: 'Quest Fantasy',
    description:
      'A bedtime-safe adventure with a clear destination, gentle bravery, and a warm return home.',
    bedtime_safety_notes:
      'Keep the journey wondrous rather than perilous; any danger should feel temporary, buffered by helpers, and resolved before sleep.',
    arc_notes: {
      core_arc:
        'Leave a familiar safe place, face one meaningful but gentle challenge, and return more settled and confident.',
      tension_ceiling: 'Low to moderate',
    },
    sort_order: 0,
  },
  {
    id: 'genre-2',
    slug: 'gentle-mystery',
    label: 'Gentle Mystery',
    description:
      'A puzzle-forward bedtime story driven by clues, curiosity, and a reassuring explanation.',
    bedtime_safety_notes:
      'Mystery should never feel menacing; clues can be strange, but the world must stay emotionally safe and readable.',
    arc_notes: {
      core_arc:
        'Notice a small mystery, gather clues, make a calm discovery, and restore ease.',
      tension_ceiling: 'Low',
    },
    sort_order: 1,
  },
] as const

const sampleToneCatalogByGenre = {
  'quest-fantasy': [
    {
      id: 'tone-1',
      genre_id: 'genre-1',
      slug: 'hushed-wonder',
      label: 'Hushed Wonder',
      description:
        'Moonlit awe, soft magic, and quiet courage lead the adventure.',
      bedtime_notes:
        'Avoid sharp reversals or loud triumph; let discoveries feel luminous and safe.',
      descriptors: ['luminous', 'moonlit', 'gentle', 'reverent'],
      default_planning_hints: {
        pacing: 'unhurried',
        conflict_style:
          'obstacles yield through patience, observation, or kindness',
        sensory_motifs: ['lantern light', 'silver water', 'whispering leaves'],
        ending_style: 'return home carrying a small token of wonder',
      },
      sort_order: 0,
    },
    {
      id: 'tone-2',
      genre_id: 'genre-1',
      slug: 'lantern-brave',
      label: 'Lantern Brave',
      description:
        'A steadier, more active quest tone where bravery feels cozy instead of intense.',
      bedtime_notes:
        "Keep the hero's courage rooted in reassurance from mentors, companions, or familiar rituals.",
      descriptors: [
        'steady',
        'reassuring',
        'warmhearted',
        'lightly adventurous',
      ],
      default_planning_hints: {
        pacing: 'steady',
        conflict_style:
          'one central problem solved through teamwork and persistence',
        sensory_motifs: ['lantern glow', 'packed satchel', 'firelit path'],
        ending_style: 'celebrate quietly, then settle into rest',
      },
      sort_order: 1,
    },
  ],
  'gentle-mystery': [
    {
      id: 'tone-3',
      genre_id: 'genre-2',
      slug: 'cozy-sleuthing',
      label: 'Cozy Sleuthing',
      description:
        'Homey detective energy with snacks, family, and friendly helpers in the loop.',
      bedtime_notes:
        'Let the investigation happen in familiar spaces with emotionally available companions.',
      descriptors: ['homey', 'playful', 'reassuring', 'neighborly'],
      default_planning_hints: {
        pacing: 'brisk enough to feel engaging, but never frantic',
        conflict_style:
          'clues are solved through conversation, memory, and shared effort',
        sensory_motifs: ['kitchen light', 'padded footsteps', 'sleepy pets'],
        ending_style: 'finish with everyone gathered and content',
      },
      sort_order: 0,
    },
  ],
} as const

const allSampleToneCatalogEntries = Object.values(
  sampleToneCatalogByGenre,
).flat()

function buildJsonResponse(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response
}

function resolveRequestUrl(input: RequestInfo | URL) {
  if (typeof input === 'string') {
    return input
  }

  if (input instanceof URL) {
    return input.toString()
  }

  return input.url
}

function buildUiActionEvent(body: Record<string, unknown>) {
  return {
    id: `ui-event-${String(body.action ?? 'unknown')}`,
    session_id: 'moonlit-harbor',
    sequence_number: 8,
    actor: {
      actor_type: 'user',
      actor_id: 'local-user',
    },
    event_type: 'ui.action.recorded',
    stage: body.stage ?? null,
    summary: `Recorded UI action: ${String(body.action ?? 'unknown')}.`,
    payload: {
      schema_version: 1,
      action: body.action,
      control_id: body.control_id ?? null,
      value_summary: body.value_summary ?? null,
      origin: body.origin ?? 'workspace',
    },
    created_at: '2026-04-01T03:04:00Z',
  }
}

function buildContextUpdateResponse(body: Record<string, unknown>) {
  const detail =
    typeof body.values === 'object' &&
    body.values !== null &&
    'detail' in body.values &&
    typeof body.values.detail === 'string'
      ? body.values.detail
      : ''

  return {
    snapshot: {
      ...sampleSnapshot,
      updated_at: '2026-04-01T03:05:00Z',
      stage_states: sampleSnapshot.stage_states.map((stageState) =>
        stageState.stage === body.stage
          ? {
              ...stageState,
              detail,
              last_event_summary:
                'Updated beat sheet notes from the workspace.',
              last_event_type: 'content.user_edit.recorded',
              last_event_at: '2026-04-01T03:05:00Z',
            }
          : stageState,
      ),
      agent_context_summary: `Session title: Lanterns Over Juniper Lake\nCurrent beat sheet detail: ${detail}`,
    },
    event: {
      id: 'context-update-event',
      session_id: 'moonlit-harbor',
      sequence_number: 9,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'content.user_edit.recorded',
      stage: body.stage ?? null,
      summary: 'Saved user edit for beat sheet.',
      payload: {
        schema_version: 1,
        target_kind: 'beat_sheet',
        changed_fields: ['detail'],
        source: body.origin ?? 'workspace',
        field_values: {
          detail,
          control_id: body.control_id ?? null,
        },
        summary_text: 'Updated beat sheet notes from the workspace.',
      },
      created_at: '2026-04-01T03:05:00Z',
    },
  }
}

function buildGenreSelectionResponse(body: Record<string, unknown>) {
  const requestedGenre =
    sampleGenreCatalog.find((genre) => genre.id === body.genre_id) ??
    sampleGenreCatalog.find((genre) => genre.slug === body.genre_slug) ??
    sampleGenreCatalog.find((genre) => genre.label === body.genre_label) ??
    sampleGenreCatalog[0]

  return {
    snapshot: {
      ...sampleSnapshot,
      current_stage: 'tone',
      resume_stage: 'tone',
      furthest_completed_stage: 'genre',
      overall_status: 'in_progress',
      updated_at: '2026-04-01T05:16:00Z',
      selected_genre: {
        id: requestedGenre.id,
        slug: requestedGenre.slug,
        label: requestedGenre.label,
      },
      selected_tone_profile: null,
      progress: {
        total_stages: 10,
        completed_stages: 1,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => {
        if (index === 0) {
          return {
            ...stageState,
            status: 'completed',
            detail: `Selected genre: ${requestedGenre.label}. Tone choices filter from this lane next.`,
            last_event_summary: `Selected genre: ${requestedGenre.label}.`,
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:16:00Z',
          }
        }

        if (index === 1) {
          return {
            ...stageState,
            status: 'draft',
            detail: null,
            last_event_summary: null,
            last_event_type: null,
            last_event_at: null,
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    },
    event: {
      id: 'genre-selection-event',
      session_id: 'moonlit-harbor',
      sequence_number: 10,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'genre',
      summary: `Selected genre: ${requestedGenre.label}.`,
      payload: {
        schema_version: 1,
        selection_kind: 'genre',
        selection_id: requestedGenre.id,
        slug: requestedGenre.slug,
        label: requestedGenre.label,
        accepted: true,
        source: body.origin ?? 'workspace',
      },
      created_at: '2026-04-01T05:16:00Z',
    },
  }
}

function buildToneSelectionResponse(body: Record<string, unknown>) {
  const requestedTone =
    allSampleToneCatalogEntries.find(
      (tone) => tone.id === body.tone_profile_id,
    ) ??
    allSampleToneCatalogEntries.find(
      (tone) => tone.slug === body.tone_profile_slug,
    ) ??
    allSampleToneCatalogEntries.find(
      (tone) => tone.label === body.tone_profile_label,
    ) ??
    sampleToneCatalogByGenre['quest-fantasy'][0]
  const requestedGenre =
    sampleGenreCatalog.find((genre) => genre.id === requestedTone.genre_id) ??
    sampleGenreCatalog[0]

  return {
    snapshot: {
      ...sampleSnapshot,
      current_stage: 'brief',
      resume_stage: 'brief',
      furthest_completed_stage: 'tone',
      overall_status: 'in_progress',
      updated_at: '2026-04-01T05:17:00Z',
      selected_genre: {
        id: requestedGenre.id,
        slug: requestedGenre.slug,
        label: requestedGenre.label,
      },
      selected_tone_profile: {
        id: requestedTone.id,
        slug: requestedTone.slug,
        label: requestedTone.label,
      },
      story_brief: null,
      pitch_batches: [],
      selected_pitch: null,
      selected_story_setup: null,
      progress: {
        total_stages: 10,
        completed_stages: 2,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => {
        if (index === 0) {
          return {
            ...stageState,
            status: 'completed',
            detail: `Selected genre: ${requestedGenre.label}. Tone choices filter from this lane next.`,
            last_event_summary: `Selected genre: ${requestedGenre.label}.`,
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:16:00Z',
          }
        }

        if (index === 1) {
          return {
            ...stageState,
            status: 'completed',
            detail: `Selected tone: ${requestedTone.label}. The story brief will inherit this bedtime texture.`,
            last_event_summary: `Selected tone profile: ${requestedTone.label}.`,
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:17:00Z',
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    },
    event: {
      id: 'tone-selection-event',
      session_id: 'moonlit-harbor',
      sequence_number: 11,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'tone',
      summary: `Selected tone profile: ${requestedTone.label}.`,
      payload: {
        schema_version: 1,
        selection_kind: 'tone_profile',
        selection_id: requestedTone.id,
        slug: requestedTone.slug,
        label: requestedTone.label,
        accepted: true,
        source: body.origin ?? 'workspace',
      },
      created_at: '2026-04-01T05:17:00Z',
    },
  }
}

function readStoryBriefText(body: Record<string, unknown>, key: string) {
  const value = body[key]
  return typeof value === 'string' && value.trim().length > 0
    ? value.trim()
    : null
}

function readNormalizedPreferenceList(
  body: Record<string, unknown>,
  key: string,
): string[] {
  const normalizedPreferences =
    typeof body.normalized_preferences === 'object' &&
    body.normalized_preferences !== null
      ? (body.normalized_preferences as Record<string, unknown>)
      : null
  const value = normalizedPreferences?.[key]

  return Array.isArray(value)
    ? value.filter((item): item is string => typeof item === 'string')
    : []
}

function readNormalizedPreferenceText(
  body: Record<string, unknown>,
  key: string,
) {
  const normalizedPreferences =
    typeof body.normalized_preferences === 'object' &&
    body.normalized_preferences !== null
      ? (body.normalized_preferences as Record<string, unknown>)
      : null
  const value = normalizedPreferences?.[key]

  return typeof value === 'string' && value.trim().length > 0
    ? value.trim()
    : null
}

function truncateStoryBriefText(value: string, limit = 160) {
  if (value.length <= limit) {
    return value
  }

  return `${value.slice(0, limit - 3).trimEnd()}...`
}

function buildStoryBriefRawText(body: Record<string, unknown>) {
  const storyIdea =
    readStoryBriefText(body, 'story_idea') ??
    readStoryBriefText(body, 'raw_brief')

  if (storyIdea == null) {
    return null
  }

  const sections = [storyIdea]

  for (const [label, key] of [
    ['Desired themes', 'desired_themes'],
    ['Key images', 'key_images'],
    ['Target audience notes', 'audience_notes'],
    ['Must-have elements', 'must_have_elements'],
  ] as const) {
    const value = readStoryBriefText(body, key)

    if (value != null) {
      sections.push(`${label}: ${value}`)
    }
  }

  return sections.join('\n\n')
}

function buildStoryBriefSaveResponse(body: Record<string, unknown>) {
  const storyIdea =
    readStoryBriefText(body, 'story_idea') ??
    readStoryBriefText(body, 'raw_brief') ??
    'A harbor bedtime story waits here.'
  const desiredThemes = readStoryBriefText(body, 'desired_themes')
  const keyImages = readStoryBriefText(body, 'key_images')
  const audienceNotes = readStoryBriefText(body, 'audience_notes')
  const mustHaveElements = readStoryBriefText(body, 'must_have_elements')
  const rawBrief = buildStoryBriefRawText(body) ?? storyIdea
  const normalizedSummary =
    readStoryBriefText(body, 'normalized_summary') ?? storyIdea
  const normalizedPreferences = {
    protagonist_type:
      readNormalizedPreferenceText(body, 'protagonist_type') ??
      'A child protagonist',
    setting:
      readNormalizedPreferenceText(body, 'setting') ?? 'a moonlit harbor',
    emotional_goal:
      readNormalizedPreferenceText(body, 'emotional_goal') ??
      'a calm return home',
    constraint_notes:
      readNormalizedPreferenceList(body, 'constraint_notes').length > 0
        ? readNormalizedPreferenceList(body, 'constraint_notes')
        : ['End in a clearly restful place.'],
    bedtime_safety_concerns:
      readNormalizedPreferenceList(body, 'bedtime_safety_concerns').length > 0
        ? readNormalizedPreferenceList(body, 'bedtime_safety_concerns')
        : ['Keep any mystery gentle and quickly repaired.'],
    candidate_motifs:
      readNormalizedPreferenceList(body, 'candidate_motifs').length > 0
        ? readNormalizedPreferenceList(body, 'candidate_motifs')
        : ['floating lanterns', 'still water'],
  }
  const planningNotes = readStoryBriefText(body, 'planning_notes')
  const changedFields = [
    'story_idea',
    'desired_themes',
    'key_images',
    'audience_notes',
    'must_have_elements',
  ].filter((field) => readStoryBriefText(body, field) != null)
  if ('normalized_summary' in body) {
    changedFields.push('normalized_summary')
  }
  if ('normalized_preferences' in body) {
    changedFields.push('normalized_preferences')
  }
  const summary = `Saved story brief: ${truncateStoryBriefText(rawBrief)}`

  return {
    snapshot: {
      ...sampleSnapshot,
      current_stage: 'pitches',
      resume_stage: 'pitches',
      furthest_completed_stage: 'brief',
      overall_status: 'in_progress',
      updated_at: '2026-04-01T05:18:00Z',
      story_brief: {
        id: 'brief-2',
        revision_number: 1,
        story_idea: storyIdea,
        desired_themes: desiredThemes,
        key_images: keyImages,
        audience_notes: audienceNotes,
        must_have_elements: mustHaveElements,
        raw_brief: rawBrief,
        normalized_summary: normalizedSummary,
        normalized_preferences: normalizedPreferences,
        planning_notes: planningNotes,
        updated_at: '2026-04-01T05:18:00Z',
      },
      pitch_batches: [],
      selected_pitch: null,
      selected_story_setup: null,
      progress: {
        total_stages: 10,
        completed_stages: 3,
        in_progress_stages: 1,
        needs_regeneration_stages: 0,
      },
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => {
        if (index === 0) {
          return {
            ...stageState,
            status: 'completed',
            detail:
              'Selected genre: Quest Fantasy. Tone choices filter from this lane next.',
            last_event_summary: 'Selected genre: Quest Fantasy.',
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:16:00Z',
          }
        }

        if (index === 1) {
          return {
            ...stageState,
            status: 'completed',
            detail:
              'Selected tone: Hushed Wonder. The story brief will inherit this bedtime texture.',
            last_event_summary: 'Selected tone profile: Hushed Wonder.',
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:17:00Z',
          }
        }

        if (index === 2) {
          return {
            ...stageState,
            status: 'completed',
            detail: summary,
            last_event_summary: summary,
            last_event_type: 'content.user_edit.recorded',
            last_event_at: '2026-04-01T05:18:00Z',
          }
        }

        if (index === 3) {
          return {
            ...stageState,
            status: 'in_progress',
            detail: 'The saved bedtime brief is ready for pitch generation.',
            last_event_summary: null,
            last_event_type: null,
            last_event_at: null,
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    },
    event: {
      id: 'story-brief-save-event',
      session_id: 'moonlit-harbor',
      sequence_number: 12,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'content.user_edit.recorded',
      stage: 'brief',
      summary,
      payload: {
        schema_version: 1,
        target_kind: 'story_brief',
        changed_fields: changedFields,
        source: body.origin ?? 'workspace',
        field_values: {
          story_idea: storyIdea,
          desired_themes: desiredThemes,
          key_images: keyImages,
          audience_notes: audienceNotes,
          must_have_elements: mustHaveElements,
          normalized_summary: normalizedSummary,
          normalized_preferences: normalizedPreferences,
        },
        summary_text: summary,
      },
      created_at: '2026-04-01T05:18:00Z',
    },
  }
}

function buildPitchGenerationResponse(
  body: Record<string, unknown>,
): SessionPitchGenerationResponse {
  const candidateCount =
    typeof body.candidate_count === 'number' ? body.candidate_count : 4
  const guidance =
    typeof body.guidance === 'string' && body.guidance.trim().length > 0
      ? body.guidance.trim()
      : null
  const generatedAt = '2026-04-01T05:19:00Z'
  const generationKey = 'batch-2'
  const generatedPitches = Array.from({ length: candidateCount }).map(
    (_, index) => {
      const pitchNumber = index + 1
      const titleOptions = [
        'The Juniper Lake Promise',
        'The Last Lantern Question',
        'Moonpost Harbor Map',
        'The Quiet Dock Song',
        'One More Lantern Errand',
      ]
      const title =
        titleOptions[index] ?? `Pitch Option ${pitchNumber.toString()}`

      return {
        id: `pitch-generated-${pitchNumber}`,
        generation_key: generationKey,
        pitch_index: pitchNumber,
        generation_kind: 'alternatives',
        source_pitch_id: null,
        source_pitch_title: null,
        refinement_instructions: null,
        selection_rationale: null,
        title,
        hook: `Pitch ${pitchNumber} follows the lantern trail through the harbor with a distinct bedtime-story engine.`,
        central_conflict: `Pitch ${pitchNumber} asks the child and otter to resolve a different soft nighttime problem before the harbor can settle.`,
        why_it_fits: guidance
          ? `This option honors the guidance: ${guidance}.`
          : 'This option fits the selected genre, tone, and harbor brief with gentle wonder and a restful landing.',
        logline: `Pitch ${pitchNumber} follows the lantern trail through the harbor with a distinct bedtime-story engine.`,
        summary: `Pitch ${pitchNumber} asks the child and otter to resolve a different soft nighttime problem before the harbor can settle.`,
        bedtime_notes: guidance
          ? `This option honors the guidance: ${guidance}.`
          : 'This option fits the selected genre, tone, and harbor brief with gentle wonder and a restful landing.',
        is_selected: false,
        accepted_at: null,
        created_at: generatedAt,
        updated_at: generatedAt,
      }
    },
  )

  return {
    snapshot: {
      ...sampleSnapshot,
      current_stage: 'pitches',
      resume_stage: 'pitches',
      furthest_completed_stage: 'brief',
      overall_status: 'in_progress',
      updated_at: generatedAt,
      selected_pitch:
        body.preserve_selected_pitch === true
          ? sampleSnapshot.selected_pitch
          : null,
      pitch_batches: [
        {
          generation_key: generationKey,
          candidate_count: candidateCount,
          generation_kind: 'alternatives',
          guidance,
          source_pitch_id: null,
          source_pitch_title: null,
          source_generation_key: null,
          refinement_instructions: null,
          created_at: generatedAt,
          pitches: generatedPitches,
        },
        ...(sampleSnapshot.pitch_batches ?? []),
      ],
      progress: {
        total_stages: 10,
        completed_stages: 3,
        in_progress_stages: 1,
        needs_regeneration_stages: 0,
      },
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => {
        if (index <= 2) {
          return {
            ...stageState,
            status: 'completed',
          }
        }

        if (index === 3) {
          return {
            ...stageState,
            status: 'in_progress',
            detail: `Generated ${candidateCount} pitch options. Select one to continue.`,
            last_event_summary: 'Recorded AI output for pitch_batch.',
            last_event_type: 'ai.output.recorded',
            last_event_at: generatedAt,
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    },
    event: {
      id: 'pitch-generation-event',
      session_id: 'moonlit-harbor',
      sequence_number: 13,
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      event_type: 'ai.output.recorded',
      stage: 'pitches',
      summary: 'Recorded AI output for pitch_batch.',
      payload: {
        schema_version: 1,
        output_kind: 'pitch_batch',
        generation_key: generationKey,
        candidate_count: candidateCount,
        model_id: 'gemini-3.1-pro',
        summary: `Generated pitches: ${generatedPitches
          .slice(0, 3)
          .map((pitch) => pitch.title)
          .join(', ')}.`,
      },
      created_at: generatedAt,
    },
  }
}

function buildPitchSelectionResponse(
  body: Record<string, unknown>,
): SessionPitchGenerationResponse {
  const selectedPitchId =
    typeof body.pitch_id === 'string' ? body.pitch_id : 'pitch-generated-1'
  const baseGeneration = buildPitchGenerationResponse({
    candidate_count: 4,
    preserve_selected_pitch: false,
  })
  const selectedPitch =
    baseGeneration.snapshot.pitch_batches?.[0]?.pitches.find(
      (pitch) => pitch.id === selectedPitchId,
    ) ?? baseGeneration.snapshot.pitch_batches?.[0]?.pitches[0]

  return {
    snapshot: {
      ...baseGeneration.snapshot,
      current_stage: 'characters',
      resume_stage: 'characters',
      furthest_completed_stage: 'pitches',
      selected_pitch:
        selectedPitch != null
          ? {
              ...selectedPitch,
              is_selected: true,
              accepted_at: '2026-04-01T05:20:00Z',
              updated_at: '2026-04-01T05:20:00Z',
            }
          : null,
      progress: {
        total_stages: 10,
        completed_stages: 4,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: baseGeneration.snapshot.stage_states.map(
        (stageState, index) => {
          if (index === 3) {
            return {
              ...stageState,
              status: 'completed',
              detail: `Selected pitch: ${selectedPitch?.title}. ${selectedPitch?.logline}`,
              last_event_summary: `Selected pitch: ${selectedPitch?.title}.`,
              last_event_type: 'selection.recorded',
              last_event_at: '2026-04-01T05:20:00Z',
            }
          }

          if (index === 4) {
            return {
              ...stageState,
              status: 'draft',
              detail: null,
              last_event_summary: null,
              last_event_type: null,
              last_event_at: null,
            }
          }

          return stageState
        },
      ),
    },
    event: {
      id: 'pitch-selection-event',
      session_id: 'moonlit-harbor',
      sequence_number: 14,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'pitches',
      summary: `Selected pitch: ${selectedPitch?.title}.`,
      payload: {
        schema_version: 1,
        selection_kind: 'pitch',
        selection_id: selectedPitch?.id,
        label: selectedPitch?.title,
        accepted: true,
        source: body.origin ?? 'workspace',
      },
      created_at: '2026-04-01T05:20:00Z',
    },
  }
}

function buildPitchRefinementResponse(
  body: Record<string, unknown>,
): SessionPitchGenerationResponse {
  const instructions =
    typeof body.instructions === 'string' && body.instructions.trim().length > 0
      ? body.instructions.trim()
      : 'Make it gentler while keeping the harbor bedtime feel.'
  const baseGeneration = buildPitchGenerationResponse({
    candidate_count: 4,
    preserve_selected_pitch: true,
  })
  const fallbackPitches =
    sampleSnapshot.selected_pitch != null ? [sampleSnapshot.selected_pitch] : []
  const allPitches =
    baseGeneration.snapshot.pitch_batches?.flatMap((batch) => batch.pitches ?? []) ??
    fallbackPitches
  const sourcePitchId =
    typeof body.pitch_id === 'string'
      ? body.pitch_id
      : (sampleSnapshot.selected_pitch?.id ?? allPitches[0]?.id)
  const sourcePitch =
    allPitches.find((pitch) => pitch.id === sourcePitchId) ??
    sampleSnapshot.selected_pitch ??
    allPitches[0]
  const refinedAt = '2026-04-01T05:21:00Z'
  const refinedPitch = {
    id: 'pitch-refined-1',
    generation_key: 'batch-refined-1',
    pitch_index: 1,
    generation_kind: 'refinement',
    source_pitch_id: sourcePitch?.id ?? null,
    source_pitch_title: sourcePitch?.title ?? null,
    refinement_instructions: instructions,
    selection_rationale: `Refined from ${sourcePitch?.title ?? 'the selected pitch'}. ${instructions}`,
    title: `${sourcePitch?.title ?? 'Lantern Harbor Promise'}: Siblings`,
    hook: `${
      sourcePitch?.hook ??
      'A child follows lanterns across the harbor before bed.'
    } This revision keeps the same harbor lane while making the story about siblings who help each other settle down.`,
    central_conflict:
      'Two siblings must guide the last lanterns home while helping each other calm a final bedtime worry.',
    why_it_fits: `This refinement preserves the bedtime-safe harbor mystery while applying the request: ${instructions}.`,
    logline: `${
      sourcePitch?.hook ??
      'A child follows lanterns across the harbor before bed.'
    } This revision keeps the same harbor lane while making the story about siblings who help each other settle down.`,
    summary:
      'Two siblings must guide the last lanterns home while helping each other calm a final bedtime worry.',
    bedtime_notes: `This refinement preserves the bedtime-safe harbor mystery while applying the request: ${instructions}.`,
    is_selected: true,
    accepted_at: refinedAt,
    created_at: refinedAt,
    updated_at: refinedAt,
  }

  return {
    snapshot: {
      ...baseGeneration.snapshot,
      current_stage: 'characters',
      resume_stage: 'characters',
      furthest_completed_stage: 'pitches',
      updated_at: refinedAt,
      selected_pitch: refinedPitch,
      pitch_batches: [
        {
          generation_key: refinedPitch.generation_key,
          candidate_count: 1,
          generation_kind: 'refinement',
          guidance: instructions,
          source_pitch_id: sourcePitch?.id ?? null,
          source_pitch_title: sourcePitch?.title ?? null,
          source_generation_key: sourcePitch?.generation_key ?? null,
          refinement_instructions: instructions,
          created_at: refinedAt,
          pitches: [refinedPitch],
        },
        ...(baseGeneration.snapshot.pitch_batches ?? []),
      ],
      progress: {
        total_stages: 10,
        completed_stages: 4,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: baseGeneration.snapshot.stage_states.map(
        (stageState, index) => {
          if (index === 3) {
            return {
              ...stageState,
              status: 'completed',
              detail: `Selected pitch: ${refinedPitch.title}. ${refinedPitch.selection_rationale}`,
              last_event_summary: `Selected pitch: ${refinedPitch.title}.`,
              last_event_type: 'selection.recorded',
              last_event_at: refinedAt,
            }
          }

          if (index === 4) {
            return {
              ...stageState,
              status: 'draft',
              detail: null,
              last_event_summary: null,
              last_event_type: null,
              last_event_at: null,
            }
          }

          return stageState
        },
      ),
    },
    event: {
      id: 'pitch-refinement-event',
      session_id: 'moonlit-harbor',
      sequence_number: 15,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'pitches',
      summary: `Selected pitch: ${refinedPitch.title}.`,
      payload: {
        schema_version: 1,
        selection_kind: 'pitch',
        selection_id: refinedPitch.id,
        label: refinedPitch.title,
        accepted: true,
        source: body.origin ?? 'workspace',
        rationale: refinedPitch.selection_rationale,
      },
      created_at: refinedAt,
    },
  }
}

function buildCharacterGenerationResponse(
  body: Record<string, unknown>,
): SessionCharacterSheetGenerationResponse {
  const candidateCount =
    typeof body.candidate_count === 'number' ? body.candidate_count : 3
  const guidance =
    typeof body.guidance === 'string' && body.guidance.trim().length > 0
      ? body.guidance.trim()
      : null
  const generatedAt = '2026-04-01T05:22:00Z'
  const generationKey = 'character-batch-1'
  const generatedCharacterSheets = Array.from({ length: candidateCount }).map(
    (_, index) => {
      const sheetNumber = index + 1
      const titles = [
        'Juniper Keeper Cast',
        'Harbor Listener Cast',
        'Moonpath Guide Cast',
        'Lantern Sibling Cast',
        'Stillwater Singer Cast',
      ]
      const protagonistNames = ['Mira', 'Pip', 'Tavi', 'Junie', 'Sage']
      const title = titles[index] ?? `Character Sheet ${sheetNumber.toString()}`
      const protagonistName =
        protagonistNames[index] ?? `Lead ${sheetNumber.toString()}`

      return {
        id: `character-generated-${sheetNumber}`,
        revision_number: 20 + sheetNumber,
        generation_key: generationKey,
        candidate_index: sheetNumber,
        generation_kind: 'generated',
        source_pitch_id: sampleSnapshot.selected_pitch?.id ?? null,
        source_pitch_title: sampleSnapshot.selected_pitch?.title ?? null,
        source_character_sheet_id: null,
        source_character_sheet_title: null,
        refinement_instructions: null,
        selection_rationale: null,
        title,
        protagonist_name: protagonistName,
        summary: `${title} keeps the harbor pitch bedtime-safe with a distinct protagonist flaw and a compact support dynamic.`,
        story_function: guidance
          ? `This cast applies the guidance: ${guidance}.`
          : 'This cast makes later beats easy to structure around emotional repair and clear visual motifs.',
        protagonist: {
          name: protagonistName,
          role: 'sleepy lantern-keeper in training',
          goal: 'guide the last harbor lights home before everyone settles',
          flaw: 'tries to solve every worry alone before asking for help',
          comfort_trait: 'counts steady reflections until their breathing slows',
          bedtime_safety_notes:
            'The lead stays emotionally safe because the support cast remains close and calm in every scene.',
          relationships: [
            `Trusts Otis ${sheetNumber} to steady the plan.`,
          ],
          visual_anchors: ['lantern sleeves', 'soft satchel'],
        },
        supporting_cast: [
          {
            name: `Otis ${sheetNumber}`,
            role: 'patient otter guardian',
            goal: 'help the lead slow the pacing when the night feels larger',
            flaw: 'over-explains instead of letting the lead discover the answer',
            comfort_trait: 'grounds scenes with practical rituals',
            bedtime_safety_notes:
              'The guardian keeps each obstacle small, readable, and quickly reassuring.',
            relationships: [`Acts as ${protagonistName}'s calm sounding board.`],
            visual_anchors: ['river coat', 'tidy satchel'],
          },
        ],
        bedtime_notes:
          'Every worry is buffered by visible helpers, named feelings, and a calm return home.',
        bedtime_safety_notes:
          'Every worry is buffered by visible helpers, named feelings, and a calm return home.',
        visual_motifs: ['lantern glow', 'moonlit docks', `quiet route ${sheetNumber}`],
        is_selected: false,
        accepted_at: null,
        created_at: generatedAt,
        updated_at: generatedAt,
      }
    },
  )
  const baseSelection = buildPitchSelectionResponse({
    pitch_id: sampleSnapshot.selected_pitch?.id ?? 'pitch-1',
  })

  return {
    snapshot: {
      ...baseSelection.snapshot,
      current_stage: 'characters',
      resume_stage: 'characters',
      furthest_completed_stage: 'pitches',
      updated_at: generatedAt,
      character_sheet_batches: [
        {
          generation_key: generationKey,
          candidate_count: candidateCount,
          generation_kind: 'generated',
          guidance,
          source_pitch_id: sampleSnapshot.selected_pitch?.id ?? null,
          source_pitch_title: sampleSnapshot.selected_pitch?.title ?? null,
          source_character_sheet_id: null,
          source_character_sheet_title: null,
          refinement_instructions: null,
          created_at: generatedAt,
          character_sheets: generatedCharacterSheets,
        },
      ],
      selected_character_sheet:
        body.preserve_selected_character_sheet === true
          ? sampleSnapshot.selected_character_sheet
          : null,
      progress: {
        total_stages: 10,
        completed_stages: 4,
        in_progress_stages: 1,
        needs_regeneration_stages: 0,
      },
      stage_states: baseSelection.snapshot.stage_states.map((stageState, index) => {
        if (index <= 3) {
          return {
            ...stageState,
            status: 'completed',
          }
        }

        if (index === 4) {
          return {
            ...stageState,
            status: 'in_progress',
            detail: `Generated ${candidateCount} character options. Select one to continue.`,
            last_event_summary: 'Recorded AI output for character_sheet.',
            last_event_type: 'ai.output.recorded',
            last_event_at: generatedAt,
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    },
    event: {
      id: 'character-generation-event',
      session_id: 'moonlit-harbor',
      sequence_number: 16,
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      event_type: 'ai.output.recorded',
      stage: 'characters',
      summary: 'Recorded AI output for character_sheet.',
      payload: {
        schema_version: 1,
        output_kind: 'character_sheet',
        generation_key: generationKey,
        candidate_count: candidateCount,
        model_id: 'gemini-3.1-pro',
        summary: `Generated character sheets: ${generatedCharacterSheets
          .slice(0, 3)
          .map((characterSheet) => characterSheet.title)
          .join(', ')}.`,
      },
      created_at: generatedAt,
    },
  }
}

function buildCharacterSelectionResponse(
  body: Record<string, unknown>,
): SessionCharacterSheetGenerationResponse {
  const baseGeneration = buildCharacterGenerationResponse({
    candidate_count: 3,
    preserve_selected_character_sheet: false,
  })
  const selectedCharacterSheetId =
    typeof body.character_sheet_id === 'string'
      ? body.character_sheet_id
      : 'character-generated-1'
  const selectedCharacterSheet =
    baseGeneration.snapshot.character_sheet_batches?.[0]?.character_sheets.find(
      (characterSheet) => characterSheet.id === selectedCharacterSheetId,
    ) ?? baseGeneration.snapshot.character_sheet_batches?.[0]?.character_sheets[0]
  const selectedAt = '2026-04-01T05:23:00Z'

  return {
    snapshot: {
      ...baseGeneration.snapshot,
      current_stage: 'beats',
      resume_stage: 'beats',
      furthest_completed_stage: 'characters',
      updated_at: selectedAt,
      selected_character_sheet:
        selectedCharacterSheet != null
          ? {
              ...selectedCharacterSheet,
              is_selected: true,
              accepted_at: selectedAt,
              updated_at: selectedAt,
            }
          : null,
      progress: {
        total_stages: 10,
        completed_stages: 5,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: baseGeneration.snapshot.stage_states.map((stageState, index) => {
        if (index === 4) {
          return {
            ...stageState,
            status: 'completed',
            detail: `Selected character sheet: ${selectedCharacterSheet?.title}. Lead character: ${selectedCharacterSheet?.protagonist_name}.`,
            last_event_summary: `Selected character sheet: ${selectedCharacterSheet?.title}.`,
            last_event_type: 'selection.recorded',
            last_event_at: selectedAt,
          }
        }

        if (index === 5) {
          return {
            ...stageState,
            status: 'draft',
            detail: null,
            last_event_summary: null,
            last_event_type: null,
            last_event_at: null,
          }
        }

        return stageState
      }),
    },
    event: {
      id: 'character-selection-event',
      session_id: 'moonlit-harbor',
      sequence_number: 17,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'characters',
      summary: `Selected character sheet: ${selectedCharacterSheet?.title}.`,
      payload: {
        schema_version: 1,
        selection_kind: 'character_sheet',
        selection_id: selectedCharacterSheet?.id,
        label: selectedCharacterSheet?.title,
        accepted: true,
        source: body.origin ?? 'workspace',
      },
      created_at: selectedAt,
    },
  }
}

function buildCharacterRefinementResponse(
  body: Record<string, unknown>,
): SessionCharacterSheetGenerationResponse {
  const instructions =
    typeof body.instructions === 'string' && body.instructions.trim().length > 0
      ? body.instructions.trim()
      : 'Make the cast more sibling-like while keeping the harbor bedtime feel.'
  const baseGeneration = buildCharacterGenerationResponse({
    candidate_count: 3,
    preserve_selected_character_sheet: true,
  })
  const fallbackCharacterSheets =
    sampleSnapshot.selected_character_sheet != null
      ? [sampleSnapshot.selected_character_sheet]
      : []
  const allCharacterSheets =
    baseGeneration.snapshot.character_sheet_batches?.flatMap(
      (batch) => batch.character_sheets ?? [],
    ) ?? fallbackCharacterSheets
  const sourceCharacterSheetId =
    typeof body.character_sheet_id === 'string'
      ? body.character_sheet_id
      : (sampleSnapshot.selected_character_sheet?.id ?? allCharacterSheets[0]?.id)
  const sourceCharacterSheet =
    allCharacterSheets.find(
      (characterSheet) => characterSheet.id === sourceCharacterSheetId,
    ) ??
    sampleSnapshot.selected_character_sheet ??
    allCharacterSheets[0]
  const refinedAt = '2026-04-01T05:24:00Z'
  const refinedCharacterSheet = {
    id: 'character-refined-1',
    revision_number: 30,
    generation_key: 'character-batch-refined-1',
    candidate_index: 1,
    generation_kind: 'refinement',
    source_pitch_id: sampleSnapshot.selected_pitch?.id ?? null,
    source_pitch_title: sampleSnapshot.selected_pitch?.title ?? null,
    source_character_sheet_id: sourceCharacterSheet?.id ?? null,
    source_character_sheet_title: sourceCharacterSheet?.title ?? null,
    refinement_instructions: instructions,
    selection_rationale: `Refined from ${sourceCharacterSheet?.title ?? 'the selected character sheet'}. ${instructions}`,
    title: `${sourceCharacterSheet?.title ?? 'Juniper Keeper Cast'}: Revised`,
    protagonist_name: sourceCharacterSheet?.protagonist_name ?? 'Mira',
    summary: `This revision keeps ${sourceCharacterSheet?.title ?? 'the current cast'} recognizable while applying: ${instructions}`,
    story_function:
      'The refined cast preserves the harbor bedtime lane while tightening the requested relationship change.',
    protagonist: {
      ...(sourceCharacterSheet?.protagonist ?? {
        name: 'Mira',
        role: 'sleepy lantern-keeper in training',
        goal: 'guide the last harbor lights home before everyone settles',
        flaw: 'tries to solve every worry alone before asking for help',
        comfort_trait: 'counts steady reflections until their breathing slows',
        relationships: [],
        visual_anchors: [],
      }),
      bedtime_safety_notes:
        'The revision keeps the lead emotionally safe because the support cast stays visibly close and calm.',
    },
    supporting_cast:
      sourceCharacterSheet?.supporting_cast ?? [],
    bedtime_notes:
      'The revision keeps all emotional pressure buffered by companionship, clear naming, and a visibly safe return to calm.',
    bedtime_safety_notes:
      'The revision keeps all emotional pressure buffered by companionship, clear naming, and a visibly safe return to calm.',
    visual_motifs: sourceCharacterSheet?.visual_motifs ?? [
      'lantern glow',
      'moonlit docks',
      'soft satchel',
    ],
    is_selected: true,
    accepted_at: refinedAt,
    created_at: refinedAt,
    updated_at: refinedAt,
  }

  return {
    snapshot: {
      ...baseGeneration.snapshot,
      current_stage: 'beats',
      resume_stage: 'beats',
      furthest_completed_stage: 'characters',
      updated_at: refinedAt,
      selected_character_sheet: refinedCharacterSheet,
      character_sheet_batches: [
        {
          generation_key: refinedCharacterSheet.generation_key,
          candidate_count: 1,
          generation_kind: 'refinement',
          guidance: instructions,
          source_pitch_id: sampleSnapshot.selected_pitch?.id ?? null,
          source_pitch_title: sampleSnapshot.selected_pitch?.title ?? null,
          source_character_sheet_id: sourceCharacterSheet?.id ?? null,
          source_character_sheet_title: sourceCharacterSheet?.title ?? null,
          refinement_instructions: instructions,
          created_at: refinedAt,
          character_sheets: [refinedCharacterSheet],
        },
        ...(baseGeneration.snapshot.character_sheet_batches ?? []),
      ],
      progress: {
        total_stages: 10,
        completed_stages: 5,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: baseGeneration.snapshot.stage_states.map((stageState, index) => {
        if (index === 4) {
          return {
            ...stageState,
            status: 'completed',
            detail: `Selected character sheet: ${refinedCharacterSheet.title}. Lead character: ${refinedCharacterSheet.protagonist_name}.`,
            last_event_summary: `Selected character sheet: ${refinedCharacterSheet.title}.`,
            last_event_type: 'selection.recorded',
            last_event_at: refinedAt,
          }
        }

        if (index === 5) {
          return {
            ...stageState,
            status: 'draft',
            detail: null,
            last_event_summary: null,
            last_event_type: null,
            last_event_at: null,
          }
        }

        return stageState
      }),
    },
    event: {
      id: 'character-refinement-event',
      session_id: 'moonlit-harbor',
      sequence_number: 18,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'characters',
      summary: `Selected character sheet: ${refinedCharacterSheet.title}.`,
      payload: {
        schema_version: 1,
        selection_kind: 'character_sheet',
        selection_id: refinedCharacterSheet.id,
        label: refinedCharacterSheet.title,
        accepted: true,
        source: body.origin ?? 'workspace',
        rationale: refinedCharacterSheet.selection_rationale,
      },
      created_at: refinedAt,
    },
  }
}

function buildCommandChatIntentResponse(requestBody: Record<string, unknown>) {
  const explicitCommand =
    typeof requestBody.explicit_command === 'object' &&
    requestBody.explicit_command !== null
      ? (requestBody.explicit_command as Record<string, unknown>)
      : null
  const proposedActions =
    explicitCommand != null &&
    typeof explicitCommand.proposed_actions === 'object' &&
    explicitCommand.proposed_actions !== null
      ? explicitCommand.proposed_actions
      : {
          schema_version: 1,
          actions: [],
        }
  const actions =
    typeof proposedActions === 'object' &&
    proposedActions !== null &&
    Array.isArray((proposedActions as { actions?: unknown[] }).actions)
      ? ((proposedActions as { actions: unknown[] }).actions as Array<
          Record<string, unknown>
        >)
      : []
  const commandId =
    explicitCommand != null && typeof explicitCommand.command_id === 'string'
      ? explicitCommand.command_id
      : null

  if (commandId === 'summarize_plan') {
    return {
      schema_version: 1,
      status: 'parsed',
      needs_clarification: false,
      assistant_response:
        'Current focus is beat sheet. Plan so far: Quest Fantasy, Hushed Wonder, pitch "Lanterns Over Juniper Lake", ~12 minutes, 4 chapters, 1500 words.',
      clarification_reason: null,
      proposed_actions: {
        schema_version: 1,
        actions: [],
      },
      policy_evaluation: null,
    }
  }

  return {
    schema_version: 1,
    status: 'parsed',
    needs_clarification: false,
    assistant_response:
      commandId === 'next_stage'
        ? 'I can move the workspace to Story setup.'
        : 'I can translate that command into the story workspace.',
    clarification_reason: null,
    proposed_actions: proposedActions,
    policy_evaluation: {
      schema_version: 1,
      session_id: 'moonlit-harbor',
      evaluated_actions: actions.map((action, actionIndex) => ({
        action_index: actionIndex,
        action_type: action.action_type,
        target_stage: action.target_stage,
        decision: 'accepted',
        summary:
          action.action_type === 'navigate_to_stage'
            ? 'Navigation is allowed.'
            : 'Action can be applied.',
        reasons: [],
        side_effects: [],
        prerequisite_action_types: [],
      })),
    },
  }
}

function mockWorkspaceApi(options?: {
  characterGenerationResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  characterSelectionResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  characterRefinementResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  genreCatalog?: unknown
  genreSelectionResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  pitchGenerationResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  pitchSelectionResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  pitchRefinementResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  storyBriefSaveResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  toneCatalogByGenre?: Record<string, unknown>
  toneSelectionResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
  history?: unknown
  hydration?: unknown
  hydrationStatus?: number
  chatIntentResponse?:
    | unknown
    | ((requestBody: Record<string, unknown>) => unknown)
}) {
  const history = options?.history ?? sampleHistory
  const genreCatalog = options?.genreCatalog ?? sampleGenreCatalog
  const toneCatalogByGenre: Record<string, unknown> =
    options?.toneCatalogByGenre ??
    (sampleToneCatalogByGenre as unknown as Record<string, unknown>)
  const hydration =
    options?.hydration ??
    ({
      ...sampleHydration,
      recent_history: history,
    } as const)
  const hydrationStatus = options?.hydrationStatus ?? 200
  const chatIntentRequests: Record<string, unknown>[] = []
  const characterGenerationRequests: Record<string, unknown>[] = []
  const characterRefinementRequests: Record<string, unknown>[] = []
  const characterSelectionRequests: Record<string, unknown>[] = []
  const genreSelectionRequests: Record<string, unknown>[] = []
  const pitchGenerationRequests: Record<string, unknown>[] = []
  const pitchRefinementRequests: Record<string, unknown>[] = []
  const pitchSelectionRequests: Record<string, unknown>[] = []
  const storyBriefSaveRequests: Record<string, unknown>[] = []
  const toneSelectionRequests: Record<string, unknown>[] = []
  const genreSelectionResponse =
    options?.genreSelectionResponse ?? buildGenreSelectionResponse
  const pitchGenerationResponse =
    options?.pitchGenerationResponse ?? buildPitchGenerationResponse
  const pitchSelectionResponse =
    options?.pitchSelectionResponse ?? buildPitchSelectionResponse
  const pitchRefinementResponse =
    options?.pitchRefinementResponse ?? buildPitchRefinementResponse
  const storyBriefSaveResponse =
    options?.storyBriefSaveResponse ?? buildStoryBriefSaveResponse
  const toneSelectionResponse =
    options?.toneSelectionResponse ?? buildToneSelectionResponse
  const chatIntentResponse = options?.chatIntentResponse ?? {
    schema_version: 1,
    status: 'parsed',
    needs_clarification: false,
    assistant_response:
      'I can open the audio stage so you can review narration settings.',
    clarification_reason: null,
    proposed_actions: {
      schema_version: 1,
      actions: [
        {
          schema_version: 1,
          action_type: 'navigate_to_stage',
          target_stage: 'audio',
          confidence: 0.96,
          rationale: 'The user asked to move to audio controls.',
          requires_confirmation: false,
          extracted_values: {},
        },
      ],
    },
    policy_evaluation: {
      schema_version: 1,
      session_id: 'moonlit-harbor',
      evaluated_actions: [
        {
          action_index: 0,
          action_type: 'navigate_to_stage',
          target_stage: 'audio',
          decision: 'accepted',
          summary: 'Navigation is allowed.',
          reasons: [],
          side_effects: [],
          prerequisite_action_types: [],
        },
      ],
    },
  }
  const characterGenerationResponse =
    options?.characterGenerationResponse ?? buildCharacterGenerationResponse
  const characterSelectionResponse =
    options?.characterSelectionResponse ?? buildCharacterSelectionResponse
  const characterRefinementResponse =
    options?.characterRefinementResponse ?? buildCharacterRefinementResponse

  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = resolveRequestUrl(input)
      const { pathname } = new URL(url, 'http://localhost')

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/hydrate' &&
        (init?.method == null || init.method === 'GET')
      ) {
        return Promise.resolve(buildJsonResponse(hydrationStatus, hydration))
      }

      if (
        pathname === '/api/v1/catalog/genres' &&
        (init?.method == null || init.method === 'GET')
      ) {
        return Promise.resolve(buildJsonResponse(200, genreCatalog))
      }

      const toneCatalogMatch = pathname.match(
        /^\/api\/v1\/catalog\/genres\/([^/]+)\/tones$/,
      )

      if (
        toneCatalogMatch != null &&
        (init?.method == null || init.method === 'GET')
      ) {
        const genreSlug = decodeURIComponent(toneCatalogMatch[1] ?? '')
        return Promise.resolve(
          buildJsonResponse(200, toneCatalogByGenre[genreSlug] ?? []),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/chat/intents' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}

        chatIntentRequests.push(requestBody)
        const resolvedChatIntentResponse =
          typeof chatIntentResponse === 'function'
            ? chatIntentResponse(requestBody)
            : chatIntentResponse

        return Promise.resolve(
          resolvedChatIntentResponse instanceof Response
            ? resolvedChatIntentResponse
            : buildJsonResponse(200, resolvedChatIntentResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/ui-actions' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}

        return Promise.resolve(
          buildJsonResponse(201, buildUiActionEvent(requestBody)),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/context-updates' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}

        return Promise.resolve(
          buildJsonResponse(200, buildContextUpdateResponse(requestBody)),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/selections/genre' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        genreSelectionRequests.push(requestBody)
        const resolvedGenreSelectionResponse =
          typeof genreSelectionResponse === 'function'
            ? genreSelectionResponse(requestBody)
            : genreSelectionResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedGenreSelectionResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/selections/tone' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        toneSelectionRequests.push(requestBody)
        const resolvedToneSelectionResponse =
          typeof toneSelectionResponse === 'function'
            ? toneSelectionResponse(requestBody)
            : toneSelectionResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedToneSelectionResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/pitches/generate' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        pitchGenerationRequests.push(requestBody)
        const resolvedPitchGenerationResponse =
          typeof pitchGenerationResponse === 'function'
            ? pitchGenerationResponse(requestBody)
            : pitchGenerationResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedPitchGenerationResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/pitches/refine' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        pitchRefinementRequests.push(requestBody)
        const resolvedPitchRefinementResponse =
          typeof pitchRefinementResponse === 'function'
            ? pitchRefinementResponse(requestBody)
            : pitchRefinementResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedPitchRefinementResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/characters/generate' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        characterGenerationRequests.push(requestBody)
        const resolvedCharacterGenerationResponse =
          typeof characterGenerationResponse === 'function'
            ? characterGenerationResponse(requestBody)
            : characterGenerationResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedCharacterGenerationResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/characters/refine' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        characterRefinementRequests.push(requestBody)
        const resolvedCharacterRefinementResponse =
          typeof characterRefinementResponse === 'function'
            ? characterRefinementResponse(requestBody)
            : characterRefinementResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedCharacterRefinementResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/selections/pitch' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        pitchSelectionRequests.push(requestBody)
        const resolvedPitchSelectionResponse =
          typeof pitchSelectionResponse === 'function'
            ? pitchSelectionResponse(requestBody)
            : pitchSelectionResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedPitchSelectionResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/selections/character-sheet' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        characterSelectionRequests.push(requestBody)
        const resolvedCharacterSelectionResponse =
          typeof characterSelectionResponse === 'function'
            ? characterSelectionResponse(requestBody)
            : characterSelectionResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedCharacterSelectionResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/story-brief' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}
        storyBriefSaveRequests.push(requestBody)
        const resolvedStoryBriefSaveResponse =
          typeof storyBriefSaveResponse === 'function'
            ? storyBriefSaveResponse(requestBody)
            : storyBriefSaveResponse

        return Promise.resolve(
          buildJsonResponse(200, resolvedStoryBriefSaveResponse),
        )
      }

      throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${url}`)
    }),
  )

  return {
    chatIntentRequests,
    characterGenerationRequests,
    characterRefinementRequests,
    characterSelectionRequests,
    genreSelectionRequests,
    pitchGenerationRequests,
    pitchRefinementRequests,
    pitchSelectionRequests,
    storyBriefSaveRequests,
    toneSelectionRequests,
  }
}

function renderWorkspaceRoute(
  initialEntry = '/sessions/moonlit-harbor',
) {
  return renderWithAppProviders(
    <MemoryRouter initialEntries={[initialEntry]}>
      <Routes>
        <Route path="/sessions/:sessionId" element={<SessionWorkspacePage />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('SessionWorkspacePage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the session snapshot inside the workspace shell', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Lanterns Over Juniper Lake',
      }),
    ).toBeInTheDocument()
    expect(screen.getByTestId('workspace-route')).toBeInTheDocument()
    expect(
      screen.getByText('Selected genre: Quest Fantasy'),
    ).toBeInTheDocument()
    expect(screen.getByText('Selected tone: Hushed Wonder')).toBeInTheDocument()
    expect(screen.getByText('5 of 10 stages complete')).toBeInTheDocument()
    expect(
      screen.getByRole('navigation', { name: 'Stage navigator' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', {
        level: 2,
        name: 'Refine the Save-the-Cat beats',
      }),
    ).toBeInTheDocument()
    expect(screen.getAllByText('Live feed idle').length).toBeGreaterThan(0)
    expect(screen.getByTestId('live-feed-status')).toHaveTextContent('Idle')
    expect(screen.getByRole('link', { name: 'Return home' })).toHaveAttribute(
      'href',
      '/',
    )
    expect(screen.getByRole('log')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Send message' }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'The current focus is softening the midpoint before composition starts.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText('Midpoint needs one more bedtime-soft pass.').length,
    ).toBeGreaterThan(0)
    expect(
      screen.getByRole('heading', { level: 3, name: 'Workflow component kit' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Choice cards')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Next stage' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Regenerate pitches' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Summarize plan' }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'Slash commands: /next-stage, /regenerate-pitches, /plan',
      ),
    ).toBeInTheDocument()
  })

  it('renders genre cards from the catalog and persists a selected genre', async () => {
    const genreStageSnapshot = {
      ...sampleSnapshot,
      current_stage: 'genre',
      resume_stage: 'genre',
      furthest_completed_stage: null,
      overall_status: 'draft',
      selected_genre: null,
      selected_tone_profile: null,
      progress: {
        total_stages: 10,
        completed_stages: 0,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => ({
        ...stageState,
        status: index === 0 ? 'draft' : 'draft',
        detail: null,
        last_event_summary: null,
        last_event_type: null,
        last_event_at: null,
      })),
    } as const
    const genreStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 1,
      events: [sampleHistory.events[0]],
    } as const

    const { genreSelectionRequests } = mockWorkspaceApi({
      history: genreStageHistory,
      hydration: {
        snapshot: genreStageSnapshot,
        recent_history: genreStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 1,
          history_event_count: 1,
          materialized_through_sequence_number: 1,
        },
      },
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Choose a bedtime genre lane',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 3,
        name: 'Quest Fantasy',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 3,
        name: 'Gentle Mystery',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Tone selection comes next')).toBeInTheDocument()

    const questFantasyCard = screen
      .getByText('Quest Fantasy')
      .closest('article')
    expect(questFantasyCard).not.toBeNull()

    fireEvent.click(
      within(questFantasyCard as HTMLElement).getByRole('button', {
        name: 'Choose genre',
      }),
    )

    expect(
      await screen.findByText('Selected genre: Quest Fantasy'),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Tune the bedtime mood',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Quest Fantasy / Tone pending')).toBeInTheDocument()
    expect(genreSelectionRequests).toEqual([
      {
        genre_id: sampleGenreCatalog[0].id,
        origin: 'workspace',
      },
    ])
  })

  it('renders tone cards from the filtered catalog and persists a selected tone', async () => {
    const toneStageSnapshot = {
      ...sampleSnapshot,
      current_stage: 'tone',
      resume_stage: 'tone',
      furthest_completed_stage: 'genre',
      overall_status: 'in_progress',
      selected_tone_profile: null,
      progress: {
        total_stages: 10,
        completed_stages: 1,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      story_brief: null,
      selected_pitch: null,
      selected_story_setup: null,
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => {
        if (index === 0) {
          return {
            ...stageState,
            status: 'completed',
            detail:
              'Selected genre: Quest Fantasy. Tone choices filter from this lane next.',
            last_event_summary: 'Selected genre: Quest Fantasy.',
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:16:00Z',
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    } as const
    const toneStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 2,
      events: [sampleHistory.events[0], sampleHistory.events[1]],
    } as const

    const { toneSelectionRequests } = mockWorkspaceApi({
      history: toneStageHistory,
      hydration: {
        snapshot: toneStageSnapshot,
        recent_history: toneStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 2,
          history_event_count: 2,
          materialized_through_sequence_number: 2,
        },
      },
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Tune the bedtime mood',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 3,
        name: 'Hushed Wonder',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { level: 3, name: 'Lantern Brave' }),
    ).toBeInTheDocument()
    expect(screen.queryByText('Cozy Sleuthing')).not.toBeInTheDocument()

    const hushedWonderCard = screen
      .getByText('Hushed Wonder')
      .closest('article')
    expect(hushedWonderCard).not.toBeNull()

    fireEvent.click(
      within(hushedWonderCard as HTMLElement).getByRole('button', {
        name: 'Choose tone',
      }),
    )

    expect(
      await screen.findByText('Selected tone: Hushed Wonder'),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Capture the free-form story brief',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText('Quest Fantasy / Hushed Wonder').length,
    ).toBeGreaterThan(0)
    expect(toneSelectionRequests).toEqual([
      {
        tone_profile_id: 'tone-1',
        origin: 'workspace',
      },
    ])
  })

  it('renders the story brief editor and persists a saved brief', async () => {
    const briefStageSnapshot = buildToneSelectionResponse({
      tone_profile_id: 'tone-1',
      origin: 'workspace',
    }).snapshot
    const briefStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 3,
      events: [
        sampleHistory.events[0],
        sampleHistory.events[1],
        sampleHistory.events[2],
      ],
    } as const

    const { storyBriefSaveRequests } = mockWorkspaceApi({
      history: briefStageHistory,
      hydration: {
        snapshot: briefStageSnapshot,
        recent_history: briefStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 3,
          history_event_count: 3,
          materialized_through_sequence_number: 3,
        },
      },
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Capture the free-form story brief',
      }),
    ).toBeInTheDocument()
    expect(await screen.findByLabelText('Story idea')).toBeInTheDocument()
    expect(screen.getByLabelText('Desired themes')).toBeInTheDocument()
    expect(screen.getByLabelText('Key images')).toBeInTheDocument()
    expect(screen.getByLabelText('Target audience notes')).toBeInTheDocument()
    expect(screen.getByLabelText('Must-have elements')).toBeInTheDocument()
    expect(screen.getByLabelText('Normalized summary')).toBeInTheDocument()
    expect(screen.getByLabelText('Protagonist type')).toBeInTheDocument()
    expect(screen.getByLabelText('Setting')).toBeInTheDocument()
    expect(screen.getByLabelText('Emotional goal')).toBeInTheDocument()
    expect(screen.getByLabelText('Constraint notes')).toBeInTheDocument()
    expect(screen.getByLabelText('Bedtime-safety concerns')).toBeInTheDocument()
    expect(screen.getByLabelText('Candidate motifs')).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Story idea'), {
      target: {
        value:
          'A sleepy child follows floating lanterns across a moonlit harbor to help an otter guardian guide them home.',
      },
    })
    fireEvent.change(screen.getByLabelText('Desired themes'), {
      target: {
        value: 'Gentle courage, belonging, and returning home.',
      },
    })
    fireEvent.change(screen.getByLabelText('Key images'), {
      target: {
        value: 'Floating lanterns, still water, and a warm harbor light.',
      },
    })
    fireEvent.change(screen.getByLabelText('Target audience notes'), {
      target: {
        value:
          'For a sensitive five-year-old who likes rescue stories without villains.',
      },
    })
    fireEvent.change(screen.getByLabelText('Must-have elements'), {
      target: {
        value: 'An otter friend and a restful final page.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save brief' }))

    expect(storyBriefSaveRequests).toHaveLength(1)
    expect(storyBriefSaveRequests[0]).toMatchObject({
      story_idea:
        'A sleepy child follows floating lanterns across a moonlit harbor to help an otter guardian guide them home.',
      desired_themes: 'Gentle courage, belonging, and returning home.',
      key_images: 'Floating lanterns, still water, and a warm harbor light.',
      audience_notes:
        'For a sensitive five-year-old who likes rescue stories without villains.',
      must_have_elements: 'An otter friend and a restful final page.',
      raw_brief: null,
      planning_notes: null,
      edit_mode: 'replace',
      origin: 'workspace',
    })
    expect(storyBriefSaveRequests[0]).not.toHaveProperty('normalized_summary')
    expect(storyBriefSaveRequests[0]).not.toHaveProperty(
      'normalized_preferences',
    )
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Review and select story pitches',
      }),
    ).toBeInTheDocument()
    expect(await screen.findByText(/saved story brief:/i)).toBeInTheDocument()
  })

  it('persists manual overrides to the extracted brief interpretation', async () => {
    const baseSnapshot = buildToneSelectionResponse({
      tone_profile_id: 'tone-1',
      origin: 'workspace',
    }).snapshot
    const savedBriefSnapshot = {
      ...baseSnapshot,
      furthest_completed_stage: 'brief',
      story_brief: {
        ...sampleSnapshot.story_brief,
      },
      stage_states: baseSnapshot.stage_states.map((stageState, index) => {
        if (index === 2) {
          return {
            ...stageState,
            status: 'completed',
            detail: 'Saved story brief: A harbor bedtime quest.',
            last_event_summary: 'Saved story brief: A harbor bedtime quest.',
            last_event_type: 'content.user_edit.recorded',
            last_event_at: '2026-04-01T05:18:00Z',
          }
        }

        return stageState
      }),
    } as const
    const briefStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 4,
      events: [
        sampleHistory.events[0],
        sampleHistory.events[1],
        sampleHistory.events[2],
        sampleHistory.events[3],
      ],
    } as const

    const { storyBriefSaveRequests } = mockWorkspaceApi({
      history: briefStageHistory,
      hydration: {
        snapshot: savedBriefSnapshot,
        recent_history: briefStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 4,
          history_event_count: 4,
          materialized_through_sequence_number: 4,
        },
      },
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByDisplayValue(/harbor bedtime quest/i),
    ).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Normalized summary'), {
      target: {
        value:
          'A calmer harbor quest where each lantern return helps the child and otter settle the night.',
      },
    })
    fireEvent.change(screen.getByLabelText('Bedtime-safety concerns'), {
      target: {
        value:
          'Let any mystery resolve quickly and clearly.\nKeep every separation brief and reassuring.',
      },
    })
    fireEvent.change(screen.getByLabelText('Candidate motifs'), {
      target: {
        value: 'floating lanterns\notter paws\nmoonlit docks',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save brief' }))

    expect(storyBriefSaveRequests).toHaveLength(1)
    expect(storyBriefSaveRequests[0]).toMatchObject({
      normalized_summary:
        'A calmer harbor quest where each lantern return helps the child and otter settle the night.',
      normalized_preferences: {
        protagonist_type: 'A child and an otter guardian',
        setting: 'a moonlit harbor',
        emotional_goal: 'belonging, gentle courage, and a calm reunion',
        constraint_notes: ['Keep the ending restful.'],
        bedtime_safety_concerns: [
          'Let any mystery resolve quickly and clearly.',
          'Keep every separation brief and reassuring.',
        ],
        candidate_motifs: ['floating lanterns', 'otter paws', 'moonlit docks'],
      },
    })
  })

  it('generates a durable pitch batch from the pitches stage', async () => {
    const pitchStageSnapshot = buildStoryBriefSaveResponse({
      story_idea:
        'A sleepy child follows floating lanterns across a moonlit harbor.',
      origin: 'workspace',
    }).snapshot
    const pitchStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 4,
      events: sampleHistory.events,
    } as const

    const { pitchGenerationRequests } = mockWorkspaceApi({
      history: pitchStageHistory,
      hydration: {
        snapshot: pitchStageSnapshot,
        recent_history: pitchStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 4,
          history_event_count: 4,
          materialized_through_sequence_number: 4,
        },
      },
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Review and select story pitches',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { level: 3, name: 'Generate a pitch batch' }),
    ).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Pitch count'), {
      target: { value: '5' },
    })
    fireEvent.change(screen.getByLabelText('Optional pitch guidance'), {
      target: {
        value:
          'Lean toward a gentler mystery with a clearer reunion at the end.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Generate pitches' }))

    expect(pitchGenerationRequests).toEqual([
      {
        candidate_count: 5,
        guidance:
          'Lean toward a gentler mystery with a clearer reunion at the end.',
        preserve_selected_pitch: false,
        origin: 'workspace',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 3,
        name: 'The Juniper Lake Promise',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(/generated 5 pitch options/i),
    ).toBeInTheDocument()
  })

  it('selects a generated pitch card and advances to characters', async () => {
    const generatedPitchSnapshot = buildPitchGenerationResponse({
      candidate_count: 4,
    }).snapshot
    const generatedPitchHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 5,
      events: sampleHistory.events,
    } as const

    const { pitchSelectionRequests } = mockWorkspaceApi({
      history: generatedPitchHistory,
      hydration: {
        snapshot: generatedPitchSnapshot,
        recent_history: generatedPitchHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 5,
          history_event_count: 5,
          materialized_through_sequence_number: 5,
        },
      },
    })

    renderWorkspaceRoute()

    const pitchCard = await screen.findByRole('heading', {
      level: 3,
      name: 'The Juniper Lake Promise',
    })
    fireEvent.click(
      within(pitchCard.closest('article') as HTMLElement).getByRole('button', {
        name: 'Choose pitch',
      }),
    )

    expect(pitchSelectionRequests).toEqual([
      {
        pitch_id: 'pitch-generated-1',
        generation_key: 'batch-2',
        pitch_index: 1,
        title: 'The Juniper Lake Promise',
        origin: 'workspace',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Shape the character sheet',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText('Selected pitch: The Juniper Lake Promise'),
    ).toBeInTheDocument()
  })

  it('refines a saved pitch from the workspace without overwriting earlier batches', async () => {
    const generatedPitchSnapshot = buildPitchGenerationResponse({
      candidate_count: 4,
    }).snapshot
    const generatedPitchHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 5,
      events: sampleHistory.events,
    } as const

    const { pitchRefinementRequests } = mockWorkspaceApi({
      history: generatedPitchHistory,
      hydration: {
        snapshot: generatedPitchSnapshot,
        recent_history: generatedPitchHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 5,
          history_event_count: 5,
          materialized_through_sequence_number: 5,
        },
      },
    })

    renderWorkspaceRoute()

    await screen.findByRole('heading', {
      level: 2,
      name: 'Review and select story pitches',
    })

    fireEvent.change(screen.getByLabelText('Pitch to refine'), {
      target: { value: 'pitch-generated-2' },
    })
    fireEvent.change(screen.getByLabelText('Refinement instructions'), {
      target: {
        value: 'Make it about siblings who help each other settle down.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Refine pitch' }))

    expect(pitchRefinementRequests).toEqual([
      {
        pitch_id: 'pitch-generated-2',
        generation_key: 'batch-2',
        pitch_index: 2,
        title: 'The Last Lantern Question',
        instructions: 'Make it about siblings who help each other settle down.',
        origin: 'workspace',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Shape the character sheet',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        /Selected pitch: The Last Lantern Question: Siblings\./i,
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /Refined from The Last Lantern Question. Make it about siblings who help each other settle down./i,
      ),
    ).toBeInTheDocument()
  })

  it('generates a durable character batch from the characters stage', async () => {
    const characterStageSnapshot = buildPitchSelectionResponse({
      pitch_id: 'pitch-generated-1',
      origin: 'workspace',
    }).snapshot
    const characterStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 6,
      events: sampleHistory.events,
    } as const

    const { characterGenerationRequests } = mockWorkspaceApi({
      history: characterStageHistory,
      hydration: {
        snapshot: characterStageSnapshot,
        recent_history: characterStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 6,
          history_event_count: 6,
          materialized_through_sequence_number: 6,
        },
      },
    })

    renderWorkspaceRoute('/sessions/moonlit-harbor?stage=characters')

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Shape the character sheet',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', {
        level: 3,
        name: 'Generate a character batch',
      }),
    ).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Character sheet count'), {
      target: { value: '5' },
    })
    fireEvent.change(screen.getByLabelText('Optional character guidance'), {
      target: {
        value: 'Keep the support cast compact and clearly cozy.',
      },
    })
    fireEvent.click(
      screen.getByRole('button', { name: 'Generate character sheets' }),
    )

    expect(characterGenerationRequests).toEqual([
      {
        candidate_count: 5,
        guidance: 'Keep the support cast compact and clearly cozy.',
        origin: 'workspace',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 3,
        name: 'Juniper Keeper Cast',
      }),
    ).toBeInTheDocument()
    expect(await screen.findByText('5 cast cards ready')).toBeInTheDocument()
  })

  it('selects a generated character sheet and advances to beats', async () => {
    const generatedCharacterSnapshot = buildCharacterGenerationResponse({
      candidate_count: 3,
    }).snapshot
    const generatedCharacterHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 7,
      events: sampleHistory.events,
    } as const

    const { characterSelectionRequests } = mockWorkspaceApi({
      history: generatedCharacterHistory,
      hydration: {
        snapshot: generatedCharacterSnapshot,
        recent_history: generatedCharacterHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 7,
          history_event_count: 7,
          materialized_through_sequence_number: 7,
        },
      },
    })

    renderWorkspaceRoute('/sessions/moonlit-harbor?stage=characters')

    const characterCard = await screen.findByRole('heading', {
      level: 3,
      name: 'Juniper Keeper Cast',
    })
    fireEvent.click(
      within(characterCard.closest('article') as HTMLElement).getByRole('button', {
        name: 'Choose cast',
      }),
    )

    expect(characterSelectionRequests).toEqual([
      {
        character_sheet_id: 'character-generated-1',
        revision_number: 21,
        title: 'Juniper Keeper Cast',
        origin: 'workspace',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Refine the Save-the-Cat beats',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'Selected character sheet: Juniper Keeper Cast',
      ),
    ).toBeInTheDocument()
  })

  it('refines a saved character sheet from the workspace without overwriting earlier batches', async () => {
    const generatedCharacterSnapshot = buildCharacterGenerationResponse({
      candidate_count: 3,
    }).snapshot
    const generatedCharacterHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 7,
      events: sampleHistory.events,
    } as const

    const { characterRefinementRequests } = mockWorkspaceApi({
      history: generatedCharacterHistory,
      hydration: {
        snapshot: generatedCharacterSnapshot,
        recent_history: generatedCharacterHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 7,
          history_event_count: 7,
          materialized_through_sequence_number: 7,
        },
      },
    })

    renderWorkspaceRoute('/sessions/moonlit-harbor?stage=characters')

    await screen.findByRole('heading', {
      level: 2,
      name: 'Shape the character sheet',
    })

    fireEvent.change(screen.getByLabelText('Refinement instructions'), {
      target: {
        value: 'Make the support cast siblings who settle together.',
      },
    })
    fireEvent.click(
      screen.getByRole('button', { name: 'Refine character sheet' }),
    )

    expect(characterRefinementRequests).toEqual([
      {
        character_sheet_id: 'character-generated-1',
        revision_number: 21,
        title: 'Juniper Keeper Cast',
        instructions: 'Make the support cast siblings who settle together.',
        focus_character_names: [],
        change_summary: null,
        origin: 'workspace',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Refine the Save-the-Cat beats',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'Selected character sheet: Juniper Keeper Cast: Revised',
      ),
    ).toBeInTheDocument()
  })

  it('applies accepted character-sheet chat actions through the same durable endpoints', async () => {
    const characterStageSnapshot = buildCharacterGenerationResponse({
      candidate_count: 3,
    }).snapshot
    const characterStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 7,
      events: sampleHistory.events,
    } as const

    const { characterSelectionRequests } = mockWorkspaceApi({
      history: characterStageHistory,
      hydration: {
        snapshot: characterStageSnapshot,
        recent_history: characterStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 7,
          history_event_count: 7,
          materialized_through_sequence_number: 7,
        },
      },
      chatIntentResponse: {
        schema_version: 1,
        status: 'parsed',
        needs_clarification: false,
        assistant_response: 'I can select the first character sheet for you.',
        clarification_reason: null,
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              schema_version: 1,
              action_type: 'select_character_sheet',
              target_stage: 'characters',
              confidence: 0.97,
              rationale: 'The user asked to choose the first character sheet.',
              requires_confirmation: false,
              extracted_values: {
                character_sheet_id: 'character-generated-1',
                revision_number: 21,
                title: 'Juniper Keeper Cast',
              },
            },
          ],
        },
        policy_evaluation: {
          schema_version: 1,
          session_id: 'moonlit-harbor',
          evaluated_actions: [
            {
              action_index: 0,
              action_type: 'select_character_sheet',
              target_stage: 'characters',
              decision: 'accepted',
              summary: 'The character sheet can be selected.',
              reasons: [],
              side_effects: [],
              prerequisite_action_types: [],
            },
          ],
        },
      },
    })

    renderWorkspaceRoute('/sessions/moonlit-harbor?stage=characters')

    await screen.findByRole('heading', {
      level: 2,
      name: 'Shape the character sheet',
    })

    fireEvent.change(screen.getByLabelText('Message composer'), {
      target: { value: 'Choose the first character sheet.' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(await screen.findByText('I can select the first character sheet for you.')).toBeInTheDocument()
    expect(characterSelectionRequests).toEqual([
      {
        character_sheet_id: 'character-generated-1',
        revision_number: 21,
        title: 'Juniper Keeper Cast',
        origin: 'chat',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Refine the Save-the-Cat beats',
      }),
    ).toBeInTheDocument()
  })

  it('queues confirm-first pitch refinements from chat and applies them on confirmation', async () => {
    const generatedPitchSnapshot = buildPitchGenerationResponse({
      candidate_count: 4,
    }).snapshot
    const generatedPitchHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 5,
      events: sampleHistory.events,
    } as const

    const { pitchRefinementRequests } = mockWorkspaceApi({
      history: generatedPitchHistory,
      hydration: {
        snapshot: generatedPitchSnapshot,
        recent_history: generatedPitchHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 5,
          history_event_count: 5,
          materialized_through_sequence_number: 5,
        },
      },
      chatIntentResponse: {
        schema_version: 1,
        status: 'parsed',
        needs_clarification: false,
        assistant_response:
          'I can refine pitch two into a sibling story once you confirm the change.',
        clarification_reason: null,
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              schema_version: 1,
              action_type: 'refine_pitch',
              target_stage: 'pitches',
              confidence: 0.94,
              rationale:
                'The user asked to keep pitch two but turn it into a sibling story.',
              requires_confirmation: true,
              extracted_values: {
                pitch_id: 'pitch-generated-2',
                generation_key: 'batch-2',
                pitch_index: 2,
                title: 'The Last Lantern Question',
                instructions:
                  'Make it about siblings who help each other settle down.',
              },
            },
          ],
        },
        policy_evaluation: {
          schema_version: 1,
          session_id: 'moonlit-harbor',
          evaluated_actions: [
            {
              action_index: 0,
              action_type: 'refine_pitch',
              target_stage: 'pitches',
              decision: 'requires_confirmation',
              summary:
                'Generate a targeted revision from The Last Lantern Question.',
              reasons: [],
              side_effects: [],
              prerequisite_action_types: [],
            },
          ],
        },
      },
    })

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: 'Take pitch two but make it about siblings.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      await screen.findByText(
        'I can refine pitch two into a sibling story once you confirm the change.',
      ),
    ).toBeInTheDocument()
    expect(await screen.findByText('Pending confirmations')).toBeInTheDocument()
    expect(screen.getByText('Refine this pitch')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Generate a targeted revision from The Last Lantern Question.',
      ),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Confirm' }))

    expect(pitchRefinementRequests).toEqual([
      {
        pitch_id: 'pitch-generated-2',
        generation_key: 'batch-2',
        pitch_index: 2,
        title: 'The Last Lantern Question',
        instructions: 'Make it about siblings who help each other settle down.',
        origin: 'chat',
      },
    ])
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Shape the character sheet',
      }),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        /Selected pitch: The Last Lantern Question: Siblings\./i,
      ),
    ).toBeInTheDocument()
  })

  it('supports route-backed stage preview without changing the durable current step', async () => {
    mockWorkspaceApi()

    renderWithAppProviders(
      <MemoryRouter initialEntries={['/sessions/moonlit-harbor?stage=audio']}>
        <Routes>
          <Route
            path="/sessions/:sessionId"
            element={<SessionWorkspacePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Configure narration and music',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /the route is previewing audio via the stage query parameter/i,
      ),
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /audio/i })).toHaveAttribute(
      'href',
      '/sessions/moonlit-harbor?stage=audio',
    )
    expect(screen.getAllByText('?stage=audio').length).toBeGreaterThan(0)
  })

  it('records direct stage-preview clicks as action echoes in the transcript', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    const audioLink = await screen.findByRole('link', { name: /audio/i })

    fireEvent.click(audioLink)

    expect(
      await screen.findByText('Opened Audio in the main pane.'),
    ).toBeInTheDocument()
  })

  it('shows chat-driven action echoes when a parsed action changes the visible UI', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: 'Take me to the audio settings.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      within(screen.getByRole('log')).getByText(
        'Take me to the audio settings.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'I can open the audio stage so you can review narration settings.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText('Opened Audio in the main pane.'),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Configure narration and music',
      }),
    ).toBeInTheDocument()
  })

  it('applies accepted chat-driven tone selections through the workspace runtime', async () => {
    const toneStageSnapshot = {
      ...sampleSnapshot,
      current_stage: 'tone',
      resume_stage: 'tone',
      furthest_completed_stage: 'genre',
      overall_status: 'in_progress',
      selected_tone_profile: null,
      progress: {
        total_stages: 10,
        completed_stages: 1,
        in_progress_stages: 0,
        needs_regeneration_stages: 0,
      },
      story_brief: null,
      selected_pitch: null,
      selected_story_setup: null,
      stage_states: sampleSnapshot.stage_states.map((stageState, index) => {
        if (index === 0) {
          return {
            ...stageState,
            status: 'completed',
            detail:
              'Selected genre: Quest Fantasy. Tone choices filter from this lane next.',
            last_event_summary: 'Selected genre: Quest Fantasy.',
            last_event_type: 'selection.recorded',
            last_event_at: '2026-04-01T05:16:00Z',
          }
        }

        return {
          ...stageState,
          status: 'draft',
          detail: null,
          last_event_summary: null,
          last_event_type: null,
          last_event_at: null,
        }
      }),
    } as const
    const toneStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 2,
      events: [sampleHistory.events[0], sampleHistory.events[1]],
    } as const

    const { toneSelectionRequests } = mockWorkspaceApi({
      history: toneStageHistory,
      hydration: {
        snapshot: toneStageSnapshot,
        recent_history: toneStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 2,
          history_event_count: 2,
          materialized_through_sequence_number: 2,
        },
      },
      chatIntentResponse: {
        schema_version: 1,
        status: 'parsed',
        needs_clarification: false,
        assistant_response:
          'I can shift the mood to Hushed Wonder before we draft the brief.',
        clarification_reason: null,
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              schema_version: 1,
              action_type: 'select_tone',
              target_stage: 'tone',
              confidence: 0.93,
              rationale:
                'The user explicitly asked for the hush-and-wonder tone.',
              requires_confirmation: false,
              extracted_values: {
                tone_profile_slug: 'hushed-wonder',
              },
            },
          ],
        },
        policy_evaluation: {
          schema_version: 1,
          session_id: 'moonlit-harbor',
          evaluated_actions: [
            {
              action_index: 0,
              action_type: 'select_tone',
              target_stage: 'tone',
              decision: 'accepted',
              summary: 'Tone selection is allowed.',
              reasons: [],
              side_effects: [],
              prerequisite_action_types: [],
            },
          ],
        },
      },
    })

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: 'Make it feel like hushed wonder.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      within(screen.getByRole('log')).getByText(
        'Make it feel like hushed wonder.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'I can shift the mood to Hushed Wonder before we draft the brief.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText('Selected tone: Hushed Wonder'),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Capture the free-form story brief',
      }),
    ).toBeInTheDocument()
    expect(toneSelectionRequests).toEqual([
      {
        tone_profile_slug: 'hushed-wonder',
        origin: 'chat',
      },
    ])
  })

  it('applies accepted chat-driven story brief updates through the workspace runtime', async () => {
    const briefStageSnapshot = buildToneSelectionResponse({
      tone_profile_id: 'tone-1',
      origin: 'workspace',
    }).snapshot
    const briefStageHistory = {
      session_id: 'moonlit-harbor',
      latest_sequence_number: 3,
      events: [
        sampleHistory.events[0],
        sampleHistory.events[1],
        sampleHistory.events[2],
      ],
    } as const

    const { storyBriefSaveRequests } = mockWorkspaceApi({
      history: briefStageHistory,
      hydration: {
        snapshot: briefStageSnapshot,
        recent_history: briefStageHistory,
        hydration: {
          ...sampleHydration.hydration,
          latest_sequence_number: 3,
          history_event_count: 3,
          materialized_through_sequence_number: 3,
        },
      },
      chatIntentResponse: {
        schema_version: 1,
        status: 'parsed',
        needs_clarification: false,
        assistant_response:
          'I can save that harbor-lantern brief and move the workspace on to pitches.',
        clarification_reason: null,
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              schema_version: 1,
              action_type: 'update_story_brief',
              target_stage: 'brief',
              confidence: 0.91,
              rationale:
                'The user provided story brief details for the brief stage.',
              requires_confirmation: false,
              extracted_values: {
                story_idea:
                  'A child and an otter guardian drift after runaway lanterns to bring each light home before the harbor sleeps.',
                desired_themes:
                  'Gentle courage, belonging, and a calm return home.',
                key_images: 'Lantern reflections, otter paws, and quiet docks.',
                audience_notes: 'Keep it cozy for a sensitive five-year-old.',
                must_have_elements:
                  'A harbor reunion and a soft bedtime ending.',
                edit_mode: 'replace',
              },
            },
          ],
        },
        policy_evaluation: {
          schema_version: 1,
          session_id: 'moonlit-harbor',
          evaluated_actions: [
            {
              action_index: 0,
              action_type: 'update_story_brief',
              target_stage: 'brief',
              decision: 'accepted',
              summary: 'Story brief updates are allowed.',
              reasons: [],
              side_effects: [],
              prerequisite_action_types: [],
            },
          ],
        },
      },
    })

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value:
          'Save this as the brief: a child and an otter guardian drift after runaway lanterns to bring each light home before the harbor sleeps.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      within(screen.getByRole('log')).getByText(
        'Save this as the brief: a child and an otter guardian drift after runaway lanterns to bring each light home before the harbor sleeps.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'I can save that harbor-lantern brief and move the workspace on to pitches.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Review and select story pitches',
      }),
    ).toBeInTheDocument()
    expect(storyBriefSaveRequests).toHaveLength(1)
    expect(storyBriefSaveRequests[0]).toMatchObject({
      story_idea:
        'A child and an otter guardian drift after runaway lanterns to bring each light home before the harbor sleeps.',
      desired_themes: 'Gentle courage, belonging, and a calm return home.',
      key_images: 'Lantern reflections, otter paws, and quiet docks.',
      audience_notes: 'Keep it cozy for a sensitive five-year-old.',
      must_have_elements: 'A harbor reunion and a soft bedtime ending.',
      edit_mode: 'replace',
      origin: 'chat',
    })
    expect(storyBriefSaveRequests[0]).not.toHaveProperty('normalized_summary')
    expect(storyBriefSaveRequests[0]).not.toHaveProperty(
      'normalized_preferences',
    )
  })

  it('shows rejected chat-driven action echoes without mutating the visible workspace stage', async () => {
    mockWorkspaceApi({
      chatIntentResponse: {
        schema_version: 1,
        status: 'parsed',
        needs_clarification: false,
        assistant_response:
          'I can shorten the story once story setup is ready.',
        clarification_reason: null,
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              schema_version: 1,
              action_type: 'update_story_setup',
              target_stage: 'story_setup',
              confidence: 0.82,
              rationale: 'The user asked for a shorter runtime.',
              requires_confirmation: false,
              extracted_values: {
                target_runtime_minutes: 8,
              },
            },
          ],
        },
        policy_evaluation: {
          schema_version: 1,
          session_id: 'moonlit-harbor',
          evaluated_actions: [
            {
              action_index: 0,
              action_type: 'update_story_setup',
              target_stage: 'story_setup',
              decision: 'rejected',
              summary:
                'Complete or regenerate beats before changing story_setup.',
              reasons: [
                {
                  code: 'prerequisite_stage_incomplete',
                  message:
                    'Complete or regenerate beats before changing story_setup.',
                  stage: 'story_setup',
                  related_stages: ['beats'],
                  related_action_types: [],
                },
              ],
              side_effects: [],
              prerequisite_action_types: [],
            },
          ],
        },
      },
    })

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: 'Make it shorter.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      within(screen.getByRole('log')).getByText('Make it shorter.'),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'I can shorten the story once story setup is ready.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        "Couldn't update story setup yet. Finish Beat sheet first.",
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', {
        level: 2,
        name: 'Refine the Save-the-Cat beats',
      }),
    ).toBeInTheDocument()
  })

  it('submits slash commands through the explicit command contract', async () => {
    const { chatIntentRequests } = mockWorkspaceApi({
      chatIntentResponse: buildCommandChatIntentResponse,
    })

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: '/plan',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      await screen.findByText(
        'Current focus is beat sheet. Plan so far: Quest Fantasy, Hushed Wonder, pitch "Lanterns Over Juniper Lake", ~12 minutes, 4 chapters, 1500 words.',
      ),
    ).toBeInTheDocument()
    expect(chatIntentRequests).toHaveLength(1)
    expect(chatIntentRequests[0]).toMatchObject({
      message: '/plan',
      explicit_command: {
        command_id: 'summarize_plan',
        source: 'slash_command',
        proposed_actions: {
          schema_version: 1,
          actions: [],
        },
      },
    })
  })

  it('runs quick actions through the same explicit command request shape', async () => {
    const { chatIntentRequests } = mockWorkspaceApi({
      chatIntentResponse: buildCommandChatIntentResponse,
    })

    renderWorkspaceRoute()

    fireEvent.click(await screen.findByRole('button', { name: 'Next stage' }))

    expect(
      await screen.findByText('I can move the workspace to Story setup.'),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Set soft story targets',
      }),
    ).toBeInTheDocument()
    expect(chatIntentRequests).toHaveLength(1)
    expect(chatIntentRequests[0]).toMatchObject({
      message: '/next-stage',
      explicit_command: {
        command_id: 'next_stage',
        source: 'quick_action',
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              action_type: 'navigate_to_stage',
              target_stage: 'story_setup',
            },
          ],
        },
      },
    })
  })

  it('saves a stage note through the durable context update pipeline', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    const noteField = await screen.findByLabelText('Beat sheet note')

    fireEvent.change(noteField, {
      target: {
        value: 'Add one calmer beat before the return home.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save note' }))

    expect(
      await screen.findByText('Updated beat sheet notes from the workspace.'),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Beat sheet note')).toHaveValue(
      'Add one calmer beat before the return home.',
    )
  })

  it('replays durable ui-originated echoes and hydrated stage detail when resuming', async () => {
    const resumedHistory = {
      ...sampleHistory,
      latest_sequence_number: 6,
      events: [
        ...sampleHistory.events,
        {
          id: 'event-5',
          session_id: 'moonlit-harbor',
          sequence_number: 5,
          actor: {
            actor_type: 'user',
            actor_id: 'local-user',
          },
          event_type: 'ui.action.recorded',
          stage: 'audio',
          summary: 'Recorded UI action: navigate_to_stage.',
          payload: {
            schema_version: 1,
            action: 'navigate_to_stage',
            control_id: 'stage-navigator',
            value_summary: 'Audio',
            origin: 'workspace',
          },
          created_at: '2026-04-01T03:04:00Z',
        },
        {
          id: 'event-6',
          session_id: 'moonlit-harbor',
          sequence_number: 6,
          actor: {
            actor_type: 'user',
            actor_id: 'local-user',
          },
          event_type: 'content.user_edit.recorded',
          stage: 'beats',
          summary: 'Saved user edit for beat sheet.',
          payload: {
            schema_version: 1,
            target_kind: 'beat_sheet',
            changed_fields: ['detail'],
            source: 'workspace',
            field_values: {
              detail: 'Add one calmer beat before the return home.',
              control_id: 'stage-note-editor',
            },
            summary_text: 'Updated beat sheet notes from the workspace.',
          },
          created_at: '2026-04-01T03:05:00Z',
        },
      ],
    } as const
    const resumedHydration = {
      ...sampleHydration,
      snapshot: {
        ...sampleSnapshot,
        updated_at: '2026-04-01T03:05:00Z',
        stage_states: sampleSnapshot.stage_states.map((stageState) =>
          stageState.stage === 'beats'
            ? {
                ...stageState,
                detail: 'Add one calmer beat before the return home.',
                last_event_summary:
                  'Updated beat sheet notes from the workspace.',
                last_event_type: 'content.user_edit.recorded',
                last_event_at: '2026-04-01T03:05:00Z',
              }
            : stageState,
        ),
      },
      recent_history: resumedHistory,
      hydration: {
        ...sampleHydration.hydration,
        materialized_through_sequence_number: 6,
        latest_sequence_number: 6,
        history_event_count: 6,
      },
    } as const

    mockWorkspaceApi({
      history: resumedHistory,
      hydration: resumedHydration,
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByText('Opened Audio in the main pane.'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Updated beat sheet notes from the workspace.'),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Beat sheet note')).toHaveValue(
      'Add one calmer beat before the return home.',
    )
  })

  it('shows a missing-session state when the snapshot request returns 404', async () => {
    mockWorkspaceApi({
      hydrationStatus: 404,
      hydration: { detail: 'missing' },
    })

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Workspace unavailable',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'The session moonlit-harbor could not be found in the durable store.',
      ),
    ).toBeInTheDocument()
  })
})
