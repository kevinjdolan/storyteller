import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createSession,
  type FetchRecentSessionsOptions,
  fetchSessionArtifactInventory,
  fetchSessionDebugInspector,
  fetchSessionHydration,
  fetchRecentSessions,
  fetchSessionHistory,
  fetchSessionSnapshot,
} from '../../api/sessions.ts'

export const sessionQueryKeys = {
  all: ['sessions'] as const,
  lists: () => [...sessionQueryKeys.all, 'list'] as const,
  list: (options: FetchRecentSessionsOptions) =>
    [...sessionQueryKeys.lists(), options] as const,
  hydrations: () => [...sessionQueryKeys.all, 'hydration'] as const,
  hydration: (sessionId: string) =>
    [...sessionQueryKeys.hydrations(), sessionId] as const,
  details: () => [...sessionQueryKeys.all, 'detail'] as const,
  detail: (sessionId: string) =>
    [...sessionQueryKeys.details(), sessionId] as const,
  histories: () => [...sessionQueryKeys.all, 'history'] as const,
  history: (sessionId: string) =>
    [...sessionQueryKeys.histories(), sessionId] as const,
  artifactInventories: () => [...sessionQueryKeys.all, 'artifact-inventory'] as const,
  artifactInventory: (sessionId: string) =>
    [...sessionQueryKeys.artifactInventories(), sessionId] as const,
  debugInspectors: () => [...sessionQueryKeys.all, 'debug-inspector'] as const,
  debugInspector: (sessionId: string) =>
    [...sessionQueryKeys.debugInspectors(), sessionId] as const,
}

export function useRecentSessionsQuery(options: FetchRecentSessionsOptions = {}) {
  return useQuery({
    placeholderData: (previousData) => previousData,
    queryKey: sessionQueryKeys.list(options),
    queryFn: () => fetchRecentSessions(options),
    staleTime: 30_000,
  })
}

export function useSessionSnapshotQuery(sessionId: string) {
  return useQuery({
    queryKey: sessionQueryKeys.detail(sessionId),
    queryFn: () => fetchSessionSnapshot(sessionId),
    enabled: sessionId.length > 0,
    staleTime: 10_000,
  })
}

export function useSessionHydrationQuery(sessionId: string) {
  return useQuery({
    queryKey: sessionQueryKeys.hydration(sessionId),
    queryFn: () => fetchSessionHydration(sessionId),
    enabled: sessionId.length > 0,
    staleTime: 10_000,
  })
}

export function useSessionHistoryQuery(sessionId: string) {
  return useQuery({
    queryKey: sessionQueryKeys.history(sessionId),
    queryFn: () => fetchSessionHistory(sessionId),
    enabled: sessionId.length > 0,
    staleTime: 60_000,
  })
}

export function useSessionArtifactInventoryQuery(sessionId: string) {
  return useQuery({
    queryKey: sessionQueryKeys.artifactInventory(sessionId),
    queryFn: () => fetchSessionArtifactInventory(sessionId),
    enabled: sessionId.length > 0,
    staleTime: 10_000,
  })
}

export function useSessionDebugInspectorQuery(sessionId: string) {
  return useQuery({
    queryKey: sessionQueryKeys.debugInspector(sessionId),
    queryFn: () => fetchSessionDebugInspector(sessionId),
    enabled: sessionId.length > 0,
    staleTime: 5_000,
  })
}

export function useCreateSessionMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    meta: {
      feedback: {
        errorToast: {
          body: 'The home screen could not open a new workspace. Try the request again.',
          dedupeKey: 'create-session',
          title: 'Could not start a new session',
          tone: 'warning',
        },
      },
    },
    mutationFn: (workingTitle?: string) => createSession(workingTitle),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: sessionQueryKeys.lists(),
      })
    },
  })
}
