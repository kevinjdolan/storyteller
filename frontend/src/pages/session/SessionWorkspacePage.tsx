import { type MouseEvent, useEffect, useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import { selectSessionGenre, selectSessionTone } from '../../api/catalog.ts'
import {
  applySessionContextUpdate,
  cancelSessionComposition,
  editSessionBeatSheet,
  generateSessionBeatSheet,
  generateSessionCharacterSheets,
  generateSessionPitches,
  parseSessionChatIntent,
  pauseSessionComposition,
  redirectSessionComposition,
  refineSessionBeatSheet,
  refineSessionCharacterSheet,
  refineSessionPitch,
  recordSessionUiAction,
  resumeSessionComposition,
  restoreSessionPlanRevision,
  saveSessionStoryBrief,
  saveSessionStoryOutline,
  saveSessionStorySetup,
  selectSessionBeatSheet,
  selectSessionCharacterSheet,
  selectSessionPitch,
  type NormalizedBriefPreferencesView,
  type SessionHistoryEvent,
  type SessionSnapshot,
  startSessionComposition,
} from '../../api/sessions.ts'
import { buildSessionWorkspacePath, routePaths } from '../../app/routePaths.ts'
import { SessionWorkspaceErrorBoundary } from '../../features/session/SessionWorkspaceErrorBoundary.tsx'
import { SessionStageEditorPreview } from '../../features/session/SessionStageEditorPreview.tsx'
import { BeatSheetStage } from '../../features/session/BeatSheetStage.tsx'
import { CharacterSelectionStage } from '../../features/session/CharacterSelectionStage.tsx'
import { CompositionStage } from '../../features/session/CompositionStage.tsx'
import { GenreSelectionStage } from '../../features/session/GenreSelectionStage.tsx'
import { PitchSelectionStage } from '../../features/session/PitchSelectionStage.tsx'
import { StoryBriefStage } from '../../features/session/StoryBriefStage.tsx'
import { StorySetupStage } from '../../features/session/StorySetupStage.tsx'
import { ToneSelectionStage } from '../../features/session/ToneSelectionStage.tsx'
import {
  useSessionChatMessages,
  useSessionCompositionStream,
  useCurrentSessionHydrationQuery,
  useSessionCurrentSnapshot,
  useSessionEventStream,
  useSessionRuntimeActions,
} from '../../features/session/sessionWorkspaceContext.ts'
import { SessionWorkspaceProvider } from '../../features/session/SessionWorkspaceProvider.tsx'
import { SessionChatPane } from '../../features/session/chat/SessionChatPane.tsx'
import {
  buildSessionChatQuickActions,
  buildSessionChatQuickActionSubmission,
  buildSessionChatSlashCommandHint,
  resolveSessionChatSlashCommand,
  type SessionExplicitChatCommand,
} from '../../features/session/chat/chatCommands.ts'
import {
  buildInitialSessionChatMessages,
  createSessionChatMessage,
} from '../../features/session/chat/sessionChat.ts'
import type { ChatToUiAction } from '../../features/session/chat/chatToUiActions.ts'
import {
  buildIntentActionEchoMessages,
  buildSessionChatMessagesFromHistory,
} from '../../features/session/chat/actionEchoes.ts'
import { SessionFeedStatusIndicator } from '../../features/session/live/SessionFeedStatusIndicator.tsx'
import {
  buildSessionWorkspaceStageViews,
  type SessionWorkspaceStageView,
} from '../../features/session/sessionStageScaffold.ts'
import { getWorkflowStageLabel } from '../../features/session/workflowStages.ts'
import {
  Badge,
  Button,
  ProgressBar,
  TextArea,
  type BadgeTone,
} from '../../shared/ui/primitives.tsx'
import {
  BlockingFeedback,
  FeedbackBanner,
  InlineSpinner,
  SkeletonBlock,
  type FeedbackTone,
} from '../../shared/ui/feedback.tsx'
import {
  CardGrid,
  SelectionCard,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import { getButtonClassName } from '../../shared/ui/buttonStyles.ts'

type StatusBadgeCopy = {
  label: string
  tone: BadgeTone
}

const timestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function getStatusBadgeCopy(status: string): StatusBadgeCopy {
  if (status === 'completed') {
    return {
      label: 'Complete',
      tone: 'success',
    }
  }

  if (status === 'needs_regeneration') {
    return {
      label: 'Needs refresh',
      tone: 'accent',
    }
  }

  if (status === 'in_progress') {
    return {
      label: 'In progress',
      tone: 'brand',
    }
  }

  return {
    label: 'Queued',
    tone: 'warning',
  }
}

function getRuntimeConnectionLabel(connectionState: string) {
  if (connectionState === 'open') {
    return 'Live feed connected'
  }

  if (connectionState === 'connecting' || connectionState === 'reconnecting') {
    return 'Live feed connecting'
  }

  if (connectionState === 'error') {
    return 'Live feed unavailable'
  }

  if (connectionState === 'closed') {
    return 'Live feed paused'
  }

  return 'Live feed idle'
}

function getRuntimeConnectionTone(connectionState: string): BadgeTone {
  if (connectionState === 'open') {
    return 'success'
  }

  if (connectionState === 'error') {
    return 'danger'
  }

  if (connectionState === 'closed') {
    return 'warning'
  }

  return 'brand'
}

function formatSavedAt(value: string) {
  return `Saved ${timestampFormatter.format(new Date(value))}`
}

function buildProgressCopy(snapshot: SessionSnapshot) {
  const { completed_stages: completedStages, total_stages: totalStages } =
    snapshot.progress
  const percent = Math.round((completedStages / totalStages) * 100)

  return {
    label: `${completedStages} of ${totalStages} stages complete`,
    percent,
  }
}

function getStageAvailabilityCopy(
  availability: SessionWorkspaceStageView['availability'],
): StatusBadgeCopy {
  if (availability === 'revisitable') {
    return {
      label: 'Revisitable',
      tone: 'success',
    }
  }

  if (availability === 'unlocked') {
    return {
      label: 'Unlocked',
      tone: 'brand',
    }
  }

  return {
    label: 'Locked',
    tone: 'neutral',
  }
}

function buildPlanFocusCopy(snapshot: SessionSnapshot) {
  if (snapshot.selected_pitch?.logline) {
    return snapshot.selected_pitch.logline
  }

  if (snapshot.story_brief?.normalized_summary) {
    return snapshot.story_brief.normalized_summary
  }

  if (snapshot.story_brief?.story_idea) {
    return snapshot.story_brief.story_idea
  }

  if (snapshot.story_brief?.raw_brief) {
    return snapshot.story_brief.raw_brief
  }

  return 'The structured brief, pitch, and beat choices will accumulate here as the session advances.'
}

function buildProductionCopy(snapshot: SessionSnapshot) {
  if (snapshot.active_composition_job) {
    return `Writing is ${Math.round(snapshot.active_composition_job.progress_percent)}% complete.`
  }

  if (snapshot.active_audio_job) {
    const duration =
      snapshot.active_audio_job.estimated_duration_seconds != null
        ? ` Estimated length ${Math.round(snapshot.active_audio_job.estimated_duration_seconds / 60)} min.`
        : ''

    return `Audio is ${snapshot.active_audio_job.status.replace(/_/g, ' ')}.${duration}`
  }

  if (snapshot.latest_audio_job?.status === 'failed') {
    return (
      snapshot.latest_audio_job.error_message ??
      snapshot.latest_audio_job.stop_reason ??
      'The most recent narration pass failed and needs another attempt.'
    )
  }

  if (snapshot.latest_composition_job?.status === 'failed') {
    return (
      snapshot.latest_composition_job.error_message ??
      snapshot.latest_composition_job.stop_reason ??
      'The most recent writing pass failed and needs another attempt.'
    )
  }

  if (snapshot.latest_story_asset && snapshot.latest_audio_asset) {
    return 'Final reading and listening assets are already available for review.'
  }

  if (snapshot.selected_story_setup) {
    const details = [
      snapshot.selected_story_setup.target_runtime_minutes != null
        ? `~${snapshot.selected_story_setup.target_runtime_minutes} minute runtime`
        : null,
      snapshot.selected_story_setup.target_word_count != null
        ? `${snapshot.selected_story_setup.target_word_count} words`
        : null,
      snapshot.selected_story_setup.chapter_count != null
        ? `${snapshot.selected_story_setup.chapter_count} chapters`
        : null,
      snapshot.selected_story_setup.approximate_scene_count != null
        ? `about ${snapshot.selected_story_setup.approximate_scene_count} scenes`
        : null,
    ].filter(Boolean)

    if (details.length > 0) {
      return details.join(' / ')
    }
  }

  return 'Composition and audio controls will take over this area once the planning stages are complete.'
}

const continuityCategoryOrder = [
  'character',
  'location',
  'object',
  'promise',
  'voice_constraint',
  'unresolved_thread',
  'locked_detail',
] as const

const continuityCategoryLabels: Record<
  (typeof continuityCategoryOrder)[number],
  string
> = {
  character: 'Characters',
  location: 'Locations',
  object: 'Objects',
  promise: 'Promises',
  voice_constraint: 'Voice guardrails',
  unresolved_thread: 'Open threads',
  locked_detail: 'Locked details',
}

function buildContinuityFactGroups(snapshot: SessionSnapshot) {
  const continuityBible = snapshot.continuity_bible
  if (continuityBible == null) {
    return []
  }

  return continuityCategoryOrder
    .map((category) => ({
      category,
      facts: continuityBible.facts.filter((fact) => fact.category === category),
      label: continuityCategoryLabels[category],
    }))
    .filter((group) => group.facts.length > 0)
}

function buildContinuitySourceCopy(snapshot: SessionSnapshot) {
  const continuityBible = snapshot.continuity_bible
  if (continuityBible == null) {
    return null
  }

  const stageLabel =
    continuityBible.source_stage != null
      ? getWorkflowStageLabel(continuityBible.source_stage)
      : 'Session state'
  const summary = continuityBible.source_summary?.trim()

  if (summary) {
    return `Last refreshed from ${stageLabel.toLowerCase()}: ${summary}`
  }

  return `Last refreshed from ${stageLabel.toLowerCase()}.`
}

function buildChatActivityState(
  snapshot: SessionSnapshot,
  pendingActionsCount: number,
) {
  if (snapshot.active_audio_job != null) {
    return {
      activityLabel:
        'Narration rendering is active. The transcript remains readable while the audio pass runs.',
      disabledReason:
        'The composer is paused while audio generation is active. It will reopen after narration settles.',
      isBusy: true,
    }
  }

  if (snapshot.active_composition_job != null) {
    return {
      activityLabel: `Writing is ${Math.round(snapshot.active_composition_job.progress_percent)}% complete. Chat stays available for redirect notes.`,
      disabledReason: null,
      isBusy: true,
    }
  }

  if (pendingActionsCount > 0) {
    const suffix = pendingActionsCount === 1 ? '' : 's'

    return {
      activityLabel: `${pendingActionsCount} chat-requested change${suffix} still need confirmation before they apply.`,
      disabledReason: null,
      isBusy: true,
    }
  }

  return {
    activityLabel:
      'Ready for notes, approvals, and stage edits from the conversation lane.',
    disabledReason: null,
    isBusy: false,
  }
}

function buildStageDetailSummary(stage: SessionWorkspaceStageView) {
  if (stage.detail) {
    return stage.detail
  }

  if (stage.last_event_summary) {
    return stage.last_event_summary
  }

  if (stage.isCurrent) {
    return 'This is the active durable checkpoint for the next structured edit.'
  }

  if (stage.availability === 'locked') {
    return 'This panel is intentionally preview-only until the session reaches this later step.'
  }

  return 'No durable detail is saved here yet, but the scaffold is ready for future controls.'
}

function supportsStageNoteEditing(stage: SessionWorkspaceStageView['stage']) {
  return stage !== 'genre' && stage !== 'tone' && stage !== 'finalize'
}

function buildStageNoteEditorDescription(stage: SessionWorkspaceStageView) {
  if (!supportsStageNoteEditing(stage.stage)) {
    return `${stage.label} is selection-driven, so this note editor stays disabled until dedicated controls land.`
  }

  if (stage.availability === 'locked') {
    return 'Locked stages stay readable, but note editing is disabled until the session reaches that step.'
  }

  if (stage.invalidatesOnEdit.length === 0) {
    return 'This note is durable and replayable, but it does not invalidate any later stage.'
  }

  const invalidationLabels = stage.invalidatesOnEdit.map(getWorkflowStageLabel)

  return `Saving this note records a durable UI event and can refresh ${invalidationLabels.join(', ')}.`
}

function buildStageRoutingCopy(
  currentStage: SessionWorkspaceStageView,
  selectedStage: SessionWorkspaceStageView,
) {
  if (selectedStage.isCurrent) {
    return 'The route and the durable session stage are aligned. Live editors and job views can mount here later without changing the URL pattern.'
  }

  return `The route is previewing ${selectedStage.label.toLowerCase()} via the stage query parameter while the durable session state remains at ${currentStage.label.toLowerCase()}.`
}

function isPlainLeftClick(event: MouseEvent<HTMLAnchorElement>) {
  return !(
    event.button !== 0 ||
    event.metaKey ||
    event.altKey ||
    event.ctrlKey ||
    event.shiftKey
  )
}

function buildChatMessagesFromRecordedEvent(
  event: SessionHistoryEvent,
  snapshot?: SessionSnapshot | null,
) {
  return buildSessionChatMessagesFromHistory(
    {
      session_id: event.session_id,
      latest_sequence_number: event.sequence_number,
      events: [event],
    },
    snapshot,
  )
}

type PendingChatConfirmation = {
  id: string
  action: ChatToUiAction
  summary: string
  title: string
}

function buildPendingChatConfirmationTitle(action: ChatToUiAction) {
  switch (action.action_type) {
    case 'select_genre':
      return 'Apply genre change'
    case 'select_tone':
      return 'Apply tone change'
    case 'regenerate_pitches':
      return 'Generate a new pitch batch'
    case 'refine_pitch':
      return 'Refine this pitch'
    case 'select_pitch':
      return 'Select this pitch'
    case 'regenerate_character_sheet':
      return 'Generate a new character batch'
    case 'refine_character_sheet':
      return 'Refine this character sheet'
    case 'select_character_sheet':
      return 'Select this character sheet'
    case 'regenerate_beat_sheet':
      return 'Generate a new beat-sheet revision'
    case 'refine_beat_sheet':
      return 'Refine this beat sheet'
    case 'accept_beat_sheet':
      return 'Accept this beat sheet'
    case 'update_story_setup':
      return 'Save this story setup'
    case 'start_composition':
      return 'Start composition'
    case 'pause_job':
      return 'Pause writing'
    case 'resume_job':
      return 'Resume writing'
    case 'redirect_composition':
      return 'Queue a composition rewrite'
    default:
      return 'Apply chat change'
  }
}

function canApplyChatAction(action: ChatToUiAction) {
  return (
    action.action_type === 'navigate_to_stage' ||
    action.action_type === 'select_genre' ||
    action.action_type === 'select_tone' ||
    action.action_type === 'update_story_brief' ||
    action.action_type === 'regenerate_pitches' ||
    action.action_type === 'refine_pitch' ||
    action.action_type === 'select_pitch' ||
    action.action_type === 'regenerate_character_sheet' ||
    action.action_type === 'refine_character_sheet' ||
    action.action_type === 'select_character_sheet' ||
    action.action_type === 'regenerate_beat_sheet' ||
    action.action_type === 'refine_beat_sheet' ||
    action.action_type === 'accept_beat_sheet' ||
    action.action_type === 'update_story_setup' ||
    action.action_type === 'start_composition' ||
    (action.action_type === 'pause_job' &&
      action.target_stage === 'composition') ||
    (action.action_type === 'resume_job' &&
      action.target_stage === 'composition') ||
    action.action_type === 'redirect_composition' ||
    action.action_type === 'open_finalize_view'
  )
}

function WorkspaceLoadingState({ sessionId }: { sessionId: string }) {
  return (
    <section
      aria-label={`Session workspace for ${sessionId}`}
      className="workspace-page"
    >
      <header className="panel workspace-topbar" aria-busy="true">
        <div className="workspace-topbar__copy">
          <p className="eyebrow">Session workspace</p>
          <SkeletonBlock className="loading-block--title" />
          <SkeletonBlock className="loading-block--detail" />
        </div>
        <div className="workspace-topbar__status">
          {Array.from({ length: 3 }).map((_, index) => (
            <div key={index} className="workspace-topbar__status-card">
              <SkeletonBlock className="loading-block--detail loading-block--short" />
              <SkeletonBlock className="loading-block--detail" />
            </div>
          ))}
        </div>
      </header>

      <div className="workspace-shell" aria-busy="true">
        <article className="panel workspace-pane">
          <SkeletonBlock className="loading-block--title" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail loading-block--short" />
        </article>
        <article className="panel workspace-pane">
          <SkeletonBlock className="loading-block--title" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail" />
          <SkeletonBlock className="loading-block--detail" />
        </article>
      </div>
    </section>
  )
}

function WorkspaceErrorState({
  errorMessage,
  sessionId,
  onRetry,
}: {
  errorMessage: string
  sessionId: string
  onRetry: () => void
}) {
  return (
    <section
      aria-label={`Session workspace for ${sessionId}`}
      className="workspace-page"
    >
      <BlockingFeedback
        actions={
          <div className="cta-row">
            <button
              className={getButtonClassName({
                size: 'compact',
                tone: 'ghost',
              })}
              type="button"
              onClick={() => void onRetry()}
            >
              Retry
            </button>
            <Link
              className={getButtonClassName({
                size: 'compact',
                tone: 'ghost',
              })}
              to={routePaths.home}
            >
              Return home
            </Link>
          </div>
        }
        bannerTitle="Session snapshot unavailable"
        description={errorMessage}
        eyebrow="Session workspace"
        title="Workspace unavailable"
        tone="warning"
      />
    </section>
  )
}

function buildWorkspaceErrorMessage(error: Error, sessionId: string) {
  if (error.message.includes('Unexpected status code: 404')) {
    return `The session ${sessionId} could not be found in the durable store.`
  }

  return 'The workspace could not load this session right now. Try again once the backend is reachable.'
}

function getWorkspaceConnectionBanner(connectionState: string): {
  description: string
  isBusy?: boolean
  title: string
  tone: FeedbackTone
} | null {
  if (connectionState === 'open') {
    return null
  }

  if (connectionState === 'connecting' || connectionState === 'reconnecting') {
    return {
      description:
        'The durable session shell is loaded. Live event updates are still reconnecting, so recent confirmations may take a moment to appear.',
      isBusy: true,
      title: 'Live feed reconnecting',
      tone: 'info',
    }
  }

  if (connectionState === 'error') {
    return {
      description:
        'The workspace can still render the saved snapshot, but live confirmations and background progress updates are temporarily unavailable.',
      title: 'Live feed unavailable',
      tone: 'warning',
    }
  }

  if (connectionState === 'closed') {
    return {
      description:
        'The saved session remains readable, but live runtime updates are paused until the feed reconnects.',
      title: 'Live feed paused',
      tone: 'warning',
    }
  }

  return {
    description:
      'The workspace is running from the durable snapshot only. Configure the websocket endpoint to start session-scoped live updates.',
    title: 'Live feed idle',
    tone: 'info',
  }
}

function SessionWorkspaceContent({ sessionId }: { sessionId: string }) {
  const [searchParams, setSearchParams] = useSearchParams()
  const hydrationQuery = useCurrentSessionHydrationQuery()
  const runtimeSnapshot = useSessionCurrentSnapshot()
  const chatMessages = useSessionChatMessages()
  const composition = useSessionCompositionStream()
  const eventStream = useSessionEventStream()
  const runtimeStore = useSessionRuntimeActions()
  const snapshot = runtimeSnapshot ?? hydrationQuery.data?.snapshot
  const [stageNoteDraft, setStageNoteDraft] = useState('')
  const [stageNoteError, setStageNoteError] = useState<string | null>(null)
  const [isSavingStageNote, setIsSavingStageNote] = useState(false)
  const [pendingChatConfirmations, setPendingChatConfirmations] = useState<
    PendingChatConfirmation[]
  >([])

  useEffect(() => {
    if (hydrationQuery.data == null || hydrationQuery.isError) {
      return
    }

    runtimeStore.hydrateSessionSnapshot(hydrationQuery.data.snapshot)
  }, [hydrationQuery.data, hydrationQuery.isError, runtimeStore])

  useEffect(() => {
    setPendingChatConfirmations([])
  }, [sessionId])

  useEffect(() => {
    if (
      snapshot == null ||
      chatMessages.length > 0 ||
      hydrationQuery.isPending
    ) {
      return
    }

    const historyMessages =
      hydrationQuery.data != null
        ? buildSessionChatMessagesFromHistory(
            hydrationQuery.data.recent_history,
            snapshot,
          )
        : []

    runtimeStore.replaceChatMessages(
      historyMessages.length > 0
        ? historyMessages
        : buildInitialSessionChatMessages(snapshot),
    )
  }, [
    chatMessages.length,
    hydrationQuery.data,
    hydrationQuery.isPending,
    runtimeStore,
    snapshot,
  ])

  const stageScaffold =
    snapshot == null
      ? null
      : buildSessionWorkspaceStageViews(snapshot, searchParams.get('stage'))
  const selectedStage = stageScaffold?.selectedStage ?? null
  const selectedStageDetail = selectedStage?.detail ?? null
  const selectedStageId = selectedStage?.stage ?? null

  useEffect(() => {
    if (selectedStageId == null) {
      return
    }

    setStageNoteDraft(selectedStageDetail ?? '')
    setStageNoteError(null)
  }, [selectedStageDetail, selectedStageId])

  if (snapshot == null && hydrationQuery.isPending) {
    return <WorkspaceLoadingState sessionId={sessionId} />
  }

  if (snapshot == null) {
    const errorMessage =
      hydrationQuery.error instanceof Error
        ? buildWorkspaceErrorMessage(hydrationQuery.error, sessionId)
        : 'The workspace could not load this session right now.'

    return (
      <WorkspaceErrorState
        errorMessage={errorMessage}
        sessionId={sessionId}
        onRetry={() => {
          void hydrationQuery.refetch()
        }}
      />
    )
  }

  const resolvedStageScaffold = stageScaffold
  if (resolvedStageScaffold == null || selectedStage == null) {
    return (
      <WorkspaceErrorState
        errorMessage="The workspace stage scaffold could not be built."
        sessionId={sessionId}
        onRetry={() => {
          void hydrationQuery.refetch()
        }}
      />
    )
  }

  const activeStage = resolvedStageScaffold.currentStage
  const stageViews = resolvedStageScaffold.stageViews
  const currentStageStatus = getStatusBadgeCopy(activeStage.status)
  const overallStatus = getStatusBadgeCopy(snapshot.overall_status)
  const progress = buildProgressCopy(snapshot)
  const runtimeConnectionLabel = getRuntimeConnectionLabel(
    eventStream.connectionState,
  )
  const chatActivityState = buildChatActivityState(
    snapshot,
    pendingChatConfirmations.length,
  )
  const workspaceConnectionBanner = getWorkspaceConnectionBanner(
    eventStream.connectionState,
  )
  const selectedStageStatus = getStatusBadgeCopy(selectedStage.status)
  const selectedStageAvailability = getStageAvailabilityCopy(
    selectedStage.availability,
  )
  const stageRoutingCopy = buildStageRoutingCopy(activeStage, selectedStage)
  const selectedStageInvalidations = selectedStage.invalidatesOnEdit.map(
    getWorkflowStageLabel,
  )
  const chatQuickActions = buildSessionChatQuickActions({
    snapshot,
    selectedStage: selectedStage.stage,
  })
  const continuityFactGroups = buildContinuityFactGroups(snapshot)
  const continuitySourceCopy = buildContinuitySourceCopy(snapshot)
  const slashCommandHint = buildSessionChatSlashCommandHint(chatQuickActions)
  const stageNoteEditingSupported = supportsStageNoteEditing(
    selectedStage.stage,
  )
  const stageNoteEditingDisabled =
    !stageNoteEditingSupported || selectedStage.availability === 'locked'
  const savedStageDetail = selectedStage.detail ?? ''
  const stageNoteDirty = stageNoteDraft.trim() !== savedStageDetail.trim()

  function appendHistoryEventToChat(event: SessionHistoryEvent) {
    buildChatMessagesFromRecordedEvent(event, snapshot).forEach((message) => {
      runtimeStore.appendChatMessage(message)
    })
  }

  function setPreviewStage(stageId: SessionWorkspaceStageView['stage']) {
    const nextSearchParams = new URLSearchParams(searchParams)

    nextSearchParams.set('stage', stageId)
    setSearchParams(nextSearchParams)
  }

  async function persistUiAction(options: {
    action: string
    stage?: SessionWorkspaceStageView['stage']
    controlId: string
    origin: string
    valueSummary?: string | null
  }) {
    const event = await recordSessionUiAction(sessionId, {
      action: options.action,
      stage: options.stage,
      control_id: options.controlId,
      value_summary: options.valueSummary ?? null,
      origin: options.origin,
    })

    appendHistoryEventToChat(event)
  }

  async function applyGenreSelection(options: {
    genreId?: string | null
    genreLabel?: string | null
    genreSlug?: string | null
    origin: string
    previewCurrentStage?: boolean
  }) {
    const requestBody =
      options.genreId != null
        ? {
            genre_id: options.genreId,
            origin: options.origin,
          }
        : options.genreSlug != null
          ? {
              genre_slug: options.genreSlug,
              origin: options.origin,
            }
          : {
              genre_label: options.genreLabel ?? null,
              origin: options.origin,
            }

    const result = await selectSessionGenre<
      SessionSnapshot,
      SessionHistoryEvent
    >(sessionId, requestBody)

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyToneSelection(options: {
    origin: string
    previewCurrentStage?: boolean
    toneProfileId?: string | null
    toneProfileLabel?: string | null
    toneProfileSlug?: string | null
  }) {
    const requestBody =
      options.toneProfileId != null
        ? {
            tone_profile_id: options.toneProfileId,
            origin: options.origin,
          }
        : options.toneProfileSlug != null
          ? {
              tone_profile_slug: options.toneProfileSlug,
              origin: options.origin,
            }
          : {
              tone_profile_label: options.toneProfileLabel ?? null,
              origin: options.origin,
            }

    const result = await selectSessionTone<
      SessionSnapshot,
      SessionHistoryEvent
    >(sessionId, requestBody)

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyStoryBriefSave(options: {
    audienceNotes?: string | null
    desiredThemes?: string | null
    keyImages?: string | null
    mustHaveElements?: string | null
    normalizedPreferences?: NormalizedBriefPreferencesView | null
    normalizedSummary?: string | null
    origin: string
    planningNotes?: string | null
    previewCurrentStage?: boolean
    rawBrief?: string | null
    storyIdea?: string | null
    editMode?: 'replace' | 'append' | 'merge'
  }) {
    const result = await saveSessionStoryBrief(sessionId, {
      story_idea: options.storyIdea ?? null,
      desired_themes: options.desiredThemes ?? null,
      key_images: options.keyImages ?? null,
      audience_notes: options.audienceNotes ?? null,
      must_have_elements: options.mustHaveElements ?? null,
      raw_brief: options.rawBrief ?? null,
      normalized_summary: options.normalizedSummary,
      normalized_preferences: options.normalizedPreferences,
      planning_notes: options.planningNotes ?? null,
      edit_mode: options.editMode ?? 'replace',
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyPitchGeneration(options: {
    candidateCount: number
    guidance?: string | null
    origin: string
    preserveSelectedPitch?: boolean
    previewCurrentStage?: boolean
  }) {
    const result = await generateSessionPitches(sessionId, {
      candidate_count: options.candidateCount,
      guidance: options.guidance ?? null,
      preserve_selected_pitch: options.preserveSelectedPitch ?? false,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyPitchSelection(options: {
    generationKey?: string | null
    origin: string
    pitchId?: string | null
    pitchIndex?: number | null
    previewCurrentStage?: boolean
    title?: string | null
  }) {
    const result = await selectSessionPitch(sessionId, {
      pitch_id: options.pitchId ?? null,
      generation_key: options.generationKey ?? null,
      pitch_index: options.pitchIndex ?? null,
      title: options.title ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyPitchRefinement(options: {
    generationKey?: string | null
    instructions: string
    origin: string
    pitchId?: string | null
    pitchIndex?: number | null
    title?: string | null
  }) {
    const result = await refineSessionPitch(sessionId, {
      pitch_id: options.pitchId ?? null,
      generation_key: options.generationKey ?? null,
      pitch_index: options.pitchIndex ?? null,
      title: options.title ?? null,
      instructions: options.instructions,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage(result.snapshot.current_stage)

    return result
  }

  async function applyCharacterSheetGeneration(options: {
    candidateCount: number
    guidance?: string | null
    origin: string
    previewCurrentStage?: boolean
  }) {
    const result = await generateSessionCharacterSheets(sessionId, {
      candidate_count: options.candidateCount,
      guidance: options.guidance ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyCharacterSheetSelection(options: {
    origin: string
    characterSheetId?: string | null
    previewCurrentStage?: boolean
    revisionNumber?: number | null
    title?: string | null
  }) {
    const result = await selectSessionCharacterSheet(sessionId, {
      character_sheet_id: options.characterSheetId ?? null,
      revision_number: options.revisionNumber ?? null,
      title: options.title ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyCharacterSheetRefinement(options: {
    instructions: string
    origin: string
    changeSummary?: string | null
    changeImpact?: 'minor' | 'major' | null
    characterSheetId?: string | null
    focusCharacterNames?: string[]
    revisionNumber?: number | null
    title?: string | null
  }) {
    const result = await refineSessionCharacterSheet(sessionId, {
      character_sheet_id: options.characterSheetId ?? null,
      revision_number: options.revisionNumber ?? null,
      title: options.title ?? null,
      instructions: options.instructions,
      focus_character_names: options.focusCharacterNames ?? [],
      change_summary: options.changeSummary ?? null,
      change_impact: options.changeImpact ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage(result.snapshot.current_stage)

    return result
  }

  async function applyBeatSheetGeneration(options: {
    guidance?: string | null
    focusBeats?: string[]
    bedtimeGoal?: string | null
    origin: string
    previewCurrentStage?: boolean
  }) {
    const result = await generateSessionBeatSheet(sessionId, {
      guidance: options.guidance ?? null,
      focus_beats: options.focusBeats ?? [],
      bedtime_goal: options.bedtimeGoal ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyBeatSheetSelection(options: {
    origin: string
    beatSheetId?: string | null
    previewCurrentStage?: boolean
    revisionNumber?: number | null
  }) {
    const result = await selectSessionBeatSheet(sessionId, {
      beat_sheet_id: options.beatSheetId ?? null,
      revision_number: options.revisionNumber ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyBeatSheetRefinement(options: {
    instructions: string
    origin: string
    beatNames?: string[]
    beatSheetId?: string | null
    bedtimeGoal?: string | null
    revisionNumber?: number | null
  }) {
    const result = await refineSessionBeatSheet(sessionId, {
      beat_sheet_id: options.beatSheetId ?? null,
      revision_number: options.revisionNumber ?? null,
      instructions: options.instructions,
      beat_names: options.beatNames ?? [],
      bedtime_goal: options.bedtimeGoal ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage(result.snapshot.current_stage)

    return result
  }

  async function applyBeatSheetEdit(options: {
    origin: string
    beatSheetId?: string | null
    revisionNumber?: number | null
    summary?: string | null
    bedtimeNotes?: string | null
    bedtimeGoal?: string | null
    beatUpdates?: Array<{
      key: string
      summary?: string | null
      emotionalIntent?: string | null
      bedtimeSofteningNote?: string | null
    }>
    summaryText?: string | null
  }) {
    const result = await editSessionBeatSheet(sessionId, {
      beat_sheet_id: options.beatSheetId ?? null,
      revision_number: options.revisionNumber ?? null,
      summary: options.summary ?? null,
      bedtime_notes: options.bedtimeNotes ?? null,
      bedtime_goal: options.bedtimeGoal ?? null,
      beat_updates:
        options.beatUpdates?.map((beatUpdate) => ({
          key: beatUpdate.key,
          summary: beatUpdate.summary ?? null,
          emotional_intent: beatUpdate.emotionalIntent ?? null,
          bedtime_softening_note: beatUpdate.bedtimeSofteningNote ?? null,
        })) ?? [],
      summary_text: options.summaryText ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    return result
  }

  async function applyStorySetupSave(options: {
    targetWordCount?: number | null
    targetRuntimeMinutes?: number | null
    chapterCount?: number | null
    approximateSceneCount?: number | null
    guidanceNotes?: string | null
    origin: string
    previewCurrentStage?: boolean
  }) {
    const result = await saveSessionStorySetup(sessionId, {
      target_word_count: options.targetWordCount,
      target_runtime_minutes: options.targetRuntimeMinutes,
      chapter_count: options.chapterCount,
      approximate_scene_count: options.approximateSceneCount,
      guidance_notes: options.guidanceNotes ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage === true) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  async function applyStoryOutlineSave(options: {
    outlineId?: string | null
    summary?: string | null
    cards: NonNullable<SessionSnapshot['selected_story_outline']>['cards']
    regenerateCardKeys?: string[]
    origin: string
  }) {
    const result = await saveSessionStoryOutline(sessionId, {
      outline_id: options.outlineId ?? null,
      summary: options.summary ?? null,
      cards: options.cards,
      regenerate_card_keys: options.regenerateCardKeys ?? [],
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    return result
  }

  async function applyPlanRevisionRestore(options: {
    origin: string
    revisionNumber: number
    previewCurrentStage?: boolean
  }) {
    const result = await restoreSessionPlanRevision(
      sessionId,
      options.revisionNumber,
      {
        origin: options.origin,
      },
    )

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)

    if (options.previewCurrentStage !== false) {
      setPreviewStage(result.snapshot.current_stage)
    }

    return result
  }

  function resolveCompositionJobId() {
    return (
      snapshot?.active_composition_job?.id ??
      snapshot?.latest_composition_job?.id ??
      null
    )
  }

  async function applyCompositionStart(options: {
    mode?: 'continue' | 'fresh' | 'rewrite'
    instructions?: string | null
    origin: string
    restartFromSegmentIndex?: number | null
  }) {
    const result = await startSessionComposition(sessionId, {
      mode: options.mode ?? 'fresh',
      instructions: options.instructions ?? null,
      restart_from_segment_index: options.restartFromSegmentIndex ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage('composition')

    return result
  }

  async function applyCompositionPause(options: { jobId: string }) {
    const result = await pauseSessionComposition(sessionId, options.jobId)

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage('composition')

    return result
  }

  async function applyCompositionResume(options: { jobId: string }) {
    const result = await resumeSessionComposition(sessionId, options.jobId)

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage('composition')

    return result
  }

  async function applyCompositionCancel(options: { jobId: string }) {
    const result = await cancelSessionComposition(sessionId, options.jobId)

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage('composition')

    return result
  }

  async function applyCompositionRedirect(options: {
    instructions: string
    jobId: string
    origin: string
    rewriteFromSegmentIndex?: number | null
  }) {
    const result = await redirectSessionComposition(sessionId, options.jobId, {
      instructions: options.instructions,
      rewrite_from_segment_index: options.rewriteFromSegmentIndex ?? null,
      origin: options.origin,
    })

    runtimeStore.hydrateSessionSnapshot(result.snapshot)
    appendHistoryEventToChat(result.event)
    setPreviewStage('composition')

    return result
  }

  async function applySupportedChatAction(action: ChatToUiAction) {
    if (action.action_type === 'navigate_to_stage') {
      setPreviewStage(action.target_stage)
      await persistUiAction({
        action: action.action_type,
        stage: action.target_stage,
        controlId: 'chat-intent',
        origin: 'chat',
        valueSummary: getWorkflowStageLabel(action.target_stage),
      })
      return
    }

    if (action.action_type === 'select_genre') {
      await applyGenreSelection({
        genreId: action.extracted_values.genre_id ?? null,
        genreLabel: action.extracted_values.genre_label ?? null,
        genreSlug: action.extracted_values.genre_slug ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'select_tone') {
      await applyToneSelection({
        toneProfileId: action.extracted_values.tone_profile_id ?? null,
        toneProfileLabel: action.extracted_values.tone_profile_label ?? null,
        toneProfileSlug: action.extracted_values.tone_profile_slug ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'update_story_brief') {
      await applyStoryBriefSave({
        storyIdea:
          action.extracted_values.story_idea ??
          action.extracted_values.raw_brief ??
          null,
        desiredThemes: action.extracted_values.desired_themes ?? null,
        keyImages: action.extracted_values.key_images ?? null,
        audienceNotes: action.extracted_values.audience_notes ?? null,
        mustHaveElements: action.extracted_values.must_have_elements ?? null,
        rawBrief: action.extracted_values.raw_brief ?? null,
        normalizedSummary: action.extracted_values.normalized_summary,
        planningNotes: action.extracted_values.planning_notes ?? null,
        editMode: action.extracted_values.edit_mode,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'regenerate_pitches') {
      await applyPitchGeneration({
        candidateCount: action.extracted_values.candidate_count ?? 3,
        guidance: action.extracted_values.guidance ?? null,
        preserveSelectedPitch:
          action.extracted_values.preserve_selected_pitch ?? false,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'refine_pitch') {
      await applyPitchRefinement({
        pitchId: action.extracted_values.pitch_id ?? null,
        generationKey: action.extracted_values.generation_key ?? null,
        pitchIndex: action.extracted_values.pitch_index ?? null,
        title: action.extracted_values.title ?? null,
        instructions: action.extracted_values.instructions,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'select_pitch') {
      await applyPitchSelection({
        pitchId: action.extracted_values.pitch_id ?? null,
        generationKey: action.extracted_values.generation_key ?? null,
        pitchIndex: action.extracted_values.pitch_index ?? null,
        title: action.extracted_values.title ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'regenerate_character_sheet') {
      await applyCharacterSheetGeneration({
        candidateCount: 3,
        guidance: action.extracted_values.guidance ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'refine_character_sheet') {
      await applyCharacterSheetRefinement({
        characterSheetId: action.extracted_values.character_sheet_id ?? null,
        revisionNumber: action.extracted_values.revision_number ?? null,
        title: action.extracted_values.title ?? null,
        instructions: action.extracted_values.instructions,
        focusCharacterNames:
          action.extracted_values.focus_character_names ?? [],
        changeSummary: action.extracted_values.change_summary ?? null,
        changeImpact: action.extracted_values.change_impact ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'select_character_sheet') {
      await applyCharacterSheetSelection({
        characterSheetId: action.extracted_values.character_sheet_id ?? null,
        revisionNumber: action.extracted_values.revision_number ?? null,
        title: action.extracted_values.title ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'regenerate_beat_sheet') {
      await applyBeatSheetGeneration({
        guidance: action.extracted_values.guidance ?? null,
        focusBeats: action.extracted_values.focus_beats ?? [],
        bedtimeGoal: null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'refine_beat_sheet') {
      await applyBeatSheetRefinement({
        instructions: action.extracted_values.instructions,
        beatNames: action.extracted_values.beat_names ?? [],
        bedtimeGoal: action.extracted_values.bedtime_goal ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'accept_beat_sheet') {
      await applyBeatSheetSelection({
        beatSheetId: action.extracted_values.beat_sheet_id ?? null,
        revisionNumber: action.extracted_values.revision_number ?? null,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'update_story_setup') {
      await applyStorySetupSave({
        targetWordCount: action.extracted_values.target_word_count,
        targetRuntimeMinutes: action.extracted_values.target_runtime_minutes,
        chapterCount: action.extracted_values.chapter_count,
        guidanceNotes: action.extracted_values.guidance_notes,
        origin: 'chat',
        previewCurrentStage: false,
      })
      return
    }

    if (action.action_type === 'start_composition') {
      await applyCompositionStart({
        mode: action.extracted_values.mode ?? 'fresh',
        instructions: action.extracted_values.instructions ?? null,
        restartFromSegmentIndex:
          action.extracted_values.restart_from_segment_index ?? null,
        origin: 'chat',
      })
      return
    }

    if (
      action.action_type === 'pause_job' &&
      action.target_stage === 'composition'
    ) {
      const jobId = action.extracted_values.job_id ?? resolveCompositionJobId()

      if (jobId == null) {
        throw new Error('No active composition job is available to pause.')
      }

      await applyCompositionPause({
        jobId,
      })
      return
    }

    if (
      action.action_type === 'resume_job' &&
      action.target_stage === 'composition'
    ) {
      const jobId = action.extracted_values.job_id ?? resolveCompositionJobId()

      if (jobId == null) {
        throw new Error('No paused composition job is available to resume.')
      }

      await applyCompositionResume({
        jobId,
      })
      return
    }

    if (action.action_type === 'redirect_composition') {
      const jobId = resolveCompositionJobId()

      if (jobId == null) {
        throw new Error('No active composition job is available to redirect.')
      }

      await applyCompositionRedirect({
        jobId,
        instructions: action.extracted_values.instructions,
        rewriteFromSegmentIndex:
          action.extracted_values.rewrite_from_segment_index ??
          snapshot?.active_composition_job?.current_segment_index ??
          1,
        origin: 'chat',
      })
      return
    }

    if (action.action_type === 'open_finalize_view') {
      setPreviewStage('finalize')
      await persistUiAction({
        action: action.action_type,
        stage: 'finalize',
        controlId: 'chat-intent',
        origin: 'chat',
        valueSummary: 'Finalize',
      })
    }
  }

  async function submitChatTurn(options: {
    explicitCommand?: SessionExplicitChatCommand | null
    message: string
  }) {
    const submittedAt = new Date().toISOString()

    runtimeStore.appendChatMessage(
      createSessionChatMessage({
        role: 'user',
        body: options.message,
        createdAt: submittedAt,
      }),
    )

    const parsedIntent = await parseSessionChatIntent(
      sessionId,
      options.message,
      {
        explicitCommand: options.explicitCommand ?? null,
      },
    )
    const assistantCreatedAt = new Date().toISOString()

    runtimeStore.appendChatMessage(
      createSessionChatMessage({
        role: 'assistant',
        body: parsedIntent.assistant_response,
        createdAt: assistantCreatedAt,
      }),
    )

    buildIntentActionEchoMessages({
      result: parsedIntent,
      createdAt: assistantCreatedAt,
      idPrefix: `intent-${submittedAt}`,
    }).forEach((actionEcho) => {
      runtimeStore.appendChatMessage(actionEcho)
    })

    const evaluatedActions =
      parsedIntent.policy_evaluation?.evaluated_actions ?? []

    for (const evaluatedAction of evaluatedActions) {
      const action =
        parsedIntent.proposed_actions.actions[evaluatedAction.action_index]

      if (action == null || !canApplyChatAction(action)) {
        continue
      }

      if (
        evaluatedAction.decision === 'accepted' ||
        evaluatedAction.decision === 'accepted_with_side_effects'
      ) {
        await applySupportedChatAction(action).catch(() => {})
        continue
      }

      if (evaluatedAction.decision === 'requires_confirmation') {
        setPendingChatConfirmations((current) => [
          ...current,
          {
            id: `pending-chat-action-${submittedAt}-${evaluatedAction.action_index}`,
            action,
            summary: evaluatedAction.summary,
            title: buildPendingChatConfirmationTitle(action),
          },
        ])
      }
    }
  }

  async function confirmPendingChatAction(actionId: string) {
    const pendingAction = pendingChatConfirmations.find(
      (entry) => entry.id === actionId,
    )

    if (pendingAction == null) {
      return
    }

    await applySupportedChatAction(pendingAction.action)
    setPendingChatConfirmations((current) =>
      current.filter((entry) => entry.id !== actionId),
    )
  }

  function dismissPendingChatAction(actionId: string) {
    setPendingChatConfirmations((current) =>
      current.filter((entry) => entry.id !== actionId),
    )
  }

  async function saveStageNote() {
    if (
      stageNoteEditingDisabled ||
      !stageNoteDirty ||
      isSavingStageNote ||
      selectedStageId == null
    ) {
      return
    }

    setIsSavingStageNote(true)
    setStageNoteError(null)

    try {
      const result = await applySessionContextUpdate(sessionId, {
        target_kind: 'stage_note',
        stage: selectedStageId,
        control_id: 'stage-note-editor',
        origin: 'workspace',
        values: {
          detail: stageNoteDraft,
        },
      })

      runtimeStore.hydrateSessionSnapshot(result.snapshot)
      appendHistoryEventToChat(result.event)
    } catch (error) {
      setStageNoteError(
        error instanceof Error
          ? error.message
          : 'The note could not be saved right now.',
      )
    } finally {
      setIsSavingStageNote(false)
    }
  }

  return (
    <section
      aria-label={`Session workspace for ${snapshot.display_title}`}
      className="workspace-page"
    >
      <header className="panel workspace-topbar">
        <div className="workspace-topbar__copy">
          <p className="eyebrow">Session workspace</p>
          <h1>{snapshot.display_title}</h1>
          <p className="body-copy">
            Chat and stage-driven workflow controls now share one persistent
            surface, with the left lane reserved for conversation and the right
            canvas reserved for structured editing.
          </p>
        </div>

        <dl className="workspace-topbar__status" aria-label="Session status">
          <div className="workspace-topbar__status-card">
            <dt>Current stage</dt>
            <dd>
              <Badge tone={currentStageStatus.tone}>{activeStage.label}</Badge>
            </dd>
          </div>
          <div className="workspace-topbar__status-card">
            <dt>Save status</dt>
            <dd>{formatSavedAt(snapshot.updated_at)}</dd>
          </div>
          <div className="workspace-topbar__status-card">
            <dt>Session ID</dt>
            <dd>{snapshot.id}</dd>
          </div>
          <div className="workspace-topbar__status-card">
            <dt>Live updates</dt>
            <dd>
              <SessionFeedStatusIndicator eventStream={eventStream} />
            </dd>
          </div>
        </dl>

        <div className="workspace-topbar__actions">
          <Badge tone={overallStatus.tone}>{overallStatus.label}</Badge>
          <Link
            className={getButtonClassName({ size: 'compact', tone: 'ghost' })}
            to={routePaths.home}
          >
            Return home
          </Link>
        </div>
      </header>

      {workspaceConnectionBanner != null ? (
        <FeedbackBanner
          className="workspace-page__banner"
          description={workspaceConnectionBanner.description}
          icon={
            workspaceConnectionBanner.isBusy ? (
              <InlineSpinner label="Live feed status update" />
            ) : undefined
          }
          title={workspaceConnectionBanner.title}
          tone={workspaceConnectionBanner.tone}
        />
      ) : null}

      <div className="workspace-shell" data-testid="workspace-route">
        <aside className="panel workspace-pane workspace-pane--chat">
          <SessionChatPane
            activityLabel={chatActivityState.activityLabel}
            connectionLabel={runtimeConnectionLabel}
            connectionTone={getRuntimeConnectionTone(
              eventStream.connectionState,
            )}
            disabledReason={chatActivityState.disabledReason}
            isBusy={chatActivityState.isBusy}
            messages={chatMessages}
            onConfirmPendingAction={confirmPendingChatAction}
            onDismissPendingAction={dismissPendingChatAction}
            onQuickAction={async (commandId) => {
              const submission = buildSessionChatQuickActionSubmission({
                commandId,
                snapshot,
                selectedStage: selectedStage.stage,
              })

              if (submission == null) {
                throw new Error('The requested quick action is not available.')
              }

              await submitChatTurn({
                message: submission.message,
                explicitCommand: submission.explicitCommand,
              })
            }}
            onSubmit={async (message) => {
              const commandSubmission = resolveSessionChatSlashCommand({
                input: message,
                snapshot,
                selectedStage: selectedStage.stage,
              })

              await submitChatTurn({
                message,
                explicitCommand: commandSubmission?.explicitCommand ?? null,
              })
            }}
            pendingConfirmations={pendingChatConfirmations}
            quickActions={chatQuickActions}
            slashCommandHint={slashCommandHint}
          />
        </aside>

        <section className="panel workspace-pane workspace-pane--canvas">
          <div className="pane-heading">
            <div>
              <h2>Workflow canvas</h2>
              <p className="body-copy">
                The main pane keeps enough width for forms, stage review, and
                later composition or audio progress views.
              </p>
            </div>
            <Badge tone={currentStageStatus.tone}>
              {currentStageStatus.label}
            </Badge>
          </div>

          <section
            aria-label="Workflow scaffold"
            className="workspace-stage-shell"
          >
            <nav
              aria-label="Stage navigator"
              className="workspace-stage-navigator"
            >
              <div className="panel-heading">
                <div>
                  <h2>Stage navigator</h2>
                  <p>
                    Every required workflow step is visible now, with URL-backed
                    panel selection that can coexist with backend-owned stage
                    truth.
                  </p>
                </div>
              </div>

              <ol className="workspace-stage-nav__list">
                {stageViews.map((stage) => {
                  const stageStatus = getStatusBadgeCopy(stage.status)
                  const availabilityCopy = getStageAvailabilityCopy(
                    stage.availability,
                  )

                  return (
                    <li key={stage.stage}>
                      <Link
                        aria-current={stage.isSelected ? 'step' : undefined}
                        className="workflow-card-link"
                        onClick={(event) => {
                          if (!isPlainLeftClick(event) || stage.isSelected) {
                            return
                          }

                          void persistUiAction({
                            action: 'navigate_to_stage',
                            stage: stage.stage,
                            controlId: 'stage-navigator',
                            origin: 'workspace',
                            valueSummary: stage.label,
                          }).catch(() => {})
                        }}
                        to={buildSessionWorkspacePath(snapshot.id, {
                          stage: stage.stage,
                        })}
                      >
                        <SelectionCard
                          description={stage.description}
                          eyebrow={`Stage ${(stage.index + 1)
                            .toString()
                            .padStart(2, '0')}`}
                          footer={
                            stage.isCurrent
                              ? 'This is the durable current stage saved by the backend.'
                              : stage.availability === 'locked'
                                ? 'Locked stages stay previewable without implying they are editable yet.'
                                : 'Available stages can mount richer editors later without changing the shell.'
                          }
                          leading={(stage.index + 1)
                            .toString()
                            .padStart(2, '0')}
                          meta={
                            <>
                              <Badge tone={stageStatus.tone}>
                                {stageStatus.label}
                              </Badge>
                              <Badge tone={availabilityCopy.tone}>
                                {availabilityCopy.label}
                              </Badge>
                            </>
                          }
                          selected={stage.isSelected}
                          title={stage.label}
                        />
                      </Link>
                    </li>
                  )
                })}
              </ol>
            </nav>

            <article className="workspace-stage-detail">
              <div className="workspace-stage-detail__hero">
                <div>
                  <p className="eyebrow">Stage scaffold</p>
                  <h2>{selectedStage.scaffoldTitle}</h2>
                  <p className="body-copy">{selectedStage.scaffoldSummary}</p>
                </div>

                <div className="workspace-stage-detail__badges">
                  <Badge tone={selectedStageStatus.tone}>
                    {selectedStageStatus.label}
                  </Badge>
                  <Badge tone={selectedStageAvailability.tone}>
                    {selectedStageAvailability.label}
                  </Badge>
                </div>
              </div>

              <p className="workspace-stage-detail__note">{stageRoutingCopy}</p>

              {selectedStage.stage === 'genre' ? (
                <GenreSelectionStage
                  onPreviewStage={setPreviewStage}
                  onSelectGenre={applyGenreSelection}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'tone' ? (
                <ToneSelectionStage
                  onPreviewStage={setPreviewStage}
                  onSelectTone={applyToneSelection}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'brief' ? (
                <StoryBriefStage
                  onPreviewStage={setPreviewStage}
                  onSaveStoryBrief={applyStoryBriefSave}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'pitches' ? (
                <PitchSelectionStage
                  onGeneratePitches={applyPitchGeneration}
                  onPreviewStage={setPreviewStage}
                  onRefinePitch={applyPitchRefinement}
                  onRestorePlanRevision={applyPlanRevisionRestore}
                  onSelectPitch={applyPitchSelection}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'characters' ? (
                <CharacterSelectionStage
                  onGenerateCharacterSheets={applyCharacterSheetGeneration}
                  onPreviewStage={setPreviewStage}
                  onRefineCharacterSheet={applyCharacterSheetRefinement}
                  onRestorePlanRevision={applyPlanRevisionRestore}
                  onSelectCharacterSheet={applyCharacterSheetSelection}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'beats' ? (
                <BeatSheetStage
                  onEditBeatSheet={applyBeatSheetEdit}
                  onGenerateBeatSheet={applyBeatSheetGeneration}
                  onPreviewStage={setPreviewStage}
                  onRefineBeatSheet={applyBeatSheetRefinement}
                  onRestorePlanRevision={applyPlanRevisionRestore}
                  onSelectBeatSheet={applyBeatSheetSelection}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'story_setup' ? (
                <StorySetupStage
                  onPreviewStage={setPreviewStage}
                  onRestorePlanRevision={applyPlanRevisionRestore}
                  onSaveStoryOutline={applyStoryOutlineSave}
                  onSaveStorySetup={applyStorySetupSave}
                  selectedStage={selectedStage}
                  snapshot={snapshot}
                />
              ) : selectedStage.stage === 'composition' ? (
                <CompositionStage
                  composition={composition}
                  connectionState={eventStream.connectionState}
                  onCancelComposition={async (jobId) =>
                    applyCompositionCancel({
                      jobId,
                    })
                  }
                  onPauseComposition={async (jobId) =>
                    applyCompositionPause({
                      jobId,
                    })
                  }
                  onRedirectComposition={async (options) => {
                    const jobId = resolveCompositionJobId()

                    if (jobId == null) {
                      throw new Error(
                        'No active composition job is available to redirect.',
                      )
                    }

                    return applyCompositionRedirect({
                      jobId,
                      instructions: options.instructions,
                      rewriteFromSegmentIndex:
                        options.rewriteFromSegmentIndex ?? null,
                      origin: 'workspace',
                    })
                  }}
                  onResumeComposition={async (jobId) =>
                    applyCompositionResume({
                      jobId,
                    })
                  }
                  onReturnToPlan={async () => {
                    setPreviewStage('story_setup')
                    await persistUiAction({
                      action: 'navigate_to_stage',
                      stage: 'story_setup',
                      controlId: 'composition-return-to-plan',
                      origin: 'workspace',
                      valueSummary: getWorkflowStageLabel('story_setup'),
                    })
                  }}
                  onStartComposition={async (body) =>
                    applyCompositionStart({
                      mode: body.mode ?? 'fresh',
                      instructions: body.instructions ?? null,
                      restartFromSegmentIndex:
                        body.restart_from_segment_index ?? null,
                      origin: body.origin ?? 'workspace',
                    })
                  }
                  snapshot={snapshot}
                />
              ) : (
                <>
                  <CardGrid
                    className="workspace-stage-detail__cards"
                    columns={3}
                  >
                    <SummaryPanel
                      description="Accepted detail, last-event summaries, and later live job progress can all drop into the same compact summary shell."
                      label="Current session signal"
                      title={buildStageDetailSummary(selectedStage)}
                    />

                    <SummaryPanel
                      description="Navigator links preview a stage through routing instead of mutating the backend-owned session snapshot in the browser."
                      label="Route mapping"
                      title={
                        <span className="workspace-stage-detail__route">
                          ?stage={selectedStage.stage}
                        </span>
                      }
                    />

                    <SummaryPanel
                      description={
                        selectedStageInvalidations.length > 0
                          ? selectedStageInvalidations.join(', ')
                          : 'Finalize sits at the end of the workflow and can remain review-only.'
                      }
                      label="Downstream impact"
                      title={
                        selectedStageInvalidations.length > 0
                          ? `Editing this step can refresh ${selectedStageInvalidations.length} later stage${selectedStageInvalidations.length === 1 ? '' : 's'}.`
                          : 'This terminal review step does not invalidate anything later.'
                      }
                    />
                  </CardGrid>

                  <section className="workspace-stage-panel">
                    <div className="panel-heading">
                      <div>
                        <h3>Stage note</h3>
                        <p>{buildStageNoteEditorDescription(selectedStage)}</p>
                      </div>
                      <Badge tone={selectedStageStatus.tone}>
                        {selectedStageStatus.label}
                      </Badge>
                    </div>

                    <TextArea
                      description="Saved notes become durable session context, show up in replayable history, and feed the backend agent summary."
                      disabled={stageNoteEditingDisabled}
                      error={stageNoteError}
                      label={`${selectedStage.label} note`}
                      onChange={(event) => {
                        setStageNoteDraft(event.currentTarget.value)
                      }}
                      rows={5}
                      value={stageNoteDraft}
                    />

                    <div className="cta-row">
                      <Button
                        disabled={
                          stageNoteEditingDisabled ||
                          !stageNoteDirty ||
                          isSavingStageNote
                        }
                        onClick={() => {
                          void saveStageNote()
                        }}
                        tone="primary"
                      >
                        {isSavingStageNote ? 'Saving note...' : 'Save note'}
                      </Button>
                      <Button
                        disabled={
                          stageNoteEditingDisabled ||
                          !stageNoteDirty ||
                          isSavingStageNote
                        }
                        onClick={() => {
                          setStageNoteDraft(savedStageDetail)
                          setStageNoteError(null)
                        }}
                        tone="ghost"
                      >
                        Reset
                      </Button>
                    </div>
                  </section>

                  <SessionStageEditorPreview
                    invalidationLabels={selectedStageInvalidations}
                    selectedStage={selectedStage}
                    snapshot={snapshot}
                  />

                  <section className="workspace-stage-detail__list">
                    <div className="panel-heading">
                      <div>
                        <h3>Planned controls</h3>
                        <p>
                          These placeholder bullets mark the extension points
                          for the real business logic that will arrive in later
                          prompts.
                        </p>
                      </div>
                    </div>

                    <ul>
                      {selectedStage.scaffoldBullets.map((bullet) => (
                        <li key={bullet}>{bullet}</li>
                      ))}
                    </ul>
                  </section>
                </>
              )}
            </article>
          </section>

          <section
            aria-label="Workspace overview"
            className="workspace-overview-grid"
          >
            <SummaryPanel label="Progress">
              <ProgressBar
                aria-label={`${snapshot.display_title} workflow progress`}
                hint={`Resume at ${getWorkflowStageLabel(snapshot.resume_stage)} with ${progress.percent}% of the workflow currently complete.`}
                label="Workflow progress"
                value={progress.percent}
                valueText={progress.label}
              />
            </SummaryPanel>

            <SummaryPanel
              description={buildPlanFocusCopy(snapshot)}
              label="Story lane"
              title={`${snapshot.selected_genre?.label ?? 'Genre pending'} / ${snapshot.selected_tone_profile?.label ?? 'Tone pending'}`}
            />

            <SummaryPanel
              description={buildProductionCopy(snapshot)}
              label="Production"
              title={activeStage.label}
            />
          </section>

          {snapshot.continuity_bible != null &&
          continuityFactGroups.length > 0 ? (
            <section
              aria-label="Continuity bible"
              className="workspace-stage-panel continuity-inspector"
            >
              <div className="panel-heading">
                <div>
                  <h3>Continuity bible</h3>
                  <p>{snapshot.continuity_bible.summary_text}</p>
                </div>
                <Badge tone="brand">
                  Revision {snapshot.continuity_bible.revision_number}
                </Badge>
              </div>

              {continuitySourceCopy != null ? (
                <p className="workspace-stage-detail__note">
                  {continuitySourceCopy}
                </p>
              ) : null}

              <CardGrid columns={3}>
                {continuityFactGroups.map((group) => (
                  <SummaryPanel
                    key={group.category}
                    label={group.label}
                    title={`${group.facts.length} fact${group.facts.length === 1 ? '' : 's'}`}
                    tone={
                      group.category === 'voice_constraint' ||
                      group.category === 'unresolved_thread'
                        ? 'accent'
                        : 'default'
                    }
                  >
                    <ul className="continuity-inspector__list">
                      {group.facts.map((fact) => (
                        <li key={fact.key}>
                          <strong>{fact.title}</strong>
                          <span>{fact.detail}</span>
                        </li>
                      ))}
                    </ul>
                  </SummaryPanel>
                ))}
              </CardGrid>
            </section>
          ) : null}
        </section>
      </div>
    </section>
  )
}

export function SessionWorkspacePage() {
  const { sessionId = 'unknown-session' } = useParams()

  return (
    <SessionWorkspaceProvider key={sessionId} sessionId={sessionId}>
      <SessionWorkspaceErrorBoundary sessionId={sessionId}>
        <SessionWorkspaceContent sessionId={sessionId} />
      </SessionWorkspaceErrorBoundary>
    </SessionWorkspaceProvider>
  )
}
