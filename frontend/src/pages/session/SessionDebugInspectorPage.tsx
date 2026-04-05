import { Link, useParams } from 'react-router-dom'
import type {
  AudioJobView,
  CompositionJobView,
  SessionArtifactInventoryItemView,
  SessionDebugInspector,
  SessionHistoryEvent,
  SessionUsageBucketSummaryView,
} from '../../api/sessions.ts'
import { buildSessionWorkspacePath, routePaths } from '../../app/routePaths.ts'
import { useSessionDebugInspectorQuery } from '../../features/session/sessionQueries.ts'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'
import { BlockingFeedback, InlineSpinner } from '../../shared/ui/feedback.tsx'
import {
  Badge,
  Button,
  Panel,
  StackedList,
  StackedListItem,
} from '../../shared/ui/primitives.tsx'
import { CardGrid } from '../../shared/ui/workflow.tsx'

const timestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

const currencyFormatter = new Intl.NumberFormat(undefined, {
  currency: 'USD',
  maximumFractionDigits: 4,
  minimumFractionDigits: 2,
  style: 'currency',
})

function formatTimestamp(value?: string | null) {
  if (value == null || value.length === 0) {
    return 'Not recorded'
  }

  return timestampFormatter.format(new Date(value))
}

function formatCurrency(value?: number | null) {
  if (value == null) {
    return 'Unavailable'
  }

  return currencyFormatter.format(value)
}

function formatCount(value?: number | null) {
  if (value == null) {
    return 'Unavailable'
  }

  return new Intl.NumberFormat().format(value)
}

function formatDuration(value?: number | null) {
  if (value == null) {
    return 'Unavailable'
  }

  if (value < 1000) {
    return `${Math.round(value)} ms`
  }

  return `${(value / 1000).toFixed(2)} s`
}

function getStatusTone(status: string) {
  if (status === 'completed' || status === 'ready' || status === 'succeeded') {
    return 'success' as const
  }

  if (status === 'failed' || status === 'cancelled') {
    return 'danger' as const
  }

  if (status === 'stale' || status === 'needs_regeneration') {
    return 'warning' as const
  }

  if (status === 'in_progress' || status === 'generating') {
    return 'brand' as const
  }

  return 'neutral' as const
}

function renderJobSummary(
  job: CompositionJobView | AudioJobView | null | undefined,
  label: string,
) {
  if (job == null) {
    return (
      <StackedListItem>
        <strong>{label}</strong>
        <p className="body-copy">
          No active or latest job is recorded right now.
        </p>
      </StackedListItem>
    )
  }

  const detail =
    'current_step' in job
      ? job.current_step
      : (job.error_message ??
        job.stop_reason ??
        ('latest_segment_summary' in job ? job.latest_segment_summary : null))

  return (
    <StackedListItem>
      <div className="debug-inspector__row">
        <strong>{label}</strong>
        <Badge tone={getStatusTone(job.status)}>
          {job.status.replace(/_/g, ' ')}
        </Badge>
      </div>
      <dl className="debug-inspector__facts">
        <div>
          <dt>Job ID</dt>
          <dd>{job.id}</dd>
        </div>
        <div>
          <dt>Progress</dt>
          <dd>{Math.round(job.progress_percent ?? 0)}%</dd>
        </div>
        <div>
          <dt>Updated</dt>
          <dd>{formatTimestamp(job.updated_at)}</dd>
        </div>
      </dl>
      {detail != null ? <p className="body-copy">{detail}</p> : null}
    </StackedListItem>
  )
}

function renderArtifactSummary(item: SessionArtifactInventoryItemView) {
  return (
    <StackedListItem key={item.key}>
      <div className="debug-inspector__row">
        <strong>{item.label}</strong>
        <Badge tone={getStatusTone(item.status)}>{item.status}</Badge>
      </div>
      <p className="body-copy">{item.status_detail}</p>
      {item.asset != null ? (
        <dl className="debug-inspector__facts">
          <div>
            <dt>Asset ID</dt>
            <dd>{item.asset.id}</dd>
          </div>
          <div>
            <dt>Kind</dt>
            <dd>{item.asset.asset_kind}</dd>
          </div>
          <div>
            <dt>Updated</dt>
            <dd>{formatTimestamp(item.asset.updated_at)}</dd>
          </div>
        </dl>
      ) : null}
    </StackedListItem>
  )
}

