import { useEffect, useId, useMemo, useState } from 'react'
import type {
  AudioJobView,
  CompositionSegmentView,
  SessionArtifactInventoryItemView,
  SessionArtifactInventoryStatus,
  SessionAssetView,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { FeedbackBanner, InlineSpinner } from '../../shared/ui/feedback.tsx'
import {
  Badge,
  Button,
  ProgressBar,
  type BadgeTone,
} from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import {
  fetchSessionAssetText,
  resolveSessionAssetStreamUrl,
} from './sessionArtifacts.ts'
import { useSessionArtifactInventoryQuery } from './sessionQueries.ts'
import { SegmentVersionComparePanel } from './SegmentVersionComparePanel.tsx'

type FinalizeStageProps = {
  onAcceptRewrite: (jobId: string) => Promise<unknown>
  onDownloadAudio: () => void
  onDownloadStoryExport: () => void
  onKeepExploringRewrite: (segmentIndex: number) => void
  onRejectRewrite: (jobId: string) => Promise<unknown>
  onRestoreSegmentVersion: (
    segmentIndex: number,
    versionId: string,
  ) => Promise<unknown>
  onReturnToComposition: () => void
  snapshot: SessionSnapshot
}

type ReviewTab = 'read' | 'listen'

type StoryBlock =
  | {
      content: string
      kind: 'heading'
    }
  | {
      content: string
      kind: 'paragraph'
    }

type AudioReviewState =
  | 'planned'
  | 'queued'
  | 'generating'
  | 'mixing'
  | 'paused'
  | 'failed'
  | 'completed'

type ActionState = 'acceptRewrite' | 'rejectRewrite' | 'restoreVersion' | null

const reviewTimestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function countWords(value: string) {
  const normalizedValue = value.replace(/^#{1,6}\s+/gmu, '').trim()

  if (normalizedValue.length === 0) {
    return 0
  }

  return normalizedValue.split(/\s+/u).length
}

function formatTimestamp(value: string | null | undefined) {
  if (value == null) {
    return null
  }

  const parsedValue = new Date(value)
  if (Number.isNaN(parsedValue.getTime())) {
    return null
  }

  return reviewTimestampFormatter.format(parsedValue)
}

function formatDurationLabel(value: number | null | undefined) {
  if (value == null || !Number.isFinite(value) || value <= 0) {
    return null
  }

  const roundedSeconds = Math.round(value)
  const minutes = Math.floor(roundedSeconds / 60)
  const seconds = roundedSeconds % 60

  if (minutes <= 0) {
    return `${seconds}s`
  }

  return `${minutes}m ${seconds.toString().padStart(2, '0')}s`
}

function humanizeToken(value: string | null | undefined) {
  if (value == null || value.length === 0) {
    return null
  }

  return value.replace(/_/g, ' ')
}

function readDetailsRecord(value: unknown): Record<string, unknown> | null {
  return value != null && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null
}

function readNestedRecord(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  return readDetailsRecord(value?.[key])
}

function readOptionalNumber(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  const rawValue = value?.[key]
  return typeof rawValue === 'number' && Number.isFinite(rawValue)
    ? rawValue
    : null
}

function readOptionalString(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  const rawValue = value?.[key]
  return typeof rawValue === 'string' && rawValue.trim().length > 0
    ? rawValue.trim()
    : null
}

function buildCompiledAudioMeta(asset: SessionAssetView | null | undefined) {
  if (asset == null) {
    return []
  }

  const details = readDetailsRecord(asset.details)
  const generation = readNestedRecord(details, 'generation')
  const mix = readNestedRecord(details, 'mix')
  const metadata: string[] = []

  const runtimeLabel = formatDurationLabel(asset.duration_seconds)
  if (runtimeLabel != null) {
    metadata.push(`Runtime ${runtimeLabel}`)
  }

  const voiceName = readOptionalString(generation, 'voice_name')
  const voiceKey = readOptionalString(generation, 'voice_key')
  const voiceLabel = voiceName ?? humanizeToken(voiceKey)
  if (voiceLabel != null) {
    metadata.push(`Voice ${voiceLabel}`)
  }

  const mixApplied = mix?.applied
  if (mixApplied === true) {
    metadata.push('Music mixed')
  } else if (mixApplied === false) {
    metadata.push('Voice only')
  }

  const publishedAtLabel = formatTimestamp(asset.ready_at)
  if (publishedAtLabel != null) {
    metadata.push(`Published ${publishedAtLabel}`)
  }

  return metadata
}

function resolveCurrentSegmentText(segment: CompositionSegmentView) {
  const currentVersion =
    segment.versions.find(
      (version) => version.id === segment.current_version_id,
    ) ??
    segment.versions.find(
      (version) =>
        version.is_current &&
        version.acceptance_state === 'accepted' &&
        version.text_content != null,
    ) ??
    segment.versions.find(
      (version) =>
        version.acceptance_state === 'accepted' && version.text_content != null,
    ) ??
    segment.versions.find(
      (version) =>
        version.status === 'completed' && version.text_content != null,
    )

  const textContent = currentVersion?.text_content?.trim()
  return textContent != null && textContent.length > 0 ? textContent : null
}

function buildFallbackStoryText(snapshot: SessionSnapshot) {
  const compositionJob =
    snapshot.active_composition_job ?? snapshot.latest_composition_job ?? null

  const acceptedStory = compositionJob?.accepted_story_so_far?.trim()
  if (acceptedStory != null && acceptedStory.length > 0) {
    return acceptedStory
  }

  const partialOutput = compositionJob?.latest_partial_output?.trim()
  if (partialOutput != null && partialOutput.length > 0) {
    return partialOutput
  }

  const segmentTexts = (snapshot.composition_segments ?? [])
    .map((segment) => resolveCurrentSegmentText(segment))
    .filter((value): value is string => value != null)

  if (segmentTexts.length === 0) {
    return null
  }

  return segmentTexts.join('\n\n')
}

function buildStoryBlocks(value: string): StoryBlock[] {
  return value
    .split(/\n{2,}/u)
    .map((block) => block.trim())
    .filter(Boolean)
    .map((block) => {
      const headingMatch = block.match(/^#{1,6}\s+(.+)$/u)
      if (headingMatch != null) {
        return {
          kind: 'heading' as const,
          content: headingMatch[1].trim(),
        }
      }

      return {
        kind: 'paragraph' as const,
        content: block.replace(/\n+/gu, ' ').trim(),
      }
    })
}

function buildLengthTargetsCopy(snapshot: SessionSnapshot) {
  const storySetup = snapshot.selected_story_setup
  if (storySetup == null) {
    return 'Targets are still flexible.'
  }

  const parts: string[] = []
  if (storySetup.target_word_count != null) {
    parts.push(`${storySetup.target_word_count.toLocaleString()} words`)
  }
  if (storySetup.target_runtime_minutes != null) {
    parts.push(`~${storySetup.target_runtime_minutes} min`)
  }
  if (storySetup.chapter_count != null) {
    parts.push(
      `${storySetup.chapter_count} ${storySetup.chapter_count === 1 ? 'chapter' : 'chapters'}`,
    )
  } else if (storySetup.approximate_scene_count != null) {
    parts.push(
      `${storySetup.approximate_scene_count} ${storySetup.approximate_scene_count === 1 ? 'scene' : 'scenes'}`,
    )
  }

  return parts.length > 0 ? parts.join(' • ') : 'Targets are still flexible.'
}

function resolveAudioReviewState(
  audioJob: AudioJobView | null,
  finalAudioReady: boolean,
): AudioReviewState {
  if (audioJob == null) {
    return finalAudioReady ? 'completed' : 'planned'
  }

  if (audioJob.status === 'completed') {
    return 'completed'
  }

  if (audioJob.status === 'failed' || audioJob.status === 'cancelled') {
    return 'failed'
  }

  if (audioJob.status === 'paused') {
    return 'paused'
  }

  if (audioJob.status === 'queued') {
    return 'queued'
  }

  const currentStep = audioJob.current_step?.toLowerCase() ?? ''
  const allSegmentsRendered =
    audioJob.total_segments != null &&
    audioJob.completed_segments != null &&
    audioJob.total_segments > 0 &&
    audioJob.completed_segments >= audioJob.total_segments

  if (
    currentStep.includes('mix') ||
    currentStep.includes('publish') ||
    currentStep.includes('assemble') ||
    allSegmentsRendered
  ) {
    return 'mixing'
  }

  return 'generating'
}

function getAudioBadgeTone(
  state: AudioReviewState,
  options: {
    showingPreviousMaster: boolean
  },
): BadgeTone {
  const { showingPreviousMaster } = options

  if (showingPreviousMaster) {
    return 'warning'
  }

  if (state === 'completed') {
    return 'success'
  }

  if (state === 'failed') {
    return 'danger'
  }

  if (state === 'paused') {
    return 'warning'
  }

  if (state === 'generating' || state === 'mixing') {
    return 'accent'
  }

  if (state === 'queued') {
    return 'brand'
  }

  return 'neutral'
}

function getAudioStatusLabel(
  state: AudioReviewState,
  options: {
    finalAudioReady: boolean
    showingPreviousMaster: boolean
  },
) {
  const { finalAudioReady, showingPreviousMaster } = options

  if (showingPreviousMaster) {
    return finalAudioReady
      ? 'Previous master still playable'
      : 'Previous master still available'
  }

  switch (state) {
    case 'completed':
      return 'Ready to listen'
    case 'failed':
      return 'Needs another narration pass'
    case 'paused':
      return 'Narration paused'
    case 'mixing':
      return 'Final narration assembly underway'
    case 'generating':
      return 'Narration is rendering'
    case 'queued':
      return 'Narration queued'
    default:
      return 'Narration not started'
  }
}

function buildAudioStatusCopy(options: {
  audioJob: AudioJobView | null
  finalAudioReady: boolean
  renderState: AudioReviewState
  showingPreviousMaster: boolean
}) {
  const { audioJob, finalAudioReady, renderState, showingPreviousMaster } =
    options

  if (showingPreviousMaster) {
    if (renderState === 'failed') {
      return (
        audioJob?.error_message ??
        audioJob?.stop_reason ??
        'The latest narration attempt stopped, but the previous published master is still available for listening.'
      )
    }

    return 'A previous published narration master stays available while a replacement pass catches up.'
  }

  if (finalAudioReady) {
    return 'The merged narration master is ready for a final spot-check or full listen.'
  }

  if (renderState === 'failed') {
    return (
      audioJob?.error_message ??
      audioJob?.stop_reason ??
      'Narration stopped before a playable master was published.'
    )
  }

  if (renderState === 'paused') {
    return 'Narration is paused with the current checkpoint preserved.'
  }

  if (renderState === 'mixing') {
    return 'Narration segments are rendered and the merged master is assembling now.'
  }

  if (renderState === 'generating') {
    return (
      audioJob?.current_step ??
      'Narration is rendering segment by segment from the accepted manuscript.'
    )
  }

  if (renderState === 'queued') {
    return 'Narration is queued and waiting for the worker to begin.'
  }

  return 'Narration will appear here once the audio stage publishes a compiled master.'
}

function getStoryBadgeTone(options: {
  finalStoryReady: boolean
  storyError: string | null
  storyState: 'idle' | 'loading' | 'ready' | 'error'
  usingFallbackStoryText: boolean
  reviewPending: boolean
}) {
  const {
    finalStoryReady,
    reviewPending,
    storyError,
    storyState,
    usingFallbackStoryText,
  } = options

  if (storyState === 'ready') {
    return 'success'
  }

  if (storyError != null) {
    return usingFallbackStoryText ? 'warning' : 'danger'
  }

  if (finalStoryReady && storyState === 'loading') {
    return 'accent'
  }

  if (usingFallbackStoryText) {
    return 'accent'
  }

  if (reviewPending) {
    return 'warning'
  }

  return 'neutral'
}

function getStoryStatusLabel(options: {
  finalStoryReady: boolean
  storyError: string | null
  storyState: 'idle' | 'loading' | 'ready' | 'error'
  usingFallbackStoryText: boolean
  reviewPending: boolean
}) {
  const {
    finalStoryReady,
    reviewPending,
    storyError,
    storyState,
    usingFallbackStoryText,
  } = options

  if (storyState === 'ready') {
    return 'Ready to read'
  }

  if (storyError != null) {
    return usingFallbackStoryText
      ? 'Showing accepted manuscript snapshot'
      : 'Inline manuscript unavailable'
  }

  if (finalStoryReady && storyState === 'loading') {
    return 'Loading final manuscript'
  }

  if (usingFallbackStoryText) {
    return 'Accepted manuscript snapshot'
  }

  if (reviewPending) {
    return 'Rewrite decision pending'
  }

  return 'Manuscript pending'
}

function buildFinalizeHeroTitle(options: {
  finalAudioReady: boolean
  finalStoryReady: boolean
  reviewPending: boolean
}) {
  const { finalAudioReady, finalStoryReady, reviewPending } = options

  if (reviewPending) {
    return 'Resolve the last rewrite, then settle into the final read and listen pass.'
  }

  if (finalStoryReady && finalAudioReady) {
    return 'The bedtime story is ready for its last calm pass.'
  }

  if (finalStoryReady) {
    return 'The manuscript is ready to read while narration finishes catching up.'
  }

  if (finalAudioReady) {
    return 'Narration is ready while the final manuscript syncs into the review surface.'
  }

  return 'Final review keeps the accepted manuscript, narration status, and exports in one quiet finish-line view.'
}

function buildFinalizeHeroDescription(options: {
  audioStatusCopy: string
  finalAudioReady: boolean
  finalStoryReady: boolean
  reviewPending: boolean
  storyStatusLabel: string
}) {
  const {
    audioStatusCopy,
    finalAudioReady,
    finalStoryReady,
    reviewPending,
    storyStatusLabel,
  } = options

  if (reviewPending) {
    return 'Late rewrite decisions stay explicit here, so the story never feels finalized by accident.'
  }

  if (finalStoryReady && finalAudioReady) {
    return 'Read the finished story, listen to the merged narration master, and keep the exports close at hand.'
  }

  if (finalStoryReady) {
    return `${storyStatusLabel}. ${audioStatusCopy}`
  }

  if (finalAudioReady) {
    return `${audioStatusCopy} The text surface will switch to the durable final manuscript as soon as it is available.`
  }

  return 'This stage stays useful even when only part of the finish line is ready, so reading, listening, and export status never disappear behind a loading gap.'
}

function getArtifactBadgeTone(
  status: SessionArtifactInventoryStatus,
): BadgeTone {
  switch (status) {
    case 'ready':
      return 'success'
    case 'generating':
      return 'accent'
    case 'failed':
      return 'danger'
    case 'stale':
      return 'warning'
    default:
      return 'neutral'
  }
}

function formatArtifactStatusLabel(
  status: SessionArtifactInventoryStatus,
) {
  switch (status) {
    case 'ready':
      return 'Ready'
    case 'generating':
      return 'Generating'
    case 'failed':
      return 'Failed'
    case 'stale':
      return 'Stale'
    default:
      return 'Missing'
  }
}

function resolveArtifactFilename(
  item: SessionArtifactInventoryItemView,
) {
  const accessFilename = item.asset?.access?.filename?.trim()
  if (accessFilename != null && accessFilename.length > 0) {
    return accessFilename
  }

  const objectPath = item.asset?.object_path?.trim()
  if (objectPath == null || objectPath.length === 0) {
    return null
  }

  const objectPathParts = objectPath.split('/').filter(Boolean)
  return objectPathParts.at(-1) ?? null
}

export function FinalizeStage({
  onAcceptRewrite,
  onDownloadAudio,
  onDownloadStoryExport,
  onKeepExploringRewrite,
  onRejectRewrite,
  onRestoreSegmentVersion,
  onReturnToComposition,
  snapshot,
}: FinalizeStageProps) {
  const [actionError, setActionError] = useState<string | null>(null)
  const [actionState, setActionState] = useState<ActionState>(null)
  const fallbackStoryText = useMemo(
    () => buildFallbackStoryText(snapshot),
    [snapshot],
  )
  const initialTab: ReviewTab =
    snapshot.latest_story_asset != null || fallbackStoryText != null
      ? 'read'
      : 'listen'
  const [activeTab, setActiveTab] = useState<ReviewTab>(initialTab)
  const [storyAssetText, setStoryAssetText] = useState<string | null>(null)
  const [storyTextState, setStoryTextState] = useState<
    'idle' | 'loading' | 'ready' | 'error'
  >('idle')
  const [storyTextError, setStoryTextError] = useState<string | null>(null)
  const tabSetId = useId()
  const artifactInventoryQuery = useSessionArtifactInventoryQuery(snapshot.id)

  const compositionSegments = snapshot.composition_segments ?? []
  const reviewJob = snapshot.latest_composition_job?.pending_review
    ? snapshot.latest_composition_job
    : null
  const finalStoryReady = snapshot.latest_story_asset != null
  const finalAudioReady = snapshot.latest_audio_asset != null
  const displayAudioJob =
    snapshot.active_audio_job ?? snapshot.latest_audio_job ?? null
  const audioRenderState = resolveAudioReviewState(
    displayAudioJob,
    finalAudioReady,
  )
  const audioStreamUrl = resolveSessionAssetStreamUrl(
    snapshot.latest_audio_asset,
  )
  const compiledAudioMeta = useMemo(
    () => buildCompiledAudioMeta(snapshot.latest_audio_asset),
    [snapshot.latest_audio_asset],
  )
  const showingPreviousMaster =
    snapshot.latest_audio_asset?.audio_job_id != null &&
    displayAudioJob != null &&
    snapshot.latest_audio_asset.audio_job_id !== displayAudioJob.id
  const displayStoryText = storyAssetText ?? fallbackStoryText ?? null
  const storyBlocks = useMemo(
    () =>
      displayStoryText != null
        ? buildStoryBlocks(displayStoryText)
        : ([] as StoryBlock[]),
    [displayStoryText],
  )
  const usingFallbackStoryText =
    storyAssetText == null && fallbackStoryText != null
  const storyWordCount = useMemo(() => {
    const assetWordCount = readOptionalNumber(
      readDetailsRecord(snapshot.latest_story_asset?.details),
      'word_count',
    )
    if (assetWordCount != null) {
      return assetWordCount
    }

    return displayStoryText != null ? countWords(displayStoryText) : null
  }, [displayStoryText, snapshot.latest_story_asset])
  const storyMeta: string[] = []
  if (storyWordCount != null && storyWordCount > 0) {
    storyMeta.push(`${storyWordCount.toLocaleString()} words`)
  }
  if (storyAssetText != null) {
    const publishedAtLabel = formatTimestamp(
      snapshot.latest_story_asset?.ready_at,
    )
    if (publishedAtLabel != null) {
      storyMeta.push(`Published ${publishedAtLabel}`)
    }
  } else if (usingFallbackStoryText) {
    storyMeta.push('Accepted manuscript snapshot')
  }
  if (finalStoryReady && storyTextState === 'loading') {
    storyMeta.push('Syncing final manuscript')
  }

  const storyStatusLabel = getStoryStatusLabel({
    finalStoryReady,
    storyError: storyTextError,
    storyState: storyTextState,
    usingFallbackStoryText,
    reviewPending: reviewJob != null,
  })
  const storyBadgeTone = getStoryBadgeTone({
    finalStoryReady,
    storyError: storyTextError,
    storyState: storyTextState,
    usingFallbackStoryText,
    reviewPending: reviewJob != null,
  })
  const audioStatusLabel = getAudioStatusLabel(audioRenderState, {
    finalAudioReady,
    showingPreviousMaster,
  })
  const audioStatusCopy = buildAudioStatusCopy({
    audioJob: displayAudioJob,
    finalAudioReady,
    renderState: audioRenderState,
    showingPreviousMaster,
  })
  const audioBadgeTone = getAudioBadgeTone(audioRenderState, {
    showingPreviousMaster,
  })
  const audioProgressPercent =
    displayAudioJob?.progress_percent != null
      ? Math.max(0, Math.min(displayAudioJob.progress_percent, 100))
      : finalAudioReady
        ? 100
        : 0
  const completionSummary =
    snapshot.completed_at != null
      ? `Completed ${formatTimestamp(snapshot.completed_at) ?? 'recently'}`
      : `Updated ${formatTimestamp(snapshot.updated_at) ?? 'recently'}`
  const artifactInventoryItems = useMemo(
    () => artifactInventoryQuery.data?.items ?? [],
    [artifactInventoryQuery.data],
  )
  const artifactInventoryByKey = useMemo(
    () =>
      new Map(
        artifactInventoryItems.map((item) => [item.key, item] as const),
      ),
    [artifactInventoryItems],
  )
  const inventoryRefreshedAt =
    formatTimestamp(artifactInventoryQuery.data?.generated_at) ?? null
  const storyTextInventoryItem =
    artifactInventoryByKey.get('story_text') ?? null
  const storyDocxInventoryItem =
    artifactInventoryByKey.get('story_docx') ?? null
  const finalAudioInventoryItem =
    artifactInventoryByKey.get('final_audio') ?? null
  const artifactPanelItems = [
    storyTextInventoryItem,
    storyDocxInventoryItem,
    finalAudioInventoryItem,
  ].filter(
    (
      item,
    ): item is SessionArtifactInventoryItemView => item != null,
  )

  function buildArtifactMeta(item: SessionArtifactInventoryItemView) {
    const metadata: string[] = []

    const filename = resolveArtifactFilename(item)
    if (filename != null) {
      metadata.push(filename)
    }

    if (item.key === 'story_text' && storyWordCount != null && storyWordCount > 0) {
      metadata.push(`${storyWordCount.toLocaleString()} words`)
    }

    if (item.key === 'final_audio') {
      const runtimeLabel = formatDurationLabel(item.asset?.duration_seconds)
      if (runtimeLabel != null) {
        metadata.push(`Runtime ${runtimeLabel}`)
      }

      if (item.preview_asset_count > 0 && item.status !== 'ready') {
        metadata.push(
          item.preview_asset_count === 1
            ? '1 preview clip ready'
            : `${item.preview_asset_count} preview clips ready`,
        )
      }
    }

    const publishedAtLabel = formatTimestamp(item.asset?.ready_at)
    if (publishedAtLabel != null) {
      metadata.push(`Published ${publishedAtLabel}`)
    }

    return metadata
  }

  function buildArtifactAction(
    item: SessionArtifactInventoryItemView,
  ): {
    label: string
    onClick: () => void
  } | null {
    if (item.key === 'story_text') {
      if (displayStoryText == null) {
        return null
      }

      return {
        label: 'Open reader',
        onClick: () => {
          setActiveTab('read')
        },
      }
    }

    if (item.key === 'story_docx') {
      if (finalStoryReady || item.status === 'ready') {
        return {
          label:
            item.status === 'stale'
              ? 'Refresh Word document'
              : item.status === 'missing'
                ? 'Generate Word document'
                : item.status === 'failed'
                  ? 'Retry Word document'
                  : 'Download Word document',
          onClick: () => {
            onDownloadStoryExport()
          },
        }
      }

      return null
    }

    if (item.status === 'ready' || item.status === 'stale') {
      return {
        label:
          item.status === 'stale'
            ? 'Download previous master'
            : 'Download narration',
        onClick: () => {
          onDownloadAudio()
        },
      }
    }

    if (
      item.status === 'generating' ||
      item.status === 'failed' ||
      item.preview_asset_count > 0
    ) {
      return {
        label: 'Open listener',
        onClick: () => {
          setActiveTab('listen')
        },
      }
    }

    return null
  }

  useEffect(() => {
    let isActive = true

    if (!finalStoryReady) {
      setStoryAssetText(null)
      setStoryTextState('idle')
      setStoryTextError(null)
      return () => {
        isActive = false
      }
    }

    setStoryTextState('loading')
    setStoryTextError(null)

    void fetchSessionAssetText(snapshot.latest_story_asset)
      .then((text) => {
        if (!isActive) {
          return
        }

        setStoryAssetText(text)
        setStoryTextState('ready')
      })
      .catch((error: unknown) => {
        if (!isActive) {
          return
        }

        setStoryAssetText(null)
        setStoryTextState('error')
        setStoryTextError(
          error instanceof Error
            ? error.message
            : 'The final manuscript could not be loaded inline right now.',
        )
      })

    return () => {
      isActive = false
    }
  }, [finalStoryReady, snapshot.latest_story_asset])

  async function runAction(
    nextActionState: Exclude<ActionState, null>,
    operation: () => Promise<unknown>,
  ) {
    setActionState(nextActionState)
    setActionError(null)

    try {
      await operation()
    } catch (error) {
      setActionError(
        error instanceof Error
          ? error.message
          : 'The selected manuscript version could not be updated right now.',
      )
    } finally {
      setActionState(null)
    }
  }

  return (
    <>
      <section className="workspace-stage-panel finalize-stage__hero">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Final review</p>
            <h3>
              {buildFinalizeHeroTitle({
                finalAudioReady,
                finalStoryReady,
                reviewPending: reviewJob != null,
              })}
            </h3>
            <p>
              {buildFinalizeHeroDescription({
                audioStatusCopy,
                finalAudioReady,
                finalStoryReady,
                reviewPending: reviewJob != null,
                storyStatusLabel,
              })}
            </p>
          </div>

          <div className="workspace-stage-detail__badges">
            {reviewJob != null ? (
              <Badge tone="warning">Rewrite pending</Badge>
            ) : null}
            <Badge tone={storyBadgeTone}>{storyStatusLabel}</Badge>
            <Badge tone={audioBadgeTone}>{audioStatusLabel}</Badge>
          </div>
        </div>

        <CardGrid className="workspace-stage-detail__cards" columns={3}>
          <SummaryPanel
            description={
              reviewJob != null
                ? 'A rewrite candidate is still waiting for review before it replaces the accepted manuscript.'
                : displayStoryText != null
                  ? 'The story is readable inside the app now, even if the durable export is still syncing.'
                  : 'The reading surface will unlock as soon as the accepted manuscript is available.'
            }
            label="Manuscript"
            title={storyStatusLabel}
            tone={displayStoryText != null ? 'accent' : 'default'}
          />

          <SummaryPanel
            description={audioStatusCopy}
            label="Narration"
            title={audioStatusLabel}
            tone={finalAudioReady ? 'accent' : 'default'}
          />

          <SummaryPanel
            description={completionSummary}
            label="Finish line"
            title={
              finalStoryReady && finalAudioReady && reviewJob == null
                ? 'Ready to tuck in'
                : reviewJob != null
                  ? 'One last decision remains'
                  : 'Finish line in sight'
            }
            tone={
              finalStoryReady && finalAudioReady && reviewJob == null
                ? 'accent'
                : 'default'
            }
          />
        </CardGrid>

        <div className="cta-row">
          {inventoryRefreshedAt != null ? (
            <p className="finalize-stage__surface-note">
              Artifact inventory refreshed {inventoryRefreshedAt}.
            </p>
          ) : null}
          <Button
            onClick={() => {
              onReturnToComposition()
            }}
            tone="ghost"
          >
            Return to composition
          </Button>
        </div>
      </section>

      <div className="finalize-stage__layout">
        <section className="workspace-stage-panel finalize-stage__experience">
          <div
            aria-label="Finalize review modes"
            className="finalize-stage__tablist"
            role="tablist"
          >
            <button
              aria-controls={`${tabSetId}-read-panel`}
              aria-selected={activeTab === 'read'}
              className="finalize-stage__tab"
              id={`${tabSetId}-read-tab`}
              onClick={() => {
                setActiveTab('read')
              }}
              role="tab"
              type="button"
            >
              Read story
            </button>
            <button
              aria-controls={`${tabSetId}-listen-panel`}
              aria-selected={activeTab === 'listen'}
              className="finalize-stage__tab"
              id={`${tabSetId}-listen-tab`}
              onClick={() => {
                setActiveTab('listen')
              }}
              role="tab"
              type="button"
            >
              Listen back
            </button>
          </div>

          <div
            aria-labelledby={`${tabSetId}-read-tab`}
            className="finalize-stage__surface"
            hidden={activeTab !== 'read'}
            id={`${tabSetId}-read-panel`}
            role="tabpanel"
          >
            <div className="finalize-stage__surface-header">
              <div>
                <p className="eyebrow">Read mode</p>
                <h3>Current manuscript</h3>
                <p>
                  A calm reading surface for the accepted story text, with room
                  for the durable export to catch up in the background.
                </p>
              </div>
              <Badge tone={storyBadgeTone}>{storyStatusLabel}</Badge>
            </div>

            {storyTextError != null && usingFallbackStoryText ? (
              <FeedbackBanner
                description="The durable manuscript could not be loaded inline, so this reader is showing the latest accepted checkpoint instead."
                title="Using the accepted manuscript snapshot"
                tone="warning"
              />
            ) : null}

            {storyTextState === 'loading' && usingFallbackStoryText ? (
              <p className="finalize-stage__surface-note">
                <InlineSpinner label="Loading final manuscript" /> Loading the
                durable manuscript while this accepted checkpoint keeps the
                story readable.
              </p>
            ) : null}

            {displayStoryText != null ? (
              <>
                {storyMeta.length > 0 ? (
                  <div className="finalize-stage__meta">
                    {storyMeta.map((item) => (
                      <span key={item}>{item}</span>
                    ))}
                  </div>
                ) : null}

                <div className="finalize-stage__reader">
                  <div className="finalize-stage__reader-copy">
                    {storyBlocks.map((block, index) =>
                      block.kind === 'heading' ? (
                        <h4 key={`story-block-${index}`}>{block.content}</h4>
                      ) : (
                        <p key={`story-block-${index}`}>{block.content}</p>
                      ),
                    )}
                  </div>
                </div>
              </>
            ) : storyTextState === 'loading' ? (
              <div className="finalize-stage__pending">
                <InlineSpinner label="Loading manuscript" />
                <p>Loading the final manuscript into the reader.</p>
              </div>
            ) : storyTextError != null ? (
              <FeedbackBanner
                description={storyTextError}
                title="The manuscript could not be loaded inline"
                tone="danger"
              />
            ) : (
              <EmptyStateBlock
                description={
                  reviewJob != null
                    ? 'Accept or reject the pending rewrite before the final manuscript settles into place here.'
                    : 'The reading surface will appear after the accepted manuscript is published into durable storage.'
                }
                title="Story text still settling"
              />
            )}
          </div>

          <div
            aria-labelledby={`${tabSetId}-listen-tab`}
            className="finalize-stage__surface"
            hidden={activeTab !== 'listen'}
            id={`${tabSetId}-listen-panel`}
            role="tabpanel"
          >
            <div className="finalize-stage__surface-header">
              <div>
                <p className="eyebrow">Listen mode</p>
                <h3>Compiled narration</h3>
                <p>
                  Listen to the merged narration master when it is ready, or
                  follow the last stretch of audio progress without leaving the
                  finish line.
                </p>
              </div>
              <Badge tone={audioBadgeTone}>{audioStatusLabel}</Badge>
            </div>

            {(displayAudioJob != null || finalAudioReady) && (
              <ProgressBar
                aria-label="Narration review progress"
                className="finalize-stage__progress"
                hint={audioStatusCopy}
                label={displayAudioJob?.current_step ?? 'Narration readiness'}
                tone={finalAudioReady ? 'moss' : 'accent'}
                value={audioProgressPercent}
                valueText={
                  finalAudioReady && displayAudioJob == null
                    ? 'Ready'
                    : `${Math.round(audioProgressPercent)}%`
                }
              />
            )}

            {audioRenderState === 'failed' ? (
              <FeedbackBanner
                description={audioStatusCopy}
                title={
                  finalAudioReady
                    ? 'The latest narration pass stopped, but a previous master is still available'
                    : 'Narration stopped before the final master was published'
                }
                tone={finalAudioReady ? 'warning' : 'danger'}
              />
            ) : null}

            {showingPreviousMaster && audioRenderState !== 'failed' ? (
              <FeedbackBanner
                description="This player is showing the previous published narration master while a replacement pass is still rendering."
                title="Previous master still available"
                tone="warning"
              />
            ) : null}

            {finalAudioReady ? (
              <div className="finalize-stage__listen-card">
                {audioStreamUrl != null ? (
                  <audio
                    aria-label="Final narration preview"
                    className="audio-stage__player"
                    controls
                    preload="none"
                    src={audioStreamUrl}
                  />
                ) : (
                  <p className="finalize-stage__surface-note">
                    The final narration file is ready in durable storage, but
                    inline playback is unavailable in this environment.
                  </p>
                )}

                {compiledAudioMeta.length > 0 ? (
                  <div className="finalize-stage__meta">
                    {compiledAudioMeta.map((item) => (
                      <span key={item}>{item}</span>
                    ))}
                  </div>
                ) : null}
              </div>
            ) : audioRenderState === 'planned' ? (
              <EmptyStateBlock
                description="Narration has not started yet. Once the audio stage publishes a master, this panel will switch from status tracking to inline listening."
                title="Narration not published yet"
              />
            ) : audioRenderState === 'paused' ? (
              <EmptyStateBlock
                description="The latest narration pass is paused. Its checkpoints are preserved until the worker resumes."
                title="Narration paused"
              />
            ) : (
              <EmptyStateBlock
                description={audioStatusCopy}
                title={
                  audioRenderState === 'mixing'
                    ? 'Narration assembly underway'
                    : audioRenderState === 'queued'
                      ? 'Narration queued'
                      : 'Narration still rendering'
                }
              />
            )}
          </div>
        </section>

        <aside className="workspace-stage-panel finalize-stage__review-panel">
          <SummaryPanel
            label="Session completion summary"
            sticky
            title="Review panel"
            tone="accent"
          >
            <dl className="finalize-stage__review-list">
              <div className="finalize-stage__review-item">
                <dt>Genre</dt>
                <dd>{snapshot.selected_genre?.label ?? 'Not chosen yet'}</dd>
              </div>
              <div className="finalize-stage__review-item">
                <dt>Tone</dt>
                <dd>
                  {snapshot.selected_tone_profile?.label ?? 'Not chosen yet'}
                </dd>
              </div>
              <div className="finalize-stage__review-item">
                <dt>Length targets</dt>
                <dd>{buildLengthTargetsCopy(snapshot)}</dd>
              </div>
              <div className="finalize-stage__review-item">
                <dt>Story status</dt>
                <dd>{storyStatusLabel}</dd>
              </div>
              <div className="finalize-stage__review-item">
                <dt>Narration status</dt>
                <dd>{audioStatusLabel}</dd>
              </div>
              <div className="finalize-stage__review-item">
                <dt>Session</dt>
                <dd>{completionSummary}</dd>
              </div>
            </dl>
          </SummaryPanel>

          <SummaryPanel
            description="One panel keeps the manuscript, packaged export, and narration master in sync, including stale or missing handoff states."
            label="Downloads and handoff"
            title="Artifact inventory"
          >
            {artifactInventoryQuery.isLoading && artifactInventoryItems.length === 0 ? (
              <p className="finalize-stage__surface-note">
                <InlineSpinner label="Loading artifact inventory" /> Loading
                the current artifact statuses.
              </p>
            ) : null}

            {artifactInventoryQuery.isError ? (
              <FeedbackBanner
                description="The finalize review surfaces are still available, but the packaged artifact inventory could not be refreshed right now."
                title="Artifact inventory unavailable"
                tone="warning"
              />
            ) : null}

            {artifactPanelItems.length > 0 ? (
              <div className="finalize-stage__artifact-list">
                {artifactPanelItems.map((item) => {
                  const metadata = buildArtifactMeta(item)
                  const action = buildArtifactAction(item)

                  return (
                    <section
                      className="finalize-stage__artifact"
                      data-status={item.status}
                      key={item.key}
                    >
                      <div className="finalize-stage__artifact-header">
                        <div className="finalize-stage__artifact-copy">
                          <h4>{item.label}</h4>
                          <p>{item.status_detail}</p>
                        </div>
                        <Badge tone={getArtifactBadgeTone(item.status)}>
                          {formatArtifactStatusLabel(item.status)}
                        </Badge>
                      </div>

                      {metadata.length > 0 ? (
                        <div className="finalize-stage__artifact-meta">
                          {metadata.map((value) => (
                            <span key={value}>{value}</span>
                          ))}
                        </div>
                      ) : null}

                      {action != null ? (
                        <div className="finalize-stage__artifact-actions">
                          <Button
                            onClick={action.onClick}
                            size="compact"
                            tone={
                              item.key === 'story_text'
                                ? 'ghost'
                                : 'secondary'
                            }
                          >
                            {action.label}
                          </Button>
                        </div>
                      ) : null}
                    </section>
                  )
                })}
              </div>
            ) : null}
          </SummaryPanel>

          {reviewJob != null ? (
            <FeedbackBanner
              description="A rewrite is still waiting for review, so the manuscript and exports should still be treated as provisional."
              title="Revision decision still pending"
              tone="warning"
            />
          ) : (
            <SummaryPanel
              description="Use this summary to confirm that the chosen story lane, target length, manuscript status, and narration status all feel ready to leave the workshop."
              label="Why this stage exists"
              title="A true finish line"
            />
          )}
        </aside>
      </div>

      {compositionSegments.length > 0 ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Revision compare</h3>
              <p>
                Compare any saved segment revision against the live manuscript,
                then restore an older revision or resolve pending rewrite review
                from here.
              </p>
            </div>
          </div>

          <SegmentVersionComparePanel
            actionError={actionError}
            actionState={actionState}
            compareContext="finalize"
            disabled={actionState != null}
            onAcceptRewrite={(jobId) => {
              void runAction('acceptRewrite', () => onAcceptRewrite(jobId))
            }}
            onKeepExploring={(segmentIndex) => {
              onKeepExploringRewrite(segmentIndex)
            }}
            onRejectRewrite={(jobId) => {
              void runAction('rejectRewrite', () => onRejectRewrite(jobId))
            }}
            onRestoreVersion={(segmentIndex, versionId) => {
              void runAction('restoreVersion', () =>
                onRestoreSegmentVersion(segmentIndex, versionId),
              )
            }}
            reviewJob={reviewJob}
            segments={compositionSegments}
          />
        </section>
      ) : null}
    </>
  )
}
