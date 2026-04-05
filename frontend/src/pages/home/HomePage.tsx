import { useDeferredValue, useId, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { buildSessionWorkspacePath } from '../../app/routePaths.ts'
import {
  type RecentSessionSummary,
  type RecentSessionsStatusFilter,
  type SessionArtifactReadiness,
} from '../../api/sessions.ts'
import { useGenreCatalogQuery } from '../../features/session/catalogQueries.ts'
import {
  type WorkflowStageId,
  type WorkflowStageState,
  workflowStageDefinitions,
} from '../../features/session/workflowStages.ts'
import {
  useCreateSessionMutation,
  useRecentSessionsQuery,
} from '../../features/session/sessionQueries.ts'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'
import {
  BlockingFeedback,
  FeedbackBanner,
  InlineSpinner,
  SkeletonBlock,
} from '../../shared/ui/feedback.tsx'
import {
  Badge,
  Button,
  Panel,
  ProgressBar,
  TextInput,
} from '../../shared/ui/primitives.tsx'
import {
  SelectField,
  type SelectFieldOption,
} from '../../shared/ui/workflow.tsx'

type SessionLoadState = 'loading' | 'ready' | 'error'

type SessionMonthGroupView = {
  key: string
  label: string
  sessions: RecentSessionSummary[]
}

const updatedAtFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  year: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

const monthGroupFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'long',
  year: 'numeric',
})

const statusFilterOptions: ReadonlyArray<SelectFieldOption> = [
  { value: 'all', label: 'All sessions' },
  { value: 'active', label: 'Drafts and active' },
  { value: 'draft', label: 'Draft only' },
  { value: 'in_progress', label: 'In progress' },
  { value: 'needs_regeneration', label: 'Needs refresh' },
  { value: 'completed', label: 'Completed stories' },
]

const activeStatuses: ReadonlyArray<WorkflowStageState> = [
  'draft',
  'in_progress',
  'needs_regeneration',
]

const defaultSessionLibrarySummary = {
  display_kind: 'draft_session',
  title_source: 'fallback',
  runtime_seconds: null,
  runtime_source: null,
  artifact_readiness: {
    story_text: 'missing',
    story_docx: 'missing',
    final_audio: 'missing',
    ready_count: 0,
    total_count: 3,
  },
} as const

function formatUpdatedAt(value: string) {
  return updatedAtFormatter.format(new Date(value))
}

function formatUpdatedMonth(value: string) {
  return monthGroupFormatter.format(new Date(value))
}

function getLibrarySummary(session: RecentSessionSummary) {
  return session.library_summary ?? defaultSessionLibrarySummary
}

function formatDurationLabel(value: number | null | undefined) {
  if (value == null || !Number.isFinite(value) || value <= 0) {
    return null
  }

  const roundedSeconds = Math.round(value)
  const minutes = Math.floor(roundedSeconds / 60)
  const seconds = roundedSeconds % 60

  if (minutes <= 0) {
    return `${seconds}s`
  }

  return `${minutes}m ${seconds.toString().padStart(2, '0')}s`
}

function getStageLabel(stageId: WorkflowStageId) {
  return (
    workflowStageDefinitions.find((stage) => stage.id === stageId)?.label ??
    stageId
  )
}

function getSessionStatusCopy(session: RecentSessionSummary) {
  const librarySummary = getLibrarySummary(session)

  if (session.overall_status === 'completed') {
    return {
      actionLabel: 'Open story',
      label:
        librarySummary.display_kind === 'polished_story'
          ? 'Polished'
          : 'Completed',
      tone: 'success' as const,
    }
  }

  if (session.overall_status === 'needs_regeneration') {
    return {
      actionLabel: 'Resume',
      label: 'Needs refresh',
      tone: 'accent' as const,
    }
  }

  if (session.overall_status === 'in_progress') {
    return {
      actionLabel: 'Resume',
      label: 'In progress',
      tone: 'brand' as const,
    }
  }

  return {
    actionLabel: 'Start',
    label: 'Draft',
    tone: 'warning' as const,
  }
}

function buildSessionKindCopy(session: RecentSessionSummary) {
  const librarySummary = getLibrarySummary(session)

  if (librarySummary.display_kind === 'polished_story') {
    return 'Polished bedtime story'
  }

  if (librarySummary.display_kind === 'completed_story') {
    return 'Completed bedtime story'
  }

  if (session.overall_status === 'needs_regeneration') {
    return 'Draft waiting for refreshed output'
  }

  if (session.overall_status === 'in_progress') {
    return 'Draft in progress'
  }

  return 'Draft session'
}

