import { createBrowserRouter, type RouteObject } from 'react-router-dom'
import { HomePage } from '../pages/home/HomePage.tsx'
import { NotFoundPage } from '../pages/not-found/NotFoundPage.tsx'
import { SessionWorkspacePage } from '../pages/session/SessionWorkspacePage.tsx'
import { AppShell } from './AppShell.tsx'
import { routePaths } from './routePaths.ts'

export const appRoutes: RouteObject[] = [
  {
    path: routePaths.home,
    element: <AppShell />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: routePaths.sessionWorkspace,
        element: <SessionWorkspacePage />,
      },
      {
        path: routePaths.notFound,
        element: <NotFoundPage />,
      },
    ],
  },
]

export const router = createBrowserRouter(appRoutes)
