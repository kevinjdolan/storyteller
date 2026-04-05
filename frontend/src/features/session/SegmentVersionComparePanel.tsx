import { useMemo, useState } from 'react'
import type {
  CompositionJobView,
  CompositionSegmentVersionView,
  CompositionSegmentView,
} from '../../api/sessions.ts'
import { Badge, Button } from '../../shared/ui/primitives.tsx'
import { buildSegmentDiffSummary } from './segmentVersionDiff.ts'

type SegmentVersionComparePanelProps = {
  actionError?: string | null
  actionState?: 'acceptRewrite' | 'rejectRewrite' | 'restoreVersion' | null
  compareContext: 'composition' | 'finalize'
  disabled?: boolean
  onAcceptRewrite?: (jobId: string) => void
  onKeepExploring?: (segmentIndex: number) => void
  onRejectRewrite?: (jobId: string) => void
  onRestoreVersion?: (segmentIndex: number, versionId: string) => void
  reviewJob?: CompositionJobView | null
  segments: CompositionSegmentView[]
}

function buildSegmentStatusLabel(segment: CompositionSegmentView) {
  if (segment.pending_version_id != null) {
    return 'Pending rewrite'
  }

  if (segment.is_stale) {
    return 'Stale downstream'
  }

  return 'Current manuscript'
}

function buildVersionLabel(version: CompositionSegmentVersionView) {
  const parts = [`Rev ${String(version.revision_number).padStart(2, '0')}`]

  if (version.acceptance_state === 'pending') {
    parts.push('Pending')
  } else if (version.is_current) {
    parts.push('Current')
  } else if (version.acceptance_state === 'rejected') {
    parts.push('Dismissed')
  } else {
    parts.push('Archived')
  }

  return parts.join(' · ')
}

function getSelectedSegmentVersion(
  segment: CompositionSegmentView | null,
  versionId: string | null,
) {
  if (segment == null || versionId == null) {
    return null
  }

  return segment.versions.find((version) => version.id === versionId) ?? null
}

function findCurrentVersion(segment: CompositionSegmentView | null) {
  if (segment == null) {
    return null
  }

  return (
    segment.versions.find((version) => version.is_current) ??
    segment.versions.find((version) => version.acceptance_state === 'accepted') ??
    null
  )
}

function findDefaultInspectedVersion(segment: CompositionSegmentView | null) {
  if (segment == null) {
    return null
  }

  return (
    getSelectedSegmentVersion(segment, segment.pending_version_id ?? null) ??
    segment.versions.find(
      (version) =>
        version.acceptance_state === 'accepted' && version.is_current === false,
    ) ??
    findCurrentVersion(segment) ??
    segment.versions[0] ??
    null
  )
}

function renderHighlightedText(
  parts: ReturnType<typeof buildSegmentDiffSummary>['parts'],
  mode: 'before' | 'after',
) {
  return parts.map((part, index) => {
    if (mode === 'before' && part.kind === 'added') {
      return null
    }

    if (mode === 'after' && part.kind === 'removed') {
      return null
    }

    return (
      <span
        className="segment-compare__token"
        data-kind={part.kind}
        key={`${part.kind}-${index}-${part.value.length}`}
      >
        {part.value}
      </span>
    )
  })
}

function buildReviewActionSummary(
  compareContext: SegmentVersionComparePanelProps['compareContext'],
) {
  if (compareContext === 'finalize') {
    return 'You can approve the rewrite here or return to composition to request another pass.'
  }

  return 'Approve the rewrite once the highlighted changes feel right, or keep the current draft and ask for another pass.'
}