function buildSessionStageSummary(session: RecentSessionSummary) {
  const librarySummary = getLibrarySummary(session)

  if (session.overall_status === 'completed') {
    const readiness = librarySummary.artifact_readiness
    const runtimeLabel = formatDurationLabel(librarySummary.runtime_seconds)
    const parts = [
      runtimeLabel != null ? `Runtime ${runtimeLabel}` : null,
      readiness.ready_count === readiness.total_count
        ? 'All artifacts ready'
        : `${readiness.ready_count} of ${readiness.total_count} artifacts ready`,
    ].filter(Boolean)

    return parts.join(' · ') || 'Completed story ready to reopen.'
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

function buildArtifactBadgeCopy(
  label: string,
  status: SessionArtifactReadiness['final_audio'],
) {
  if (status === 'ready') {
    return `${label} ready`
  }

  if (status === 'stale') {
    return `${label} stale`
  }

  return `${label} missing`
}

function getArtifactBadgeTone(status: SessionArtifactReadiness['final_audio']) {
  if (status === 'ready') {
    return 'success' as const
  }

  if (status === 'stale') {
    return 'warning' as const
  }

  return 'neutral' as const
}

function groupSessionsByUpdatedMonth(
  sessions: RecentSessionSummary[],
): SessionMonthGroupView[] {
  const groups: SessionMonthGroupView[] = []

  for (const session of sessions) {
    const date = new Date(session.updated_at)
    const key = `${date.getFullYear()}-${date.getMonth()}`
    const label = formatUpdatedMonth(session.updated_at)
    const existingGroup = groups.at(-1)

    if (existingGroup != null && existingGroup.key === key) {
      existingGroup.sessions.push(session)
      continue
    }

    groups.push({
      key,
      label,
      sessions: [session],
    })
  }

  return groups
}

function HomePageLoadingState() {
  return (
    <Panel
      aria-busy="true"
      as="article"
      className="sessions-panel"
      description="Loading session library results from the durable backend."
      title="Session library"
    >
      <ul className="session-card-list">
        {Array.from({ length: 3 }).map((_, index) => (
          <li key={index} className="session-card session-card--loading">
            <SkeletonBlock className="loading-block--title" />
            <SkeletonBlock className="loading-block--detail" />
            <SkeletonBlock className="loading-block--detail loading-block--short" />
          </li>
        ))}
      </ul>
    </Panel>
  )
}

function HomePageErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <BlockingFeedback
      actions={
        <Button size="compact" tone="ghost" onClick={() => void onRetry()}>
          Retry
        </Button>
      }
      bannerTitle="Session library could not load"
      className="sessions-panel"
      description="The home screen could not load searchable session results from the backend. Retry once the API is reachable again."
      eyebrow="Session library"
      headingLevel={2}
      title="Could not load past sessions."
      tone="warning"
    />
  )
}

function EmptySessionsState() {
  return (
    <Panel
      as="article"
      className="sessions-panel"
      description="Your session library will fill in as soon as you start the first bedtime story."
      title="Session library"
    >
      <div className="empty-state">
        <p className="empty-state__title">No sessions yet.</p>
        <p className="body-copy">
          Start a fresh bedtime story to open the workspace and begin the first
          session.
        </p>
      </div>
    </Panel>
  )
}

function NoMatchingSessionsState({
  onClearFilters,
}: {
  onClearFilters: () => void
}) {
  return (
    <div className="empty-state sessions-empty-state">
      <p className="empty-state__title">No sessions match those filters.</p>
      <p className="body-copy">
        Try a broader title search or clear the status and genre filters to see
        more of the library.
      </p>
      <Button size="compact" tone="ghost" onClick={() => void onClearFilters()}>
        Clear filters
      </Button>
    </div>
  )
}

