import { describe, expect, it } from 'vitest'
import {
  WORKFLOW_STAGE_SEQUENCE,
  WORKFLOW_STAGE_STATES,
  getWorkflowStageLabel,
  isWorkflowStageId,
  getInvalidatedStagesAfterEdit,
  resolveResumeStage,
  workflowStageDefinitions,
} from './workflowStages.ts'

describe('workflowStages', () => {
  it('exposes the canonical stage order and state identifiers', () => {
    expect(WORKFLOW_STAGE_SEQUENCE).toEqual([
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
    expect(workflowStageDefinitions.map(({ id }) => id)).toEqual(
      WORKFLOW_STAGE_SEQUENCE,
    )
    expect(WORKFLOW_STAGE_STATES).toEqual([
      'draft',
      'in_progress',
      'completed',
      'needs_regeneration',
    ])
    expect(
      workflowStageDefinitions.every(
        ({ scaffoldBullets }) => scaffoldBullets.length >= 3,
      ),
    ).toBe(true)
  })

  it('describes which downstream stages become stale after an edit', () => {
    expect(getInvalidatedStagesAfterEdit('genre')).toEqual([
      'tone',
      'brief',
      'pitches',
      'characters',
      'beats',
      'composition',
      'audio',
      'finalize',
    ])
    expect(getInvalidatedStagesAfterEdit('beats')).toEqual([
      'composition',
      'audio',
      'finalize',
    ])
    expect(getInvalidatedStagesAfterEdit('composition')).toEqual([
      'audio',
      'finalize',
    ])
    expect(getInvalidatedStagesAfterEdit('finalize')).toEqual([])
  })

  it('resolves the resume stage to the earliest non-completed stage', () => {
    expect(
      resolveResumeStage({
        genre: 'completed',
        tone: 'completed',
        brief: 'completed',
        pitches: 'in_progress',
        characters: 'draft',
      }),
    ).toBe('pitches')

    expect(
      resolveResumeStage({
        genre: 'completed',
        tone: 'completed',
        brief: 'needs_regeneration',
        pitches: 'completed',
        characters: 'completed',
        beats: 'completed',
        story_setup: 'completed',
        composition: 'completed',
        audio: 'completed',
        finalize: 'completed',
      }),
    ).toBe('brief')

    expect(
      resolveResumeStage({
        genre: 'completed',
        tone: 'completed',
        brief: 'completed',
        pitches: 'completed',
        characters: 'completed',
        beats: 'completed',
        story_setup: 'completed',
        composition: 'completed',
        audio: 'completed',
        finalize: 'completed',
      }),
    ).toBe('finalize')
  })

  it('exposes helpers for validating and labeling stage ids', () => {
    expect(isWorkflowStageId('audio')).toBe(true)
    expect(isWorkflowStageId('not-a-stage')).toBe(false)
    expect(getWorkflowStageLabel('story_setup')).toBe('Story setup')
    expect(getWorkflowStageLabel('mystery-stage')).toBe('mystery-stage')
  })
})
