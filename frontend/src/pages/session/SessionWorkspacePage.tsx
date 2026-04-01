import { Link, useParams } from 'react-router-dom'
import { routePaths } from '../../app/routePaths.ts'
import { workflowStageDefinitions } from '../../features/session/workflowStages.ts'

const chatRailPreview = [
  'Conversation history and quick actions will live in the left rail.',
  'UI actions will echo back into chat as compact structured messages.',
  'Agent summaries during composition and audio jobs will dock here.',
] as const

export function SessionWorkspacePage() {
  const { sessionId = 'unknown-session' } = useParams()

  return (
    <section
      className="workspace-page"
      aria-label={`Session workspace for ${sessionId}`}
    >
      <header className="workspace-page__header">
        <div>
          <p className="eyebrow">Session workspace</p>
          <h1>Session {sessionId}</h1>
          <p className="body-copy">
            This route-scoped shell reserves the left pane for chat and the
            right pane for the structured workflow UI.
          </p>
        </div>

        <Link className="ghost-link" to={routePaths.home}>
          Back to sessions
        </Link>
      </header>

      <div className="workspace-shell" data-testid="workspace-route">
        <aside className="panel workspace-pane workspace-pane--chat">
          <div className="pane-heading">
            <h2>Chat lane</h2>
            <span className="status-chip">1/3 width target</span>
          </div>
          <p className="body-copy">
            The left rail is reserved for conversation, quick actions, and
            durable chat history.
          </p>

          <ol className="placeholder-list">
            {chatRailPreview.map((entry) => (
              <li key={entry}>{entry}</li>
            ))}
          </ol>
        </aside>

        <section className="panel workspace-pane workspace-pane--canvas">
          <div className="pane-heading">
            <h2>Workflow canvas</h2>
            <span className="status-chip">Route param bound</span>
          </div>
          <p className="body-copy">
            The workspace already keys itself off the session route so future
            data loaders, stores, and websocket subscriptions can stay
            session-specific.
          </p>

          <dl className="workspace-meta">
            <div>
              <dt>Session ID</dt>
              <dd>{sessionId}</dd>
            </div>
            <div>
              <dt>Active route</dt>
              <dd>{`/sessions/${sessionId}`}</dd>
            </div>
            <div>
              <dt>Next prompt</dt>
              <dd>Two-pane workflow layout</dd>
            </div>
          </dl>

          <ol className="workspace-stage-list">
            {workflowStageDefinitions.map((stage, index) => (
              <li key={stage.id}>
                <span>{index + 1}</span>
                <div>
                  <strong>{stage.label}</strong>
                  <p>{stage.description}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </section>
  )
}
