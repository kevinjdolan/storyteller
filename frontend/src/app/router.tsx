import { createBrowserRouter } from 'react-router-dom'
import { HomeRoute } from '../features/home/HomeRoute.tsx'
import { AppShell } from './AppShell.tsx'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      {
        index: true,
        element: <HomeRoute />,
      },
    ],
  },
])
