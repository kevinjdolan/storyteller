import { useBackendStatus } from '../system/useBackendStatus.ts'
import { workflowStageDefinitions } from '../session/workflowStages.ts'

const sessionPreview = [
  {
    title: 'Lanterns Over Juniper Lake',
    status: 'Drafting beats',
    note: 'Calm mystery with a reassuring finish',
  },
  {
    title: 'The Moss Door in Maple Hollow',
    status: 'Ready for narration',
    note: 'Whispery woodland adventure for a shorter read-aloud',
  },
  {
    title: 'Cloud Harbor Night Shift',
    status: 'In progress',
    note: 'Skyport bedtime tale with gentle teamwork stakes',
  },
] as const

const qualitySignals = [
  'Strict TypeScript',
  'Router shell',
  'ESLint',
  'Prettier',
  'Vitest',
] as const

export function HomeRoute() {
  const backendStatus = useBackendStatus()

  return (
    <section className="home-grid" aria-label="Storyteller scaffold overview">
      <article className="panel panel-hero" data-testid="app-card">
        <p className="eyebrow">Prompt 02 scaffold</p>
        <h1>Storyteller</h1>
        <p className="lede">
          A calm studio for shaping bedtime stories from first spark to finished
          narration.
        </p>
        <p className="body-copy">
          This placeholder route proves the Vite foundation is running while
          keeping the product pointed at its sessions-first, workflow-driven
          future.
        </p>

        <ul className="tag-list" aria-label="Frontend quality signals">
          {qualitySignals.map((signal) => (
            <li key={signal} className="tag">
              {signal}
            </li>
          ))}
        </ul>
      </article>

      <article className="panel">
        <div className="panel-heading">
          <h2>Past sessions come first</h2>
          <p>
            The real session list arrives in a later prompt. For now, the home
            route already reflects the product contract.
          </p>
        </div>

        <ul className="session-list">
          {sessionPreview.map((session) => (
            <li key={session.title} className="session-item">
              <div>
                <h3>{session.title}</h3>
                <p>{session.note}</p>
              </div>
              <span className="status-chip">{session.status}</span>
            </li>
          ))}
        </ul>
      </article>

      <article className="panel">
        <div className="panel-heading">
          <h2>Story studio path</h2>
          <p>
            The route shell is intentionally lightweight, but it already mirrors
            the staged workflow the product needs.
          </p>
        </div>

        <ol className="stage-list">
          {workflowStageDefinitions.map((stage, index) => (
            <li key={stage.id}>
              <span>{index + 1}</span>
              <strong>{stage.label}</strong>
            </li>
          ))}
        </ol>
      </article>

      <article className="panel panel-status">
        <div className="status-header">
          <div>
            <p className="eyebrow eyebrow-muted">Backend bridge</p>
            <h2>Frontend isolation check</h2>
          </div>

          <span
            className={`status-badge status-badge--${backendStatus.state}`}
            data-testid="backend-state"
          >
            {backendStatus.label}
          </span>
        </div>

        <p className="body-copy">{backendStatus.detail}</p>
        <p className="api-message" data-testid="api-message">
          {backendStatus.message}
        </p>
      </article>
    </section>
  )
}
