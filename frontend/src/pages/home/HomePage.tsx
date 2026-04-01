import { Link, useNavigate } from 'react-router-dom'
import { buildSessionWorkspacePath } from '../../app/routePaths.ts'
import { type RecentSessionSummary } from '../../api/sessions.ts'
import {
  type WorkflowStageId,
  type WorkflowStageState,
  workflowStageDefinitions,
} from '../../features/session/workflowStages.ts'
import {
  useCreateSessionMutation,
  useRecentSessionsQuery,
} from '../../features/session/sessionQueries.ts'

type SessionLoadState = 'loading' | 'ready' | 'error'

const dateFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  year: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

const activeStatuses: ReadonlyArray<WorkflowStageState> = [
  'draft',
  'in_progress',
  'needs_regeneration',
]

function formatUpdatedAt(value: string) {
  return dateFormatter.format(new Date(value))
}

function getStageLabel(stageId: WorkflowStageId) {
  return (
    workflowStageDefinitions.find((stage) => stage.id === stageId)?.label ??
    stageId
  )
}

function getSessionStatusCopy(status: WorkflowStageState) {
  if (status === 'completed') {
    return {
      label: 'Complete',
      className: 'status-chip status-chip--completed',
      actionLabel: 'Review',
    }
  }

  if (status === 'needs_regeneration') {
    return {
      label: 'Needs refresh',
      className: 'status-chip status-chip--needs-regeneration',
      actionLabel: 'Resume',
    }
  }

  if (status === 'in_progress') {
    return {
      label: 'In progress',
      className: 'status-chip status-chip--in-progress',
      actionLabel: 'Resume',
    }
  }

  return {
    label: 'Ready to begin',
    className: 'status-chip status-chip--draft',
    actionLabel: 'Start',
  }
}

function buildSessionStageSummary(session: RecentSessionSummary) {
  if (session.overall_status === 'completed') {
    return 'Finished and ready to revisit.'
  }

  return `Resume at ${getStageLabel(session.resume_stage)}.`
}

function buildProgressCopy(session: RecentSessionSummary) {
  const { completed_stages: completedStages, total_stages: totalStages } =
    session.progress

  return {
    label: `${completedStages} of ${totalStages} stages complete`,
    percent: Math.round((completedStages / totalStages) * 100),
  }
}

function splitSessionsByStatus(sessions: RecentSessionSummary[]) {
  return {
    active: sessions.filter((session) =>
      activeStatuses.includes(session.overall_status),
    ),
    completed: sessions.filter(
      (session) => session.overall_status === 'completed',
    ),
  }
}

function HomePageLoadingState() {
  return (
    <article className="panel sessions-panel" aria-busy="true">
      <div className="panel-heading">
        <h2>Recent sessions</h2>
        <p>Loading recent sessions from the durable backend.</p>
      </div>

      <ul className="session-card-list">
        {Array.from({ length: 3 }).map((_, index) => (
          <li key={index} className="session-card session-card--loading">
            <div className="loading-block loading-block--title" />
            <div className="loading-block loading-block--detail" />
            <div className="loading-block loading-block--detail loading-block--short" />
          </li>
        ))}
      </ul>
    </article>
  )
}

function HomePageErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <article className="panel sessions-panel">
      <div className="panel-heading">
        <h2>Recent sessions</h2>
        <p>
          The home screen could not load prior sessions from the backend. Retry
          once the API is reachable again.
        </p>
      </div>

      <div className="empty-state">
        <p className="empty-state__title">Could not load past sessions.</p>
        <p className="body-copy">
          The list request failed before the home screen could show in-progress
          and completed stories.
        </p>
        <button
          className="ghost-link"
          type="button"
          onClick={() => void onRetry()}
        >
          Retry
        </button>
      </div>
    </article>
  )
}

function EmptySessionsState() {
  return (
    <article className="panel sessions-panel">
      <div className="panel-heading">
        <h2>Recent sessions</h2>
        <p>Your story history will appear here as soon as you create one.</p>
      </div>

      <div className="empty-state">
        <p className="empty-state__title">No sessions yet.</p>
        <p className="body-copy">
          Start a fresh bedtime story to open the workspace and begin the first
          session.
        </p>
      </div>
    </article>
  )
}

