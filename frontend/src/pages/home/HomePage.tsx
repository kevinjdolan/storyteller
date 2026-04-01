import { Link } from 'react-router-dom'
import { buildSessionWorkspacePath } from '../../app/routePaths.ts'
import { workflowStageDefinitions } from '../../features/session/workflowStages.ts'

const sessionPreview = [
  {
    id: 'juniper-lake',
    title: 'Lanterns Over Juniper Lake',
    status: 'Drafting beats',
    note: 'Calm mystery with a reassuring finish',
  },
  {
    id: 'maple-hollow',
    title: 'The Moss Door in Maple Hollow',
    status: 'Ready for narration',
    note: 'Whispery woodland adventure tuned for a shorter read-aloud',
  },
  {
    id: 'cloud-harbor',
    title: 'Cloud Harbor Night Shift',
    status: 'In progress',
    note: 'Skyport teamwork tale with bedtime-safe tension',
  },
] as const

const frontendExtensions = [
  {
    label: 'pages/',
    detail:
      'Route-level screens live here, including the sessions home, workspace shell, and fallback pages.',
  },
  {
    label: 'shared/ui/',
    detail:
      'Reusable chrome such as status indicators, layout primitives, and future cards can stay detached from route modules.',
  },
  {
    label: 'hooks/',
    detail:
      'Data hooks such as backend status checks now sit outside route components and can grow into loaders or realtime subscriptions.',
  },
  {
    label: 'api/',
    detail:
      'Backend-facing helpers have a single home for request wrappers and service-specific clients.',
  },
  {
    label: 'state/',
    detail:
      'Shell-level and session-level stores can expand here without overloading components with global coordination logic.',
  },
] as const

export function HomePage() {
  return (
    <section
      className="page-grid home-page"
      aria-label="Storyteller app shell overview"
    >
      <article className="panel panel-hero" data-testid="app-card">
        <p className="eyebrow">Prompt 20 app shell</p>
        <h1>Storyteller</h1>
        <p className="lede">
          Past sessions now live on a real home route, ready to hand off into
          the workspace shell.
        </p>
        <p className="body-copy">
          This screen stays intentionally light while the rest of the
          bedtime-story workflow arrives behind durable routing and shared
          chrome.
        </p>

        <div className="cta-row">
          <Link
            className="primary-link"
            to={buildSessionWorkspacePath(sessionPreview[0].id)}
          >
            Open sample workspace
          </Link>
          <p className="cta-note">
            The shell now covers home, route-scoped sessions, and a not-found
            fallback.
          </p>
        </div>
      </article>

      <article className="panel">
        <div className="panel-heading">
          <h2>Past sessions come first</h2>
          <p>
            The home screen is now a dedicated route, ready for durable session
            loading and resume flows.
          </p>
        </div>

        <ul className="session-list">
          {sessionPreview.map((session) => (
            <li key={session.id} className="session-item">
              <div>
                <h3>{session.title}</h3>
                <p>{session.note}</p>
              </div>

              <div className="session-item__actions">
                <span className="status-chip">{session.status}</span>
                <Link
                  className="ghost-link"
                  to={buildSessionWorkspacePath(session.id)}
                >
                  Open {session.title}
                </Link>
              </div>
            </li>
          ))}
        </ul>
      </article>

      <article className="panel">
        <div className="panel-heading">
          <h2>Workflow runway</h2>
          <p>
            The route shell is still lightweight, but it already reflects the
            staged story workflow the app has to support.
          </p>
        </div>

        <ol className="stage-list">
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
      </article>

      <article className="panel">
        <div className="panel-heading">
          <h2>Frontend extension points</h2>
          <p>
            The shell now has predictable landing zones for shared components,
            hooks, route pages, request helpers, and future state stores.
          </p>
        </div>

        <ul className="extension-list">
          {frontendExtensions.map((entry) => (
            <li key={entry.label} className="extension-item">
              <code>{entry.label}</code>
              <p>{entry.detail}</p>
            </li>
          ))}
        </ul>
      </article>
    </section>
  )
}