function renderUsageBucket(bucket: SessionUsageBucketSummaryView) {
  return (
    <StackedListItem key={bucket.usage_bucket}>
      <div className="debug-inspector__row">
        <strong>{bucket.usage_bucket}</strong>
        <Badge
          tone={getStatusTone(bucket.failed_calls > 0 ? 'failed' : 'completed')}
        >
          {bucket.total_calls} calls
        </Badge>
      </div>
      <dl className="debug-inspector__facts">
        <div>
          <dt>Tokens</dt>
          <dd>{formatCount(bucket.token_usage.total_tokens)}</dd>
        </div>
        <div>
          <dt>Latency</dt>
          <dd>{formatDuration(bucket.average_elapsed_ms)}</dd>
        </div>
        <div>
          <dt>Approx cost</dt>
          <dd>{formatCurrency(bucket.approximate_cost_usd)}</dd>
        </div>
      </dl>
      {bucket.models_used.length > 0 ? (
        <p className="body-copy">Models: {bucket.models_used.join(', ')}</p>
      ) : null}
    </StackedListItem>
  )
}

function renderRecentEvent(event: SessionHistoryEvent) {
  return (
    <StackedListItem key={event.id}>
      <div className="debug-inspector__row">
        <strong>{event.summary}</strong>
        <Badge tone="neutral">#{event.sequence_number}</Badge>
      </div>
      <p className="body-copy">
        {event.event_type}
        {event.stage != null ? ` · ${event.stage}` : ''}
        {` · ${event.actor.actor_type}`}
      </p>
      <p className="body-copy">{formatTimestamp(event.created_at)}</p>
    </StackedListItem>
  )
}

function buildTroubleshootingHighlights(data: SessionDebugInspector) {
  const highlights: string[] = []
  const { snapshot, artifact_inventory: artifactInventory } = data

  if (snapshot.latest_composition_job?.status === 'failed') {
    highlights.push(
      snapshot.latest_composition_job.error_message ??
        snapshot.latest_composition_job.stop_reason ??
        'The latest composition job failed without a recorded message.',
    )
  }

  if (snapshot.latest_audio_job?.status === 'failed') {
    highlights.push(
      snapshot.latest_audio_job.error_message ??
        snapshot.latest_audio_job.stop_reason ??
        'The latest audio job failed without a recorded message.',
    )
  }

  artifactInventory.items.forEach((item) => {
    if (item.status === 'failed' || item.status === 'stale') {
      highlights.push(`${item.label}: ${item.status_detail}`)
    }
  })

  return highlights
}

function JsonPanel({ title, value }: { title: string; value: unknown }) {
  return (
    <Panel as="section" title={title} headingLevel={2} tone="subtle">
      <pre className="debug-inspector__json">
        <code>{JSON.stringify(value, null, 2)}</code>
      </pre>
    </Panel>
  )
}

function InspectorLoadingState({ sessionId }: { sessionId: string }) {
  return (
    <section
      className="debug-inspector-page"
      aria-label={`Loading debug inspector for ${sessionId}`}
    >
      <Panel
        as="section"
        title="Developer debug inspector"
        description={
          <p>
            Loading the latest backend-owned session snapshot, event history,
            and artifact state.
          </p>
        }
      >
        <div className="debug-inspector__loading">
          <InlineSpinner label="Loading debug inspector" />
        </div>
      </Panel>
    </section>
  )
}

