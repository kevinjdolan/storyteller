# Frontend

This directory contains the browser application for Storyteller.

The frontend now uses the current Vite React TypeScript baseline as its foundation, then layers in the app shell, route structure, and shared primitives required by the prompt pack.

Key entrypoints:

- `src/main.tsx`: browser entrypoint
- `src/app/router.tsx`: browser-router configuration for the home page, session workspace, and not-found fallback
- `src/app/routePaths.ts`: central path helpers, including the session-workspace URL builder
- `src/app/AppShell.tsx`: global chrome with navigation, connection status, and toast space
- `src/pages/`: route-level screens
- `src/shared/ui/`: reusable shell-level UI primitives
- `src/hooks/`: shared data hooks
- `src/api/`: backend request helpers and service-specific clients
- `src/state/`: app-level state shapes and future store modules
- `src/styles/index.css`: global styles and design tokens for the scaffold
- `vite.config.ts`: Vite dev server configuration, including the backend proxy

Folder conventions:

- `src/app/`: router, app shell, route constants, and future global providers
- `src/pages/`: page modules that map directly to routes
- `src/features/`: reusable product-domain logic that can be shared across pages
- `src/shared/ui/`: composable display primitives and chrome
- `src/hooks/`: cross-cutting React hooks that are not owned by a single page
- `src/api/`: fetch wrappers, endpoint clients, and request helpers
- `src/state/`: state models and future global/session store modules

Useful commands:

- `npm run dev`: start the Vite dev server on port `8566`
- `npm run build`: run TypeScript checks and create a production build
- `npm run lint`: lint the frontend source
- `npm run test`: run the frontend unit tests
- `npm run format`: format the frontend files with Prettier

Later prompts should extend this TypeScript app into the sessions-first workspace rather than replacing it.
