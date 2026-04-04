import { useState } from 'react'
import type { ToneCatalogEntry } from '../../api/catalog.ts'
import type {
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { Badge, Button } from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  InlineHelp,
  SelectionCard,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import { useToneCatalogQuery } from './catalogQueries.ts'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

type ToneSelectionStageProps = {
  onPreviewStage: (stageId: 'brief' | 'genre') => void
  onSelectTone: (selection: {
    origin: string
    toneProfileId?: string | null
    toneProfileLabel?: string | null
    toneProfileSlug?: string | null
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

type PlanningHints = ToneCatalogEntry['default_planning_hints']

function readPlanningHintText(
  hints: PlanningHints,
  key: string,
): string | null {
  const value = hints[key]

  if (typeof value === 'string') {
    const normalized = value.trim()
    return normalized.length > 0 ? normalized : null
  }

  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value)
  }

  if (Array.isArray(value)) {
    const values = value
      .filter(
        (entry): entry is string | number | boolean =>
          typeof entry === 'string' ||
          typeof entry === 'number' ||
          typeof entry === 'boolean',
      )
      .map((entry) => String(entry).trim())
      .filter((entry) => entry.length > 0)

    return values.length > 0 ? values.join(', ') : null
  }

  return null
}

function readPlanningHintList(hints: PlanningHints, key: string): string[] {
  const value = hints[key]

  if (!Array.isArray(value)) {
    return []
  }

  return value
    .filter((entry): entry is string => typeof entry === 'string')
    .map((entry) => entry.trim())
    .filter((entry) => entry.length > 0)
}

function buildNextStepCopy(
  selectedGenreLabel: string | null,
  selectedTone: ToneCatalogEntry | null,
) {
  if (selectedGenreLabel == null) {
    return 'Pick a genre first so the tone catalog can filter correctly.'
  }

  if (selectedTone == null) {
    return `Choose the ${selectedGenreLabel} mood you want before writing the free-form brief.`
  }

  return `The story brief will now inherit ${selectedTone.label.toLowerCase()} as its read-aloud posture.`
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  selectedGenreLabel: string | null,
  selectedTone: ToneCatalogEntry | null,
) {
  if (selectedGenreLabel == null) {
    return {
      body: 'Tone selection stays locked until the session has a genre. That keeps the catalog focused and prevents mismatched bedtime moods.',
      title: 'Choose genre first',
      tone: 'warning' as const,
    }
  }

  if (selectedStage.availability === 'revisitable' && selectedTone != null) {
    return {
      body: `Changing ${selectedTone.label} will refresh the brief and any later planning that already depends on this tone.`,
      title: 'Changing tone refreshes downstream work',
      tone: 'warning' as const,
    }
  }

  if (selectedTone != null) {
    return {
      body: `The brief, pitches, and later beats can now stay anchored in the ${selectedGenreLabel} lane without drifting away from ${selectedTone.label}.`,
      title: 'Tone is now part of the durable plan',
      tone: 'success' as const,
    }
  }

  return {
    body: `Only ${selectedGenreLabel} tone profiles are shown here, with concrete bedtime cues instead of vague adjectives.`,
    title: 'Filtered to the selected genre',
    tone: 'info' as const,
  }
}

export function ToneSelectionStage({
  onPreviewStage,
  onSelectTone,
  selectedStage,
  snapshot,
}: ToneSelectionStageProps) {
  const selectedGenre = snapshot.selected_genre
  const toneCatalogQuery = useToneCatalogQuery(selectedGenre?.slug)
  const [pendingToneId, setPendingToneId] = useState<string | null>(null)
  const [selectionError, setSelectionError] = useState<string | null>(null)

  const selectedTone =
    toneCatalogQuery.data?.find(
      (tone) => tone.id === snapshot.selected_tone_profile?.id,
    ) ??
    toneCatalogQuery.data?.find(
      (tone) => tone.slug === snapshot.selected_tone_profile?.slug,
    ) ??
    null
  const selectedTonePacing =
    selectedTone != null
      ? readPlanningHintText(selectedTone.default_planning_hints, 'pacing')
      : null
  const selectedToneConflictStyle =
    selectedTone != null
      ? readPlanningHintText(
          selectedTone.default_planning_hints,
          'conflict_style',
        )
      : null
  const selectedToneEndingStyle =
    selectedTone != null
      ? readPlanningHintText(
          selectedTone.default_planning_hints,
          'ending_style',
        )
      : null
  const selectedToneMotifs =
    selectedTone != null
      ? readPlanningHintList(
          selectedTone.default_planning_hints,
          'sensory_motifs',
        )
      : []
  const revisionHelp = buildRevisionHelp(
    selectedStage,
    selectedGenre?.label ?? null,
    selectedTone,
  )

  async function handleToneSelection(tone: ToneCatalogEntry) {
    setPendingToneId(tone.id)
    setSelectionError(null)

    try {
      await onSelectTone({
        toneProfileId: tone.id,
        toneProfileSlug: tone.slug,
        toneProfileLabel: tone.label,
        origin: 'workspace',
      })
    } catch (error) {
      setSelectionError(
        error instanceof Error
          ? error.message
          : 'The selected tone could not be saved right now.',
      )
    } finally {
      setPendingToneId(null)
    }
  }

  return (
    <section
      aria-label="Tone selection stage"
      className="workspace-stage-panel"
    >
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            selectedTone?.description ??
            'Choose the emotional texture that should guide pacing, comfort, and the eventual bedtime landing.'
          }
          label="Current mood"
          title={selectedTone?.label ?? 'Tone pending'}
          tone={selectedTone != null ? 'accent' : 'default'}
        >
          {selectedTone != null && selectedTone.descriptors.length > 0 ? (
            <div className="workspace-stage-detail__badges">
              {selectedTone.descriptors.map((descriptor) => (
                <Badge key={descriptor} tone="brand">
                  {descriptor}
                </Badge>
              ))}
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={
            selectedToneConflictStyle ??
            selectedTone?.bedtime_notes ??
            'The selected tone should make comfort, suspense, and read-aloud rhythm explicit before story planning begins.'
          }
          label="Read-aloud feel"
          title={selectedTonePacing ?? 'Calm pacing guidance pending'}
        >
          {selectedToneMotifs.length > 0 ? (
            <div className="workspace-stage-detail__badges">
              {selectedToneMotifs.map((motif) => (
                <Badge key={motif} tone="neutral">
                  {motif}
                </Badge>
              ))}
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={buildNextStepCopy(
            selectedGenre?.label ?? null,
            selectedTone,
          )}
          label="Next step"
          title={selectedToneEndingStyle ?? 'Story brief comes next'}
        >
          {selectedTone != null ? (
            <div className="cta-row">
              <Button
                onClick={() => {
                  onPreviewStage('brief')
                }}
                tone="ghost"
              >
                Preview story brief
              </Button>
            </div>
          ) : null}
        </SummaryPanel>
      </CardGrid>

      <InlineHelp title={revisionHelp.title} tone={revisionHelp.tone}>
        {revisionHelp.body}
      </InlineHelp>

      {selectionError != null ? (
        <InlineHelp title="Tone selection failed" tone="warning">
          {selectionError}
        </InlineHelp>
      ) : null}

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Bedtime tone profiles</h3>
            <p>
              Each option is filtered to{' '}
              {selectedGenre?.label ?? 'the selected genre'} and includes
              concrete pacing, conflict, and ending cues.
            </p>
          </div>
          <Badge tone={selectedTone != null ? 'success' : 'warning'}>
            {selectedTone != null ? 'Selected' : 'Required'}
          </Badge>
        </div>

        {selectedGenre == null ? (
          <EmptyStateBlock
            action={
              <Button
                onClick={() => {
                  onPreviewStage('genre')
                }}
                tone="ghost"
              >
                Choose genre first
              </Button>
            }
            description="This stage only loads tone options after a genre is chosen, because each genre has its own curated mood set."
            title="Genre selection is required before tone selection"
          />
        ) : null}

        {selectedGenre != null && toneCatalogQuery.isPending ? (
          <EmptyStateBlock
            description={`Loading tone profiles for ${selectedGenre.label}.`}
            title="Preparing tone options"
          />
        ) : null}

        {selectedGenre != null && toneCatalogQuery.isError ? (
          <EmptyStateBlock
            action={
              <Button
                onClick={() => {
                  void toneCatalogQuery.refetch()
                }}
                tone="ghost"
              >
                Retry tone load
              </Button>
            }
            description="The filtered tone catalog did not respond, so this stage cannot yet show the bedtime mood options."
            title="Tone catalog unavailable"
          />
        ) : null}

        {selectedGenre != null &&
        !toneCatalogQuery.isPending &&
        !toneCatalogQuery.isError &&
        (toneCatalogQuery.data?.length ?? 0) === 0 ? (
          <EmptyStateBlock
            description="The selected genre is active, but it does not currently have any tone profiles seeded in the backend catalog."
            title="No tones are currently available for this genre"
          />
        ) : null}

        {selectedGenre != null &&
        !toneCatalogQuery.isPending &&
        !toneCatalogQuery.isError &&
        (toneCatalogQuery.data?.length ?? 0) > 0 ? (
          <CardGrid className="tone-selection-grid" columns={2}>
            {toneCatalogQuery.data?.map((tone) => {
              const selected = snapshot.selected_tone_profile?.id === tone.id
              const isPending = pendingToneId === tone.id
              const pacing = readPlanningHintText(
                tone.default_planning_hints,
                'pacing',
              )
              const conflictStyle = readPlanningHintText(
                tone.default_planning_hints,
                'conflict_style',
              )
              const endingStyle = readPlanningHintText(
                tone.default_planning_hints,
                'ending_style',
              )
              const sensoryMotifs = readPlanningHintList(
                tone.default_planning_hints,
                'sensory_motifs',
              )

              return (
                <SelectionCard
                  key={tone.id}
                  description={tone.description ?? undefined}
                  eyebrow={
                    selected ? 'Selected tone' : `${selectedGenre.label} tone`
                  }
                  footer={
                    <div className="tone-selection-card__footer">
                      <p>
                        {selected
                          ? 'This tone is already guiding the bedtime plan.'
                          : 'Choosing this tone moves the workspace into the story brief.'}
                      </p>
                      <Button
                        disabled={selected || isPending}
                        onClick={() => {
                          void handleToneSelection(tone)
                        }}
                        tone={selected ? 'ghost' : 'primary'}
                      >
                        {selected
                          ? 'Selected'
                          : isPending
                            ? 'Saving tone...'
                            : 'Choose tone'}
                      </Button>
                    </div>
                  }
                  leading={(tone.sort_order + 1).toString().padStart(2, '0')}
                  meta={
                    <>
                      <Badge tone={selected ? 'success' : 'neutral'}>
                        {selected ? 'Current' : 'Available'}
                      </Badge>
                      {pacing != null ? (
                        <Badge tone="brand">{pacing}</Badge>
                      ) : null}
                    </>
                  }
                  selected={selected}
                  title={tone.label}
                >
                  {tone.descriptors.length > 0 ? (
                    <div className="tone-selection-card__descriptors">
                      {tone.descriptors.map((descriptor) => (
                        <Badge key={descriptor} tone="neutral">
                          {descriptor}
                        </Badge>
                      ))}
                    </div>
                  ) : null}

                  <dl className="genre-selection-card__facts tone-selection-card__facts">
                    <div>
                      <dt>Read-aloud feel</dt>
                      <dd>{pacing ?? 'Calm, bedtime-forward rhythm.'}</dd>
                    </div>
                    <div>
                      <dt>Comfort + tension</dt>
                      <dd>
                        {conflictStyle ??
                          tone.bedtime_notes ??
                          'Comfort stays explicit while tension remains soft.'}
                      </dd>
                    </div>
                    <div>
                      <dt>Ending cue</dt>
                      <dd>
                        {endingStyle ??
                          'Land in visible rest, reassurance, or a gentle sense of home.'}
                      </dd>
                    </div>
                  </dl>

                  {sensoryMotifs.length > 0 ? (
                    <div className="tone-selection-card__motifs">
                      <span>Motifs</span>
                      <p>{sensoryMotifs.join(', ')}</p>
                    </div>
                  ) : null}
                </SelectionCard>
              )
            })}
          </CardGrid>
        ) : null}
      </section>
    </section>
  )
}
