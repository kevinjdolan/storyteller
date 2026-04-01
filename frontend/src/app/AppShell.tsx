import { Outlet } from 'react-router-dom'

export function AppShell() {
  return (
    <div className="app-shell">
      <div
        className="app-shell__glow app-shell__glow--left"
        aria-hidden="true"
      />
      <div
        className="app-shell__glow app-shell__glow--right"
        aria-hidden="true"
      />

      <header className="app-header">
        <div>
          <p className="app-kicker">Bedtime story studio</p>
          <span className="app-brand">Storyteller</span>
        </div>

        <p className="app-caption">React + Vite + TypeScript foundation</p>
      </header>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
