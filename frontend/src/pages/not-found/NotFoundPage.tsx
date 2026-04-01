import { Link, useLocation } from 'react-router-dom'
import { routePaths } from '../../app/routePaths.ts'

export function NotFoundPage() {
  const location = useLocation()

  return (
    <section className="not-found-page" aria-label="Unknown route fallback">
      <article className="panel panel-centered" data-testid="not-found">
        <p className="eyebrow">Route fallback</p>
        <h1>Page not found</h1>
        <p className="body-copy">
          No screen is registered for <code>{location.pathname}</code> yet.
        </p>
        <Link className="primary-link" to={routePaths.home}>
          Return to sessions home
        </Link>
      </article>
    </section>
  )
}
