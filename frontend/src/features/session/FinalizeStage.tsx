import { useState } from 'react'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { Badge, Button } from '../../shared/ui/primitives.tsx'
import { CardGrid, SummaryPanel } from '../../shared/ui/workflow.tsx'
import { SegmentVersionComparePanel } from './SegmentVersionComparePanel.tsx'

type FinalizeStageProps = {
  onAcceptRewrite: (jobId: string) => Promise<unknown>
  onKeepExploringRewrite: (segmentIndex: number) => void
  onRejectRewrite: (jobId: string) => Promise<unknown>
  onRestoreSegmentVersion: (
    segmentIndex: number,
    versionId: string,
  ) => Promise<unknown>
  onReturnToComposition: () => void
  snapshot: SessionSnapshot
}

export function FinalizeStage({
  onAcceptRewrite,
  onKeepExploringRewrite,
  onRejectRewrite,
  onRestoreSegmentVersion,
  onReturnToComposition,
  snapshot,
}: FinalizeStageProps) {
  const [actionError, setActionError] = useState<string | null>(null)
  const [actionState, setActionState] = useState<
    'acceptRewrite' | 'rejectRewrite' | 'restoreVersion' | null
  >(null)
  const compositionSegments = snapshot.composition_segments ?? []
  const reviewJob = snapshot.latest_composition_job?.pending_review
    ? snapshot.latest_composition_job
    : null
  const finalStoryReady = snapshot.latest_story_asset != null
  const finalAudioReady = snapshot.latest_audio_asset != null
  const activeAudioJob = snapshot.active_audio_job ?? null

  async function runAction(
    nextActionState: 'acceptRewrite' | 'rejectRewrite' | 'restoreVersion',
    operation: () => Promise<unknown>,
  ) {
    setActionState(nextActionState)
    setActionError(null)

    try {
      await operation()
    } catch (error) {
      setActionError(
        error instanceof Error
          ? error.message
          : 'The selected manuscript version could not be updated right now.',
      )
    } finally {
      setActionState(null)
    }
  }

  return (
    <>
      <section className="workspace-stage-panel finalize-stage__hero">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Final review</p>
            <h3>Read the current manuscript and compare revisions before export.</h3>
            <p>
              Finalize keeps the current draft, export readiness, and segment-level
              version history in one place so late rewrite decisions stay explicit.
            </p>
          </div>

          <div className="workspace-stage-detail__badges">
            {reviewJob != null ? <Badge tone="accent">Rewrite pending</Badge> : null}
            <Badge tone={finalStoryReady ? 'success' : 'neutral'}>
              {finalStoryReady ? 'Story export ready' : 'Story export pending'}
            </Badge>
            <Badge tone={finalAudioReady ? 'success' : 'neutral'}>
              {finalAudioReady ? 'Audio ready' : 'Audio pending'}
            </Badge>
          </div>
        </div>

        <CardGrid className="workspace-stage-detail__cards" columns={3}>
          <SummaryPanel
            description={
              reviewJob != null
                ? 'A rewrite candidate is waiting for approval before it replaces the live manuscript.'
                : 'The current manuscript is stable enough to review, listen to, and export.'
            }
            label="Manuscript status"
            title={
              reviewJob != null ? 'Rewrite requires review' : 'Current draft is active'
            }
            tone={reviewJob != null ? 'accent' : 'default'}
          />

          <SummaryPanel
            description={
              finalStoryReady
                ? 'The latest accepted manuscript has already been compiled into a durable story asset.'
                : 'Story export will become available after the next fully accepted composition state.'
            }
            label="Story asset"
            title={finalStoryReady ? 'Ready to export' : 'Export pending'}
            tone={finalStoryReady ? 'accent' : 'default'}
          />

          <SummaryPanel
            description={
              finalAudioReady
                ? 'A ready narration asset is attached to the accepted manuscript.'
                : activeAudioJob?.current_step
                  ? activeAudioJob.current_step
                : 'Narration still depends on the currently accepted text version.'
            }
            label="Audio asset"
            title={
              finalAudioReady
                ? 'Ready to listen'
                : activeAudioJob?.progress_percent != null
                  ? `Narration ${Math.round(activeAudioJob.progress_percent)}% complete`
                  : 'Narration pending'
            }
            tone={finalAudioReady ? 'accent' : activeAudioJob != null ? 'accent' : 'default'}
          />
        </CardGrid>

        <div className="cta-row">
          <Button
            onClick={() => {
              onReturnToComposition()
            }}
            tone="ghost"
          >
            Return to composition
          </Button>
        </div>
      </section>

      {compositionSegments.length > 0 ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Revision compare</h3>
              <p>
                Compare any saved segment revision against the live manuscript, then
                restore an older revision or resolve pending rewrite review from here.
              </p>
            </div>
          </div>

          <SegmentVersionComparePanel
            actionError={actionError}
            actionState={actionState}
            compareContext="finalize"
            disabled={actionState != null}
            onAcceptRewrite={(jobId) => {
              void runAction('acceptRewrite', () => onAcceptRewrite(jobId))
            }}
            onKeepExploring={(segmentIndex) => {
              onKeepExploringRewrite(segmentIndex)
            }}
            onRejectRewrite={(jobId) => {
              void runAction('rejectRewrite', () => onRejectRewrite(jobId))
            }}
            onRestoreVersion={(segmentIndex, versionId) => {
              void runAction('restoreVersion', () =>
                onRestoreSegmentVersion(segmentIndex, versionId),
              )
            }}
            reviewJob={reviewJob}
            segments={compositionSegments}
          />
        </section>
      ) : null}
    </>
  )
}
