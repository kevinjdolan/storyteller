import type { SessionSnapshot } from '../../../api/sessions.ts'
import type { SessionWorkspaceStageView } from '../sessionStageScaffold.ts'
import {
  CHAT_TO_UI_ACTION_SCHEMA_VERSION,
  getChatToUiActionDefaultPolicy,
  type ChatToUiAction,
  type ChatToUiActionBatch,
  type ChatToUiJobKind,
} from './chatToUiActions.ts'
import {
  WORKFLOW_STAGE_SEQUENCE,
  type WorkflowStageId,
  getWorkflowStageLabel,
} from '../workflowStages.ts'

export const sessionChatCommandIds = [
  'next_stage',
  'summarize_plan',
  'regenerate_pitches',
  'pause_writing',
  'resume_writing',
] as const

export type SessionChatCommandId = (typeof sessionChatCommandIds)[number]
export type SessionChatCommandSource = 'slash_command' | 'quick_action'

export type SessionExplicitChatCommand = {
  command_id: SessionChatCommandId
  source: SessionChatCommandSource
  proposed_actions: ChatToUiActionBatch
}

export type SessionChatQuickAction = {
  commandId: SessionChatCommandId
  description: string
  label: string
  slashCommand: string
}

type SessionChatCommandSubmission = {
  explicitCommand: SessionExplicitChatCommand
  message: string
}

type SessionChatCommandContext = {
  selectedStageId: WorkflowStageId
  snapshot: SessionSnapshot
}

type SessionChatCommandDefinition = {
  aliases: readonly string[]
  buildActions: (context: SessionChatCommandContext) => ChatToUiAction[]
  description: string
  id: SessionChatCommandId
  isQuickActionVisible: (context: SessionChatCommandContext) => boolean
  label: string
}

function getStageIndex(stageId: WorkflowStageId) {
  return WORKFLOW_STAGE_SEQUENCE.indexOf(stageId)
}

function getPitchStageIndex() {
  return getStageIndex('pitches')
}

function buildBatch(actions: ChatToUiAction[]): ChatToUiActionBatch {
  return {
    schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
    actions,
  }
}

function buildRequiresConfirmation(actionType: ChatToUiAction['action_type']) {
  return getChatToUiActionDefaultPolicy(actionType) === 'confirm_first'
}

function buildNavigateToStageAction(targetStage: WorkflowStageId): ChatToUiAction {
  return {
    schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
    action_type: 'navigate_to_stage',
    target_stage: targetStage,
    confidence: 1,
    rationale: `Explicit command requested navigation to ${getWorkflowStageLabel(targetStage)}.`,
    requires_confirmation: buildRequiresConfirmation('navigate_to_stage'),
    extracted_values: {},
  }
}

function buildRegeneratePitchesAction(
  snapshot: SessionSnapshot,
): ChatToUiAction {
  return {
    schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
    action_type: 'regenerate_pitches',
    target_stage: 'pitches',
    confidence: 1,
    rationale: 'Explicit command requested a fresh pitch batch.',
    requires_confirmation: buildRequiresConfirmation('regenerate_pitches'),
    extracted_values: {
      preserve_selected_pitch: snapshot.selected_pitch != null,
    },
  }
}

function buildCompositionJobAction(options: {
  actionType: 'pause_job' | 'resume_job'
  jobId?: string | null
  jobKind: ChatToUiJobKind
  reason: string
}): ChatToUiAction {
  return {
    schema_version: CHAT_TO_UI_ACTION_SCHEMA_VERSION,
    action_type: options.actionType,
    target_stage: 'composition',
    confidence: 1,
    rationale: options.reason,
    requires_confirmation: buildRequiresConfirmation(options.actionType),
    extracted_values: {
      job_kind: options.jobKind,
      job_id: options.jobId ?? null,
      reason: options.reason,
    },
  }
}

function resolveNextStageId(stageId: WorkflowStageId) {
  const stageIndex = getStageIndex(stageId)
  return WORKFLOW_STAGE_SEQUENCE[stageIndex + 1] ?? null
}

