export type AppShellToastTone = 'info' | 'success' | 'warning'

export type AppShellToast = {
  id: string
  title: string
  body: string
  tone: AppShellToastTone
}

export type AppShellState = {
  toasts: AppShellToast[]
}

export function createInitialAppShellState(): AppShellState {
  return {
    toasts: [],
  }
}
