import { fireEvent, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'
import { AudioSettingsStage } from './AudioSettingsStage.tsx'

const sampleSnapshot: SessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  current_stage: 'audio',
  resume_stage: 'audio',
  furthest_completed_stage: 'composition',
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
    completed_stages: 8,
    in_progress_stages: 1,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'audio',
      label: 'Audio',
      description: 'Configure narration settings and generate resumable audio artifacts.',
      status: 'in_progress',
      detail: 'Tune narration settings.',
    },
  ],
  latest_story_asset: {
    id: 'story-asset-1',
    asset_kind: 'story_text',
    status: 'ready',
    ready_at: '2026-04-02T05:10:00Z',
  },
  latest_audio_asset: null,
  audio_settings: {
    voice_key: 'moonbeam',
    narration_style: 'calm',
    playback_speed: 0.95,
    include_background_music: false,
    music_profile: 'lullaby_piano',
    narration_volume: 92,
    music_volume: 24,
    guidance_notes: null,
    runtime_estimate: {
      estimated_word_count: 1800,
      target_duration_seconds: 780,
      minimum_duration_seconds: 660,
      maximum_duration_seconds: 900,
      basis_source: 'story_setup_target',
      pacing_band: 'balanced',
    },
  },
}

const selectedStage: SessionWorkspaceStageView = {
  stage: 'audio',
  label: 'Audio',
  description: 'Configure narration settings and generate resumable audio artifacts.',
  status: 'in_progress',
  detail: 'Tune narration settings.',
  availability: 'unlocked',
  index: 8,
  invalidatesOnEdit: ['finalize'],
  isCurrent: true,
  isSelected: true,
  scaffoldBullets: [],
  scaffoldSummary: 'Audio settings live here.',
  scaffoldTitle: 'Audio',
}

describe('AudioSettingsStage', () => {
  it('renders the saved audio plan and estimate copy', () => {
    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={vi.fn()}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    expect(screen.getByText('Shape the narration pass before the audio render starts.')).toBeInTheDocument()
    expect(screen.getByText('About 13 min')).toBeInTheDocument()
    expect(
      screen.getByText('Usually 11-15 min. Final runtime can still vary.'),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Narration voice')).toHaveValue('moonbeam')
    expect(screen.getByLabelText('Narration style')).toHaveValue('calm')
  })

  it('saves the full audio settings form state through the workspace callback', async () => {
    const onSaveAudioSettings = vi.fn().mockResolvedValue({
      event: {
        id: 'audio-event-1',
        session_id: 'moonlit-harbor',
        sequence_number: 1,
        actor: { actor_type: 'user' },
        event_type: 'content.user_edit.recorded',
        stage: 'audio',
        summary: 'Saved user edit for audio settings.',
        payload: null,
        created_at: '2026-04-02T05:20:00Z',
      },
      snapshot: sampleSnapshot,
    })

    renderWithAppProviders(
      <AudioSettingsStage
        onSaveAudioSettings={onSaveAudioSettings}
        selectedStage={selectedStage}
        snapshot={sampleSnapshot}
      />,
    )

    fireEvent.change(screen.getByLabelText('Narration voice'), {
      target: { value: 'storykeeper' },
    })
    fireEvent.change(screen.getByLabelText('Playback speed'), {
      target: { value: '1.05' },
    })
    fireEvent.click(screen.getByLabelText('Background music'))
    fireEvent.change(screen.getByLabelText('Music style'), {
      target: { value: 'night_ambience' },
    })
    fireEvent.change(screen.getByLabelText('Narration volume'), {
      target: { value: '89' },
    })
    fireEvent.change(screen.getByLabelText('Music volume'), {
      target: { value: '15' },
    })
    fireEvent.change(screen.getByLabelText('Mix and delivery note'), {
      target: { value: 'Lean even softer on chapter endings.' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save audio settings' }))

    expect(onSaveAudioSettings).toHaveBeenCalledWith({
      voiceKey: 'storykeeper',
      narrationStyle: 'calm',
      playbackSpeed: 1.05,
      includeBackgroundMusic: true,
      musicProfile: 'night_ambience',
      narrationVolume: 89,
      musicVolume: 15,
      guidanceNotes: 'Lean even softer on chapter endings.',
      origin: 'workspace',
    })
  })
})
