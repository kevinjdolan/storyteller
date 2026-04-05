import { useMemo } from 'react'
import type { AudioSegmentView, SessionAssetView } from '../../api/sessions.ts'

export type NarrationTimelineSegment = {
  durationSeconds: number
  endSeconds: number
  pauseAfterSeconds: number
  pauseHint: string | null
  segmentId: string | null
  segmentIndex: number
  sourceBoundaryKind: string | null
  sourceOutlineCardKey: string | null
  sourceOutlineCardTitle: string | null
  splitReason: string | null
  startSeconds: number
  textEndOffset: number | null
  textStartOffset: number | null
  timelineEndSeconds: number
  wordCount: number | null
}

export type AudioPlaybackMarker = {
  endSeconds: number
  id: string
  kind: 'chapter' | 'segment'
  label: string
  order: number
  segmentIndexes: number[]
  sourceOutlineCardKey: string | null
  sourceOutlineCardTitle: string | null
  startSeconds: number
}

export type AudioPlaybackSyncSource =
  | 'asset_timeline'
  | 'preview_segments'
  | 'unavailable'

type UseNarrationPlaybackSyncOptions = {
  asset: SessionAssetView | null | undefined
  audioSegments: AudioSegmentView[]
  currentTime: number
}

type NarrationPlaybackSyncState = {
  activeMarker: AudioPlaybackMarker | null
  activeSegment: NarrationTimelineSegment | null
  markers: AudioPlaybackMarker[]
  syncSource: AudioPlaybackSyncSource
  timeline: NarrationTimelineSegment[]
}

export function useNarrationPlaybackSync(
  options: UseNarrationPlaybackSyncOptions,
): NarrationPlaybackSyncState {
  const timelineResult = useMemo(
    () => buildNarrationTimeline(options.asset, options.audioSegments),
    [options.asset, options.audioSegments],
  )

  const markers = useMemo(
    () => buildAudioPlaybackMarkers(timelineResult.timeline),
    [timelineResult.timeline],
  )

  return useMemo(
    () => ({
      timeline: timelineResult.timeline,
      markers,
      syncSource: timelineResult.syncSource,
      activeSegment: resolveActiveNarrationTimelineSegment(
        timelineResult.timeline,
        options.currentTime,
      ),
      activeMarker: resolveActiveAudioPlaybackMarker(
        markers,
        options.currentTime,
      ),
    }),
    [
      markers,
      options.currentTime,
      timelineResult.syncSource,
      timelineResult.timeline,
    ],
  )
}

export function buildNarrationTimeline(
  asset: SessionAssetView | null | undefined,
  audioSegments: AudioSegmentView[],
): {
  syncSource: AudioPlaybackSyncSource
  timeline: NarrationTimelineSegment[]
} {
  const assetTimeline = buildNarrationTimelineFromAsset(asset)
  if (assetTimeline.length > 0) {
    return {
      syncSource: 'asset_timeline',
      timeline: assetTimeline,
    }
  }

  const previewTimeline =
    buildNarrationTimelineFromPreviewSegments(audioSegments)
  if (previewTimeline.length > 0) {
    return {
      syncSource: 'preview_segments',
      timeline: previewTimeline,
    }
  }

  return {
    syncSource: 'unavailable',
    timeline: [],
  }
}

export function buildAudioPlaybackMarkers(
  timeline: NarrationTimelineSegment[],
): AudioPlaybackMarker[] {
  const markers: AudioPlaybackMarker[] = []

  for (const segment of timeline) {
    const nextMarkerId = buildPlaybackMarkerId(segment)
    const markerKind = resolvePlaybackMarkerKind(segment)
    const markerLabel =
      segment.sourceOutlineCardTitle?.trim() ||
      (markerKind === 'chapter'
        ? `Chapter ${markers.length + 1}`
        : `Segment ${segment.segmentIndex}`)
    const previousMarker = markers.at(-1)

    if (previousMarker != null && previousMarker.id === nextMarkerId) {
      previousMarker.endSeconds = segment.timelineEndSeconds
      previousMarker.segmentIndexes.push(segment.segmentIndex)
      continue
    }

    markers.push({
      id: nextMarkerId,
      order: markers.length + 1,
      kind: markerKind,
      label: markerLabel,
      startSeconds: segment.startSeconds,
      endSeconds: segment.timelineEndSeconds,
      segmentIndexes: [segment.segmentIndex],
      sourceOutlineCardKey: segment.sourceOutlineCardKey,
      sourceOutlineCardTitle: segment.sourceOutlineCardTitle,
    })
  }

  return markers
}

export function resolveActiveNarrationTimelineSegment(
  timeline: NarrationTimelineSegment[],
  currentTime: number,
) {
  return resolveActiveEntry(
    timeline,
    currentTime,
    (segment) => segment.timelineEndSeconds,
  )
}

export function resolveActiveAudioPlaybackMarker(
  markers: AudioPlaybackMarker[],
  currentTime: number,
) {
  return resolveActiveEntry(markers, currentTime, (marker) => marker.endSeconds)
}

function buildNarrationTimelineFromAsset(
  asset: SessionAssetView | null | undefined,
) {
  const details = readRecord(asset?.details)
  const rawTimeline = details?.segment_timeline
  if (!Array.isArray(rawTimeline)) {
    return [] as NarrationTimelineSegment[]
  }

  return rawTimeline
    .map((entry) => buildTimelineSegmentFromRecord(readRecord(entry)))
    .filter((segment): segment is NarrationTimelineSegment => segment != null)
    .sort((left, right) => left.segmentIndex - right.segmentIndex)
}

