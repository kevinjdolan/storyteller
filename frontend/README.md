# Frontend

This directory contains the browser application for Storyteller.

The frontend now uses the current Vite React TypeScript baseline as its foundation, then layers in the project-specific shell and tooling required by the prompt pack.

Key entrypoints:

- `src/main.tsx`: browser entrypoint
- `src/app/router.tsx`: minimal route shell for future screens
- `src/features/home/HomeRoute.tsx`: branded placeholder landing route
- `src/shared/api.ts`: typed helper for backend-relative API URLs
- `src/styles/index.css`: global styles and design tokens for the scaffold
- `vite.config.ts`: Vite dev server configuration, including the backend proxy

Useful commands:

- `npm run dev`: start the Vite dev server on port `8566`
- `npm run build`: run TypeScript checks and create a production build
- `npm run lint`: lint the frontend source
- `npm run test`: run the frontend unit tests
- `npm run format`: format the frontend files with Prettier

Later prompts should extend this TypeScript app into the sessions-first workspace rather than replacing it.
