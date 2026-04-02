import { useState } from 'react'
import type {
  SessionSnapshot,
  StartSessionCompositionRequest,
} from '../../api/sessions.ts'
import type { SessionFeedConnectionState } from './live/sessionFeedConnection.ts'
import type { SessionCompositionStreamState } from './sessionRuntimeStore.ts'
import { Badge, Button, ProgressBar, TextArea } from '../../shared/ui/primitives.tsx'
import { CardGrid, SummaryPanel } from '../../shared/ui/workflow.tsx'

type CompositionStageProps = {
  composition: SessionCompositionStreamState
  connectionState: SessionFeedConnectionState
  onCancelComposition: (jobId: string) => Promise<unknown>
  onPauseComposition: (jobId: string) => Promise<unknown>
  onRedirectComposition: (options: {
    instructions: string
    rewriteFromSegmentIndex?: number | null
  }) => Promise<unknown>
  onResumeComposition: (jobId: string) => Promise<unknown>
  onStartComposition: (body: StartSessionCompositionRequest) => Promise<unknown>
  snapshot: SessionSnapshot
}

function getCompositionStatusTone(status: string | null) {
  if (status === 'completed') {
    return 'success'
  }

  if (status === 'failed' || status === 'cancelled') {
    return 'danger'
  }

  if (status === 'paused') {
    return 'warning'
  }

  if (status === 'queued' || status === 'in_progress') {
    return 'brand'
  }

  return 'neutral'
}

function buildConnectionCopy(
  connectionState: SessionFeedConnectionState,
  composition: SessionCompositionStreamState,
) {
  if (connectionState === 'open') {
    return composition.source === 'live'
      ? 'Live chunks are arriving from the session feed.'
      : 'Live updates are connected. The manuscript is showing the latest saved checkpoint.'
  }

  if (connectionState === 'connecting' || connectionState === 'reconnecting') {
    return 'Reconnecting the live writing feed. The saved checkpoint remains visible.'
  }

  if (connectionState === 'error' || connectionState === 'closed') {
    return 'Live updates are unavailable. The saved checkpoint stays readable until the feed returns.'
  }

  return 'The stage is ready to stream as soon as writing begins.'
}

