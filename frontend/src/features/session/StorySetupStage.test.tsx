import { fireEvent, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'
import { StorySetupStage } from './StorySetupStage.tsx'

const sampleSnapshot: SessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  current_stage: 'story_setup',
  resume_stage: 'story_setup',
  furthest_completed_stage: 'beats',
  overall_status: 'in_progress',
  created_at: '2026-04-01T03:00:00Z',
  updated_at: '2026-04-02T05:15:00Z',
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
    completed_stages: 6,
    in_progress_stages: 1,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'story_setup',
      label: 'Story setup',
      description: 'Store soft planning targets for the selected beat sheet.',
      status: 'in_progress',
      detail: null,
    },
  ],
  story_brief: null,
  selected_pitch: null,
  selected_character_sheet: null,
  selected_beat_sheet: {
    id: 'beat-1',
    revision_number: 2,
    summary: 'A lantern quest that softens into homecoming.',
    beats: [],
    focus_beats: [],
    accepted_at: '2026-04-02T04:45:00Z',
  },
  selected_story_setup: null,
  selected_story_outline: null,
  active_composition_job: null,
  active_audio_job: null,
  latest_story_asset: null,
  latest_audio_asset: null,
}

const selectedStage: SessionWorkspaceStageView = {
  stage: 'story_setup',
  label: 'Story setup',
  description: 'Store soft planning targets such as word count and runtime.',
  status: 'in_progress',
  detail: null,
  availability: 'unlocked',
  index: 6,
  invalidatesOnEdit: ['composition', 'audio', 'finalize'],
  isCurrent: true,
  isSelected: true,
  scaffoldBullets: [],
  scaffoldSummary: 'Story setup preferences guide later writing work.',
  scaffoldTitle: 'Story setup',
}

