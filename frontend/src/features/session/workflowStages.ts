export const WORKFLOW_STAGE_STATES = [
  'draft',
  'in_progress',
  'completed',
  'needs_regeneration',
] as const

export type WorkflowStageState = (typeof WORKFLOW_STAGE_STATES)[number]

export const workflowStageDefinitions = [
  {
    id: 'genre',
    label: 'Genre',
    description:
      'Choose the overall bedtime-story lane before the rest of the plan is shaped.',
    invalidatesOnEdit: [
      'tone',
      'brief',
      'pitches',
      'characters',
      'beats',
      'composition',
      'audio',
      'finalize',
    ],
  },
  {
    id: 'tone',
    label: 'Tone',
    description:
      'Choose the emotional texture and bedtime-safety posture for the session.',
    invalidatesOnEdit: [
      'brief',
      'pitches',
      'characters',
      'beats',
      'composition',
      'audio',
      'finalize',
    ],
  },
  {
    id: 'brief',
    label: 'Story brief',
    description:
      "Capture the user's free-form idea and any normalized planning summary derived from it.",
    invalidatesOnEdit: [
      'pitches',
      'characters',
      'beats',
      'composition',
      'audio',
      'finalize',
    ],
  },
  {
    id: 'pitches',
    label: 'Pitches',
    description:
      'Generate, compare, refine, and accept candidate story directions.',
    invalidatesOnEdit: [
      'characters',
      'beats',
      'composition',
      'audio',
      'finalize',
    ],
  },
  {
    id: 'characters',
    label: 'Characters',
    description:
      'Define the accepted character sheet that later planning and writing will reference.',
    invalidatesOnEdit: ['beats', 'composition', 'audio', 'finalize'],
  },
  {
    id: 'beats',
    label: 'Beat sheet',
    description: 'Store the accepted Save-the-Cat beat sheet for the session.',
    invalidatesOnEdit: ['composition', 'audio', 'finalize'],
  },
  {
    id: 'story_setup',
    label: 'Story setup',
    description:
      'Store soft planning targets such as word count, runtime, and chapter structure.',
    invalidatesOnEdit: ['composition', 'audio', 'finalize'],
  },
  {
    id: 'composition',
    label: 'Composition',
    description:
      'Write the story durably in segments, with room for interruption and targeted rewrites.',
    invalidatesOnEdit: ['audio', 'finalize'],
  },
  {
    id: 'audio',
    label: 'Audio',
    description:
      'Configure narration settings and generate resumable audio artifacts.',
    invalidatesOnEdit: ['finalize'],
  },
  {
    id: 'finalize',
    label: 'Finalize',
    description: 'Read, listen, review final assets, and download exports.',
    invalidatesOnEdit: [],
  },
] as const

export type WorkflowStageId = (typeof workflowStageDefinitions)[number]['id']

export const WORKFLOW_STAGE_SEQUENCE: ReadonlyArray<WorkflowStageId> =
  workflowStageDefinitions.map(({ id }) => id)

export function getInvalidatedStagesAfterEdit(
  stageId: WorkflowStageId,
): ReadonlyArray<WorkflowStageId> {
  const definition = workflowStageDefinitions.find(({ id }) => id === stageId)
  return definition?.invalidatesOnEdit ?? []
}

export function resolveResumeStage(
  stageStates: Partial<Record<WorkflowStageId, WorkflowStageState>>,
): WorkflowStageId {
  for (const stage of WORKFLOW_STAGE_SEQUENCE) {
    if (stageStates[stage] !== 'completed') {
      return stage
    }
  }

  return 'finalize'
}