export function CompositionStage({
  composition,
  connectionState,
  onCancelComposition,
  onPauseComposition,
  onRedirectComposition,
  onResumeComposition,
  onStartComposition,
  snapshot,
}: CompositionStageProps) {
  const [redirectInstructions, setRedirectInstructions] = useState('')
  const [actionError, setActionError] = useState<string | null>(null)
  const [activeAction, setActiveAction] = useState<
    'cancel' | 'pause' | 'redirect' | 'resume' | 'start' | null
  >(null)

  const activeJob = snapshot.active_composition_job
  const latestJob = snapshot.latest_composition_job ?? null
  const compositionJob = activeJob ?? latestJob
  const storyText =
    composition.storyText ||
    compositionJob?.accepted_story_so_far ||
    compositionJob?.latest_partial_output ||
    ''
  const latestSummary =
    composition.latestSegmentSummary ?? compositionJob?.latest_segment_summary ?? null
  const progressPercent = compositionJob?.progress_percent ?? 0
  const currentSegmentIndex =
    composition.currentSegmentIndex ?? compositionJob?.current_segment_index ?? null
  const totalSegments =
    composition.totalSegments ?? compositionJob?.total_segments ?? null
  const canStart =
    snapshot.selected_story_setup != null &&
    snapshot.selected_story_outline != null &&
    snapshot.selected_beat_sheet != null &&
    activeJob == null &&
    latestJob?.status !== 'completed' &&
    latestJob?.status !== 'paused'
  const canPause =
    activeJob != null &&
    (activeJob.status === 'queued' || activeJob.status === 'in_progress')
  const canResume = activeJob != null && activeJob.status === 'paused'
  const canCancel = activeJob != null
  const canRedirect = activeJob != null
  const stageStatus = compositionJob?.status ?? 'draft'

  async function runAction(
    action: 'cancel' | 'pause' | 'redirect' | 'resume' | 'start',
    operation: () => Promise<unknown>,
  ) {
    setActiveAction(action)
    setActionError(null)

    try {
      await operation()
      if (action === 'redirect') {
        setRedirectInstructions('')
      }
    } catch (error) {
      setActionError(
        error instanceof Error
          ? error.message
          : 'The writing control could not be applied right now.',
      )
    } finally {
      setActiveAction(null)
    }
  }

  return (
    <>
      <section aria-label="Composition stage" className="workspace-stage-panel">
        <CardGrid className="workspace-stage-detail__cards" columns={3}>
          <SummaryPanel
            description={buildConnectionCopy(connectionState, composition)}
            label="Runtime status"
            title={
              <span className="composition-stage__status">
                <Badge tone={getCompositionStatusTone(stageStatus)}>
                  {stageStatus.replace(/_/g, ' ')}
                </Badge>
              </span>
            }
          />

          <SummaryPanel
            description={
              currentSegmentIndex != null && totalSegments != null
                ? `Segment ${currentSegmentIndex} of ${totalSegments} is the current drafting focus.`
                : 'The outline cards become durable writing segments once composition starts.'
            }
            label="Segment pointer"
            title={
              currentSegmentIndex != null && totalSegments != null
                ? `Segment ${currentSegmentIndex} / ${totalSegments}`
                : 'Awaiting first segment'
            }
          />

          <SummaryPanel
            description={
              latestSummary ??
              'Each completed segment posts a compact recap here before the next segment begins.'
            }
            label="Latest recap"
            title={latestSummary != null ? 'Segment summary ready' : 'No recap yet'}
            tone={latestSummary != null ? 'accent' : 'default'}
          />
        </CardGrid>

        <ProgressBar
          aria-label="Composition progress"
          hint={
            currentSegmentIndex != null && totalSegments != null
              ? `Live text should keep pacing ahead of a normal reading speed while staying readable.`
              : 'Progress stays durable so a reconnect can recover the latest accepted checkpoint.'
          }
          label="Writing progress"
          value={progressPercent}
          valueText={`${Math.round(progressPercent)}%`}
        />

        {actionError != null ? (
          <p className="field__error" role="alert">
            {actionError}
          </p>
        ) : null}
      </section>

      <section className="workspace-stage-panel composition-stage__panel">
        <div className="panel-heading">
          <div>
            <h3>Live manuscript</h3>
            <p>
              This surface renders the saved draft-so-far immediately, then
              appends live chunks as the worker advances through the current
              segment.
            </p>
          </div>

          <div className="workspace-stage-detail__badges">
            <Badge tone={getCompositionStatusTone(stageStatus)}>
              {stageStatus.replace(/_/g, ' ')}
            </Badge>
            <Badge tone={composition.source === 'live' ? 'success' : 'neutral'}>
              {composition.source === 'live' ? 'Live chunks' : 'Saved checkpoint'}
            </Badge>
          </div>
        </div>

        <div className="composition-stage__manuscript-shell">
          <div className="visually-hidden" aria-live="polite">
            {composition.lastChunkText ?? latestSummary ?? 'Composition status updated.'}
          </div>

          {storyText.length > 0 ? (
            <div
              className="composition-stage__manuscript"
              data-testid="composition-manuscript"
            >
              <pre>{storyText}</pre>
              {activeJob != null &&
              (activeJob.status === 'queued' || activeJob.status === 'in_progress') ? (
                <span
                  aria-hidden="true"
                  className="composition-stage__cursor"
                />
              ) : null}
            </div>
          ) : (
            <div className="composition-stage__empty">
              <p>
                Composition has not started yet. Once the worker begins, the
                story will type itself into this panel a chunk at a time.
              </p>
            </div>
          )}
        </div>

        <div className="cta-row composition-stage__actions">
          {canStart ? (
            <Button
              disabled={activeAction != null}
              onClick={() => {
                void runAction('start', () =>
                  onStartComposition({
                    mode: latestJob != null ? 'continue' : 'fresh',
                    origin: 'workspace',
                  }),
                )
              }}
              tone="primary"
            >
              {activeAction === 'start'
                ? 'Starting...'
                : latestJob != null
                  ? 'Continue writing'
                  : 'Start writing'}
            </Button>
          ) : null}

          {canPause && activeJob != null ? (
            <Button
              disabled={activeAction != null}
              onClick={() => {
                void runAction('pause', () => onPauseComposition(activeJob.id))
              }}
              tone="ghost"
            >
              {activeAction === 'pause' ? 'Pausing...' : 'Pause writing'}
            </Button>
          ) : null}

          {canResume && activeJob != null ? (
            <Button
              disabled={activeAction != null}
              onClick={() => {
                void runAction('resume', () => onResumeComposition(activeJob.id))
              }}
              tone="primary"
            >
              {activeAction === 'resume' ? 'Resuming...' : 'Resume writing'}
            </Button>
          ) : null}

          {canCancel && activeJob != null ? (
            <Button
              disabled={activeAction != null}
              onClick={() => {
                void runAction('cancel', () => onCancelComposition(activeJob.id))
              }}
              tone="ghost"
            >
              {activeAction === 'cancel' ? 'Stopping...' : 'Cancel run'}
            </Button>
          ) : null}
        </div>
      </section>

      <section className="workspace-stage-panel composition-stage__panel">
        <div className="panel-heading">
          <div>
            <h3>Redirect and rewrite</h3>
            <p>
              Mid-stream changes create a rewrite pass from the current segment
              so the feed can keep moving without pretending earlier text stayed
              authoritative.
            </p>
          </div>
        </div>

        <TextArea
          description="Use a concrete note such as ‘soften the midpoint, add the otter sooner, and keep the ending hushed.’"
          disabled={!canRedirect || activeAction != null}
          label="Rewrite guidance"
          onChange={(event) => {
            setRedirectInstructions(event.currentTarget.value)
          }}
          rows={4}
          value={redirectInstructions}
        />

        <div className="cta-row">
          <Button
            disabled={
              !canRedirect ||
              redirectInstructions.trim().length === 0 ||
              activeAction != null ||
              activeJob == null
            }
            onClick={() => {
              if (activeJob == null) {
                return
              }

              void runAction('redirect', () =>
                onRedirectComposition({
                  instructions: redirectInstructions.trim(),
                  rewriteFromSegmentIndex: activeJob.current_segment_index ?? 1,
                }),
              )
            }}
            tone="primary"
          >
            {activeAction === 'redirect'
              ? 'Queueing rewrite...'
              : 'Rewrite from current segment'}
          </Button>
        </div>
      </section>
    </>
  )
}
