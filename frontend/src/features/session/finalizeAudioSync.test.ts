import { describe, expect, it } from 'vitest'
import type { AudioSegmentView, SessionAssetView } from '../../api/sessions.ts'
import {
  buildAudioPlaybackMarkers,
  buildNarrationTimeline,
  resolveActiveAudioPlaybackMarker,
  resolveActiveNarrationTimelineSegment,
} from './finalizeAudioSync.ts'

describe('finalizeAudioSync', () => {
  it('prefers exact segment timelines embedded in the final audio asset', () => {
    const asset: SessionAssetView = {
      id: 'final-audio-1',
      asset_kind: 'final_audio',
      status: 'ready',
      details: {
        segment_timeline: [
          {
            segment_id: 'segment-1',
            segment_index: 1,
            start_seconds: 0,
            end_seconds: 12.4,
            timeline_end_seconds: 15.4,
            duration_seconds: 12.4,
            pause_after_seconds: 3,
            pause_hint: 'chapter_break',
            source_boundary_kind: 'chapter',
            source_outline_card_key: 'chapter-1',
            source_outline_card_title: 'Lantern Wake',
            text_start_offset: 0,
            text_end_offset: 420,
            word_count: 91,
            split_reason: 'paragraph_boundary',
          },
          {
            segment_id: 'segment-2',
            segment_index: 2,
            start_seconds: 15.4,
            end_seconds: 28.1,
            timeline_end_seconds: 28.1,
            duration_seconds: 12.7,
            pause_after_seconds: 0,
            pause_hint: 'none',
            source_boundary_kind: 'chapter',
            source_outline_card_key: 'chapter-2',
            source_outline_card_title: 'Moonlit Crossing',
            text_start_offset: 421,
            text_end_offset: 860,
            word_count: 96,
            split_reason: 'sentence_boundary',
          },
        ],
      },
    }

    const result = buildNarrationTimeline(asset, [])
    const markers = buildAudioPlaybackMarkers(result.timeline)

    expect(result.syncSource).toBe('asset_timeline')
    expect(result.timeline).toHaveLength(2)
    expect(result.timeline[0].timelineEndSeconds).toBe(15.4)
    expect(markers).toEqual([
      expect.objectContaining({
        id: 'outline:chapter-1',
        kind: 'chapter',
        label: 'Lantern Wake',
        startSeconds: 0,
        endSeconds: 15.4,
      }),
      expect.objectContaining({
        id: 'outline:chapter-2',
        kind: 'chapter',
        label: 'Moonlit Crossing',
        startSeconds: 15.4,
        endSeconds: 28.1,
      }),
    ])
    expect(
      resolveActiveNarrationTimelineSegment(result.timeline, 14.9)
        ?.segmentIndex,
    ).toBe(1)
    expect(resolveActiveAudioPlaybackMarker(markers, 16)?.label).toBe(
      'Moonlit Crossing',
    )
  })

  it('falls back to preview-segment durations when older masters lack embedded timing', () => {
    const audioSegments: AudioSegmentView[] = [
      {
        id: 'segment-1',
        audio_job_id: 'audio-job-1',
        segment_index: 1,
        status: 'completed',
        source_boundary_kind: 'chapter',
        source_outline_card_title: 'Lantern Wake',
        word_count: 91,
        pause_after_seconds: 3,
        pause_hint: 'chapter_break',
        preview_asset: {
          id: 'audio-preview-1',
          asset_kind: 'audio_segment',
          status: 'ready',
          duration_seconds: 12.4,
        },
      },
      {
        id: 'segment-2',
        audio_job_id: 'audio-job-1',
        segment_index: 2,
        status: 'completed',
        source_boundary_kind: 'chapter',
        source_outline_card_title: 'Moonlit Crossing',
        word_count: 96,
        pause_after_seconds: 0,
        pause_hint: 'none',
        preview_asset: {
          id: 'audio-preview-2',
          asset_kind: 'audio_segment',
          status: 'ready',
          duration_seconds: 12.7,
        },
      },
    ]

    const result = buildNarrationTimeline(null, audioSegments)

    expect(result.syncSource).toBe('preview_segments')
    expect(result.timeline).toEqual([
      expect.objectContaining({
        segmentIndex: 1,
        startSeconds: 0,
        endSeconds: 12.4,
        timelineEndSeconds: 15.4,
      }),
      expect.objectContaining({
        segmentIndex: 2,
        startSeconds: 15.4,
        endSeconds: 28.1,
        timelineEndSeconds: 28.1,
      }),
    ])
  })

  it('reports sync as unavailable when no timing data exists', () => {
    const result = buildNarrationTimeline(null, [
      {
        id: 'segment-1',
        audio_job_id: 'audio-job-1',
        segment_index: 1,
        status: 'completed',
        source_boundary_kind: 'chapter',
        source_outline_card_title: 'Lantern Wake',
        word_count: 91,
        pause_after_seconds: 3,
        pause_hint: 'chapter_break',
      },
    ])

    expect(result.syncSource).toBe('unavailable')
    expect(result.timeline).toEqual([])
  })

  it('merges consecutive split segments into one chapter marker', () => {
    const result = buildNarrationTimeline(
      {
        id: 'final-audio-2',
        asset_kind: 'final_audio',
        status: 'ready',
        details: {
          segment_timeline: [
            {
              segment_id: 'segment-1a',
              segment_index: 1,
              start_seconds: 0,
              end_seconds: 10,
              timeline_end_seconds: 10,
              duration_seconds: 10,
              pause_after_seconds: 0,
              source_boundary_kind: 'chapter',
              source_outline_card_key: 'chapter-1',
              source_outline_card_title: 'Lantern Wake',
            },
            {
              segment_id: 'segment-1b',
              segment_index: 2,
              start_seconds: 10,
              end_seconds: 18,
              timeline_end_seconds: 21,
              duration_seconds: 8,
              pause_after_seconds: 3,
              source_boundary_kind: 'chapter',
              source_outline_card_key: 'chapter-1',
              source_outline_card_title: 'Lantern Wake',
            },
            {
              segment_id: 'segment-2',
              segment_index: 3,
              start_seconds: 21,
              end_seconds: 32,
              timeline_end_seconds: 32,
              duration_seconds: 11,
              pause_after_seconds: 0,
              source_boundary_kind: 'chapter',
              source_outline_card_key: 'chapter-2',
              source_outline_card_title: 'Moonlit Crossing',
            },
          ],
        },
      },
      [],
    )

    const markers = buildAudioPlaybackMarkers(result.timeline)

    expect(markers).toHaveLength(2)
    expect(markers[0]).toEqual(
      expect.objectContaining({
        id: 'outline:chapter-1',
        segmentIndexes: [1, 2],
        endSeconds: 21,
      }),
    )
  })
})
