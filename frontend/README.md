# Frontend

This directory contains the browser application for Storyteller.

The frontend now uses the current Vite React TypeScript baseline as its foundation, then layers in the app shell, route structure, and shared primitives required by the prompt pack.

Key entrypoints:

- `src/main.tsx`: browser entrypoint
- `src/app/router.tsx`: browser-router configuration for the home page, session workspace, and not-found fallback
- `src/app/AppProviders.tsx`: global providers, including the shared React Query client
- `src/app/routePaths.ts`: central path helpers, including the session-workspace URL builder
- `src/app/AppShell.tsx`: global chrome with navigation, connection status, and toast space
- `src/pages/`: route-level screens
- `src/shared/ui/`: reusable shell-level UI primitives
- `src/hooks/`: shared data hooks
- `src/api/`: backend request helpers and service-specific clients
- `src/state/`: app-level state shapes and future store modules
- `src/features/session/sessionQueries.ts`: React Query hooks and cache keys for session server state
- `src/features/session/sessionRuntimeStore.ts`: local session runtime store for live events and optimistic actions
- `src/styles/index.css`: global styles and design tokens for the scaffold
- `vite.config.ts`: Vite dev server configuration, including the backend proxy

Folder conventions:

- `src/app/`: router, app shell, route constants, and future global providers
- `src/pages/`: page modules that map directly to routes
- `src/features/`: reusable product-domain logic that can be shared across pages, including session query hooks and runtime state
- `src/shared/ui/`: composable display primitives and chrome
- `src/hooks/`: cross-cutting React hooks that are not owned by a single page
- `src/api/`: fetch wrappers, endpoint clients, and request helpers
- `src/state/`: state models and future global/session store modules

See [docs/frontend-state-architecture.md](/Users/kevin/code/storyteller/docs/frontend-state-architecture.md) for the current split between React Query server state and the workspace-local runtime store.

Useful commands:

- `npm run dev`: start the Vite dev server on port `8566`
- `npm run build`: run TypeScript checks and create a production build
- `npm run lint`: lint the frontend source
- `npm run test`: run the frontend unit tests
- `npm run format`: format the frontend files with Prettier

## Container targets

`frontend/Dockerfile` now exposes explicit stages for:

- `development`: Vite dev server for the local Compose override
- `build`: production asset compilation with `VITE_*` build arguments
- `runtime`: nginx serving the built SPA and proxying `/api` traffic to the backend service

That split keeps local hot reload intact while leaving the checked-in runtime image closer to how the frontend would be deployed behind a real reverse proxy or ingress later.

Later prompts should extend this TypeScript app into the sessions-first workspace rather than replacing it.
