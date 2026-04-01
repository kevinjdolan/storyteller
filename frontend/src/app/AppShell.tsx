import { useState } from 'react'
import { Link, NavLink, Outlet, matchPath, useLocation } from 'react-router-dom'
import { useBackendStatus } from '../hooks/useBackendStatus.ts'
import { ConnectionStatusBadge } from '../shared/ui/ConnectionStatusBadge.tsx'
import { ToastRegion } from '../shared/ui/ToastRegion.tsx'
import { createInitialAppShellState } from '../state/appShellStore.ts'
import { routePaths } from './routePaths.ts'

export function AppShell() {
  const location = useLocation()
  const backendStatus = useBackendStatus()
  const [shellState] = useState(createInitialAppShellState)
  const workspaceNavIsActive =
    matchPath(routePaths.sessionWorkspace, location.pathname) !== null

  return (
    <div className="app-shell">
      <a className="skip-link" href="#app-main-content">
        Skip to main content
      </a>
      <div
        className="app-shell__glow app-shell__glow--left"
        aria-hidden="true"
      />
      <div
        className="app-shell__glow app-shell__glow--right"
        aria-hidden="true"
      />

      <div className="app-frame">
        <header className="app-header">
          <div className="app-header__brand-block">
            <p className="app-kicker">Bedtime story studio</p>
            <Link className="app-brand-link" to={routePaths.home}>
              <span className="app-brand">Storyteller</span>
            </Link>
          </div>

          <nav className="app-nav" aria-label="Primary">
            <NavLink
              className={({ isActive }) =>
                isActive
                  ? 'app-nav__link app-nav__link--active'
                  : 'app-nav__link'
              }
              end
              to={routePaths.home}
            >
              Sessions
            </NavLink>
            <span
              className={
                workspaceNavIsActive
                  ? 'app-nav__link app-nav__link--active'
                  : 'app-nav__link app-nav__link--muted'
              }
            >
              Workspace
            </span>
          </nav>

          <p className="app-caption">
            Resume existing stories or open a session workspace when you are
            ready to continue.
          </p>
        </header>

        <section
          className="app-utility-bar"
          aria-label="Application utility rail"
        >
          <ConnectionStatusBadge status={backendStatus} />
          <ToastRegion toasts={shellState.toasts} />
        </section>

        <main className="app-main" id="app-main-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
