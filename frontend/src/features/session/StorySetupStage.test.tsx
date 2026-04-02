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
})
