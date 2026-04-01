import { describe, expect, it } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { buildSessionWorkspaceStageViews } from './sessionStageScaffold.ts'

const snapshot: SessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  current_stage: 'beats',
  resume_stage: 'beats',
  furthest_completed_stage: 'characters',
  overall_status: 'in_progress',
  created_at: '2026-04-01T03:00:00Z',
  updated_at: '2026-04-01T05:15:00Z',
  completed_at: null,
  selected_genre: null,
  selected_tone_profile: null,
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
      stage: 'beats',
      label: 'Beat sheet',
      description:
        'Store the accepted Save-the-Cat beat sheet for the session.',
      status: 'in_progress',
      detail: 'Midpoint needs one more bedtime-soft pass.',
    },
  ],
  story_brief: null,
  selected_pitch: null,
  selected_character_sheet: null,
  selected_story_setup: null,
  active_composition_job: null,
  active_audio_job: null,
  latest_story_asset: null,
  latest_audio_asset: null,
}

describe('sessionStageScaffold', () => {
  it('normalizes the session stage list to the canonical workflow order', () => {
    const result = buildSessionWorkspaceStageViews(snapshot, null)

    expect(result.stageViews).toHaveLength(10)
    expect(result.stageViews.map((stage) => stage.stage)).toEqual([
      'genre',
      'tone',
      'brief',
      'pitches',
      'characters',
      'beats',
      'story_setup',
      'composition',
      'audio',
      'finalize',
    ])
    expect(result.currentStage.stage).toBe('beats')
    expect(result.selectedStage.stage).toBe('beats')
  })

  it('derives availability and fallback states for missing stages', () => {
    const result = buildSessionWorkspaceStageViews(snapshot, 'audio')
    const genreStage = result.stageViews[0]
    const toneStage = result.stageViews[1]
    const audioStage = result.selectedStage

    expect(genreStage.availability).toBe('revisitable')
    expect(toneStage.status).toBe('completed')
    expect(audioStage.stage).toBe('audio')
    expect(audioStage.availability).toBe('locked')
    expect(audioStage.scaffoldBullets).toHaveLength(3)
  })
})