export function SegmentVersionComparePanel({
  actionError,
  actionState = null,
  compareContext,
  disabled = false,
  onAcceptRewrite,
  onKeepExploring,
  onRejectRewrite,
  onRestoreVersion,
  reviewJob = null,
  segments,
}: SegmentVersionComparePanelProps) {
  const [selectedSegmentIndex, setSelectedSegmentIndex] = useState<number | null>(
    null,
  )
  const [inspectedVersionId, setInspectedVersionId] = useState<string | null>(null)

  const defaultSegmentIndex = useMemo(
    () =>
      segments.find((segment) => segment.pending_version_id != null)?.segment_index ??
      segments.find((segment) => segment.is_stale)?.segment_index ??
      segments[0]?.segment_index ??
      null,
    [segments],
  )
  const resolvedSelectedSegmentIndex =
    selectedSegmentIndex != null &&
    segments.some((segment) => segment.segment_index === selectedSegmentIndex)
      ? selectedSegmentIndex
      : defaultSegmentIndex
  const selectedSegment =
    segments.find((segment) => segment.segment_index === resolvedSelectedSegmentIndex) ??
    null
  const defaultInspectedVersion = findDefaultInspectedVersion(selectedSegment)
  const resolvedInspectedVersionId =
    inspectedVersionId != null &&
    selectedSegment?.versions.some((version) => version.id === inspectedVersionId)
      ? inspectedVersionId
      : defaultInspectedVersion?.id ?? null
  const inspectedVersion =
    getSelectedSegmentVersion(selectedSegment, resolvedInspectedVersionId) ??
    defaultInspectedVersion
  const currentVersion = findCurrentVersion(selectedSegment)
  const compareAgainstCurrent =
    currentVersion != null &&
    inspectedVersion != null &&
    currentVersion.id !== inspectedVersion.id

  const diffSummary = useMemo(() => {
    if (!compareAgainstCurrent) {
      return null
    }

    return buildSegmentDiffSummary(
      currentVersion?.text_content ?? '',
      inspectedVersion?.text_content ?? '',
    )
  }, [compareAgainstCurrent, currentVersion, inspectedVersion])

  const showPendingRewriteActions =
    inspectedVersion?.acceptance_state === 'pending' && reviewJob != null
  const showRestoreAction =
    inspectedVersion?.acceptance_state === 'accepted' &&
    inspectedVersion.is_current === false

  return (
    <section className="segment-compare">
      <div className="segment-compare__grid">
        <aside className="segment-compare__segment-list">
          {segments.map((segment) => {
            const isSelected = selectedSegment?.segment_index === segment.segment_index

            return (
              <button
                className="segment-compare__segment-entry"
                data-selected={isSelected || undefined}
                key={segment.segment_index}
                onClick={() => {
                  setSelectedSegmentIndex(segment.segment_index)
                }}
                type="button"
              >
                <div>
                  <strong>
                    {segment.outline_card_title ?? `Segment ${segment.segment_index}`}
                  </strong>
                  <span>{buildSegmentStatusLabel(segment)}</span>
                </div>

                <div className="segment-compare__segment-entry-badges">
                  {segment.pending_version_id != null ? (
                    <Badge tone="accent">Pending</Badge>
                  ) : null}
                  {segment.is_stale ? <Badge tone="warning">Stale</Badge> : null}
                  {segment.current_revision_number != null ? (
                    <Badge tone="neutral">
                      Rev {segment.current_revision_number}
                    </Badge>
                  ) : null}
                </div>
              </button>
            )
          })}
        </aside>

        <section className="segment-compare__review">
          {selectedSegment != null && inspectedVersion != null ? (
            <>
              <div className="segment-compare__header">
                <div>
                  <p className="eyebrow">Segment {selectedSegment.segment_index}</p>
                  <h4>
                    {selectedSegment.outline_card_title ??
                      `Segment ${selectedSegment.segment_index}`}
                  </h4>
                  <p>
                    {inspectedVersion.accepted_summary ??
                      inspectedVersion.planned_summary ??
                      selectedSegment.stale_reason ??
                      selectedSegment.outline_card_summary ??
                      'No saved revision summary is available yet.'}
                  </p>
                  {(selectedSegment.hidden_version_count ?? 0) > 0 ? (
                    <p className="body-copy">
                      Showing{' '}
                      {selectedSegment.included_version_count ??
                        selectedSegment.versions.length}{' '}
                      of {selectedSegment.version_count ?? selectedSegment.versions.length}{' '}
                      saved revisions in the workspace window.
                    </p>
                  ) : null}
                </div>

                <div className="workspace-stage-detail__badges">
                  <Badge
                    tone={
                      inspectedVersion.acceptance_state === 'pending'
                        ? 'accent'
                        : inspectedVersion.is_current
                          ? 'success'
                          : inspectedVersion.acceptance_state === 'rejected'
                            ? 'warning'
                            : 'neutral'
                    }
                  >
                    {buildVersionLabel(inspectedVersion)}
                  </Badge>
                  {selectedSegment.is_stale ? (
                    <Badge tone="warning">Needs downstream refresh</Badge>
                  ) : null}
                </div>
              </div>

              {compareAgainstCurrent && diffSummary != null ? (
                <>
                  <div className="segment-compare__summary">
                    <Badge tone="brand">
                      {diffSummary.changedRegionCount} change
                      {diffSummary.changedRegionCount === 1 ? '' : 's'}
                    </Badge>
                    <Badge tone="success">
                      +{diffSummary.addedWords} words
                    </Badge>
                    <Badge tone="warning">
                      -{diffSummary.removedWords} words
                    </Badge>
                  </div>

                  {diffSummary.regions.length > 0 ? (
                    <div className="segment-compare__change-list">
                      {diffSummary.regions.map((region, index) => (
                        <article
                          className="segment-compare__change-card"
                          key={`${region.kind}-${index}`}
                        >
                          <strong>
                            {region.kind === 'replacement'
                              ? 'Changed'
                              : region.kind === 'addition'
                                ? 'Added'
                                : 'Removed'}
                          </strong>
                          <div className="segment-compare__change-copy">
                            {region.beforeText.length > 0 ? (
                              <p>
                                <span>Before</span>
                                {region.beforeText}
                              </p>
                            ) : null}
                            {region.afterText.length > 0 ? (
                              <p>
                                <span>After</span>
                                {region.afterText}
                              </p>
                            ) : null}
                          </div>
                        </article>
                      ))}
                    </div>
                  ) : null}
                </>
              ) : (
                <p className="segment-compare__empty-note">
                  This segment only has one durable text version so far.
                </p>
              )}

              <div className="segment-compare__columns">
                <article className="segment-compare__compare-card">
                  <div className="segment-compare__compare-card-header">
                    <span>Current manuscript</span>
                    {currentVersion != null ? (
                      <Badge tone="neutral">{buildVersionLabel(currentVersion)}</Badge>
                    ) : null}
                  </div>
                  <div className="segment-compare__text">
                    {compareAgainstCurrent && diffSummary != null
                      ? renderHighlightedText(diffSummary.parts, 'before')
                      : currentVersion?.text_content ??
                        'No current manuscript text exists for this segment yet.'}
                  </div>
                </article>

                <article
                  className="segment-compare__compare-card"
                  data-tone={
                    inspectedVersion.acceptance_state === 'pending'
                      ? 'pending'
                      : showRestoreAction
                        ? 'alternate'
                        : undefined
                  }
                >
                  <div className="segment-compare__compare-card-header">
                    <span>
                      {inspectedVersion.acceptance_state === 'pending'
                        ? 'Candidate rewrite'
                        : inspectedVersion.is_current
                          ? 'Active manuscript'
                          : 'Selected revision'}
                    </span>
                    <Badge
                      tone={
                        inspectedVersion.acceptance_state === 'pending'
                          ? 'accent'
                          : inspectedVersion.is_current
                            ? 'success'
                            : 'neutral'
                      }
                    >
                      {buildVersionLabel(inspectedVersion)}
                    </Badge>
                  </div>
                  <div className="segment-compare__text">
                    {compareAgainstCurrent && diffSummary != null
                      ? renderHighlightedText(diffSummary.parts, 'after')
                      : inspectedVersion.text_content ??
                        'No saved text exists for this revision yet.'}
                  </div>
                </article>
              </div>

              {showPendingRewriteActions || showRestoreAction ? (
                <div className="segment-compare__actions">
                  {showPendingRewriteActions && reviewJob != null && onAcceptRewrite != null ? (
                    <Button
                      disabled={disabled}
                      onClick={() => {
                        onAcceptRewrite(reviewJob.id)
                      }}
                      tone="primary"
                    >
                      {actionState === 'acceptRewrite'
                        ? 'Accepting...'
                        : 'Accept rewrite'}
                    </Button>
                  ) : null}

                  {showPendingRewriteActions && reviewJob != null && onRejectRewrite != null ? (
                    <Button
                      disabled={disabled}
                      onClick={() => {
                        onRejectRewrite(reviewJob.id)
                      }}
                      tone="ghost"
                    >
                      {actionState === 'rejectRewrite'
                        ? 'Keeping current draft...'
                        : 'Keep current draft'}
                    </Button>
                  ) : null}

                  {showPendingRewriteActions && onKeepExploring != null ? (
                    <Button
                      disabled={disabled}
                      onClick={() => {
                        onKeepExploring(selectedSegment.segment_index)
                      }}
                      tone="ghost"
                    >
                      Try another rewrite
                    </Button>
                  ) : null}

                  {showRestoreAction && onRestoreVersion != null ? (
                    <Button
                      disabled={disabled}
                      onClick={() => {
                        onRestoreVersion(
                          selectedSegment.segment_index,
                          inspectedVersion.id,
                        )
                      }}
                      tone="primary"
                    >
                      {actionState === 'restoreVersion'
                        ? 'Restoring...'
                        : 'Restore this revision'}
                    </Button>
                  ) : null}
                </div>
              ) : null}

              {showPendingRewriteActions ? (
                <p className="segment-compare__action-note">
                  {buildReviewActionSummary(compareContext)}
                </p>
              ) : null}

              {actionError != null ? (
                <p className="field__error" role="alert">
                  {actionError}
                </p>
              ) : null}

              {selectedSegment.versions.length > 1 ? (
                <div className="segment-compare__history-list">
                  {selectedSegment.versions.map((version) => {
                    const isPreviewed = inspectedVersion.id === version.id

                    return (
                      <article
                        className="segment-compare__history-card"
                        data-selected={isPreviewed || undefined}
                        key={version.id}
                      >
                        <div className="segment-compare__history-card-header">
                          <div>
                            <strong>{buildVersionLabel(version)}</strong>
                            <span>{version.job_kind}</span>
                          </div>

                          <Button
                            onClick={() => {
                              setInspectedVersionId(version.id)
                            }}
                            size="compact"
                            tone="ghost"
                          >
                            {isPreviewed ? 'Previewing' : 'Compare'}
                          </Button>
                        </div>
                        <p>
                          {version.accepted_summary ??
                            version.planned_summary ??
                            'No revision summary was captured for this version.'}
                        </p>
                      </article>
                    )
                  })}
                </div>
              ) : null}
            </>
          ) : (
            <div className="composition-stage__empty">
              <p>Once the first segment lands, its revision history will appear here.</p>
            </div>
          )}
        </section>
      </div>
    </section>
  )
}
