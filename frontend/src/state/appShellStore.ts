import { useSyncExternalStore } from 'react'

export type AppShellToastTone = 'info' | 'success' | 'warning' | 'danger'

export type AppShellToast = {
  body: string
  createdAt: string
  dedupeKey?: string
  id: string
  title: string
  tone: AppShellToastTone
}

export type AppShellState = {
  toasts: AppShellToast[]
}

type AppShellListener = () => void

type EnqueueToastInput = {
  body: string
  dedupeKey?: string
  id?: string
  title: string
  tone?: AppShellToastTone
}

const maxToastCount = 4
let toastSequence = 0
let state = createInitialAppShellState()
const listeners = new Set<AppShellListener>()

function emitChange() {
  listeners.forEach((listener) => listener())
}

function setState(nextState: AppShellState) {
  state = nextState
  emitChange()
}

function buildToastId() {
  return globalThis.crypto?.randomUUID?.() ?? `toast-${++toastSequence}`
}

export function createInitialAppShellState(): AppShellState {
  return {
    toasts: [],
  }
}

export function enqueueAppShellToast({
  body,
  dedupeKey,
  id = buildToastId(),
  title,
  tone = 'info',
}: EnqueueToastInput) {
  const nextToast: AppShellToast = {
    body,
    createdAt: new Date().toISOString(),
    dedupeKey,
    id,
    title,
    tone,
  }

  const existingToasts =
    dedupeKey == null
      ? state.toasts
      : state.toasts.filter((toast) => toast.dedupeKey !== dedupeKey)

  setState({
    toasts: [...existingToasts, nextToast].slice(-maxToastCount),
  })

  return nextToast.id
}

export function dismissAppShellToast(toastId: string) {
  setState({
    toasts: state.toasts.filter((toast) => toast.id !== toastId),
  })
}

export function resetAppShellState() {
  toastSequence = 0
  setState(createInitialAppShellState())
}

export function subscribeToAppShellState(listener: AppShellListener) {
  listeners.add(listener)

  return () => {
    listeners.delete(listener)
  }
}

export function getAppShellState() {
  return state
}

export function useAppShellState() {
  return useSyncExternalStore(
    subscribeToAppShellState,
    getAppShellState,
    getAppShellState,
  )
}

export function useAppShellToasts() {
  return useSyncExternalStore(
    subscribeToAppShellState,
    () => getAppShellState().toasts,
    () => getAppShellState().toasts,
  )
}
