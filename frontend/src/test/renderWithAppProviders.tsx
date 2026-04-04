import { QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'
import type { ReactElement } from 'react'
import { createAppQueryClient } from '../app/queryClient.ts'
import { resetAppShellState } from '../state/appShellStore.ts'

export function renderWithAppProviders(ui: ReactElement) {
  const queryClient = createAppQueryClient()
  resetAppShellState()

  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  )
}
