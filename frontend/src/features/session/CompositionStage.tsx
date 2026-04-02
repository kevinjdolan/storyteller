import { useEffect, useMemo, useState } from 'react'
import type {
  CompositionSegmentView,
  CompositionSegmentVersionView,
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
import { CardGrid, SelectField, SummaryPanel } from '../../shared/ui/workflow.tsx'

type RewriteDownstreamMode = 'auto_regenerate' | 'require_confirmation'

type CompositionStageProps = {
  composition: SessionCompositionStreamState
  connectionState: SessionFeedConnectionState
  onAcceptRewrite: (jobId: string) => Promise<unknown>
  onCancelComposition: (jobId: string) => Promise<unknown>
  onPauseComposition: (jobId: string) => Promise<unknown>
  onRedirectComposition: (options: {
    instructions: string
    rewriteFromSegmentIndex?: number | null
    rewriteToSegmentIndex?: number | null
    downstreamRegenerationMode?: RewriteDownstreamMode | null
  }) => Promise<unknown>
  onResumeComposition: (jobId: string) => Promise<unknown>
  onReturnToPlan: () => Promise<unknown>
  onStartComposition: (body: StartSessionCompositionRequest) => Promise<unknown>
  snapshot: SessionSnapshot
}

type SegmentChoice = {
  index: number
  label: string
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

function buildSegmentChoices(snapshot: SessionSnapshot): SegmentChoice[] {
  const segments = snapshot.composition_segments ?? []
  if (segments.length > 0) {
    return segments.map((segment) => ({
      index: segment.segment_index,
      label:
        segment.outline_card_title != null
          ? `Segment ${segment.segment_index}: ${segment.outline_card_title}`
          : `Segment ${segment.segment_index}`,
    }))
  }

  return (snapshot.selected_story_outline?.cards ?? []).map((card) => ({
    index: card.position,
    label: `Segment ${card.position}: ${card.title}`,
  }))
}

function getSelectedSegmentVersion(
  segment: CompositionSegmentView | null,
  versionId: string | null | undefined,
) {
  if (segment == null || versionId == null) {
    return null
  }

  return segment.versions.find((version) => version.id === versionId) ?? null
}

function findLatestCurrentVersion(segment: CompositionSegmentView | null) {
  if (segment == null) {
    return null
  }

  return (
    segment.versions.find((version) => version.is_current) ??
    segment.versions[0] ??
    null
  )
}

function buildSegmentStatusLabel(segment: CompositionSegmentView) {
  if (segment.pending_version_id != null) {
    return 'Pending rewrite'
  }

  if (segment.is_stale) {
    return 'Stale downstream'
  }

  return 'Current manuscript'
}

function buildVersionLabel(version: CompositionSegmentVersionView) {
  const parts = [`Rev ${String(version.revision_number).padStart(2, '0')}`]

  if (version.acceptance_state === 'pending') {
    parts.push('Pending')
  } else if (version.is_current) {
    parts.push('Current')
  } else {
    parts.push('Archived')
  }

  return parts.join(' · ')
}

export function CompositionStage({
  composition,
  connectionState,
  onAcceptRewrite,
  onCancelComposition,
  onPauseComposition,
  onRedirectComposition,
  onResumeComposition,
  onReturnToPlan,
  onStartComposition,
  snapshot,
}: CompositionStageProps) {
  const [rewriteInstructions, setRewriteInstructions] = useState('')
  const [rewriteFromSegmentIndex, setRewriteFromSegmentIndex] = useState<
    number | null
  >(null)
  const [rewriteToSegmentIndex, setRewriteToSegmentIndex] = useState<
    number | null
  >(null)
  const [rewriteDownstreamMode, setRewriteDownstreamMode] =
    useState<RewriteDownstreamMode>('auto_regenerate')
  const [comparisonSegmentIndex, setComparisonSegmentIndex] = useState<
    number | null
  >(null)
  const [actionError, setActionError] = useState<string | null>(null)
  const [activeAction, setActiveAction] = useState<
    | 'acceptRewrite'
    | 'cancel'
    | 'pause'
    | 'redirect'
    | 'resume'
    | 'returnToPlan'
    | 'start'
    | null
  >(null)

  const activeJob = snapshot.active_composition_job
  const latestJob = snapshot.latest_composition_job ?? null
  const reviewJob = latestJob?.pending_review ? latestJob : null
  const compositionJob = activeJob ?? latestJob
  const compositionSegments = useMemo(
    () => snapshot.composition_segments ?? [],
    [snapshot.composition_segments],
  )
  const pendingReviewSegments = useMemo(
    () =>
      compositionSegments.filter((segment) => segment.pending_version_id != null),
    [compositionSegments],
  )
  const staleSegments = useMemo(
    () => compositionSegments.filter((segment) => segment.is_stale),
    [compositionSegments],
  )
  const segmentChoices = useMemo(
    () => buildSegmentChoices(snapshot),
    [snapshot],
  )
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
  const canReturnToPlan =
    snapshot.selected_story_setup != null ||
    snapshot.selected_story_outline != null
  const canRewrite =
    segmentChoices.length > 0 &&
    snapshot.selected_story_setup != null &&
    snapshot.selected_story_outline != null &&
    snapshot.selected_beat_sheet != null
  const interruptionLabel =
    interruptionRequest == null
      ? null
      : interruptionRequest.request_kind === 'pause'
        ? 'Pause queued'
        : 'Redirect queued'

  const defaultRewriteStart =
    activeJob?.current_segment_index ??
    latestJob?.stale_from_segment_index ??
    segmentChoices[0]?.index ??
    1
  const effectiveRewriteStart =
    rewriteFromSegmentIndex ?? defaultRewriteStart ?? 1
  const effectiveRewriteEnd =
    rewriteToSegmentIndex != null && rewriteToSegmentIndex >= effectiveRewriteStart
      ? rewriteToSegmentIndex
      : effectiveRewriteStart
  const downstreamSegmentCount = compositionSegments.filter(
    (segment) =>
      segment.segment_index > effectiveRewriteEnd &&
      segment.current_version_id != null,
  ).length
  const selectedComparisonSegment =
    compositionSegments.find(
      (segment) => segment.segment_index === comparisonSegmentIndex,
    ) ??
    pendingReviewSegments[0] ??
    staleSegments[0] ??
    compositionSegments[0] ??
    null
  const comparisonCurrentVersion =
    getSelectedSegmentVersion(
      selectedComparisonSegment,
      selectedComparisonSegment?.current_version_id,
    ) ?? findLatestCurrentVersion(selectedComparisonSegment)
  const comparisonPendingVersion = getSelectedSegmentVersion(
    selectedComparisonSegment,
    selectedComparisonSegment?.pending_version_id,
  )

  useEffect(() => {
    if (
      rewriteFromSegmentIndex == null ||
      !segmentChoices.some((choice) => choice.index === rewriteFromSegmentIndex)
    ) {
      setRewriteFromSegmentIndex(defaultRewriteStart)
    }
  }, [defaultRewriteStart, rewriteFromSegmentIndex, segmentChoices])

  useEffect(() => {
    if (
      rewriteToSegmentIndex == null ||
      rewriteToSegmentIndex < effectiveRewriteStart
    ) {
      setRewriteToSegmentIndex(effectiveRewriteStart)
    }
  }, [effectiveRewriteStart, rewriteToSegmentIndex])

  useEffect(() => {
    const nextComparisonSegmentIndex =
      pendingReviewSegments[0]?.segment_index ??
      staleSegments[0]?.segment_index ??
      compositionSegments[0]?.segment_index ??
      null

    if (
      comparisonSegmentIndex == null ||
      !compositionSegments.some(
        (segment) => segment.segment_index === comparisonSegmentIndex,
      )
    ) {
      setComparisonSegmentIndex(nextComparisonSegmentIndex)
    }
  }, [
    comparisonSegmentIndex,
    compositionSegments,
    pendingReviewSegments,
    staleSegments,
  ])

  async function runAction(
    action:
      | 'acceptRewrite'
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
      if (action === 'redirect' || action === 'start') {
        setRewriteInstructions('')
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
              staleSegments.length > 0
                ? `${staleSegments.length} downstream segment${staleSegments.length === 1 ? '' : 's'} need continuity refresh.`
                : beatLabelCopy != null
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
            tone={staleSegments.length > 0 ? 'accent' : 'default'}
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
                <p className="eyebrow">
                  {reviewJob != null ? 'Rewrite review' : 'Current segment'}
                </p>
                <h3>
                  {reviewJob != null && selectedComparisonSegment != null
                    ? selectedComparisonSegment.outline_card_title ??
                      `Segment ${selectedComparisonSegment.segment_index}`
                    : currentSegmentTitle}
                </h3>
                <p>
                  {reviewJob != null && comparisonPendingVersion != null
                    ? 'Compare the proposed rewrite against the current manuscript before accepting it.'
                    : latestSegmentSummary ??
                      'The newest words stay in the foreground so you can follow the draft as it lands.'}
                </p>
              </div>

              <div className="workspace-stage-detail__badges">
                <Badge tone={getCompositionStatusTone(stageStatus)}>
                  {stageStatus.replace(/_/g, ' ')}
                </Badge>
                {reviewJob != null ? (
                  <Badge tone="accent">Pending review</Badge>
                ) : null}
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
                {reviewJob != null && selectedComparisonSegment != null
                  ? `Segment ${selectedComparisonSegment.segment_index}`
                  : currentSegmentLabel}
              </span>
              {beatLabelCopy?.map((label) => (
                <span className="composition-stage__beat-pill" key={label}>
                  {label}
                </span>
              ))}
              {selectedComparisonSegment?.is_stale ? (
                <span className="composition-stage__beat-pill">
                  Stale downstream
                </span>
              ) : null}
            </div>

            <div className="composition-stage__manuscript-shell composition-stage__manuscript-shell--live">
              <div className="visually-hidden" aria-live="polite">
                {composition.lastChunkText ??
                  latestSegmentSummary ??
                  'Composition status updated.'}
              </div>

              {(
                reviewJob != null && comparisonPendingVersion?.text_content
                  ? comparisonPendingVersion.text_content
                  : recentSegmentText
              ).length > 0 ? (
                <div
                  className="composition-stage__manuscript"
                  data-testid="composition-manuscript"
                >
                  <pre>
                    {reviewJob != null && comparisonPendingVersion?.text_content
                      ? comparisonPendingVersion.text_content
                      : recentSegmentText}
                  </pre>
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
                  Pause, resume, rewrite earlier passages, or step back to the
                  plan without losing the durable checkpoint.
                </p>
              </div>
            </div>

            {reviewJob != null ? (
              <SummaryPanel
                description={
                  reviewJob.downstream_regeneration_mode ===
                    'require_confirmation' &&
                  reviewJob.stale_from_segment_index != null &&
                  reviewJob.stale_to_segment_index != null
                    ? `Accepting this rewrite keeps segments ${reviewJob.stale_from_segment_index} through ${reviewJob.stale_to_segment_index} readable but marks them stale until you regenerate them.`
                    : 'Accepting this rewrite will replace the current manuscript revisions shown in the comparison panel.'
                }
                label="Pending rewrite"
                title={`Review segments ${reviewJob.start_segment_index ?? reviewJob.current_segment_index ?? 1} to ${reviewJob.rewrite_to_segment_index ?? reviewJob.current_segment_index ?? reviewJob.start_segment_index ?? 1}`}
                tone="accent"
              />
            ) : interruptionRequest != null ? (
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

              {reviewJob != null ? (
                <Button
                  disabled={activeAction != null}
                  onClick={() => {
                    void runAction('acceptRewrite', () =>
                      onAcceptRewrite(reviewJob.id),
                    )
                  }}
                  tone="primary"
                >
                  {activeAction === 'acceptRewrite'
                    ? 'Accepting...'
                    : 'Accept rewrite'}
                </Button>
              ) : null}
            </div>

            <div className="composition-stage__rewrite-fields">
              <SelectField
                description="Pick the first written segment that should change."
                disabled={!canRewrite || activeAction != null}
                label="Rewrite from"
                onChange={(event) => {
                  const nextValue = Number(event.currentTarget.value)
                  setRewriteFromSegmentIndex(nextValue)
                  if (
                    rewriteToSegmentIndex == null ||
                    rewriteToSegmentIndex < nextValue
                  ) {
                    setRewriteToSegmentIndex(nextValue)
                  }
                }}
                options={segmentChoices.map((choice) => ({
                  label: choice.label,
                  value: String(choice.index),
                }))}
                value={String(effectiveRewriteStart)}
              />

              <SelectField
                description="Choose the last segment the rewrite should directly replace before any downstream handling kicks in."
                disabled={!canRewrite || activeAction != null}
                label="Rewrite through"
                onChange={(event) => {
                  setRewriteToSegmentIndex(Number(event.currentTarget.value))
                }}
                options={segmentChoices
                  .filter((choice) => choice.index >= effectiveRewriteStart)
                  .map((choice) => ({
                    label: choice.label,
                    value: String(choice.index),
                  }))}
                value={String(effectiveRewriteEnd)}
              />

              <SelectField
                description={
                  downstreamSegmentCount > 0
                    ? `${downstreamSegmentCount} later segment${downstreamSegmentCount === 1 ? '' : 's'} already exist after this rewrite range.`
                    : 'No written downstream text sits beyond this range yet.'
                }
                disabled={
                  downstreamSegmentCount === 0 ||
                  !canRewrite ||
                  activeAction != null
                }
                label="Downstream handling"
                onChange={(event) => {
                  setRewriteDownstreamMode(
                    event.currentTarget.value as RewriteDownstreamMode,
                  )
                }}
                options={[
                  {
                    disabled: downstreamSegmentCount === 0,
                    label:
                      downstreamSegmentCount > 0
                        ? 'Auto-regenerate downstream'
                        : 'No downstream text to refresh',
                    value: 'auto_regenerate',
                  },
                  {
                    disabled: downstreamSegmentCount === 0,
                    label: 'Require confirmation first',
                    value: 'require_confirmation',
                  },
                ]}
                value={rewriteDownstreamMode}
              />
            </div>

            <TextArea
              description="Use a concrete note such as ‘soften the midpoint, add the otter sooner, and keep the ending hushed.’"
              disabled={
                !canRewrite ||
                activeAction != null ||
                interruptionRequest != null
              }
              label="Rewrite guidance"
              onChange={(event) => {
                setRewriteInstructions(event.currentTarget.value)
              }}
              rows={5}
              value={rewriteInstructions}
            />

            <p className="composition-stage__rewrite-note">
              {interruptionRequest != null
                ? interruptionRequest.message
                : downstreamSegmentCount > 0
                  ? rewriteDownstreamMode === 'auto_regenerate'
                    ? `The rewrite will regenerate later written segments after segment ${effectiveRewriteEnd} so continuity stays aligned.`
                    : `The rewrite will stop at segment ${effectiveRewriteEnd} and later written segments will wait for confirmation before regeneration.`
                  : `The rewrite will focus on segments ${effectiveRewriteStart}${effectiveRewriteEnd > effectiveRewriteStart ? ` through ${effectiveRewriteEnd}` : ''} and leave unwritten future slots untouched.`}
            </p>

            <div className="cta-row">
              <Button
                disabled={
                  !canRewrite ||
                  rewriteInstructions.trim().length === 0 ||
                  activeAction != null ||
                  interruptionRequest != null
                }
                onClick={() => {
                  const rewritePayload = {
                    instructions: rewriteInstructions.trim(),
                    rewriteFromSegmentIndex: effectiveRewriteStart,
                    rewriteToSegmentIndex: effectiveRewriteEnd,
                    downstreamRegenerationMode:
                      downstreamSegmentCount > 0 ? rewriteDownstreamMode : null,
                  }

                  void runAction(
                    activeJob != null ? 'redirect' : 'start',
                    () =>
                      activeJob != null
                        ? onRedirectComposition(rewritePayload)
                        : onStartComposition({
                            mode: 'rewrite',
                            instructions: rewritePayload.instructions,
                            restart_from_segment_index:
                              rewritePayload.rewriteFromSegmentIndex,
                            rewrite_to_segment_index:
                              rewritePayload.rewriteToSegmentIndex,
                            downstream_regeneration_mode:
                              rewritePayload.downstreamRegenerationMode,
                            origin: 'workspace',
                          }),
                  )
                }}
                tone="primary"
              >
                {activeAction === 'redirect'
                  ? 'Queueing rewrite...'
                  : activeAction === 'start'
                    ? 'Starting rewrite...'
                    : activeJob != null
                      ? 'Queue rewrite'
                      : 'Start rewrite'}
              </Button>
            </div>
          </aside>
        </div>
      </section>

      {compositionSegments.length > 0 ? (
        <section className="workspace-stage-panel composition-stage__segments">
          <div className="panel-heading">
            <div>
              <h3>Segment revisions</h3>
              <p>
                Inspect the current manuscript, pending rewrite candidates, and
                older segment versions side by side.
              </p>
            </div>
          </div>

          <div className="composition-stage__segments-grid">
            <aside className="composition-stage__segment-list">
              {compositionSegments.map((segment) => {
                const isSelected =
                  selectedComparisonSegment?.segment_index ===
                  segment.segment_index

                return (
                  <button
                    className="composition-stage__segment-entry"
                    data-selected={isSelected || undefined}
                    key={segment.segment_index}
                    onClick={() => {
                      setComparisonSegmentIndex(segment.segment_index)
                    }}
                    type="button"
                  >
                    <div>
                      <strong>
                        {segment.outline_card_title ??
                          `Segment ${segment.segment_index}`}
                      </strong>
                      <span>{buildSegmentStatusLabel(segment)}</span>
                    </div>

                    <div className="composition-stage__segment-entry-badges">
                      {segment.pending_version_id != null ? (
                        <Badge tone="accent">Pending</Badge>
                      ) : null}
                      {segment.is_stale ? (
                        <Badge tone="warning">Stale</Badge>
                      ) : null}
                      {segment.current_version_id != null ? (
                        <Badge tone="neutral">
                          Rev {segment.current_revision_number ?? '?'}
                        </Badge>
                      ) : null}
                    </div>
                  </button>
                )
              })}
            </aside>

            <section className="composition-stage__compare-panel">
              {selectedComparisonSegment != null ? (
                <>
                  <div className="composition-stage__compare-header">
                    <div>
                      <p className="eyebrow">
                        Segment {selectedComparisonSegment.segment_index}
                      </p>
                      <h4>
                        {selectedComparisonSegment.outline_card_title ??
                          `Segment ${selectedComparisonSegment.segment_index}`}
                      </h4>
                      <p>
                        {selectedComparisonSegment.stale_reason ??
                          selectedComparisonSegment.outline_card_summary ??
                          'No stored segment summary is available yet.'}
                      </p>
                    </div>
                  </div>

                  {comparisonPendingVersion != null ? (
                    <div className="composition-stage__compare-columns">
                      <article className="composition-stage__compare-card">
                        <div className="composition-stage__compare-card-header">
                          <span>Current accepted</span>
                          {comparisonCurrentVersion != null ? (
                            <Badge tone="neutral">
                              {buildVersionLabel(comparisonCurrentVersion)}
                            </Badge>
                          ) : null}
                        </div>
                        <pre>
                          {comparisonCurrentVersion?.text_content ??
                            'No current accepted text exists for this segment yet.'}
                        </pre>
                      </article>

                      <article className="composition-stage__compare-card composition-stage__compare-card--pending">
                        <div className="composition-stage__compare-card-header">
                          <span>Pending rewrite</span>
                          <Badge tone="accent">
                            {buildVersionLabel(comparisonPendingVersion)}
                          </Badge>
                        </div>
                        <pre>{comparisonPendingVersion.text_content}</pre>
                      </article>
                    </div>
                  ) : (
                    <article className="composition-stage__compare-card">
                      <div className="composition-stage__compare-card-header">
                        <span>Current accepted</span>
                        {comparisonCurrentVersion != null ? (
                          <Badge tone="neutral">
                            {buildVersionLabel(comparisonCurrentVersion)}
                          </Badge>
                        ) : null}
                      </div>
                      <pre>
                        {comparisonCurrentVersion?.text_content ??
                          'This segment does not have accepted manuscript text yet.'}
                      </pre>
                    </article>
                  )}

                  {selectedComparisonSegment.versions.length > 1 ? (
                    <div className="composition-stage__history-list">
                      {selectedComparisonSegment.versions.map((version) => (
                        <article
                          className="composition-stage__history-card"
                          key={version.id}
                        >
                          <div className="composition-stage__history-card-header">
                            <strong>{buildVersionLabel(version)}</strong>
                            <span>{version.job_kind}</span>
                          </div>
                          <p>
                            {version.accepted_summary ??
                              version.planned_summary ??
                              'No revision summary was captured for this version.'}
                          </p>
                        </article>
                      ))}
                    </div>
                  ) : null}
                </>
              ) : (
                <div className="composition-stage__empty">
                  <p>
                    Once the first segment lands, its revision history will
                    appear here.
                  </p>
                </div>
              )}
            </section>
          </div>
        </section>
      ) : null}

      {earlierAcceptedText != null && reviewJob == null ? (
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
