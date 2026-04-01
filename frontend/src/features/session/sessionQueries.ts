import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createSession,
  fetchRecentSessions,
  fetchSessionHistory,
  fetchSessionSnapshot,
} from '../../api/sessions.ts'

export const sessionQueryKeys = {
  all: ['sessions'] as const,
  lists: () => [...sessionQueryKeys.all, 'list'] as const,
  list: (limit: number) => [...sessionQueryKeys.lists(), limit] as const,
  details: () => [...sessionQueryKeys.all, 'detail'] as const,
  detail: (sessionId: string) =>
    [...sessionQueryKeys.details(), sessionId] as const,
  histories: () => [...sessionQueryKeys.all, 'history'] as const,
  history: (sessionId: string) =>
    [...sessionQueryKeys.histories(), sessionId] as const,
}

export function useRecentSessionsQuery(limit = 20) {
  return useQuery({
    queryKey: sessionQueryKeys.list(limit),
    queryFn: () => fetchRecentSessions(limit),
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

export function useSessionHistoryQuery(sessionId: string) {
  return useQuery({
    queryKey: sessionQueryKeys.history(sessionId),
    queryFn: () => fetchSessionHistory(sessionId),
    enabled: sessionId.length > 0,
    staleTime: 60_000,
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