export function SessionDebugInspectorPage() {
  const params = useParams<{ sessionId: string }>()
  const sessionId = params.sessionId ?? ''
  const inspectorQuery = useSessionDebugInspectorQuery(sessionId)

  if (sessionId.length === 0) {
    return (
      <BlockingFeedback
        description="Open the developer inspector from a concrete session route."
        eyebrow="Developer tools"
        title="Session ID missing"
        tone="danger"
      />
    )
  }

  if (inspectorQuery.isLoading) {
    return <InspectorLoadingState sessionId={sessionId} />
  }

  if (inspectorQuery.error != null || inspectorQuery.data == null) {
    return (
      <section
        className="debug-inspector-page"
        aria-label={`Debug inspector unavailable for ${sessionId}`}
      >
        <BlockingFeedback
          actions={
            <>
              <Link
                className={getButtonClassName({ tone: 'ghost' })}
                to={buildSessionWorkspacePath(sessionId)}
              >
                Back to workspace
              </Link>
              <Button onClick={() => void inspectorQuery.refetch()}>
                Try again
              </Button>
            </>
          }
          description={
            inspectorQuery.error?.message ??
            'The developer inspector is unavailable right now.'
          }
          eyebrow="Developer tools"
          title="Debug inspector unavailable"
          tone="warning"
        />
      </section>
    )
  }

  const data = inspectorQuery.data
  const highlights = buildTroubleshootingHighlights(data)
  const { snapshot } = data

  return (
    <section
      className="debug-inspector-page"
      aria-label={`Developer debug inspector for ${sessionId}`}
    >
      <Panel
        as="section"
        title="Developer debug inspector"
        description={
          <div>
            <p>
              Hidden troubleshooting surface for inspecting the backend-owned
              truth of a story session without querying Postgres directly.
            </p>
            <p>
              Session <code>{data.session_id}</code> · Generated{' '}
              {formatTimestamp(data.generated_at)}
            </p>
          </div>
        }
        eyebrow="Developer tools"
        actions={
          <>
            <Link
              className={getButtonClassName({ tone: 'ghost' })}
              to={buildSessionWorkspacePath(sessionId)}
            >
              Back to workspace
            </Link>
            <Button onClick={() => void inspectorQuery.refetch()}>
              Refresh
            </Button>
          </>
        }
      >
        <CardGrid columns={3}>
          <Panel
            as="section"
            className="debug-inspector__mini-panel"
            title="Session truth"
            headingLevel={3}
            tone="subtle"
          >
            <dl className="debug-inspector__facts">
              <div>
                <dt>Stage</dt>
                <dd>{snapshot.current_stage}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{snapshot.overall_status.replace(/_/g, ' ')}</dd>
              </div>
              <div>
                <dt>Latest event</dt>
                <dd>
                  {data.hydration.latest_sequence_number ?? 'Unavailable'}
                </dd>
              </div>
            </dl>
          </Panel>
          <Panel
            as="section"
            className="debug-inspector__mini-panel"
            title="Plan revision"
            headingLevel={3}
            tone="subtle"
          >
            {snapshot.current_plan_revision != null ? (
              <>
                <div className="debug-inspector__row">
                  <strong>
                    Revision {snapshot.current_plan_revision.revision_number}
                  </strong>
                  <Badge tone="brand">Current</Badge>
                </div>
                <p className="body-copy">
                  {snapshot.current_plan_revision.change_summary ??
                    'No change summary recorded.'}
                </p>
                <p className="body-copy">
                  Changed artifacts:{' '}
                  {snapshot.current_plan_revision.changed_artifacts.join(
                    ', ',
                  ) || 'None'}
                </p>
              </>
            ) : (
              <p className="body-copy">
                No plan revision has been materialized yet.
              </p>
            )}
          </Panel>
          <Panel
            as="section"
            className="debug-inspector__mini-panel"
            title="Usage summary"
            headingLevel={3}
            tone="subtle"
          >
            <dl className="debug-inspector__facts">
              <div>
                <dt>Total calls</dt>
                <dd>{data.usage_diagnostics.summary.total_calls}</dd>
              </div>
              <div>
                <dt>Total tokens</dt>
                <dd>
                  {formatCount(
                    data.usage_diagnostics.summary.token_usage.total_tokens,
                  )}
                </dd>
              </div>
              <div>
                <dt>Approx cost</dt>
                <dd>
                  {formatCurrency(
                    data.usage_diagnostics.summary.approximate_cost_usd,
                  )}
                </dd>
              </div>
            </dl>
          </Panel>
        </CardGrid>
      </Panel>

      {highlights.length > 0 ? (
        <Panel
          as="section"
          title="Troubleshooting highlights"
          description={
            <p>
              Recent failures or stale outputs that explain why composition or
              narration may look stuck.
            </p>
          }
          headingLevel={2}
        >
          <StackedList>
            {highlights.map((highlight) => (
              <StackedListItem key={highlight} tone="accent">
                <p className="body-copy">{highlight}</p>
              </StackedListItem>
            ))}
          </StackedList>
        </Panel>
      ) : null}

      <CardGrid columns={2}>
        <Panel as="section" title="Active jobs" headingLevel={2}>
          <StackedList>
            {renderJobSummary(
              snapshot.active_composition_job ??
                snapshot.latest_composition_job,
              'Composition',
            )}
            {renderJobSummary(
              snapshot.active_audio_job ?? snapshot.latest_audio_job,
              'Audio',
            )}
          </StackedList>
        </Panel>

        <Panel as="section" title="Artifact inventory" headingLevel={2}>
          <StackedList>
            {data.artifact_inventory.items.map((item) =>
              renderArtifactSummary(item),
            )}
          </StackedList>
        </Panel>
      </CardGrid>

      <CardGrid columns={2}>
        <Panel
          as="section"
          title="Recent events"
          description={
            <p>
              Latest durable event log entries from the hydrated history window.
            </p>
          }
          headingLevel={2}
        >
          <StackedList>
            {[...data.recent_history.events]
              .reverse()
              .map((event) => renderRecentEvent(event))}
          </StackedList>
        </Panel>

        <Panel as="section" title="Usage buckets" headingLevel={2}>
          <StackedList>
            {data.usage_diagnostics.summary.buckets.map((bucket) =>
              renderUsageBucket(bucket),
            )}
          </StackedList>
        </Panel>
      </CardGrid>

      <CardGrid columns={2}>
        <JsonPanel title="Session snapshot JSON" value={data.snapshot} />
        <JsonPanel
          title="Usage diagnostics JSON"
          value={data.usage_diagnostics}
        />
      </CardGrid>

      <JsonPanel
        title="Artifact inventory JSON"
        value={data.artifact_inventory}
      />

      <p className="debug-inspector__footer body-copy">
        This route is intentionally not linked from the main product navigation.
        Return to <Link to={routePaths.home}>sessions</Link> when you are done
        debugging.
      </p>
    </section>
  )
}