function SessionCard({ session }: { session: RecentSessionSummary }) {
  const statusCopy = getSessionStatusCopy(session)
  const progress = buildProgressCopy(session)
  const librarySummary = getLibrarySummary(session)
  const runtimeLabel = formatDurationLabel(librarySummary.runtime_seconds)
  const artifactReadiness = librarySummary.artifact_readiness
  const isCompleted = session.overall_status === 'completed'
  const cardClassName = [
    'session-card',
    isCompleted ? 'session-card--completed' : null,
    librarySummary.display_kind === 'polished_story'
      ? 'session-card--polished'
      : null,
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <li className={cardClassName}>
      <div className="session-card__header">
        <div>
          <p className="session-card__eyebrow">
            {buildSessionKindCopy(session)}
          </p>
          <div className="session-card__title-row">
            <h4>{session.display_title}</h4>
            <Badge tone={statusCopy.tone}>{statusCopy.label}</Badge>
          </div>
          <p className="session-card__timestamp">
            Updated {formatUpdatedAt(session.updated_at)}
            {session.completed_at != null
              ? ` · Finalized ${formatUpdatedAt(session.completed_at)}`
              : ''}
          </p>
        </div>

        <Link
          className={getButtonClassName({
            size: 'compact',
            tone: 'ghost',
          })}
          aria-label={`${statusCopy.actionLabel} ${session.display_title}`}
          to={buildSessionWorkspacePath(session.id)}
        >
          {statusCopy.actionLabel}
        </Link>
      </div>

      <div className="session-card__tag-row">
        <Badge tone="brand">
          {session.selected_genre?.label ?? 'Genre pending'}
        </Badge>
        <Badge tone="neutral">
          {session.selected_tone_profile?.label ?? 'Tone pending'}
        </Badge>
        {runtimeLabel != null ? (
          <Badge tone="success">{runtimeLabel}</Badge>
        ) : null}
      </div>

      <dl className="session-card__meta">
        <div>
          <dt>{isCompleted ? 'Story' : 'Next step'}</dt>
          <dd>{buildSessionStageSummary(session)}</dd>
        </div>
        <div>
          <dt>Genre</dt>
          <dd>{session.selected_genre?.label ?? 'Not selected yet'}</dd>
        </div>
        <div>
          <dt>Tone</dt>
          <dd>{session.selected_tone_profile?.label ?? 'Not selected yet'}</dd>
        </div>
      </dl>

      {isCompleted ? (
        <div
          aria-label={`${session.display_title} artifact readiness`}
          className="session-card__artifact-row"
        >
          <Badge tone={getArtifactBadgeTone(artifactReadiness.story_text)}>
            {buildArtifactBadgeCopy('Story text', artifactReadiness.story_text)}
          </Badge>
          <Badge tone={getArtifactBadgeTone(artifactReadiness.story_docx)}>
            {buildArtifactBadgeCopy('Word doc', artifactReadiness.story_docx)}
          </Badge>
          <Badge tone={getArtifactBadgeTone(artifactReadiness.final_audio)}>
            {buildArtifactBadgeCopy('Narration', artifactReadiness.final_audio)}
          </Badge>
        </div>
      ) : (
        <ProgressBar
          aria-label={`${session.display_title} workflow progress`}
          className="session-card__progress"
          label="Workflow progress"
          tone={
            session.overall_status === 'needs_regeneration' ? 'accent' : 'brand'
          }
          value={progress.percent}
          valueText={progress.label}
        />
      )}
    </li>
  )
}

function SessionMonthGroup({ group }: { group: SessionMonthGroupView }) {
  const headingId = useId()

  return (
    <section className="session-month-group" aria-labelledby={headingId}>
      <div className="session-month-group__header">
        <div>
          <h3 id={headingId}>{group.label}</h3>
          <p>
            {group.sessions.length} session
            {group.sessions.length === 1 ? '' : 's'} updated in this span.
          </p>
        </div>
        <Badge tone="brand">{group.sessions.length}</Badge>
      </div>

      <ul className="session-card-list">
        {group.sessions.map((session) => (
          <SessionCard key={session.id} session={session} />
        ))}
      </ul>
    </section>
  )
}

