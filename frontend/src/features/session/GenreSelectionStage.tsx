import { useState } from 'react'
import type { GenreCatalogEntry } from '../../api/catalog.ts'
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
import { useGenreCatalogQuery } from './catalogQueries.ts'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

type GenreSelectionStageProps = {
  onPreviewStage: (stageId: 'tone') => void
  onSelectGenre: (selection: {
    genreId?: string | null
    genreLabel?: string | null
    genreSlug?: string | null
    origin: string
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

function readArcNote(
  arcNotes: GenreCatalogEntry['arc_notes'],
  key: string,
): string | null {
  const value = arcNotes[key]

  if (typeof value === 'string' && value.trim().length > 0) {
    return value
  }

  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value)
  }

  return null
}

function buildNextStepCopy(selectedGenre: GenreCatalogEntry | null) {
  if (selectedGenre == null) {
    return 'Choose a genre to unlock tone choices next.'
  }

  return `Tone choices will filter to ${selectedGenre.label} next.`
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  selectedGenre: GenreCatalogEntry | null,
) {
  if (selectedStage.availability === 'revisitable' && selectedGenre != null) {
    return {
      body: `Changing ${selectedGenre.label} will clear any incompatible tone selection and mark later planning stages for refresh.`,
      title: 'Changing genre rewires the plan',
      tone: 'warning' as const,
    }
  }

  if (selectedGenre != null) {
    return {
      body: `Tone selection is the next durable step, and it will only show options that match ${selectedGenre.label}.`,
      title: 'Tone filters from this choice',
      tone: 'success' as const,
    }
  }

  return {
    body: 'The catalog is seeded with bedtime-safe lanes, so the user picks from a curated set instead of inventing a genre from scratch.',
    title: 'Choose from the catalog',
    tone: 'info' as const,
  }
}

export function GenreSelectionStage({
  onPreviewStage,
  onSelectGenre,
  selectedStage,
  snapshot,
}: GenreSelectionStageProps) {
  const genreCatalogQuery = useGenreCatalogQuery()
  const [pendingGenreId, setPendingGenreId] = useState<string | null>(null)
  const [selectionError, setSelectionError] = useState<string | null>(null)

  const selectedGenre =
    genreCatalogQuery.data?.find(
      (genre) => genre.id === snapshot.selected_genre?.id,
    ) ??
    genreCatalogQuery.data?.find(
      (genre) => genre.slug === snapshot.selected_genre?.slug,
    ) ??
    null
  const selectedGenreCoreArc =
    selectedGenre != null
      ? readArcNote(selectedGenre.arc_notes, 'core_arc')
      : null
  const selectedGenreTension =
    selectedGenre != null
      ? readArcNote(selectedGenre.arc_notes, 'tension_ceiling')
      : null
  const revisionHelp = buildRevisionHelp(selectedStage, selectedGenre)

  async function handleGenreSelection(genre: GenreCatalogEntry) {
    setPendingGenreId(genre.id)
    setSelectionError(null)

    try {
      await onSelectGenre({
        genreId: genre.id,
        genreSlug: genre.slug,
        genreLabel: genre.label,
        origin: 'workspace',
      })
    } catch (error) {
      setSelectionError(
        error instanceof Error
          ? error.message
          : 'The selected genre could not be saved right now.',
      )
    } finally {
      setPendingGenreId(null)
    }
  }

  return (
    <section
      aria-label="Genre selection stage"
      className="workspace-stage-panel"
    >
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            selectedGenre?.description ??
            'Pick a bedtime lane to ground the rest of the planning workflow.'
          }
          label="Current lane"
          title={selectedGenre?.label ?? 'Genre pending'}
          tone={selectedGenre != null ? 'accent' : 'default'}
        >
          {selectedGenreTension != null ? (
            <div className="workspace-stage-detail__badges">
              <Badge tone="brand">{selectedGenreTension}</Badge>
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={
            selectedGenre?.bedtime_safety_notes ??
            'Every entry in this catalog is pre-vetted for calm stakes, emotional repair, and a safe landing before sleep.'
          }
          label="Bedtime guardrail"
          title={selectedGenreCoreArc ?? 'A calm story arc comes built in'}
        />

        <SummaryPanel
          description={buildNextStepCopy(selectedGenre)}
          label="Next step"
          title="Tone selection comes next"
        >
          {selectedGenre != null ? (
            <div className="cta-row">
              <Button
                onClick={() => {
                  onPreviewStage('tone')
                }}
                tone="ghost"
              >
                Preview tone stage
              </Button>
            </div>
          ) : null}
        </SummaryPanel>
      </CardGrid>

      <InlineHelp title={revisionHelp.title} tone={revisionHelp.tone}>
        {revisionHelp.body}
      </InlineHelp>

      {selectionError != null ? (
        <InlineHelp title="Genre selection failed" tone="warning">
          {selectionError}
        </InlineHelp>
      ) : null}

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Curated bedtime genres</h3>
            <p>
              These cards come from the seeded catalog, with short descriptions,
              bedtime safety notes, and arc guidance for what comes next.
            </p>
          </div>
          <Badge tone={selectedGenre != null ? 'success' : 'warning'}>
            {selectedGenre != null ? 'Selected' : 'Required'}
          </Badge>
        </div>

        {genreCatalogQuery.isPending ? (
          <EmptyStateBlock
            description="Loading the backend-owned genre catalog."
            title="Preparing genre options"
          />
        ) : null}

        {genreCatalogQuery.isError ? (
          <EmptyStateBlock
            action={
              <Button
                onClick={() => {
                  void genreCatalogQuery.refetch()
                }}
                tone="ghost"
              >
                Retry catalog load
              </Button>
            }
            description="The catalog endpoint did not respond, so genre selection is temporarily unavailable."
            title="Genre catalog unavailable"
          />
        ) : null}

        {!genreCatalogQuery.isPending &&
        !genreCatalogQuery.isError &&
        (genreCatalogQuery.data?.length ?? 0) === 0 ? (
          <EmptyStateBlock
            description="Seed the backend catalog to make the curated genres available in this workspace."
            title="No genres are currently available"
          />
        ) : null}

        {!genreCatalogQuery.isPending &&
        !genreCatalogQuery.isError &&
        (genreCatalogQuery.data?.length ?? 0) > 0 ? (
          <CardGrid className="genre-selection-grid" columns={2}>
            {genreCatalogQuery.data?.map((genre) => {
              const selected = snapshot.selected_genre?.id === genre.id
              const isPending = pendingGenreId === genre.id
              const tensionCeiling = readArcNote(
                genre.arc_notes,
                'tension_ceiling',
              )
              const coreArc = readArcNote(genre.arc_notes, 'core_arc')

              return (
                <SelectionCard
                  key={genre.id}
                  description={genre.description ?? undefined}
                  eyebrow={selected ? 'Selected genre' : 'Genre option'}
                  footer={
                    <div className="genre-selection-card__footer">
                      <p>
                        {selected
                          ? 'Tone choices already filter from this genre.'
                          : 'Choosing this genre narrows the tone list for the next step.'}
                      </p>
                      <Button
                        disabled={selected || pendingGenreId != null}
                        onClick={() => {
                          void handleGenreSelection(genre)
                        }}
                        tone={selected ? 'ghost' : 'primary'}
                      >
                        {selected
                          ? 'Selected'
                          : isPending
                            ? 'Selecting...'
                            : 'Choose genre'}
                      </Button>
                    </div>
                  }
                  leading={(genre.sort_order + 1).toString().padStart(2, '0')}
                  meta={
                    <>
                      {selected ? (
                        <Badge tone="success">Current</Badge>
                      ) : (
                        <Badge tone="neutral">Available</Badge>
                      )}
                      {tensionCeiling != null ? (
                        <Badge tone="brand">{tensionCeiling}</Badge>
                      ) : null}
                    </>
                  }
                  selected={selected}
                  title={genre.label}
                >
                  <dl className="genre-selection-card__facts">
                    <div>
                      <dt>Arc</dt>
                      <dd>
                        {coreArc ?? 'Bedtime-safe arc guidance included.'}
                      </dd>
                    </div>
                    <div>
                      <dt>Safety note</dt>
                      <dd>
                        {genre.bedtime_safety_notes ??
                          'Keep stakes gentle and land the ending in visible rest.'}
                      </dd>
                    </div>
                  </dl>
                </SelectionCard>
              )
            })}
          </CardGrid>
        ) : null}
      </section>
    </section>
  )
}
