import { useState } from 'react'
import type {
  SessionSnapshot,
  StartSessionCompositionRequest,
  StoryOutlineCard,
} from '../../api/sessions.ts'
import type { SessionFeedConnectionState } from './live/sessionFeedConnection.ts'
import type { SessionCompositionStreamState } from './sessionRuntimeStore.ts'
import {
  Badge,
  Button,
  ProgressBar,
  TextArea,
} from '../../shared/ui/primitives.tsx'
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
  onReturnToPlan: () => Promise<unknown>
  onStartComposition: (body: StartSessionCompositionRequest) => Promise<unknown>
  snapshot: SessionSnapshot
}

function countWords(value: string) {
  const trimmedValue = value.trim()

  if (trimmedValue.length === 0) {
    return 0
  }

  return trimmedValue.split(/\s+/u).length
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

function buildProgressTitle(options: {
  currentSegmentIndex: number | null
  stageStatus: string
  storyText: string
  totalSegments: number | null
}) {
  if (options.stageStatus === 'completed') {
    return 'Story draft complete'
  }

  if (
    options.currentSegmentIndex != null &&
    options.totalSegments != null &&
    options.totalSegments > 0
  ) {
    return `Writing segment ${options.currentSegmentIndex} of ${options.totalSegments}`
  }

  if (options.storyText.trim().length > 0) {
    return 'Draft checkpoint recovered'
  }

  return 'Ready to write'
}

function resolveCurrentOutlineCard(
  snapshot: SessionSnapshot,
  currentSegmentIndex: number | null,
) {
  if (currentSegmentIndex == null) {
    return null
  }

  return (
    snapshot.selected_story_outline?.cards.find(
      (card) => card.position === currentSegmentIndex,
    ) ?? null
  )
}

function buildCurrentSegmentTitle(
  currentSegmentIndex: number | null,
  totalSegments: number | null,
  outlineCard: StoryOutlineCard | null,
) {
  if (outlineCard?.title) {
    return outlineCard.title
  }

  if (
    currentSegmentIndex != null &&
    totalSegments != null &&
    totalSegments > 0
  ) {
    return `Segment ${currentSegmentIndex} of ${totalSegments}`
  }

  return 'Awaiting first segment'
}

function buildCurrentSegmentDescription(options: {
  currentSegmentIndex: number | null
  outlineCard: StoryOutlineCard | null
  totalSegments: number | null
}) {
  if (options.outlineCard?.summary) {
    return options.outlineCard.summary
  }

  if (options.outlineCard?.purpose) {
    return options.outlineCard.purpose
  }

  if (
    options.currentSegmentIndex != null &&
    options.totalSegments != null &&
    options.totalSegments > 0
  ) {
    return `The manuscript is currently drafting segment ${options.currentSegmentIndex} of ${options.totalSegments}.`
  }

  return 'The first accepted outline card becomes the initial draft target once writing starts.'
}

function buildCurrentSegmentLabel(
  currentSegmentIndex: number | null,
  totalSegments: number | null,
) {
  if (
    currentSegmentIndex != null &&
    totalSegments != null &&
    totalSegments > 0
  ) {
    return `Segment ${currentSegmentIndex} of ${totalSegments}`
  }

  return 'Awaiting first segment'
}

function buildBeatLabelCopy(outlineCard: StoryOutlineCard | null) {
  if (outlineCard == null || outlineCard.beat_labels.length === 0) {
    return null
  }

  return outlineCard.beat_labels.slice(0, 3)
}

function buildEarlierAcceptedText(
  storyText: string,
  recentSegmentText: string,
) {
  const normalizedStoryText = storyText.trimEnd()
  const normalizedRecentSegmentText = recentSegmentText.trim()

  if (
    normalizedStoryText.length === 0 ||
    normalizedRecentSegmentText.length === 0 ||
    normalizedStoryText === normalizedRecentSegmentText ||
    !normalizedStoryText.endsWith(normalizedRecentSegmentText)
  ) {
    return null
  }

  const prefix = normalizedStoryText
    .slice(0, normalizedStoryText.length - normalizedRecentSegmentText.length)
    .trimEnd()

  return prefix.length > 0 ? prefix : null
}

export function CompositionStage({
  composition,
  connectionState,
  onCancelComposition,
  onPauseComposition,
  onRedirectComposition,
  onResumeComposition,
  onReturnToPlan,
  onStartComposition,
  snapshot,
}: CompositionStageProps) {
  const [redirectInstructions, setRedirectInstructions] = useState('')
  const [actionError, setActionError] = useState<string | null>(null)
  const [activeAction, setActiveAction] = useState<
    'cancel' | 'pause' | 'redirect' | 'resume' | 'returnToPlan' | 'start' | null
  >(null)

  const activeJob = snapshot.active_composition_job
  const latestJob = snapshot.latest_composition_job ?? null
  const compositionJob = activeJob ?? latestJob
  const storyText =
    composition.storyText ||
    compositionJob?.accepted_story_so_far ||
    compositionJob?.latest_partial_output ||
    ''
  const latestSegmentSummary =
    composition.latestSegmentSummary ??
    compositionJob?.latest_segment_summary ??
    null
  const interruptionRequest = compositionJob?.interruption_request ?? null
  const latestPartialOutput =
    composition.latestPartialOutput ||
    compositionJob?.latest_partial_output ||
    ''
  const recentSegmentText = latestPartialOutput || storyText
  const earlierAcceptedText = buildEarlierAcceptedText(
    storyText,
    recentSegmentText,
  )
  const progressPercent = compositionJob?.progress_percent ?? 0
  const currentSegmentIndex =
    composition.currentSegmentIndex ??
    compositionJob?.current_segment_index ??
    null
  const totalSegments =
    composition.totalSegments ?? compositionJob?.total_segments ?? null
  const stageStatus = compositionJob?.status ?? 'draft'
  const currentOutlineCard = resolveCurrentOutlineCard(
    snapshot,
    currentSegmentIndex,
  )
  const currentSegmentTitle = buildCurrentSegmentTitle(
    currentSegmentIndex,
    totalSegments,
    currentOutlineCard,
  )
  const currentSegmentDescription = buildCurrentSegmentDescription({
    currentSegmentIndex,
    outlineCard: currentOutlineCard,
    totalSegments,
  })
  const currentSegmentLabel = buildCurrentSegmentLabel(
    currentSegmentIndex,
    totalSegments,
  )
  const beatLabelCopy = buildBeatLabelCopy(currentOutlineCard)
  const draftedWordCount = countWords(storyText)
  const targetWordCount =
    snapshot.selected_story_setup?.target_word_count ?? null
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
  const canReturnToPlan =
    snapshot.selected_story_setup != null ||
    snapshot.selected_story_outline != null
  const rewriteFromSegmentIndex =
    activeJob?.current_segment_index ?? currentSegmentIndex ?? 1
  const interruptionLabel =
    interruptionRequest == null
      ? null
      : interruptionRequest.request_kind === 'pause'
        ? 'Pause queued'
        : 'Redirect queued'

  async function runAction(
    action:
      | 'cancel'
      | 'pause'
      | 'redirect'
      | 'resume'
      | 'returnToPlan'
      | 'start',
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
      <section
        aria-label="Composition stage"
        className="workspace-stage-panel composition-stage__hero"
      >
        <div className="composition-stage__hero-header">
          <div className="composition-stage__hero-copy">
            <p className="eyebrow">Composition runtime</p>
            <h3>
              {buildProgressTitle({
                currentSegmentIndex,
                stageStatus,
                storyText,
                totalSegments,
              })}
            </h3>
            <p>{buildConnectionCopy(connectionState, composition)}</p>
          </div>

          <div className="composition-stage__progress-callout">
            <strong>{Math.round(progressPercent)}%</strong>
            <span>Overall draft</span>
          </div>
        </div>

        <ProgressBar
          aria-label="Composition progress"
          className="composition-stage__progress"
          hint={
            targetWordCount != null
              ? `${draftedWordCount} words drafted so far against a soft target of about ${targetWordCount}.`
              : `${draftedWordCount} words drafted so far. Progress remains durable across reconnects and refreshes.`
          }
          label="Writing progress"
          value={progressPercent}
          valueText={`${Math.round(progressPercent)}% complete`}
        />

        <CardGrid className="workspace-stage-detail__cards" columns={3}>
          <SummaryPanel
            description={currentSegmentDescription}
            label="Current focus"
            title={currentSegmentTitle}
          />

          <SummaryPanel
            description={
              latestSegmentSummary ??
              'Each finished segment posts a durable recap here before the next segment begins.'
            }
            label="Recent recap"
            title={
              latestSegmentSummary != null
                ? 'Latest segment summary'
                : 'No recap yet'
            }
            tone={latestSegmentSummary != null ? 'accent' : 'default'}
          />

          <SummaryPanel
            description={
              beatLabelCopy != null
                ? `Beat focus: ${beatLabelCopy.join(' · ')}.`
                : targetWordCount != null
                  ? `Soft length target: about ${targetWordCount} words.`
                  : 'The accepted manuscript grows durably as each segment lands.'
            }
            label="Drafted so far"
            title={
              draftedWordCount > 0
                ? `${draftedWordCount} words`
                : 'No accepted text yet'
            }
          />
        </CardGrid>

        {actionError != null ? (
          <p className="field__error" role="alert">
            {actionError}
          </p>
        ) : null}
      </section>

      <section
        className="workspace-stage-panel composition-stage__studio"
        data-testid="composition-main-pane"
      >
        <div className="composition-stage__studio-grid">
          <section
            className="workspace-stage-panel composition-stage__surface"
            data-testid="composition-current-surface"
          >
            <div className="panel-heading composition-stage__surface-header">
              <div>
                <p className="eyebrow">Current segment</p>
                <h3>{currentSegmentTitle}</h3>
                <p>
                  {latestSegmentSummary ??
                    'The newest words stay in the foreground so you can follow the draft as it lands.'}
                </p>
              </div>

              <div className="workspace-stage-detail__badges">
                <Badge tone={getCompositionStatusTone(stageStatus)}>
                  {stageStatus.replace(/_/g, ' ')}
                </Badge>
                {interruptionLabel != null ? (
                  <Badge tone="warning">{interruptionLabel}</Badge>
                ) : null}
                <Badge
                  tone={composition.source === 'live' ? 'success' : 'neutral'}
                >
                  {composition.source === 'live'
                    ? 'Live chunks'
                    : 'Saved checkpoint'}
                </Badge>
              </div>
            </div>

            <div className="composition-stage__segment-meta">
              <span className="composition-stage__segment-pill">
                {currentSegmentLabel}
              </span>
              {beatLabelCopy?.map((label) => (
                <span className="composition-stage__beat-pill" key={label}>
                  {label}
                </span>
              ))}
            </div>

            <div className="composition-stage__manuscript-shell composition-stage__manuscript-shell--live">
              <div className="visually-hidden" aria-live="polite">
                {composition.lastChunkText ??
                  latestSegmentSummary ??
                  'Composition status updated.'}
              </div>

              {recentSegmentText.length > 0 ? (
                <div
                  className="composition-stage__manuscript"
                  data-testid="composition-manuscript"
                >
                  <pre>{recentSegmentText}</pre>
                  {activeJob != null &&
                  (activeJob.status === 'queued' ||
                    activeJob.status === 'in_progress') ? (
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
          </section>

          <aside className="workspace-stage-panel composition-stage__control-panel">
            <div className="panel-heading">
              <div>
                <h3>Writing controls</h3>
                <p>
                  Pause, resume, redirect, or step back to the plan without
                  losing the durable checkpoint.
                </p>
              </div>
            </div>

            {interruptionRequest != null ? (
              <SummaryPanel
                description={interruptionRequest.message}
                label="Pending change"
                title={interruptionLabel ?? 'Pending interruption'}
                tone="accent"
              />
            ) : null}

            <div className="composition-stage__control-grid">
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
                  disabled={activeAction != null || interruptionRequest != null}
                  onClick={() => {
                    void runAction('pause', () =>
                      onPauseComposition(activeJob.id),
                    )
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
                    void runAction('resume', () =>
                      onResumeComposition(activeJob.id),
                    )
                  }}
                  tone="primary"
                >
                  {activeAction === 'resume' ? 'Resuming...' : 'Resume writing'}
                </Button>
              ) : null}

              {canReturnToPlan ? (
                <Button
                  disabled={activeAction != null}
                  onClick={() => {
                    void runAction('returnToPlan', onReturnToPlan)
                  }}
                  tone="ghost"
                >
                  {activeAction === 'returnToPlan'
                    ? 'Opening plan...'
                    : 'Return to plan'}
                </Button>
              ) : null}

              {canCancel && activeJob != null ? (
                <Button
                  disabled={activeAction != null}
                  onClick={() => {
                    void runAction('cancel', () =>
                      onCancelComposition(activeJob.id),
                    )
                  }}
                  tone="ghost"
                >
                  {activeAction === 'cancel' ? 'Stopping...' : 'Cancel run'}
                </Button>
              ) : null}
            </div>

            <TextArea
              description="Use a concrete note such as ‘soften the midpoint, add the otter sooner, and keep the ending hushed.’"
              disabled={
                !canRedirect || activeAction != null || interruptionRequest != null
              }
              label="Rewrite guidance"
              onChange={(event) => {
                setRedirectInstructions(event.currentTarget.value)
              }}
              rows={5}
              value={redirectInstructions}
            />

            <p className="composition-stage__rewrite-note">
              {interruptionRequest != null
                ? interruptionRequest.message
                : canRedirect
                ? `A rewrite request restarts from ${currentSegmentLabel.toLowerCase()} while keeping earlier accepted pages readable.`
                : 'Rewrite requests unlock once a composition job is actively drafting.'}
            </p>

            <div className="cta-row">
              <Button
                disabled={
                  !canRedirect ||
                  redirectInstructions.trim().length === 0 ||
                  activeAction != null ||
                  interruptionRequest != null ||
                  activeJob == null
                }
                onClick={() => {
                  if (activeJob == null) {
                    return
                  }

                  void runAction('redirect', () =>
                    onRedirectComposition({
                      instructions: redirectInstructions.trim(),
                      rewriteFromSegmentIndex,
                    }),
                  )
                }}
                tone="primary"
              >
                {activeAction === 'redirect'
                  ? 'Queueing rewrite...'
                  : 'Request rewrite'}
              </Button>
            </div>
          </aside>
        </div>
      </section>

      {earlierAcceptedText != null ? (
        <section className="workspace-stage-panel composition-stage__archive">
          <div className="panel-heading">
            <div>
              <h3>Earlier accepted manuscript</h3>
              <p>
                Earlier committed text stays accessible here while the current
                segment remains in focus above.
              </p>
            </div>
          </div>

          <div
            className="composition-stage__archive-shell"
            data-testid="composition-manuscript-archive"
          >
            <pre>{earlierAcceptedText}</pre>
          </div>
        </section>
      ) : null}
    </>
  )
}
