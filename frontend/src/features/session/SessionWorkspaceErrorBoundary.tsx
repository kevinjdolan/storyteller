import { Component, type ErrorInfo, type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { routePaths } from '../../app/routePaths.ts'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'
import { BlockingFeedback } from '../../shared/ui/feedback.tsx'

type SessionWorkspaceErrorBoundaryProps = {
  children: ReactNode
  sessionId: string
}

type SessionWorkspaceErrorBoundaryState = {
  componentStack: string | null
  error: Error | null
}

export class SessionWorkspaceErrorBoundary extends Component<
  SessionWorkspaceErrorBoundaryProps,
  SessionWorkspaceErrorBoundaryState
> {
  state: SessionWorkspaceErrorBoundaryState = {
    componentStack: null,
    error: null,
  }

  static getDerivedStateFromError(error: Error) {
    return {
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({
      componentStack: errorInfo.componentStack ?? null,
      error,
    })

    if (import.meta.env.MODE !== 'test') {
      console.error('Session workspace crashed.', error, errorInfo)
    }
  }

  componentDidUpdate(previousProps: SessionWorkspaceErrorBoundaryProps) {
    if (
      previousProps.sessionId !== this.props.sessionId &&
      this.state.error != null
    ) {
      this.handleReset()
    }
  }

  handleReset = () => {
    this.setState({
      componentStack: null,
      error: null,
    })
  }

  render() {
    if (this.state.error == null) {
      return this.props.children
    }

    return (
      <section
        aria-label={`Session workspace for ${this.props.sessionId}`}
        className="workspace-page"
      >
        <BlockingFeedback
          actions={
            <div className="cta-row">
              <button
                className={getButtonClassName({
                  size: 'compact',
                  tone: 'ghost',
                })}
                type="button"
                onClick={this.handleReset}
              >
                Retry workspace
              </button>
              <Link
                className={getButtonClassName({
                  size: 'compact',
                  tone: 'ghost',
                })}
                to={routePaths.home}
              >
                Return home
              </Link>
            </div>
          }
          bannerTitle="Unexpected render error"
          description={
            this.state.error.message.trim().length > 0
              ? this.state.error.message
              : 'An unexpected error interrupted the workspace before it could finish rendering.'
          }
          eyebrow="Workspace crash"
          title="Workspace crashed"
          tone="danger"
        />

        {import.meta.env.DEV ? (
          <section className="panel workspace-error-stack">
            <p className="eyebrow">Developer detail</p>
            <h2>React component stack</h2>
            <pre className="workspace-error-stack__trace">
              {this.state.componentStack ??
                this.state.error.stack ??
                'No stack trace captured.'}
            </pre>
          </section>
        ) : null}
      </section>
    )
  }
}
