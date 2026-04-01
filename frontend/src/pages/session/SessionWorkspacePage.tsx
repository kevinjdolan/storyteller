import { useEffect } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import { type SessionSnapshot } from '../../api/sessions.ts'
import { buildSessionWorkspacePath, routePaths } from '../../app/routePaths.ts'
import { SessionWorkspaceErrorBoundary } from '../../features/session/SessionWorkspaceErrorBoundary.tsx'
import { SessionStageEditorPreview } from '../../features/session/SessionStageEditorPreview.tsx'
import {
  useSessionChatMessages,
  useSessionCurrentSnapshot,
  useCurrentSessionSnapshotQuery,
  useSessionEventStream,
  useSessionPendingActions,
  useSessionRuntimeActions,
} from '../../features/session/sessionWorkspaceContext.ts'
import { SessionWorkspaceProvider } from '../../features/session/SessionWorkspaceProvider.tsx'
import { SessionChatPane } from '../../features/session/chat/SessionChatPane.tsx'
import {
  buildInitialSessionChatMessages,
  buildMockAssistantChatReply,
  createSessionChatMessage,
} from '../../features/session/chat/sessionChat.ts'
import { SessionFeedStatusIndicator } from '../../features/session/live/SessionFeedStatusIndicator.tsx'
import {
  buildSessionWorkspaceStageViews,
  type SessionWorkspaceStageView,
} from '../../features/session/sessionStageScaffold.ts'
import { getWorkflowStageLabel } from '../../features/session/workflowStages.ts'
import {
  Badge,
  ProgressBar,
  type BadgeTone,
} from '../../shared/ui/primitives.tsx'
import {
  BlockingFeedback,
  FeedbackBanner,
  InlineSpinner,
  SkeletonBlock,
  type FeedbackTone,
} from '../../shared/ui/feedback.tsx'
import {
  CardGrid,
  SelectionCard,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'

type StatusBadgeCopy = {
  label: string
  tone: BadgeTone
}

const timestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function getStatusBadgeCopy(status: string): StatusBadgeCopy {
  if (status === 'completed') {
    return {
      label: 'Complete',
      tone: 'success',
    }
  }

  if (status === 'needs_regeneration') {
    return {
      label: 'Needs refresh',
      tone: 'accent',
    }
  }

  if (status === 'in_progress') {
    return {
      label: 'In progress',
      tone: 'brand',
    }
  }

  return {
    label: 'Queued',
    tone: 'warning',
  }
}

function getRuntimeConnectionLabel(connectionState: string) {
  if (connectionState === 'open') {
    return 'Live feed connected'
  }

  if (connectionState === 'connecting' || connectionState === 'reconnecting') {
    return 'Live feed connecting'
  }

  if (connectionState === 'error') {
    return 'Live feed unavailable'
  }

  if (connectionState === 'closed') {
    return 'Live feed paused'
  }

  return 'Live feed idle'
}

function getRuntimeConnectionTone(connectionState: string): BadgeTone {
  if (connectionState === 'open') {
    return 'success'
  }

  if (connectionState === 'error') {
    return 'danger'
  }

  if (connectionState === 'closed') {
    return 'warning'
  }

  return 'brand'
}

function formatSavedAt(value: string) {
  return `Saved ${timestampFormatter.format(new Date(value))}`
}

function buildProgressCopy(snapshot: SessionSnapshot) {
  const { completed_stages: completedStages, total_stages: totalStages } =
    snapshot.progress
  const percent = Math.round((completedStages / totalStages) * 100)

  return {
    label: `${completedStages} of ${totalStages} stages complete`,
    percent,
  }
}

function getStageAvailabilityCopy(
  availability: SessionWorkspaceStageView['availability'],
): StatusBadgeCopy {
  if (availability === 'revisitable') {
    return {
      label: 'Revisitable',
      tone: 'success',
    }
  }

  if (availability === 'unlocked') {
    return {
      label: 'Unlocked',
      tone: 'brand',
    }
  }

  return {
    label: 'Locked',
    tone: 'neutral',
  }
}

function buildPlanFocusCopy(snapshot: SessionSnapshot) {
  if (snapshot.selected_pitch?.logline) {
    return snapshot.selected_pitch.logline
  }

  if (snapshot.story_brief?.normalized_summary) {
    return snapshot.story_brief.normalized_summary
  }

  if (snapshot.story_brief?.raw_brief) {
    return snapshot.story_brief.raw_brief
  }

  return 'The structured brief, pitch, and beat choices will accumulate here as the session advances.'
}

function buildProductionCopy(snapshot: SessionSnapshot) {
  if (snapshot.active_composition_job) {
    return `Writing is ${Math.round(snapshot.active_composition_job.progress_percent)}% complete.`
  }

  if (snapshot.active_audio_job) {
    const duration =
      snapshot.active_audio_job.estimated_duration_seconds != null
        ? ` Estimated length ${Math.round(snapshot.active_audio_job.estimated_duration_seconds / 60)} min.`
        : ''

    return `Audio is ${snapshot.active_audio_job.status.replace(/_/g, ' ')}.${duration}`
  }

  if (snapshot.latest_story_asset && snapshot.latest_audio_asset) {
    return 'Final reading and listening assets are already available for review.'
  }

  if (snapshot.selected_story_setup) {
    const details = [
      snapshot.selected_story_setup.target_runtime_minutes != null
        ? `~${snapshot.selected_story_setup.target_runtime_minutes} minute runtime`
        : null,
      snapshot.selected_story_setup.target_word_count != null
        ? `${snapshot.selected_story_setup.target_word_count} words`
        : null,
      snapshot.selected_story_setup.chapter_count != null
        ? `${snapshot.selected_story_setup.chapter_count} chapters`
        : null,
    ].filter(Boolean)

    if (details.length > 0) {
      return details.join(' / ')
    }
  }

  return 'Composition and audio controls will take over this area once the planning stages are complete.'
}

function buildChatActivityState(
  snapshot: SessionSnapshot,
  pendingActionsCount: number,
) {
  if (snapshot.active_audio_job != null) {
    return {
      activityLabel:
        'Narration rendering is active. The transcript remains readable while the audio pass runs.',
      disabledReason:
        'The composer is paused while audio generation is active. It will reopen after narration settles.',
      isBusy: true,
    }
  }

  if (snapshot.active_composition_job != null) {
    return {
      activityLabel: `Writing is ${Math.round(snapshot.active_composition_job.progress_percent)}% complete. Chat stays available for redirect notes.`,
      disabledReason: null,
      isBusy: true,
    }
  }

  if (pendingActionsCount > 0) {
    const suffix = pendingActionsCount === 1 ? '' : 's'

    return {
      activityLabel: `${pendingActionsCount} workspace action${suffix} still need confirmation from the live runtime feed.`,
      disabledReason: null,
      isBusy: true,
    }
  }

  return {
    activityLabel:
      'Ready for notes, approvals, and stage edits from the conversation lane.',
    disabledReason: null,
    isBusy: false,
  }
}

function buildStageDetailSummary(stage: SessionWorkspaceStageView) {
  if (stage.detail) {
    return stage.detail
  }

  if (stage.last_event_summary) {
    return stage.last_event_summary
  }

  if (stage.isCurrent) {
    return 'This is the active durable checkpoint for the next structured edit.'
  }

  if (stage.availability === 'locked') {
    return 'This panel is intentionally preview-only until the session reaches this later step.'
  }

  return 'No durable detail is saved here yet, but the scaffold is ready for future controls.'
}

function buildStageRoutingCopy(
  currentStage: SessionWorkspaceStageView,
  selectedStage: SessionWorkspaceStageView,
) {
  if (selectedStage.isCurrent) {
    return 'The route and the durable session stage are aligned. Live editors and job views can mount here later without changing the URL pattern.'
  }

  return `The route is previewing ${selectedStage.label.toLowerCase()} via the stage query parameter while the durable session state remains at ${currentStage.label.toLowerCase()}.`
}

function WorkspaceLoadingState({ sessionId }: { sessionId: string }) {
  return (
    <section
      aria-label={`Session workspace for ${sessionId}`}
      className="workspace-page"
    >
      <header className="panel workspace-topbar" aria-busy="true">
        <div className="workspace-topbar__copy">
          <p className="eyebrow">Session workspace</p>
          <SkeletonBlock className="loading-block--title" />
          <SkeletonBlock className="loading-block--detail" />
        </div>
        <div className="workspace-topbar__status">
          {Array.from({ length: 3 }).map((_, index) => (
            <div key={index} className="workspace-topbar__status-card">
              <SkeletonBlock className="loading-block--detail loading-block--short" />
              <SkeletonBlock className="loading-block--detail" />
            </div>
          ))}
        </div>
      </header>

      <div className="workspace-shell" aria-busy="true">
        <article className="panel workspace-pane">
          <SkeletonBlock className="loading-block--title" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail loading-block--short" />
        </article>
        <article className="panel workspace-pane">
          <SkeletonBlock className="loading-block--title" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail" />
        </article>
      </div>
    </section>
  )
}

function WorkspaceErrorState({
  errorMessage,
  sessionId,
  onRetry,
}: {
  errorMessage: string
  sessionId: string
  onRetry: () => void
}) {
  return (
    <section
      aria-label={`Session workspace for ${sessionId}`}
      className="workspace-page"
    >
      <BlockingFeedback
        actions={
          <div className="cta-row">
            <button
              className={getButtonClassName({
                size: 'compact',
                tone: 'ghost',
              })}
              type="button"
              onClick={() => void onRetry()}
            >
              Retry
            </button>
            <Link
              className={getButtonClassName({
                size: 'compact',
                tone: 'ghost',
              })}
              to={routePaths.home}
            >
              Return home
            </Link>
          </div>
        }
        bannerTitle="Session snapshot unavailable"
        description={errorMessage}
        eyebrow="Session workspace"
        title="Workspace unavailable"
        tone="warning"
      />
    </section>
  )
}

function buildWorkspaceErrorMessage(error: Error, sessionId: string) {
  if (error.message.includes('Unexpected status code: 404')) {
    return `The session ${sessionId} could not be found in the durable store.`
  }

  return 'The workspace could not load this session right now. Try again once the backend is reachable.'
}

function getWorkspaceConnectionBanner(connectionState: string): {
  description: string
  isBusy?: boolean
  title: string
  tone: FeedbackTone
} | null {
  if (connectionState === 'open') {
    return null
  }

  if (connectionState === 'connecting' || connectionState === 'reconnecting') {
    return {
      description:
        'The durable session shell is loaded. Live event updates are still reconnecting, so recent confirmations may take a moment to appear.',
      isBusy: true,
      title: 'Live feed reconnecting',
      tone: 'info',
    }
  }

  if (connectionState === 'error') {
    return {
      description:
        'The workspace can still render the saved snapshot, but live confirmations and background progress updates are temporarily unavailable.',
      title: 'Live feed unavailable',
      tone: 'warning',
    }
  }

  if (connectionState === 'closed') {
    return {
      description:
        'The saved session remains readable, but live runtime updates are paused until the feed reconnects.',
      title: 'Live feed paused',
      tone: 'warning',
    }
  }

  return {
    description:
      'The workspace is running from the durable snapshot only. Configure the websocket endpoint to start session-scoped live updates.',
    title: 'Live feed idle',
    tone: 'info',
  }
}

function SessionWorkspaceContent({ sessionId }: { sessionId: string }) {
  const [searchParams] = useSearchParams()
  const snapshotQuery = useCurrentSessionSnapshotQuery()
  const runtimeSnapshot = useSessionCurrentSnapshot()
  const chatMessages = useSessionChatMessages()
  const pendingActions = useSessionPendingActions()
  const eventStream = useSessionEventStream()
  const runtimeStore = useSessionRuntimeActions()
  const snapshot = runtimeSnapshot ?? snapshotQuery.data

  useEffect(() => {
    if (snapshotQuery.data == null || snapshotQuery.isError) {
      return
    }

    runtimeStore.hydrateSessionSnapshot(snapshotQuery.data)
  }, [runtimeStore, snapshotQuery.data, snapshotQuery.isError])

  useEffect(() => {
    if (snapshot == null || chatMessages.length > 0) {
      return
    }

    runtimeStore.replaceChatMessages(buildInitialSessionChatMessages(snapshot))
  }, [
    chatMessages.length,
    runtimeStore,
    snapshot,
    snapshotQuery.isError,
    snapshotQuery.isPending,
  ])

  if (snapshot == null && snapshotQuery.isPending) {
    return <WorkspaceLoadingState sessionId={sessionId} />
  }

  if (snapshot == null) {
    const errorMessage =
      snapshotQuery.error instanceof Error
        ? buildWorkspaceErrorMessage(snapshotQuery.error, sessionId)
        : 'The workspace could not load this session right now.'

    return (
      <WorkspaceErrorState
        errorMessage={errorMessage}
        sessionId={sessionId}
        onRetry={() => {
          void snapshotQuery.refetch()
        }}
      />
    )
  }

  const stageScaffold = buildSessionWorkspaceStageViews(
    snapshot,
    searchParams.get('stage'),
  )
  const selectedStage = stageScaffold.selectedStage
  const activeStage = stageScaffold.currentStage
  const stageViews = stageScaffold.stageViews
  const currentStageStatus = getStatusBadgeCopy(activeStage.status)
  const overallStatus = getStatusBadgeCopy(snapshot.overall_status)
  const progress = buildProgressCopy(snapshot)
  const runtimeConnectionLabel = getRuntimeConnectionLabel(
    eventStream.connectionState,
  )
  const chatActivityState = buildChatActivityState(
    snapshot,
    pendingActions.length,
  )
  const workspaceConnectionBanner = getWorkspaceConnectionBanner(
    eventStream.connectionState,
  )
  const selectedStageStatus = getStatusBadgeCopy(selectedStage.status)
  const selectedStageAvailability = getStageAvailabilityCopy(
    selectedStage.availability,
  )
  const stageRoutingCopy = buildStageRoutingCopy(activeStage, selectedStage)
  const selectedStageInvalidations = selectedStage.invalidatesOnEdit.map(
    getWorkflowStageLabel,
  )

  return (
    <section
      aria-label={`Session workspace for ${snapshot.display_title}`}
      className="workspace-page"
    >
      <header className="panel workspace-topbar">
        <div className="workspace-topbar__copy">
          <p className="eyebrow">Session workspace</p>
          <h1>{snapshot.display_title}</h1>
          <p className="body-copy">
            Chat and stage-driven workflow controls now share one persistent
            surface, with the left lane reserved for conversation and the right
            canvas reserved for structured editing.
          </p>
        </div>

        <dl className="workspace-topbar__status" aria-label="Session status">
          <div className="workspace-topbar__status-card">
            <dt>Current stage</dt>
            <dd>
              <Badge tone={currentStageStatus.tone}>{activeStage.label}</Badge>
            </dd>
          </div>
          <div className="workspace-topbar__status-card">
            <dt>Save status</dt>
            <dd>{formatSavedAt(snapshot.updated_at)}</dd>
          </div>
          <div className="workspace-topbar__status-card">
            <dt>Session ID</dt>
            <dd>{snapshot.id}</dd>
          </div>
          <div className="workspace-topbar__status-card">
            <dt>Live updates</dt>
            <dd>
              <SessionFeedStatusIndicator eventStream={eventStream} />
            </dd>
          </div>
        </dl>

        <div className="workspace-topbar__actions">
          <Badge tone={overallStatus.tone}>{overallStatus.label}</Badge>
          <Link
            className={getButtonClassName({ size: 'compact', tone: 'ghost' })}
            to={routePaths.home}
          >
            Return home
          </Link>
        </div>
      </header>

      {workspaceConnectionBanner != null ? (
        <FeedbackBanner
          className="workspace-page__banner"
          description={workspaceConnectionBanner.description}
          icon={
            workspaceConnectionBanner.isBusy ? (
              <InlineSpinner label="Live feed status update" />
            ) : undefined
          }
          title={workspaceConnectionBanner.title}
          tone={workspaceConnectionBanner.tone}
        />
      ) : null}

      <div className="workspace-shell" data-testid="workspace-route">
        <aside className="panel workspace-pane workspace-pane--chat">
          <SessionChatPane
            activityLabel={chatActivityState.activityLabel}
            connectionLabel={runtimeConnectionLabel}
            connectionTone={getRuntimeConnectionTone(
              eventStream.connectionState,
            )}
            disabledReason={chatActivityState.disabledReason}
            isBusy={chatActivityState.isBusy}
            messages={chatMessages}
            onSubmit={async (message) => {
              const submittedAt = new Date().toISOString()

              runtimeStore.appendChatMessage(
                createSessionChatMessage({
                  role: 'user',
                  body: message,
                  createdAt: submittedAt,
                }),
              )

              await new Promise((resolve) => {
                window.setTimeout(resolve, 260)
              })

              runtimeStore.appendChatMessage(
                buildMockAssistantChatReply(
                  message,
                  snapshot,
                  new Date().toISOString(),
                ),
              )
            }}
          />
        </aside>

        <section className="panel workspace-pane workspace-pane--canvas">
          <div className="pane-heading">
            <div>
              <h2>Workflow canvas</h2>
              <p className="body-copy">
                The main pane keeps enough width for forms, stage review, and
                later composition or audio progress views.
              </p>
            </div>
            <Badge tone={currentStageStatus.tone}>
              {currentStageStatus.label}
            </Badge>
          </div>

          <section
            aria-label="Workflow scaffold"
            className="workspace-stage-shell"
          >
            <nav
              aria-label="Stage navigator"
              className="workspace-stage-navigator"
            >
              <div className="panel-heading">
                <div>
                  <h2>Stage navigator</h2>
                  <p>
                    Every required workflow step is visible now, with URL-backed
                    panel selection that can coexist with backend-owned stage
                    truth.
                  </p>
                </div>
              </div>

              <ol className="workspace-stage-nav__list">
                {stageViews.map((stage) => {
                  const stageStatus = getStatusBadgeCopy(stage.status)
                  const availabilityCopy = getStageAvailabilityCopy(
                    stage.availability,
                  )

                  return (
                    <li key={stage.stage}>
                      <Link
                        aria-current={stage.isSelected ? 'step' : undefined}
                        className="workflow-card-link"
                        to={buildSessionWorkspacePath(snapshot.id, {
                          stage: stage.stage,
                        })}
                      >
                        <SelectionCard
                          description={stage.description}
                          eyebrow={`Stage ${(stage.index + 1)
                            .toString()
                            .padStart(2, '0')}`}
                          footer={
                            stage.isCurrent
                              ? 'This is the durable current stage saved by the backend.'
                              : stage.availability === 'locked'
                                ? 'Locked stages stay previewable without implying they are editable yet.'
                                : 'Available stages can mount richer editors later without changing the shell.'
                          }
                          leading={(stage.index + 1)
                            .toString()
                            .padStart(2, '0')}
                          meta={
                            <>
                              <Badge tone={stageStatus.tone}>
                                {stageStatus.label}
                              </Badge>
                              <Badge tone={availabilityCopy.tone}>
                                {availabilityCopy.label}
                              </Badge>
                            </>
                          }
                          selected={stage.isSelected}
                          title={stage.label}
                        />
                      </Link>
                    </li>
                  )
                })}
              </ol>
            </nav>

            <article className="workspace-stage-detail">
              <div className="workspace-stage-detail__hero">
                <div>
                  <p className="eyebrow">Stage scaffold</p>
                  <h2>{selectedStage.scaffoldTitle}</h2>
                  <p className="body-copy">{selectedStage.scaffoldSummary}</p>
                </div>

                <div className="workspace-stage-detail__badges">
                  <Badge tone={selectedStageStatus.tone}>
                    {selectedStageStatus.label}
                  </Badge>
                  <Badge tone={selectedStageAvailability.tone}>
                    {selectedStageAvailability.label}
                  </Badge>
                </div>
              </div>

              <p className="workspace-stage-detail__note">{stageRoutingCopy}</p>

              <CardGrid className="workspace-stage-detail__cards" columns={3}>
                <SummaryPanel
                  description="Accepted detail, last-event summaries, and later live job progress can all drop into the same compact summary shell."
                  label="Current session signal"
                  title={buildStageDetailSummary(selectedStage)}
                />

                <SummaryPanel
                  description="Navigator links preview a stage through routing instead of mutating the backend-owned session snapshot in the browser."
                  label="Route mapping"
                  title={
                    <span className="workspace-stage-detail__route">
                      ?stage={selectedStage.stage}
                    </span>
                  }
                />

                <SummaryPanel
                  description={
                    selectedStageInvalidations.length > 0
                      ? selectedStageInvalidations.join(', ')
                      : 'Finalize sits at the end of the workflow and can remain review-only.'
                  }
                  label="Downstream impact"
                  title={
                    selectedStageInvalidations.length > 0
                      ? `Editing this step can refresh ${selectedStageInvalidations.length} later stage${selectedStageInvalidations.length === 1 ? '' : 's'}.`
                      : 'This terminal review step does not invalidate anything later.'
                  }
                />
              </CardGrid>

              <SessionStageEditorPreview
                invalidationLabels={selectedStageInvalidations}
                selectedStage={selectedStage}
                snapshot={snapshot}
              />

              <section className="workspace-stage-detail__list">
                <div className="panel-heading">
                  <div>
                    <h3>Planned controls</h3>
                    <p>
                      These placeholder bullets mark the extension points for
                      the real business logic that will arrive in later prompts.
                    </p>
                  </div>
                </div>

                <ul>
                  {selectedStage.scaffoldBullets.map((bullet) => (
                    <li key={bullet}>{bullet}</li>
                  ))}
                </ul>
              </section>
            </article>
          </section>

          <section
            aria-label="Workspace overview"
            className="workspace-overview-grid"
          >
            <SummaryPanel label="Progress">
              <ProgressBar
                aria-label={`${snapshot.display_title} workflow progress`}
                hint={`Resume at ${getWorkflowStageLabel(snapshot.resume_stage)} with ${progress.percent}% of the workflow currently complete.`}
                label="Workflow progress"
                value={progress.percent}
                valueText={progress.label}
              />
            </SummaryPanel>

            <SummaryPanel
              description={buildPlanFocusCopy(snapshot)}
              label="Story lane"
              title={`${snapshot.selected_genre?.label ?? 'Genre pending'} / ${snapshot.selected_tone_profile?.label ?? 'Tone pending'}`}
            />

            <SummaryPanel
              description={buildProductionCopy(snapshot)}
              label="Production"
              title={activeStage.label}
            />
          </section>
        </section>
      </div>
    </section>
  )
}

export function SessionWorkspacePage() {
  const { sessionId = 'unknown-session' } = useParams()

  return (
    <SessionWorkspaceProvider key={sessionId} sessionId={sessionId}>
      <SessionWorkspaceErrorBoundary sessionId={sessionId}>
        <SessionWorkspaceContent sessionId={sessionId} />
      </SessionWorkspaceErrorBoundary>
    </SessionWorkspaceProvider>
  )
}
