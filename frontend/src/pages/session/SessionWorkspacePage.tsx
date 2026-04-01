import { Link, useParams } from 'react-router-dom'
import {
  type SessionSnapshot,
  type SessionStageStateView,
} from '../../api/sessions.ts'
import { routePaths } from '../../app/routePaths.ts'
import {
  useCurrentSessionSnapshotQuery,
  useSessionEventStream,
  useSessionPendingActions,
} from '../../features/session/sessionWorkspaceContext.ts'
import { SessionWorkspaceProvider } from '../../features/session/SessionWorkspaceProvider.tsx'
import { workflowStageDefinitions } from '../../features/session/workflowStages.ts'
import {
  Badge,
  Panel,
  ProgressBar,
  StackedList,
  StackedListItem,
  type BadgeTone,
} from '../../shared/ui/primitives.tsx'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'

type StatusBadgeCopy = {
  label: string
  tone: BadgeTone
}

type ChatPreviewEntry = {
  body: string
  id: string
  speaker: 'assistant' | 'system' | 'user'
}

const timestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function getStageLabel(stageId: string) {
  return (
    workflowStageDefinitions.find((stage) => stage.id === stageId)?.label ??
    stageId
  )
}

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

function getChatTone(entry: ChatPreviewEntry) {
  if (entry.speaker === 'assistant') {
    return 'success' as const
  }

  if (entry.speaker === 'user') {
    return 'accent' as const
  }

  return 'brand' as const
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

function buildChatPreview(snapshot: SessionSnapshot): ChatPreviewEntry[] {
  const entries: ChatPreviewEntry[] = [
    {
      body: `Workspace ready. Resume at ${getStageLabel(snapshot.resume_stage)}.`,
      id: 'workspace-opened',
      speaker: 'system',
    },
  ]

  if (snapshot.selected_genre) {
    entries.push({
      body: `Selected genre: ${snapshot.selected_genre.label}`,
      id: 'selected-genre',
      speaker: 'user',
    })
  }

  if (snapshot.selected_tone_profile) {
    entries.push({
      body: `Selected tone: ${snapshot.selected_tone_profile.label}`,
      id: 'selected-tone',
      speaker: 'user',
    })
  }

  if (snapshot.selected_pitch) {
    entries.push({
      body: `Accepted pitch: ${snapshot.selected_pitch.title}`,
      id: 'selected-pitch',
      speaker: 'assistant',
    })
  }

  if (snapshot.active_composition_job) {
    entries.push({
      body: `Composition progress: ${Math.round(snapshot.active_composition_job.progress_percent)}%`,
      id: 'composition-job',
      speaker: 'assistant',
    })
  } else {
    entries.push({
      body: `${formatSavedAt(snapshot.updated_at)}.`,
      id: 'save-status',
      speaker: 'system',
    })
  }

  return entries.slice(0, 5)
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
          <div className="loading-block loading-block--title" />
          <div className="loading-block loading-block--detail" />
        </div>
        <div className="workspace-topbar__status">
          {Array.from({ length: 3 }).map((_, index) => (
            <div key={index} className="workspace-topbar__status-card">
              <div className="loading-block loading-block--detail loading-block--short" />
              <div className="loading-block loading-block--detail" />
            </div>
          ))}
        </div>
      </header>

      <div className="workspace-shell" aria-busy="true">
        <article className="panel workspace-pane">
          <div className="loading-block loading-block--title" />
          <div className="loading-block loading-block--detail" />
          <div className="loading-block loading-block--detail" />
          <div className="loading-block loading-block--detail loading-block--short" />
        </article>
        <article className="panel workspace-pane">
          <div className="loading-block loading-block--title" />
          <div className="loading-block loading-block--detail" />
          <div className="loading-block loading-block--detail" />
          <div className="loading-block loading-block--detail" />
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
      <Panel
        as="article"
        className="empty-state"
        description={<p className="body-copy">{errorMessage}</p>}
        eyebrow="Session workspace"
        headingLevel={1}
        title="Workspace unavailable"
      >
        <button
          className={getButtonClassName({ size: 'compact', tone: 'ghost' })}
          type="button"
          onClick={() => void onRetry()}
        >
          Retry
        </button>
        <Link
          className={getButtonClassName({ size: 'compact', tone: 'ghost' })}
          to={routePaths.home}
        >
          Return home
        </Link>
      </Panel>
    </section>
  )
}

function buildWorkspaceErrorMessage(error: Error, sessionId: string) {
  if (error.message.includes('Unexpected status code: 404')) {
    return `The session ${sessionId} could not be found in the durable store.`
  }

  return 'The workspace could not load this session right now. Try again once the backend is reachable.'
}