const commandDefinitions: ReadonlyArray<SessionChatCommandDefinition> = [
  {
    id: 'pause_writing',
    label: 'Pause writing',
    description: 'Ask the policy engine to pause the active composition job.',
    aliases: ['pause-writing', 'pause'],
    isQuickActionVisible: ({ snapshot }) =>
      snapshot.active_composition_job?.status === 'queued' ||
      snapshot.active_composition_job?.status === 'in_progress',
    buildActions: ({ snapshot }) => [
      buildCompositionJobAction({
        actionType: 'pause_job',
        jobId: snapshot.active_composition_job?.id,
        jobKind: 'composition',
        reason: 'Pause the active writing job from an explicit chat command.',
      }),
    ],
  },
  {
    id: 'resume_writing',
    label: 'Resume writing',
    description: 'Ask the policy engine to resume a paused composition job.',
    aliases: ['resume-writing', 'resume'],
    isQuickActionVisible: ({ snapshot }) =>
      snapshot.active_composition_job?.status === 'paused',
    buildActions: ({ snapshot }) => [
      buildCompositionJobAction({
        actionType: 'resume_job',
        jobId: snapshot.active_composition_job?.id,
        jobKind: 'composition',
        reason: 'Resume the paused writing job from an explicit chat command.',
      }),
    ],
  },
  {
    id: 'next_stage',
    label: 'Next stage',
    description: 'Open the next workflow panel in the main canvas.',
    aliases: ['next-stage', 'next'],
    isQuickActionVisible: ({ selectedStageId }) =>
      resolveNextStageId(selectedStageId) != null,
    buildActions: ({ selectedStageId }) => {
      const nextStageId = resolveNextStageId(selectedStageId)
      return nextStageId == null ? [] : [buildNavigateToStageAction(nextStageId)]
    },
  },
  {
    id: 'regenerate_pitches',
    label: 'Regenerate pitches',
    description: 'Preview a fresh pitch batch request from the current brief.',
    aliases: ['regenerate-pitches', 'regen-pitches'],
    isQuickActionVisible: ({ selectedStageId, snapshot }) =>
      Math.max(
        getStageIndex(selectedStageId),
        getStageIndex(snapshot.current_stage),
      ) >= getPitchStageIndex(),
    buildActions: ({ snapshot }) => [buildRegeneratePitchesAction(snapshot)],
  },
  {
    id: 'summarize_plan',
    label: 'Summarize plan',
    description: 'Ask the assistant for a compact summary of the saved plan.',
    aliases: ['plan', 'summary'],
    isQuickActionVisible: () => true,
    buildActions: () => [],
  },
] as const

function resolveCommandContext(options: {
  selectedStage: SessionWorkspaceStageView['stage']
  snapshot: SessionSnapshot
}): SessionChatCommandContext {
  return {
    snapshot: options.snapshot,
    selectedStageId: options.selectedStage,
  }
}

function getCommandDefinition(commandId: SessionChatCommandId) {
  return commandDefinitions.find((command) => command.id === commandId) ?? null
}

function buildCommandSubmission(
  definition: SessionChatCommandDefinition,
  context: SessionChatCommandContext,
  source: SessionChatCommandSource,
): SessionChatCommandSubmission {
  return {
    message: `/${definition.aliases[0]}`,
    explicitCommand: {
      command_id: definition.id,
      source,
      proposed_actions: buildBatch(definition.buildActions(context)),
    },
  }
}

export function buildSessionChatQuickActions(options: {
  selectedStage: SessionWorkspaceStageView['stage']
  snapshot: SessionSnapshot
}): SessionChatQuickAction[] {
  const context = resolveCommandContext(options)

  return commandDefinitions
    .filter((command) => command.isQuickActionVisible(context))
    .slice(0, 4)
    .map((command) => ({
      commandId: command.id,
      description: command.description,
      label: command.label,
      slashCommand: `/${command.aliases[0]}`,
    }))
}

export function buildSessionChatQuickActionSubmission(options: {
  commandId: SessionChatCommandId
  selectedStage: SessionWorkspaceStageView['stage']
  snapshot: SessionSnapshot
}): SessionChatCommandSubmission | null {
  const definition = getCommandDefinition(options.commandId)

  if (definition == null) {
    return null
  }

  return buildCommandSubmission(
    definition,
    resolveCommandContext(options),
    'quick_action',
  )
}

export function resolveSessionChatSlashCommand(options: {
  input: string
  selectedStage: SessionWorkspaceStageView['stage']
  snapshot: SessionSnapshot
}): SessionChatCommandSubmission | null {
  const trimmedInput = options.input.trim()

  if (!trimmedInput.startsWith('/')) {
    return null
  }

  const [rawCommand] = trimmedInput.slice(1).split(/\s+/, 1)
  const normalizedCommand = rawCommand?.toLowerCase()

  if (normalizedCommand == null || normalizedCommand.length === 0) {
    return null
  }

  const definition =
    commandDefinitions.find((command) =>
      command.aliases.includes(normalizedCommand),
    ) ?? null

  if (definition == null) {
    return null
  }

  return buildCommandSubmission(
    definition,
    resolveCommandContext(options),
    'slash_command',
  )
}

export function buildSessionChatSlashCommandHint(
  quickActions: ReadonlyArray<SessionChatQuickAction>,
) {
  if (quickActions.length === 0) {
    return null
  }

  return quickActions.map((action) => action.slashCommand).join(', ')
}
