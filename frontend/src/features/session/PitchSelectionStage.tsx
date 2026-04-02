import { useMemo, useState } from 'react'
import type {
  SessionHistoryEvent,
  SessionPitchGenerationResponse,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { Badge, Button, TextArea } from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  InlineHelp,
  SelectField,
  SelectionCard,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

type PitchSelectionStageProps = {
  onGeneratePitches: (input: {
    candidateCount: number
    guidance?: string | null
    origin: string
    preserveSelectedPitch?: boolean
  }) => Promise<SessionPitchGenerationResponse>
  onPreviewStage: (stageId: 'brief' | 'characters') => void
  onSelectPitch: (selection: {
    generationKey?: string | null
    origin: string
    pitchId?: string | null
    pitchIndex?: number | null
    title?: string | null
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

const batchTimestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function readPitchHook(pitch: {
  hook?: string | null
  logline?: string | null
}) {
  return pitch.hook ?? pitch.logline ?? 'Hook pending.'
}

function readPitchConflict(pitch: {
  central_conflict?: string | null
  summary?: string | null
}) {
  return (
    pitch.central_conflict ??
    pitch.summary ??
    'The core conflict will appear here once the pitch batch is generated.'
  )
}

function readPitchFitNote(pitch: {
  bedtime_notes?: string | null
  why_it_fits?: string | null
}) {
  return (
    pitch.why_it_fits ??
    pitch.bedtime_notes ??
    'The bedtime-fit note will explain why this option matches the session.'
  )
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  snapshot: SessionSnapshot,
) {
  if (selectedStage.availability === 'locked') {
    return {
      body: 'Save the story brief first. The pitch stage stays visible, but generation is disabled until the brief is durable.',
      title: 'Story brief comes first',
      tone: 'warning' as const,
    }
  }

  if (selectedStage.availability === 'revisitable' && snapshot.selected_pitch) {
    return {
      body: 'Generating a new batch reopens pitch review and refreshes later planning. The currently accepted pitch can stay visible while you compare alternatives.',
      title: 'New pitch batches refresh downstream work',
      tone: 'warning' as const,
    }
  }

  if ((snapshot.pitch_batches?.length ?? 0) > 0) {
    return {
      body: 'Compare the hook, central conflict, and fit note on each card. The goal is quick comparison, not a wall of prose.',
      title: 'Choose the strongest story lane',
      tone: 'success' as const,
    }
  }

  return {
    body: 'Generate a handful of differentiated directions from the selected genre, tone, and saved brief. Each pitch should feel like a genuinely different bedtime story path.',
    title: 'Start with several strong options',
    tone: 'info' as const,
  }
}

function formatBatchTimestamp(value: string) {
  return `Generated ${batchTimestampFormatter.format(new Date(value))}`
}

export function PitchSelectionStage({
  onGeneratePitches,
  onPreviewStage,
  onSelectPitch,
  selectedStage,
  snapshot,
}: PitchSelectionStageProps) {
  const pitchBatches = snapshot.pitch_batches ?? []
  const latestBatch = pitchBatches[0] ?? null
  const selectedPitchId = snapshot.selected_pitch?.id ?? null
  const revisionHelp = buildRevisionHelp(selectedStage, snapshot)
  const [candidateCount, setCandidateCount] = useState(
    String(latestBatch?.candidate_count ?? 4),
  )
  const [guidance, setGuidance] = useState('')
  const [generationError, setGenerationError] = useState<string | null>(null)
  const [selectionError, setSelectionError] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [pendingPitchId, setPendingPitchId] = useState<string | null>(null)

  const latestBatchPitches = useMemo(
    () => latestBatch?.pitches ?? [],
    [latestBatch],
  )

  async function handleGeneratePitches() {
    if (selectedStage.availability === 'locked' || isGenerating) {
      return
    }

    setGenerationError(null)
    setIsGenerating(true)

    try {
      await onGeneratePitches({
        candidateCount: Number(candidateCount),
        guidance: guidance.trim() || null,
        origin: 'workspace',
        preserveSelectedPitch: snapshot.selected_pitch != null,
      })
    } catch (error) {
      setGenerationError(
        error instanceof Error
          ? error.message
          : 'The pitch batch could not be generated right now.',
      )
    } finally {
      setIsGenerating(false)
    }
  }

  async function handlePitchSelection(pitch: {
    generation_key: string
    id: string
    pitch_index: number
    title: string
  }) {
    setPendingPitchId(pitch.id)
    setSelectionError(null)

    try {
      await onSelectPitch({
        pitchId: pitch.id,
        generationKey: pitch.generation_key,
        pitchIndex: pitch.pitch_index,
        title: pitch.title,
        origin: 'workspace',
      })
    } catch (error) {
      setSelectionError(
        error instanceof Error
          ? error.message
          : 'The selected pitch could not be saved right now.',
      )
    } finally {
      setPendingPitchId(null)
    }
  }

  return (
    <section
      aria-label="Pitch selection stage"
      className="workspace-stage-panel"
    >
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            snapshot.selected_pitch != null
              ? readPitchHook(snapshot.selected_pitch)
              : 'No pitch is accepted yet. Generate a batch and choose one story lane before characters.'
          }
          label="Current selection"
          title={snapshot.selected_pitch?.title ?? 'Pitch pending'}
          tone={snapshot.selected_pitch != null ? 'accent' : 'default'}
        />

        <SummaryPanel
          description={
            latestBatch != null
              ? formatBatchTimestamp(latestBatch.created_at)
              : 'The newest durable batch will appear here once pitch generation runs.'
          }
          label="Latest batch"
          title={
            latestBatch != null
              ? `${latestBatch.candidate_count} pitch cards ready`
              : 'No pitch batch yet'
          }
        >
          {latestBatch != null ? (
            <div className="workspace-stage-detail__badges">
              <Badge tone="brand">{latestBatch.generation_key}</Badge>
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={
            snapshot.selected_pitch != null
              ? 'Character generation can now stay anchored to the accepted story lane.'
              : 'Selecting a pitch completes this stage and unlocks character generation.'
          }
          label="Next step"
          title={
            snapshot.selected_pitch != null
              ? 'Characters are ready next'
              : 'Choose one pitch to continue'
          }
        >
          <div className="cta-row">
            <Button
              onClick={() => {
                onPreviewStage(
                  snapshot.selected_pitch != null ? 'characters' : 'brief',
                )
              }}
              tone="ghost"
            >
              {snapshot.selected_pitch != null
                ? 'Preview character stage'
                : 'Revisit brief'}
            </Button>
          </div>
        </SummaryPanel>
      </CardGrid>

      <InlineHelp title={revisionHelp.title} tone={revisionHelp.tone}>
        {revisionHelp.body}
      </InlineHelp>

      {generationError != null ? (
        <InlineHelp title="Pitch generation failed" tone="warning">
          {generationError}
        </InlineHelp>
      ) : null}

      {selectionError != null ? (
        <InlineHelp title="Pitch selection failed" tone="warning">
          {selectionError}
        </InlineHelp>
      ) : null}

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Generate a pitch batch</h3>
            <p>
              Create several differentiated bedtime-story directions grounded in
              the saved brief, then compare them as durable cards.
            </p>
          </div>
          <Badge tone={latestBatch != null ? 'success' : 'warning'}>
            {latestBatch != null ? 'Ready to compare' : 'Generation required'}
          </Badge>
        </div>

        <CardGrid className="pitch-stage__controls" columns={2}>
          <SelectField
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Pitch count"
            onChange={(event) => {
              setCandidateCount(event.currentTarget.value)
            }}
            options={[
              { label: '3 candidates', value: '3' },
              { label: '4 candidates', value: '4' },
              { label: '5 candidates', value: '5' },
            ]}
            value={candidateCount}
          />

          <TextArea
            description="Optional guidance can steer the next batch without locking the story too early."
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Optional pitch guidance"
            onChange={(event) => {
              setGuidance(event.currentTarget.value)
            }}
            rows={4}
            value={guidance}
          />
        </CardGrid>

        <div className="cta-row">
          <Button
            disabled={selectedStage.availability === 'locked' || isGenerating}
            onClick={() => {
              void handleGeneratePitches()
            }}
            tone="primary"
          >
            {isGenerating
              ? 'Generating pitches...'
              : latestBatch != null
                ? 'Regenerate pitches'
                : 'Generate pitches'}
          </Button>
          <Button
            onClick={() => {
              onPreviewStage('brief')
            }}
            tone="ghost"
          >
            Revisit brief
          </Button>
        </div>
      </section>

      {latestBatch == null ? (
        <EmptyStateBlock
          action={
            <Button
              disabled={selectedStage.availability === 'locked' || isGenerating}
              onClick={() => {
                void handleGeneratePitches()
              }}
              tone="primary"
            >
              Generate the first batch
            </Button>
          }
          description="The pitch stage will keep every generated batch so the user can come back later and compare old directions against new ones."
          title="No pitch cards have been generated yet"
        />
      ) : null}

      {latestBatch != null ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Latest pitch batch</h3>
              <p>
                The newest batch stays first so the cards are fast to compare.
                Earlier batches remain below for resume and review.
              </p>
            </div>
            <Badge tone="brand">
              {formatBatchTimestamp(latestBatch.created_at)}
            </Badge>
          </div>

          <CardGrid className="pitch-stage__grid" columns={2}>
            {latestBatchPitches.map((pitch) => {
              const selected = pitch.id === selectedPitchId
              const isPending = pendingPitchId === pitch.id

              return (
                <SelectionCard
                  key={pitch.id}
                  className="pitch-stage__card"
                  description={readPitchHook(pitch)}
                  eyebrow={`Pitch ${String(pitch.pitch_index).padStart(2, '0')}`}
                  footer={
                    <div className="cta-row">
                      <Button
                        disabled={selected || isPending}
                        onClick={() => {
                          void handlePitchSelection(pitch)
                        }}
                        tone={selected ? 'ghost' : 'primary'}
                      >
                        {selected
                          ? 'Selected pitch'
                          : isPending
                            ? 'Saving pitch...'
                            : 'Choose pitch'}
                      </Button>
                    </div>
                  }
                  meta={
                    <div className="workspace-stage-detail__badges">
                      <Badge tone="neutral">{pitch.generation_key}</Badge>
                      {selected ? <Badge tone="success">Selected</Badge> : null}
                    </div>
                  }
                  selected={selected}
                  title={pitch.title}
                >
                  <div className="pitch-stage__card-copy">
                    <p>
                      <strong>Central conflict.</strong>{' '}
                      {readPitchConflict(pitch)}
                    </p>
                    <p>
                      <strong>Why it fits.</strong> {readPitchFitNote(pitch)}
                    </p>
                  </div>
                </SelectionCard>
              )
            })}
          </CardGrid>
        </section>
      ) : null}

      {pitchBatches.length > 1 ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Earlier pitch batches</h3>
              <p>
                Older generations stay available so the user can revisit prior
                directions instead of losing them after each refresh.
              </p>
            </div>
            <Badge tone="neutral">
              {pitchBatches.length - 1} earlier batch
              {pitchBatches.length === 2 ? '' : 'es'}
            </Badge>
          </div>

          <div className="pitch-stage__history">
            {pitchBatches.slice(1).map((batch) => (
              <SummaryPanel
                key={batch.generation_key}
                description={formatBatchTimestamp(batch.created_at)}
                label="Earlier batch"
                title={`${batch.candidate_count} saved options`}
              >
                <div className="pitch-stage__history-titles">
                  {batch.pitches.map((pitch) => (
                    <span key={pitch.id}>{pitch.title}</span>
                  ))}
                </div>
              </SummaryPanel>
            ))}
          </div>
        </section>
      ) : null}
    </section>
  )
}