function SessionWorkspaceContent({ sessionId }: { sessionId: string }) {
  const snapshotQuery = useCurrentSessionSnapshotQuery()
  const pendingActions = useSessionPendingActions()
  const eventStream = useSessionEventStream()
  const snapshot = snapshotQuery.data

  if (snapshotQuery.isPending) {
    return <WorkspaceLoadingState sessionId={sessionId} />
  }

  if (snapshotQuery.isError || snapshot == null) {
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

  const currentStage =
    snapshot.stage_states.find(
      (stage) => stage.stage === snapshot.current_stage,
    ) ??
    ({
      description: '',
      label: getStageLabel(snapshot.current_stage),
      stage: snapshot.current_stage,
      status: snapshot.overall_status,
    } as SessionStageStateView)
  const currentStageStatus = getStatusBadgeCopy(currentStage.status)
  const overallStatus = getStatusBadgeCopy(snapshot.overall_status)
  const progress = buildProgressCopy(snapshot)
  const chatPreview = buildChatPreview(snapshot)
  const runtimeSummary = `${pendingActions.length} pending UI actions / ${eventStream.events.length} buffered live events`
  const runtimeConnectionLabel = getRuntimeConnectionLabel(
    eventStream.connectionState,
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
              <Badge tone={currentStageStatus.tone}>{currentStage.label}</Badge>
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

      <div className="workspace-shell" data-testid="workspace-route">
        <aside className="panel workspace-pane workspace-pane--chat">
          <div className="pane-heading">
            <div>
              <h2>Chat lane</h2>
              <p className="body-copy">
                Compact messages, action echoes, and interruption controls stay
                visible while the workflow advances.
              </p>
            </div>
            <Badge tone={getRuntimeConnectionTone(eventStream.connectionState)}>
              {runtimeConnectionLabel}
            </Badge>
          </div>

          <StackedList
            aria-label="Workspace chat preview"
            as="ol"
            className="workspace-chat-list"
          >
            {chatPreview.map((entry) => (
              <StackedListItem
                key={entry.id}
                className={`workspace-chat-message workspace-chat-message--${entry.speaker}`}
                tone={getChatTone(entry)}
              >
                <span className="workspace-chat-message__speaker">
                  {entry.speaker}
                </span>
                <p>{entry.body}</p>
              </StackedListItem>
            ))}
          </StackedList>

          <div className="workspace-chat-footer">
            <strong>Composer dock</strong>
            <p>
              Message input, quick action chips, and live agent summaries will
              anchor here in the next workflow prompts.
            </p>
            <p>{runtimeSummary}.</p>
          </div>
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
            aria-label="Workspace overview"
            className="workspace-overview-grid"
          >
            <article className="workspace-summary-card">
              <p className="workspace-summary-card__label">Progress</p>
              <ProgressBar
                aria-label={`${snapshot.display_title} workflow progress`}
                hint={`Resume at ${getStageLabel(snapshot.resume_stage)} with ${progress.percent}% of the workflow currently complete.`}
                label="Workflow progress"
                value={progress.percent}
                valueText={progress.label}
              />
            </article>

            <article className="workspace-summary-card">
              <p className="workspace-summary-card__label">Story lane</p>
              <strong>
                {snapshot.selected_genre?.label ?? 'Genre pending'} /{' '}
                {snapshot.selected_tone_profile?.label ?? 'Tone pending'}
              </strong>
              <p>{buildPlanFocusCopy(snapshot)}</p>
            </article>

            <article className="workspace-summary-card">
              <p className="workspace-summary-card__label">Production</p>
              <strong>{currentStage.label}</strong>
              <p>{buildProductionCopy(snapshot)}</p>
            </article>
          </section>

          <section className="workspace-stage-panel">
            <div className="panel-heading">
              <h2>Workflow stages</h2>
              <p>
                Stage state stays durable in the backend, so this grid can
                eventually drive edits, refreshes, and long-running job status.
              </p>
            </div>

            <ol className="workspace-stage-grid">
              {snapshot.stage_states.map((stage, index) => {
                const stageStatus = getStatusBadgeCopy(stage.status)
                const isCurrentStage = stage.stage === snapshot.current_stage

                return (
                  <li
                    key={stage.stage}
                    className={
                      isCurrentStage
                        ? 'workspace-stage-card workspace-stage-card--current'
                        : 'workspace-stage-card'
                    }
                  >
                    <div className="workspace-stage-card__header">
                      <span>{index + 1}</span>
                      <div>
                        <strong>{stage.label}</strong>
                        <p>{stage.description}</p>
                      </div>
                    </div>

                    <div className="workspace-stage-card__meta">
                      <Badge tone={stageStatus.tone}>{stageStatus.label}</Badge>
                      <p>
                        {stage.detail ??
                          stage.last_event_summary ??
                          (isCurrentStage
                            ? 'Current checkpoint for the next structured edit.'
                            : 'No durable updates yet.')}
                      </p>
                    </div>
                  </li>
                )
              })}
            </ol>
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
      <SessionWorkspaceContent sessionId={sessionId} />
    </SessionWorkspaceProvider>
  )
}
