import type {
  SessionSnapshot,
  SessionStageStateView,
} from '../../api/sessions.ts'
import {
  type WorkflowStageId,
  type WorkflowStageState,
  WORKFLOW_STAGE_SEQUENCE,
  getWorkflowStageDefinition,
  isWorkflowStageId,
} from './workflowStages.ts'

export type SessionStageAvailability = 'locked' | 'unlocked' | 'revisitable'

export type SessionWorkspaceStageView = SessionStageStateView & {
  availability: SessionStageAvailability
  index: number
  invalidatesOnEdit: ReadonlyArray<WorkflowStageId>
  isCurrent: boolean
  isSelected: boolean
  scaffoldBullets: ReadonlyArray<string>
  scaffoldSummary: string
  scaffoldTitle: string
}

function buildFallbackStageState(
  snapshot: SessionSnapshot,
  stageId: WorkflowStageId,
): SessionStageStateView {
  const definition = getWorkflowStageDefinition(stageId)
  let status: WorkflowStageState = 'draft'

  if (stageId === snapshot.current_stage) {
    status =
      snapshot.overall_status === 'completed'
        ? 'completed'
        : snapshot.overall_status
  } else if (snapshot.furthest_completed_stage != null) {
    const furthestCompletedIndex = WORKFLOW_STAGE_SEQUENCE.indexOf(
      snapshot.furthest_completed_stage,
    )
    const stageIndex = WORKFLOW_STAGE_SEQUENCE.indexOf(stageId)

    if (stageIndex <= furthestCompletedIndex) {
      status = 'completed'
    }
  }

  return {
    stage: stageId,
    label: definition?.label ?? stageId,
    description: definition?.description ?? '',
    status,
    detail: null,
  }
}

function getStageAvailability(
  stage: SessionStageStateView,
  currentStageId: WorkflowStageId,
): SessionStageAvailability {
  if (stage.status === 'completed') {
    return 'revisitable'
  }

  if (
    stage.stage === currentStageId ||
    stage.status === 'in_progress' ||
    stage.status === 'needs_regeneration'
  ) {
    return 'unlocked'
  }

  return 'locked'
}

export function resolveRequestedSessionStage(
  requestedStageId: string | null | undefined,
  currentStageId: WorkflowStageId,
): WorkflowStageId {
  if (requestedStageId != null && isWorkflowStageId(requestedStageId)) {
    return requestedStageId
  }

  return currentStageId
}

export function buildSessionWorkspaceStageViews(
  snapshot: SessionSnapshot,
  requestedStageId: string | null | undefined,
) {
  const selectedStageId = resolveRequestedSessionStage(
    requestedStageId,
    snapshot.current_stage,
  )
  const stagesById = new Map(
    snapshot.stage_states.map((stage) => [stage.stage, stage] as const),
  )

  const stageViews: SessionWorkspaceStageView[] = WORKFLOW_STAGE_SEQUENCE.map(
    (stageId, index) => {
      const definition = getWorkflowStageDefinition(stageId)
      const stage =
        stagesById.get(stageId) ?? buildFallbackStageState(snapshot, stageId)

      return {
        ...stage,
        availability: getStageAvailability(stage, snapshot.current_stage),
        description: stage.description || definition?.description || '',
        index,
        invalidatesOnEdit: definition?.invalidatesOnEdit ?? [],
        isCurrent: stageId === snapshot.current_stage,
        isSelected: stageId === selectedStageId,
        label: stage.label || definition?.label || stageId,
        scaffoldBullets: definition?.scaffoldBullets ?? [],
        scaffoldSummary: definition?.scaffoldSummary ?? '',
        scaffoldTitle: definition?.scaffoldTitle ?? stage.label,
      }
    },
  )

  const selectedStage =
    stageViews.find((stage) => stage.isSelected) ?? stageViews[0]
  const currentStage =
    stageViews.find((stage) => stage.isCurrent) ?? selectedStage

  return {
    currentStage,
    selectedStage,
    selectedStageId,
    stageViews,
  }
}