function buildOutlineSnapshot(): SessionSnapshot {
  return {
    ...sampleSnapshot,
    selected_story_setup: {
      id: 'setup-1',
      revision_number: 1,
      target_word_count: 1800,
      target_runtime_minutes: 13,
      chapter_count: 3,
      approximate_scene_count: 8,
      chapter_style: 'three gentle chapters',
      guidance_notes: 'Keep each chapter ending softer than it began.',
      accepted_at: '2026-04-02T05:20:00Z',
    },
    selected_story_outline: {
      id: 'outline-1',
      revision_number: 1,
      outline_kind: 'chapter',
      summary: 'Three draftable chapters mapped from the beat sheet.',
      cards: [
        {
          card_key: 'chapter-1',
          card_type: 'chapter',
          position: 1,
          title: 'Chapter 1: Opening Image to Catalyst',
          purpose:
            'Set the harbor mood and launch the first bedtime-safe problem.',
          summary:
            'Set the harbor mood and launch Mira after the drifting bell.',
          beat_keys: ['opening_image', 'catalyst'],
          beat_labels: ['Opening Image', 'Catalyst'],
          emotional_shift: 'Move from stillness toward gentle motion.',
          target_word_count: 600,
          target_runtime_minutes: 4,
          target_scene_count: 3,
          tone_direction:
            'Stay anchored in the Hushed Wonder tone while advancing the Quest Fantasy lane.',
          bedtime_guardrail:
            'Keep the problem small, visible, and quickly reassuring.',
          drafting_brief:
            'Chapter 1 should cover Opening Image and Catalyst while staying calm and luminous.',
        },
        {
          card_key: 'chapter-2',
          card_type: 'chapter',
          position: 2,
          title: 'Chapter 2: Midpoint',
          purpose: 'Let wonder peak while the bedtime tone stays intact.',
          summary:
            "Let Mira discover the hidden cove and feel the bell's meaning open up.",
          beat_keys: ['midpoint'],
          beat_labels: ['Midpoint'],
          emotional_shift:
            'Lift wonder without breaking the bedtime reassurance.',
          target_word_count: 600,
          target_runtime_minutes: 4,
          target_scene_count: 3,
          tone_direction:
            'Stay anchored in the Hushed Wonder tone while advancing the Quest Fantasy lane.',
          bedtime_guardrail:
            'Keep the surprise luminous and quickly reassuring.',
          drafting_brief:
            'Chapter 2 should center the midpoint reveal and keep the wonder soft.',
        },
      ],
      genre_label: 'Quest Fantasy',
      tone_label: 'Hushed Wonder',
      accepted_at: '2026-04-02T05:20:00Z',
    },
    story_outline_revisions: [
      {
        id: 'outline-1',
        revision_number: 1,
        outline_kind: 'chapter',
        summary: 'Three draftable chapters mapped from the beat sheet.',
        cards: [
          {
            card_key: 'chapter-1',
            card_type: 'chapter',
            position: 1,
            title: 'Chapter 1: Opening Image to Catalyst',
            purpose:
              'Set the harbor mood and launch the first bedtime-safe problem.',
            summary:
              'Set the harbor mood and launch Mira after the drifting bell.',
            beat_keys: ['opening_image', 'catalyst'],
            beat_labels: ['Opening Image', 'Catalyst'],
            emotional_shift: 'Move from stillness toward gentle motion.',
            target_word_count: 600,
            target_runtime_minutes: 4,
            target_scene_count: 3,
            tone_direction:
              'Stay anchored in the Hushed Wonder tone while advancing the Quest Fantasy lane.',
            bedtime_guardrail:
              'Keep the problem small, visible, and quickly reassuring.',
            drafting_brief:
              'Chapter 1 should cover Opening Image and Catalyst while staying calm and luminous.',
          },
          {
            card_key: 'chapter-2',
            card_type: 'chapter',
            position: 2,
            title: 'Chapter 2: Midpoint',
            purpose: 'Let wonder peak while the bedtime tone stays intact.',
            summary:
              "Let Mira discover the hidden cove and feel the bell's meaning open up.",
            beat_keys: ['midpoint'],
            beat_labels: ['Midpoint'],
            emotional_shift:
              'Lift wonder without breaking the bedtime reassurance.',
            target_word_count: 600,
            target_runtime_minutes: 4,
            target_scene_count: 3,
            tone_direction:
              'Stay anchored in the Hushed Wonder tone while advancing the Quest Fantasy lane.',
            bedtime_guardrail:
              'Keep the surprise luminous and quickly reassuring.',
            drafting_brief:
              'Chapter 2 should center the midpoint reveal and keep the wonder soft.',
          },
        ],
        genre_label: 'Quest Fantasy',
        tone_label: 'Hushed Wonder',
        accepted_at: '2026-04-02T05:20:00Z',
      },
    ],
  }
}

