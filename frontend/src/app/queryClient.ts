import { MutationCache, QueryCache, QueryClient } from '@tanstack/react-query'
import {
  enqueueAppShellToast,
  type AppShellToastTone,
} from '../state/appShellStore.ts'

type FeedbackMeta = {
  feedback?: {
    errorToast?:
      | false
      | {
          body?: string
          dedupeKey?: string
          title: string
          tone?: AppShellToastTone
        }
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function getFeedbackMeta(meta: unknown): FeedbackMeta['feedback'] | null {
  if (!isRecord(meta) || !isRecord(meta.feedback)) {
    return null
  }

  return meta.feedback as FeedbackMeta['feedback']
}

function buildErrorMessage(error: unknown) {
  if (error instanceof Error && error.message.trim().length > 0) {
    return error.message
  }

  return 'The request failed before the UI could finish the update.'
}

function notifyError(options: {
  defaultTone: AppShellToastTone
  error: unknown
  meta: unknown
  title: string
}) {
  const feedbackMeta = getFeedbackMeta(options.meta)

  if (feedbackMeta == null || feedbackMeta.errorToast === false) {
    return
  }

  enqueueAppShellToast({
    body: feedbackMeta?.errorToast?.body ?? buildErrorMessage(options.error),
    dedupeKey: feedbackMeta?.errorToast?.dedupeKey,
    title: feedbackMeta?.errorToast?.title ?? options.title,
    tone: feedbackMeta?.errorToast?.tone ?? options.defaultTone,
  })
}

export function createAppQueryClient() {
  return new QueryClient({
    mutationCache: new MutationCache({
      onError: (error, _variables, _context, mutation) => {
        notifyError({
          defaultTone: 'warning',
          error,
          meta: mutation.options.meta,
          title: 'Action failed',
        })
      },
    }),
    queryCache: new QueryCache({
      onError: (error, query) => {
        notifyError({
          defaultTone: 'warning',
          error,
          meta: query.meta,
          title: 'Request failed',
        })
      },
    }),
    defaultOptions: {
      queries: {
        retry: 0,
        refetchOnWindowFocus: false,
      },
      mutations: {
        retry: 0,
      },
    },
  })
}

export const queryClient = createAppQueryClient()
