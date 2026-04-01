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
    scaffoldTitle: 'Choose a bedtime genre lane',
    scaffoldSummary:
      'This panel will become the curated genre catalog, with clear guardrails about how each lane shapes the rest of the story workflow.',
    scaffoldBullets: [
      'Browse bedtime-ready genres with arc notes and calmness guardrails.',
      'Preview how each genre unlocks tone options and later planning prompts.',
      'Accept a genre from cards or chat and echo that action into session history.',
    ],
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
    scaffoldTitle: 'Tune the bedtime mood',
    scaffoldSummary:
      'Tone selection will sit on top of the chosen genre so the user can shape wonder, tension, and emotional softness before deeper planning begins.',
    scaffoldBullets: [
      'Show only tone profiles that fit the selected genre.',
      'Explain how each tone affects comfort, suspense, and read-aloud feel.',
      'Persist the accepted tone and mark downstream planning for refresh when it changes.',
    ],
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
    scaffoldTitle: 'Capture the free-form story brief',
    scaffoldSummary:
      'This stage will gather the raw bedtime-story idea, clarifications from chat, and the normalized planning summary that later stages rely on.',
    scaffoldBullets: [
      'Collect a free-form idea plus structured clarifications from chat.',
      'Surface the normalized planning summary that later stages compose against.',
      'Keep raw user wording and accepted normalized notes side by side.',
    ],
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
    scaffoldTitle: 'Review and select story pitches',
    scaffoldSummary:
      'Pitch generation will give the user multiple bedtime-suitable directions before the session commits to a single story lane.',
    scaffoldBullets: [
      'Display multiple candidate pitch cards from the planner model.',
      'Support regenerate, compare, and selective refinement loops.',
      'Persist the accepted pitch as the story lane for characters and beats.',
    ],
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
    scaffoldTitle: 'Shape the character sheet',
    scaffoldSummary:
      'The character stage will turn the accepted pitch into a durable cast sheet that later planning and writing can trust.',
    scaffoldBullets: [
      'Present character-sheet candidates with bedtime-fit notes and traits.',
      'Allow iterative edits that stay synced with the chat transcript.',
      'Store the accepted sheet as durable continuity input for composition.',
    ],
    invalidatesOnEdit: ['beats', 'composition', 'audio', 'finalize'],
  },
  {
    id: 'beats',
    label: 'Beat sheet',
    description: 'Store the accepted Save-the-Cat beat sheet for the session.',
    scaffoldTitle: 'Refine the Save-the-Cat beats',
    scaffoldSummary:
      'This panel will hold the explicit beat sheet so the bedtime arc stays structured, editable, and easy to revisit.',
    scaffoldBullets: [
      'Render the full beat outline as editable structured sections.',
      'Support softening or tightening beats without losing sequence integrity.',
      'Track accepted revisions and downstream refresh pressure on composition.',
    ],
    invalidatesOnEdit: ['composition', 'audio', 'finalize'],
  },
  {
    id: 'story_setup',
    label: 'Story setup',
    description:
      'Store soft planning targets such as word count, runtime, and chapter structure.',
    scaffoldTitle: 'Set soft story targets',
    scaffoldSummary:
      'Story setup preferences will hold the planning targets that guide pacing and length without turning them into hard constraints.',
    scaffoldBullets: [
      'Set target word count, runtime, and chapter organization as soft goals.',
      'Explain tradeoffs between length, pacing, and read-aloud experience.',
      'Keep planning preferences editable without collapsing the accepted outline.',
    ],
    invalidatesOnEdit: ['composition', 'audio', 'finalize'],
  },
  {
    id: 'composition',
    label: 'Composition',
    description:
      'Write the story durably in segments, with room for interruption and targeted rewrites.',
    scaffoldTitle: 'Write the story in segments',
    scaffoldSummary:
      'Composition will become the durable writing surface, with live progress, resumable segments, and room for mid-stream direction changes.',
    scaffoldBullets: [
      'Show durable segment-by-segment writing progress with live summaries.',
      'Support interrupts, redirects, and targeted rewrites from chat or UI.',
      'Persist partial story text often enough that refresh and resume feel safe.',
    ],
    invalidatesOnEdit: ['audio', 'finalize'],
  },
  {
    id: 'audio',
    label: 'Audio',
    description:
      'Configure narration settings and generate resumable audio artifacts.',
    scaffoldTitle: 'Configure narration and music',
    scaffoldSummary:
      'The audio stage will expose narration controls, runtime estimates, and resumable generation progress before the final listenable asset is assembled.',
    scaffoldBullets: [
      'Configure voice, speed, and optional music before narration begins.',
      'Estimate final runtime and show segment-level generation progress.',
      'Track intermediate audio artifacts and the final compiled narration asset.',
    ],
    invalidatesOnEdit: ['finalize'],
  },
  {
    id: 'finalize',
    label: 'Finalize',
    description: 'Read, listen, review final assets, and download exports.',
    scaffoldTitle: 'Read, listen, and export',
    scaffoldSummary:
      'Finalize will gather the completed reading and listening experience into one calm review surface with download actions.',
    scaffoldBullets: [
      'Provide in-app reading and listening views for the finished story.',
      'Expose download actions for the .docx export and narration audio file.',
      'Summarize the accepted plan, final assets, and any post-run notes.',
    ],
    invalidatesOnEdit: [],
  },
] as const

export type WorkflowStageId = (typeof workflowStageDefinitions)[number]['id']
export type WorkflowStageDefinition = (typeof workflowStageDefinitions)[number]

export const WORKFLOW_STAGE_SEQUENCE: ReadonlyArray<WorkflowStageId> =
  workflowStageDefinitions.map(({ id }) => id)

export function isWorkflowStageId(value: string): value is WorkflowStageId {
  return WORKFLOW_STAGE_SEQUENCE.includes(value as WorkflowStageId)
}

export function getWorkflowStageDefinition(
  stageId: string,
): WorkflowStageDefinition | undefined {
  return workflowStageDefinitions.find(({ id }) => id === stageId)
}

export function getWorkflowStageLabel(stageId: string) {
  return getWorkflowStageDefinition(stageId)?.label ?? stageId
}

export function getInvalidatedStagesAfterEdit(
  stageId: WorkflowStageId,
): ReadonlyArray<WorkflowStageId> {
  const definition = getWorkflowStageDefinition(stageId)
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
