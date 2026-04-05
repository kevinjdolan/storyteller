import { useMemo, useState } from 'react'
import type {
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { Badge, Button } from '../../shared/ui/primitives.tsx'

type PlanRevisionHistoryPanelProps = {
  disabled?: boolean
  onRestorePlanRevision: (input: {
    origin: string
    revisionNumber: number
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  snapshot: SessionSnapshot
}

type ArtifactKey =
  | 'pitch'
  | 'character_sheet'
  | 'beat_sheet'
  | 'story_setup'
  | 'story_outline'

type PlanRevisionArtifact = NonNullable<
  NonNullable<SessionSnapshot['current_plan_revision']>[ArtifactKey]
>

const artifactLabels: Record<ArtifactKey, string> = {
  pitch: 'Pitch',
  character_sheet: 'Character',
  beat_sheet: 'Beat sheet',
  story_setup: 'Setup',
  story_outline: 'Outline',
}

function humanizeArtifactList(values: string[]) {
  if (values.length === 0) {
    return 'No selection changes'
  }

  const labels = values.map(
    (value) => artifactLabels[value as ArtifactKey] ?? value,
  )
  if (labels.length === 1) {
    return labels[0]
  }
  if (labels.length === 2) {
    return `${labels[0]} and ${labels[1]}`
  }
  return `${labels.slice(0, -1).join(', ')}, and ${labels.at(-1)}`
}

function readPlanArtifacts(
  revision: NonNullable<SessionSnapshot['current_plan_revision']>,
) {
  return [
    revision.pitch,
    revision.character_sheet,
    revision.beat_sheet,
    revision.story_setup,
    revision.story_outline,
  ].filter((artifact): artifact is PlanRevisionArtifact => artifact != null)
}

function diffAgainstCurrent(
  currentRevision: NonNullable<SessionSnapshot['current_plan_revision']>,
  candidateRevision: NonNullable<SessionSnapshot['plan_revisions']>[number],
) {
  const differences: string[] = []
  const fields: ArtifactKey[] = [
    'pitch',
    'character_sheet',
    'beat_sheet',
    'story_setup',
    'story_outline',
  ]

  for (const field of fields) {
    const currentId = currentRevision[field]?.id ?? null
    const candidateId = candidateRevision[field]?.id ?? null
    if (currentId !== candidateId) {
      differences.push(field)
    }
  }

  return differences
}

export function PlanRevisionHistoryPanel({
  disabled = false,
  onRestorePlanRevision,
  snapshot,
}: PlanRevisionHistoryPanelProps) {
  const planRevisions = useMemo(
    () => snapshot.plan_revisions ?? [],
    [snapshot.plan_revisions],
  )
  const currentPlanRevision =
    snapshot.current_plan_revision ??
    planRevisions.find((revision) => revision.is_current) ??
    null
  const [pendingRevisionNumber, setPendingRevisionNumber] = useState<
    number | null
  >(null)
  const [restoreError, setRestoreError] = useState<string | null>(null)

  const earlierRevisions = useMemo(
    () => planRevisions.filter((revision) => !revision.is_current).slice(0, 5),
    [planRevisions],
  )

  if (currentPlanRevision == null) {
    return null
  }

  async function handleRestore(revisionNumber: number) {
    if (disabled || pendingRevisionNumber != null) {
      return
    }

    setRestoreError(null)
    setPendingRevisionNumber(revisionNumber)

    try {
      await onRestorePlanRevision({
        revisionNumber,
        origin: 'workspace',
      })
    } catch (error) {
      setRestoreError(
        error instanceof Error
          ? error.message
          : 'The saved plan revision could not be restored right now.',
      )
    } finally {
      setPendingRevisionNumber(null)
    }
  }

  const latestCompositionJob =
    snapshot.active_composition_job ?? snapshot.latest_composition_job ?? null
  const compositionPlanLabel =
    latestCompositionJob?.plan_revision_number != null
      ? `Composition is using plan revision ${latestCompositionJob.plan_revision_number}.`
      : 'The next composition pass will bind to the current saved plan revision.'

  return (
    <section className="workspace-stage-panel plan-revision-panel">
      <div className="plan-revision-panel__header">
        <div>
          <p className="eyebrow">Plan history</p>
          <h3>Current saved plan</h3>
          <p className="body-copy">
            {currentPlanRevision.change_summary ??
              currentPlanRevision.comparison_summary ??
              'The current pitch, character, beat, setup, and outline selections are captured here as one restorable planning snapshot.'}
          </p>
        </div>

        <div className="plan-revision-panel__badges">
          <Badge tone="accent">
            Revision {currentPlanRevision.revision_number}
          </Badge>
          {latestCompositionJob?.plan_revision_number ===
          currentPlanRevision.revision_number ? (
            <Badge tone="success">Composition aligned</Badge>
          ) : (
            <Badge tone="neutral">Ready for composition</Badge>
          )}
        </div>
      </div>

      <p className="plan-revision-panel__composition-note">
        {compositionPlanLabel}
      </p>

      <div className="plan-revision-panel__artifact-list">
        {readPlanArtifacts(currentPlanRevision).map((artifact) => (
          <div key={artifact.id} className="plan-revision-panel__artifact">
            <span>{artifact.label}</span>
            {artifact.revision_number != null ? (
              <span>Rev {artifact.revision_number}</span>
            ) : null}
          </div>
        ))}
      </div>

      {earlierRevisions.length > 0 ? (
        <ol className="plan-revision-panel__history" reversed>
          {earlierRevisions.map((revision) => {
            const differences = diffAgainstCurrent(
              currentPlanRevision,
              revision,
            )
            return (
              <li
                key={revision.id}
                className="plan-revision-panel__history-item"
              >
                <div className="plan-revision-panel__history-header">
                  <div>
                    <h4>Revision {revision.revision_number}</h4>
                    <p>
                      {revision.change_summary ??
                        revision.comparison_summary ??
                        'Saved plan snapshot.'}
                    </p>
                  </div>

                  <Button
                    disabled={
                      disabled ||
                      pendingRevisionNumber === revision.revision_number
                    }
                    onClick={() => {
                      void handleRestore(revision.revision_number)
                    }}
                    tone="secondary"
                  >
                    {pendingRevisionNumber === revision.revision_number
                      ? 'Restoring...'
                      : 'Restore'}
                  </Button>
                </div>

                <div className="plan-revision-panel__history-meta">
                  <Badge tone="neutral">
                    Compare to current: {humanizeArtifactList(differences)}
                  </Badge>
                  {revision.restored_from_revision_number != null ? (
                    <Badge tone="accent">
                      Restored from {revision.restored_from_revision_number}
                    </Badge>
                  ) : null}
                </div>
              </li>
            )
          })}
        </ol>
      ) : (
        <p className="plan-revision-panel__empty">
          More saved plan snapshots will appear here after the next accepted
          pitch, character, beat, setup, or outline change.
        </p>
      )}

      {restoreError != null ? (
        <p className="field__error" role="alert">
          {restoreError}
        </p>
      ) : null}
    </section>
  )
}