describe('StorySetupStage', () => {
  it('applies an explicit runtime suggestion and carries it into save', async () => {
    const onSaveStorySetup = vi.fn().mockResolvedValue({
      event: {
        id: 'event-1',
        session_id: 'moonlit-harbor',
        sequence_number: 1,
        actor: { actor_type: 'user' },
        event_type: 'selection.recorded',
        stage: 'story_setup',
        summary: 'Accepted story setup.',
        payload: null,
        created_at: '2026-04-02T05:20:00Z',
      },
      snapshot: sampleSnapshot,
    })

    renderWithAppProviders(
      <StorySetupStage
        onPreviewStage={vi.fn()}
        onSaveStorySetup={onSaveStorySetup}
        onSaveStoryOutline={vi.fn().mockResolvedValue({
          event: {
            id: 'event-outline-1',
            session_id: 'moonlit-harbor',
            sequence_number: 2,
            actor: { actor_type: 'user' },
            event_type: 'content.user_edit.recorded',
            stage: 'story_setup',
            summary: 'Updated story outline cards.',
            payload: null,
            created_at: '2026-04-02T05:25:00Z',
          },
          snapshot: sampleSnapshot,
        })}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    fireEvent.change(screen.getByLabelText('Target word count'), {
      target: { value: '1800' },
    })

    expect(
      screen.getByText(
        '1800 words usually reads aloud in about 13 minutes, often somewhere near 11-15.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'Apply the midpoint runtime if you want the related field filled in for you.',
      ),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Use ~13 minutes' }))

    expect(
      screen.getByLabelText('Target read-aloud duration (minutes)'),
    ).toHaveValue(13)

    fireEvent.click(screen.getByRole('button', { name: 'Save story setup' }))

    await waitFor(() => {
      expect(onSaveStorySetup).toHaveBeenCalledWith({
        origin: 'workspace',
        previewCurrentStage: false,
        targetRuntimeMinutes: 13,
        targetWordCount: 1800,
      })
    })
  })

  it('surfaces chapter sizing assumptions in the summary rail', () => {
    renderWithAppProviders(
      <StorySetupStage
        onPreviewStage={vi.fn()}
        onSaveStorySetup={vi.fn().mockResolvedValue({
          event: {
            id: 'event-1',
            session_id: 'moonlit-harbor',
            sequence_number: 1,
            actor: { actor_type: 'user' },
            event_type: 'selection.recorded',
            stage: 'story_setup',
            summary: 'Accepted story setup.',
            payload: null,
            created_at: '2026-04-02T05:20:00Z',
          },
          snapshot: sampleSnapshot,
        })}
        onSaveStoryOutline={vi.fn().mockResolvedValue({
          event: {
            id: 'event-outline-1',
            session_id: 'moonlit-harbor',
            sequence_number: 2,
            actor: { actor_type: 'user' },
            event_type: 'content.user_edit.recorded',
            stage: 'story_setup',
            summary: 'Updated story outline cards.',
            payload: null,
            created_at: '2026-04-02T05:25:00Z',
          },
          snapshot: sampleSnapshot,
        })}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    fireEvent.change(screen.getByLabelText('Target word count'), {
      target: { value: '1800' },
    })
    fireEvent.change(screen.getByLabelText('Chapter count'), {
      target: { value: '3' },
    })

    expect(
      screen.getByText(
        '3 chapters at 1800 words usually lands near 600 words per chapter, often roughly 500-700. Chapter count sets the broad pacing shape; chapter lengths can still breathe a little.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'Read-aloud estimates assume about 140 words per minute, with most bedtime narration landing between 120 and 160. Chapter sizing assumes individual chapters can drift by about 15% around the average rather than matching perfectly.',
      ),
    ).toBeInTheDocument()
  })

  it('saves an edited outline card as a new revision', async () => {
    const outlineSnapshot = buildOutlineSnapshot()
    const onSaveStoryOutline = vi.fn().mockResolvedValue({
      event: {
        id: 'event-outline-1',
        session_id: 'moonlit-harbor',
        sequence_number: 2,
        actor: { actor_type: 'user' },
        event_type: 'content.user_edit.recorded',
        stage: 'story_setup',
        summary: 'Updated story outline cards.',
        payload: null,
        created_at: '2026-04-02T05:25:00Z',
      },
      snapshot: outlineSnapshot,
    })

    renderWithAppProviders(
      <StorySetupStage
        onPreviewStage={vi.fn()}
        onSaveStorySetup={vi.fn().mockResolvedValue({
          event: {
            id: 'event-setup-1',
            session_id: 'moonlit-harbor',
            sequence_number: 1,
            actor: { actor_type: 'user' },
            event_type: 'selection.recorded',
            stage: 'story_setup',
            summary: 'Accepted story setup.',
            payload: null,
            created_at: '2026-04-02T05:20:00Z',
          },
          snapshot: outlineSnapshot,
        })}
        onSaveStoryOutline={onSaveStoryOutline}
        selectedStage={selectedStage}
        snapshot={outlineSnapshot}
      />,
    )

    fireEvent.change(screen.getByLabelText('Card summary'), {
      target: {
        value:
          'Open with a calmer harbor image, then let Mira follow the first drifting bell.',
      },
    })
    fireEvent.click(
      screen.getByRole('button', { name: 'Save outline revision' }),
    )

    await waitFor(() => {
      expect(onSaveStoryOutline).toHaveBeenCalledWith({
        outlineId: 'outline-1',
        summary: 'Three draftable chapters mapped from the beat sheet.',
        cards: [
          expect.objectContaining({
            card_key: 'chapter-1',
            purpose:
              'Set the harbor mood and launch the first bedtime-safe problem.',
            summary:
              'Open with a calmer harbor image, then let Mira follow the first drifting bell.',
          }),
          expect.objectContaining({
            card_key: 'chapter-2',
          }),
        ],
        regenerateCardKeys: [],
        origin: 'workspace',
      })
    })
  })

  it('shows structural invalidation messaging and saves reordered cards', async () => {
    const outlineSnapshot = buildOutlineSnapshot()
    const onSaveStoryOutline = vi.fn().mockResolvedValue({
      event: {
        id: 'event-outline-2',
        session_id: 'moonlit-harbor',
        sequence_number: 3,
        actor: { actor_type: 'user' },
        event_type: 'content.user_edit.recorded',
        stage: 'story_setup',
        summary: 'Saved a structural outline revision.',
        payload: null,
        created_at: '2026-04-02T05:35:00Z',
      },
      snapshot: outlineSnapshot,
    })

    renderWithAppProviders(
      <StorySetupStage
        onPreviewStage={vi.fn()}
        onSaveStorySetup={vi.fn().mockResolvedValue({
          event: {
            id: 'event-setup-1',
            session_id: 'moonlit-harbor',
            sequence_number: 1,
            actor: { actor_type: 'user' },
            event_type: 'selection.recorded',
            stage: 'story_setup',
            summary: 'Accepted story setup.',
            payload: null,
            created_at: '2026-04-02T05:20:00Z',
          },
          snapshot: outlineSnapshot,
        })}
        onSaveStoryOutline={onSaveStoryOutline}
        selectedStage={selectedStage}
        snapshot={outlineSnapshot}
      />,
    )

    fireEvent.click(screen.getAllByRole('button', { name: 'Move later' })[0])

    expect(
      screen.getAllByText(
        'This becomes a structural outline revision because card order changed. Composition, Audio, Finalize will need regeneration after save.',
      ),
    ).toHaveLength(2)

    fireEvent.click(
      screen.getByRole('button', { name: 'Save outline revision' }),
    )

    await waitFor(() => {
      expect(onSaveStoryOutline).toHaveBeenCalledWith(
        expect.objectContaining({
          cards: [
            expect.objectContaining({
              card_key: 'chapter-2',
              position: 1,
            }),
            expect.objectContaining({
              card_key: 'chapter-1',
              position: 2,
            }),
          ],
          regenerateCardKeys: [],
        }),
      )
    })
  })

  it('regenerates only the selected card through the save callback', async () => {
    const outlineSnapshot = buildOutlineSnapshot()
    const onSaveStoryOutline = vi.fn().mockResolvedValue({
      event: {
        id: 'event-outline-3',
        session_id: 'moonlit-harbor',
        sequence_number: 4,
        actor: { actor_type: 'user' },
        event_type: 'content.user_edit.recorded',
        stage: 'story_setup',
        summary: 'Regenerated a card.',
        payload: null,
        created_at: '2026-04-02T05:40:00Z',
      },
      snapshot: outlineSnapshot,
    })

    renderWithAppProviders(
      <StorySetupStage
        onPreviewStage={vi.fn()}
        onSaveStorySetup={vi.fn().mockResolvedValue({
          event: {
            id: 'event-setup-1',
            session_id: 'moonlit-harbor',
            sequence_number: 1,
            actor: { actor_type: 'user' },
            event_type: 'selection.recorded',
            stage: 'story_setup',
            summary: 'Accepted story setup.',
            payload: null,
            created_at: '2026-04-02T05:20:00Z',
          },
          snapshot: outlineSnapshot,
        })}
        onSaveStoryOutline={onSaveStoryOutline}
        selectedStage={selectedStage}
        snapshot={outlineSnapshot}
      />,
    )

    fireEvent.click(
      screen.getByRole('button', { name: 'Regenerate this card' }),
    )

    await waitFor(() => {
      expect(onSaveStoryOutline).toHaveBeenCalledWith(
        expect.objectContaining({
          regenerateCardKeys: ['chapter-1'],
        }),
      )
    })
  })
})