function SessionGroup({
  description,
  sessions,
  title,
}: {
  description: string
  sessions: RecentSessionSummary[]
  title: string
}) {
  return (
    <section className="session-group" aria-label={title}>
      <div className="session-group__header">
        <div>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
        <span className="status-chip status-chip--count">
          {sessions.length}
        </span>
      </div>

      <ul className="session-card-list">
        {sessions.map((session) => {
          const statusCopy = getSessionStatusCopy(session.overall_status)
          const progress = buildProgressCopy(session)

          return (
            <li key={session.id} className="session-card">
              <div className="session-card__header">
                <div>
                  <div className="session-card__title-row">
                    <h4>{session.display_title}</h4>
                    <span className={statusCopy.className}>
                      {statusCopy.label}
                    </span>
                  </div>
                  <p className="session-card__timestamp">
                    Updated {formatUpdatedAt(session.updated_at)}
                  </p>
                </div>

                <Link
                  className="ghost-link"
                  aria-label={`${statusCopy.actionLabel} ${session.display_title}`}
                  to={buildSessionWorkspacePath(session.id)}
                >
                  {statusCopy.actionLabel}
                </Link>
              </div>

              <dl className="session-card__meta">
                <div>
                  <dt>Next step</dt>
                  <dd>{buildSessionStageSummary(session)}</dd>
                </div>
                <div>
                  <dt>Genre</dt>
                  <dd>{session.selected_genre?.label ?? 'Not selected yet'}</dd>
                </div>
                <div>
                  <dt>Tone</dt>
                  <dd>
                    {session.selected_tone_profile?.label ?? 'Not selected yet'}
                  </dd>
                </div>
              </dl>

              <div className="session-card__progress">
                <div aria-hidden="true" className="session-card__progress-bar">
                  <span style={{ width: `${progress.percent}%` }} />
                </div>
                <p>{progress.label}</p>
              </div>
            </li>
          )
        })}
      </ul>
    </section>
  )
}

export function HomePage() {
  const navigate = useNavigate()
  const recentSessionsQuery = useRecentSessionsQuery()
  const createSessionMutation = useCreateSessionMutation()

  function handleRetryLoad() {
    void recentSessionsQuery.refetch()
  }

  async function handleCreateSession() {
    try {
      const session = await createSessionMutation.mutateAsync(undefined)
      navigate(buildSessionWorkspacePath(session.id))
    } catch {
      // Query state drives the visible failure message.
    }
  }

  const sessions = recentSessionsQuery.data ?? []
  const loadState: SessionLoadState = recentSessionsQuery.isPending
    ? 'loading'
    : recentSessionsQuery.isError
      ? 'error'
      : 'ready'
  const isCreatingSession = createSessionMutation.isPending
  const createError = createSessionMutation.isError
    ? 'Could not start a new session. Please try again.'
    : null
  const { active, completed } = splitSessionsByStatus(sessions)
  const totalSessions = sessions.length

  return (
    <section className="sessions-home" aria-label="Past sessions home screen">
      <article className="panel panel-hero sessions-home__hero">
        <p className="eyebrow">Past sessions</p>
        <h1>Pick up where bedtime left off.</h1>
        <p className="lede">
          Review in-progress stories, finished reads, and the next session that
          needs your attention before opening the workspace.
        </p>
        <p className="body-copy">
          The home screen is now the first meaningful route. Sessions come from
          the backend so you can tell what is underway, what is complete, and
          what should resume next.
        </p>

        <div className="session-summary-grid" aria-label="Session summary">
          <div className="session-summary-card">
            <strong>{loadState === 'ready' ? totalSessions : '...'}</strong>
            <span>Total sessions</span>
          </div>
          <div className="session-summary-card">
            <strong>{loadState === 'ready' ? active.length : '...'}</strong>
            <span>Active or needs attention</span>
          </div>
          <div className="session-summary-card">
            <strong>{loadState === 'ready' ? completed.length : '...'}</strong>
            <span>Completed stories</span>
          </div>
        </div>

        <div className="cta-row">
          <button
            className="primary-link"
            disabled={isCreatingSession}
            type="button"
            onClick={() => void handleCreateSession()}
          >
            {isCreatingSession ? 'Starting...' : 'Start a new session'}
          </button>
          <p className="cta-note">
            New sessions open directly into the workspace shell so the user can
            move from this list into the guided story flow without a blank
            editor step.
          </p>
        </div>
        {createError ? <p className="form-feedback">{createError}</p> : null}
      </article>

      {loadState === 'loading' ? <HomePageLoadingState /> : null}
      {loadState === 'error' ? (
        <HomePageErrorState onRetry={handleRetryLoad} />
      ) : null}
      {loadState === 'ready' && totalSessions === 0 ? (
        <EmptySessionsState />
      ) : null}
      {loadState === 'ready' && totalSessions > 0 ? (
        <article className="panel sessions-panel">
          <div className="panel-heading">
            <h2>Recent sessions</h2>
            <p>
              In-progress and completed stories are grouped separately so it is
              clear whether you should resume work or revisit a finished bedtime
              story.
            </p>
          </div>

          {active.length > 0 ? (
            <SessionGroup
              description="Drafts, active workflows, and sessions that need a refreshed output."
              sessions={active}
              title="Continue building"
            />
          ) : null}

          {completed.length > 0 ? (
            <SessionGroup
              description="Completed stories that are ready to open again."
              sessions={completed}
              title="Finished stories"
            />
          ) : null}
        </article>
      ) : null}
    </section>
  )
}