export function HomePage() {
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] =
    useState<RecentSessionsStatusFilter>('all')
  const [genreFilter, setGenreFilter] = useState('all')
  const deferredSearchQuery = useDeferredValue(searchQuery.trim())
  const genreCatalogQuery = useGenreCatalogQuery()
  const recentSessionsQuery = useRecentSessionsQuery({
    limit: 100,
    query: deferredSearchQuery,
    status: statusFilter,
    genreSlug: genreFilter === 'all' ? null : genreFilter,
  })
  const createSessionMutation = useCreateSessionMutation()

  function handleRetryLoad() {
    void recentSessionsQuery.refetch()
  }

  function handleClearFilters() {
    setSearchQuery('')
    setStatusFilter('all')
    setGenreFilter('all')
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
  const genreOptions: SelectFieldOption[] = [
    { value: 'all', label: 'All genres' },
    ...(genreCatalogQuery.data ?? []).map((genre) => ({
      value: genre.slug,
      label: genre.label,
    })),
  ]
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
  const hasActiveFilters =
    searchQuery.trim().length > 0 ||
    statusFilter !== 'all' ||
    genreFilter !== 'all'
  const groupedSessions = groupSessionsByUpdatedMonth(sessions)

  return (
    <section
      aria-label="Past sessions home screen"
      className="sessions-home"
      data-testid="sessions-home-route"
    >
      <Panel
        as="article"
        className="sessions-home__hero"
        description={
          <>
            <p className="lede">
              Search the session library, reopen polished stories, and spot the
              next draft that still needs your attention.
            </p>
            <p className="body-copy">
              Sessions stay grouped by when they were last touched so the home
              screen can scale beyond a handful of stories without turning into
              a dashboard.
            </p>
          </>
        }
        eyebrow="Past sessions"
        headingLevel={1}
        title="Return to the stories worth keeping."
        tone="hero"
      >
        <div className="session-summary-grid" aria-label="Session summary">
          <div className="session-summary-card">
            <strong>{loadState === 'ready' ? totalSessions : '...'}</strong>
            <span>
              {hasActiveFilters ? 'Matching sessions' : 'Total sessions'}
            </span>
          </div>
          <div className="session-summary-card">
            <strong>{loadState === 'ready' ? active.length : '...'}</strong>
            <span>Drafts or active work</span>
          </div>
          <div className="session-summary-card">
            <strong>{loadState === 'ready' ? completed.length : '...'}</strong>
            <span>Completed stories</span>
          </div>
        </div>

        <div className="cta-row">
          <Button
            disabled={isCreatingSession}
            onClick={() => void handleCreateSession()}
          >
            {isCreatingSession ? (
              <>
                <InlineSpinner label="Starting a new session" />
                Starting...
              </>
            ) : (
              'Start a new session'
            )}
          </Button>
          <p className="cta-note">
            New sessions still open directly into the workspace shell so the
            user can move from the library into the guided story flow without a
            blank editor step.
          </p>
        </div>
        {createError ? (
          <FeedbackBanner
            actions={
              <Button
                size="compact"
                tone="ghost"
                onClick={() => void handleCreateSession()}
              >
                Try again
              </Button>
            }
            className="sessions-home__feedback"
            description="The request failed before the workspace could open. The current library state is still intact."
            title={createError}
            tone="warning"
          />
        ) : null}
      </Panel>

      {loadState === 'loading' ? <HomePageLoadingState /> : null}
      {loadState === 'error' ? (
        <HomePageErrorState onRetry={handleRetryLoad} />
      ) : null}
      {loadState === 'ready' && totalSessions === 0 && !hasActiveFilters ? (
        <EmptySessionsState />
      ) : null}
      {loadState === 'ready' && (totalSessions > 0 || hasActiveFilters) ? (
        <Panel
          as="article"
          className="sessions-panel"
          description="Search titles, narrow by workflow status or genre, and reopen stories grouped by when they were last updated."
          title="Session library"
        >
          <div className="session-library__controls">
            <div className="session-library__filters">
              <TextInput
                className="session-library__search"
                label="Search sessions"
                onChange={(event) => setSearchQuery(event.target.value)}
                placeholder="Search by title or story idea"
                value={searchQuery}
              />
              <SelectField
                className="session-library__filter"
                label="Status"
                onChange={(event) =>
                  setStatusFilter(
                    event.target.value as RecentSessionsStatusFilter,
                  )
                }
                options={statusFilterOptions}
                value={statusFilter}
              />
              <SelectField
                className="session-library__filter"
                label="Genre"
                onChange={(event) => setGenreFilter(event.target.value)}
                options={genreOptions}
                value={genreFilter}
              />
            </div>

            <div className="session-library__results">
              <p
                aria-atomic="true"
                className="session-library__count"
                role="status"
              >
                {totalSessions} matching session
                {totalSessions === 1 ? '' : 's'}
              </p>
              {hasActiveFilters && totalSessions > 0 ? (
                <Button
                  size="compact"
                  tone="ghost"
                  onClick={() => void handleClearFilters()}
                >
                  Clear filters
                </Button>
              ) : null}
            </div>
          </div>

          {totalSessions === 0 ? (
            <NoMatchingSessionsState onClearFilters={handleClearFilters} />
          ) : (
            <div className="session-library__groups">
              {groupedSessions.map((group) => (
                <SessionMonthGroup key={group.key} group={group} />
              ))}
            </div>
          )}
        </Panel>
      ) : null}
    </section>
  )
}
