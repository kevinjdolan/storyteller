import { fireEvent, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import { FinalizeStage } from './FinalizeStage.tsx'

const snapshot = {
  latest_composition_job: {
    id: 'rewrite-job-4',
    job_kind: 'rewrite',
    status: 'completed',
    progress_percent: 100,
    current_segment_index: 2,
    rewrite_to_segment_index: 2,
    pending_review: true,
    rewrite_candidate_segment_indexes: [2],
    updated_at: '2026-04-02T05:30:00Z',
  },
  latest_story_asset: null,
  latest_audio_asset: null,
  composition_segments: [
    {
      segment_index: 2,
      outline_card_title: 'Lantern cove',
      outline_card_summary: 'Mira follows the bell into the cove.',
      current_version_id: 'segment-2-rev-1',
      current_revision_number: 1,
      pending_version_id: 'segment-2-rev-2',
      pending_revision_number: 2,
      is_stale: false,
      versions: [
        {
          id: 'segment-2-rev-2',
          composition_job_id: 'rewrite-job-4',
          job_kind: 'rewrite',
          segment_index: 2,
          revision_number: 2,
          status: 'completed',
          acceptance_state: 'pending',
          is_current: false,
          is_stale: false,
          accepted_summary: 'The rewrite softens the cove entrance.',
          text_content: 'Rewrite segment 2 opens the cove more gently.',
          word_count: 8,
          created_at: '2026-04-02T05:25:00Z',
          updated_at: '2026-04-02T05:30:00Z',
          completed_at: '2026-04-02T05:30:00Z',
        },
        {
          id: 'segment-2-rev-1',
          composition_job_id: 'draft-job-1',
          job_kind: 'draft',
          segment_index: 2,
          revision_number: 1,
          status: 'completed',
          acceptance_state: 'accepted',
          is_current: true,
          is_stale: false,
          accepted_summary: 'The current draft keeps the bell close.',
          text_content: 'Draft segment 2 keeps the bell close.',
          word_count: 7,
          created_at: '2026-04-02T05:20:00Z',
          updated_at: '2026-04-02T05:22:00Z',
          completed_at: '2026-04-02T05:22:00Z',
        },
      ],
    },
  ],
} as SessionSnapshot

describe('FinalizeStage', () => {
  it('keeps rewrite compare controls available from final review', async () => {
    const onAcceptRewrite = vi.fn().mockResolvedValue(undefined)
    const onRejectRewrite = vi.fn().mockResolvedValue(undefined)
    const onRestoreSegmentVersion = vi.fn().mockResolvedValue(undefined)
    const onReturnToComposition = vi.fn()

    renderWithAppProviders(
      <FinalizeStage
        onAcceptRewrite={onAcceptRewrite}
        onKeepExploringRewrite={vi.fn()}
        onRejectRewrite={onRejectRewrite}
        onRestoreSegmentVersion={onRestoreSegmentVersion}
        onReturnToComposition={onReturnToComposition}
        snapshot={snapshot}
      />,
    )

    expect(screen.getByText('Revision compare')).toBeInTheDocument()
    expect(screen.getAllByText('Changed').length).toBeGreaterThan(0)

    fireEvent.click(screen.getByRole('button', { name: 'Accept rewrite' }))
    await waitFor(() => {
      expect(onAcceptRewrite).toHaveBeenCalledWith('rewrite-job-4')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Keep current draft' }))
    await waitFor(() => {
      expect(onRejectRewrite).toHaveBeenCalledWith('rewrite-job-4')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Return to composition' }))
    expect(onReturnToComposition).toHaveBeenCalledTimes(1)
    expect(onRestoreSegmentVersion).not.toHaveBeenCalled()
  })
})