function buildNarrationTimelineFromPreviewSegments(
  audioSegments: AudioSegmentView[],
) {
  const sortedSegments = [...audioSegments].sort(
    (left, right) => left.segment_index - right.segment_index,
  )
  if (sortedSegments.length === 0) {
    return [] as NarrationTimelineSegment[]
  }

  let cursorSeconds = 0
  const timeline: NarrationTimelineSegment[] = []

  for (const segment of sortedSegments) {
    const durationSeconds = segment.preview_asset?.duration_seconds ?? null
    if (
      durationSeconds == null ||
      !Number.isFinite(durationSeconds) ||
      durationSeconds <= 0
    ) {
      return [] as NarrationTimelineSegment[]
    }

    const startSeconds = cursorSeconds
    const endSeconds = startSeconds + durationSeconds
    const pauseAfterSeconds = Math.max(segment.pause_after_seconds ?? 0, 0)
    const timelineEndSeconds = endSeconds + pauseAfterSeconds

    timeline.push({
      durationSeconds: roundSeconds(durationSeconds),
      endSeconds: roundSeconds(endSeconds),
      pauseAfterSeconds,
      pauseHint: normalizeText(segment.pause_hint),
      segmentId: normalizeText(segment.id),
      segmentIndex: segment.segment_index,
      sourceBoundaryKind: normalizeText(segment.source_boundary_kind),
      sourceOutlineCardKey: null,
      sourceOutlineCardTitle: normalizeText(segment.source_outline_card_title),
      splitReason: normalizeText(segment.split_reason),
      startSeconds: roundSeconds(startSeconds),
      textEndOffset: null,
      textStartOffset: null,
      timelineEndSeconds: roundSeconds(timelineEndSeconds),
      wordCount: segment.word_count ?? null,
    })
    cursorSeconds = timelineEndSeconds
  }

  return timeline
}

function buildTimelineSegmentFromRecord(
  value: Record<string, unknown> | null,
): NarrationTimelineSegment | null {
  if (value == null) {
    return null
  }

  const segmentIndex = readOptionalNumber(value, 'segment_index')
  const startSeconds = readOptionalNumber(value, 'start_seconds')
  const endSeconds = readOptionalNumber(value, 'end_seconds')
  const durationSeconds = readOptionalNumber(value, 'duration_seconds')

  if (
    segmentIndex == null ||
    startSeconds == null ||
    endSeconds == null ||
    durationSeconds == null
  ) {
    return null
  }

  const pauseAfterSeconds =
    readOptionalNumber(value, 'pause_after_seconds') ?? 0
  const timelineEndSeconds =
    readOptionalNumber(value, 'timeline_end_seconds') ??
    roundSeconds(endSeconds + pauseAfterSeconds)

  return {
    durationSeconds: roundSeconds(durationSeconds),
    endSeconds: roundSeconds(endSeconds),
    pauseAfterSeconds: Math.max(pauseAfterSeconds, 0),
    pauseHint: readOptionalString(value, 'pause_hint'),
    segmentId: readOptionalString(value, 'segment_id'),
    segmentIndex,
    sourceBoundaryKind: readOptionalString(value, 'source_boundary_kind'),
    sourceOutlineCardKey: readOptionalString(value, 'source_outline_card_key'),
    sourceOutlineCardTitle: readOptionalString(
      value,
      'source_outline_card_title',
    ),
    splitReason: readOptionalString(value, 'split_reason'),
    startSeconds: roundSeconds(startSeconds),
    textEndOffset: readOptionalNumber(value, 'text_end_offset'),
    textStartOffset: readOptionalNumber(value, 'text_start_offset'),
    timelineEndSeconds: roundSeconds(timelineEndSeconds),
    wordCount: readOptionalNumber(value, 'word_count'),
  }
}

function buildPlaybackMarkerId(segment: NarrationTimelineSegment) {
  const outlineCardKey = segment.sourceOutlineCardKey?.trim()
  if (outlineCardKey != null && outlineCardKey.length > 0) {
    return `outline:${outlineCardKey}`
  }

  const outlineTitle = normalizeKey(segment.sourceOutlineCardTitle)
  if (
    segment.sourceBoundaryKind === 'chapter' &&
    outlineTitle != null &&
    outlineTitle.length > 0
  ) {
    return `chapter:${outlineTitle}`
  }

  return `segment:${segment.segmentIndex}`
}

function resolvePlaybackMarkerKind(segment: NarrationTimelineSegment) {
  return segment.sourceBoundaryKind === 'chapter' ? 'chapter' : 'segment'
}

function resolveActiveEntry<TEntry>(
  entries: TEntry[],
  currentTime: number,
  resolveEndSeconds: (entry: TEntry) => number,
) {
  if (entries.length === 0) {
    return null
  }

  const clampedTime =
    Number.isFinite(currentTime) && currentTime > 0 ? currentTime : 0

  for (const entry of entries) {
    if (clampedTime < resolveEndSeconds(entry)) {
      return entry
    }
  }

  return entries.at(-1) ?? null
}

function readRecord(value: unknown): Record<string, unknown> | null {
  return value != null && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null
}

function readOptionalNumber(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  const candidate = value?.[key]
  return typeof candidate === 'number' && Number.isFinite(candidate)
    ? candidate
    : null
}

function readOptionalString(
  value: Record<string, unknown> | null | undefined,
  key: string,
) {
  return normalizeText(value?.[key])
}

function normalizeKey(value: string | null | undefined) {
  const normalizedValue = value?.trim().toLowerCase()
  if (normalizedValue == null || normalizedValue.length === 0) {
    return null
  }

  return normalizedValue.replace(/[^a-z0-9]+/gu, '-').replace(/^-+|-+$/gu, '')
}

function normalizeText(value: unknown) {
  return typeof value === 'string' && value.trim().length > 0
    ? value.trim()
    : null
}

function roundSeconds(value: number) {
  return Math.round(value * 1000) / 1000
}
