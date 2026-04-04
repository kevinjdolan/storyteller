import { useEffect, useMemo, useState } from 'react'
import type {
  SessionCharacterSheetGenerationResponse,
  SessionHistoryEvent,
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
import { PlanRevisionHistoryPanel } from './PlanRevisionHistoryPanel.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

type CharacterSelectionStageProps = {
  onGenerateCharacterSheets: (input: {
    candidateCount: number
    guidance?: string | null
    origin: string
  }) => Promise<SessionCharacterSheetGenerationResponse>
  onPreviewStage: (stageId: 'pitches' | 'beats') => void
  onRefineCharacterSheet: (selection: {
    instructions: string
    origin: string
    changeImpact?: 'minor' | 'major' | null
    changeSummary?: string | null
    characterSheetId?: string | null
    focusCharacterNames?: string[]
    revisionNumber?: number | null
    title?: string | null
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  onSelectCharacterSheet: (selection: {
    origin: string
    characterSheetId?: string | null
    revisionNumber?: number | null
    title?: string | null
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  onRestorePlanRevision: (selection: {
    origin: string
    revisionNumber: number
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

function formatBatchTimestamp(value: string) {
  return `Generated ${batchTimestampFormatter.format(new Date(value))}`
}

function readCharacterSummary(characterSheet: {
  summary?: string | null
  story_function?: string | null
}) {
  return (
    characterSheet.summary ??
    characterSheet.story_function ??
    'The cast summary will appear here once character sheets are generated.'
  )
}

function readCharacterSelectionCopy(characterSheet: {
  summary?: string | null
  selection_rationale?: string | null
}) {
  return characterSheet.selection_rationale ?? readCharacterSummary(characterSheet)
}

function readLeadSignal(characterSheet: {
  protagonist?: {
    role?: string | null
    goal?: string | null
    flaw?: string | null
    comfort_trait?: string | null
  } | null
}) {
  const protagonist = characterSheet.protagonist
  if (protagonist == null) {
    return 'The lead character notes will appear here once the sheet is generated.'
  }

  return [
    protagonist.role,
    protagonist.goal != null ? `Goal: ${protagonist.goal}` : null,
    protagonist.flaw != null ? `Flaw: ${protagonist.flaw}` : null,
    protagonist.comfort_trait != null
      ? `Comfort trait: ${protagonist.comfort_trait}`
      : null,
  ]
    .filter(Boolean)
    .join(' ')
}

function readSupportingCastSignal(characterSheet: {
  supporting_cast?: Array<{
    name: string
    role?: string | null
    relationships?: string[]
  }>
}) {
  const supportingCast = characterSheet.supporting_cast ?? []
  if (supportingCast.length === 0) {
    return 'Supporting cast details will appear here once the character sheet is generated.'
  }

  return supportingCast
    .slice(0, 2)
    .map((character) => {
      const relationship = character.relationships?.[0]
      return [
        character.name,
        character.role != null ? `(${character.role})` : null,
        relationship != null ? `- ${relationship}` : null,
      ]
        .filter(Boolean)
        .join(' ')
    })
    .join(' ')
}

function buildBatchSummary(
  batch: NonNullable<SessionSnapshot['character_sheet_batches']>[number],
) {
  if (
    batch.generation_kind === 'refinement' &&
    batch.source_character_sheet_title != null &&
    batch.refinement_instructions != null
  ) {
    const summaryTail =
      batch.change_summary != null ? ` ${batch.change_summary}` : ''
    return `Refined from ${batch.source_character_sheet_title}. ${batch.refinement_instructions}${summaryTail}`
  }

  if (
    batch.generation_kind === 'refinement' &&
    batch.source_character_sheet_title != null
  ) {
    return `Refined from ${batch.source_character_sheet_title}.`
  }

  return formatBatchTimestamp(batch.created_at)
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  snapshot: SessionSnapshot,
) {
  if (selectedStage.availability === 'locked') {
    return {
      body: 'Select a pitch first. The character stage stays visible, but generation is disabled until the story lane is locked.',
      title: 'Pitch selection comes first',
      tone: 'warning' as const,
    }
  }

  if (
    selectedStage.availability === 'revisitable' &&
    snapshot.selected_character_sheet
  ) {
    return {
      body: 'Generating a new batch reopens character review and refreshes later planning. The currently accepted sheet stays visible while you compare new cast options.',
      title: 'New character batches refresh downstream work',
      tone: 'warning' as const,
    }
  }

  if ((snapshot.character_sheet_batches?.length ?? 0) > 0) {
    return {
      body: 'Compare protagonist goals, flaws, comfort traits, and support dynamics. The best sheet should make later beats easier to write, not just more decorative.',
      title: 'Choose the cast with the strongest story function',
      tone: 'success' as const,
    }
  }

  return {
    body: 'Generate several cast directions from the accepted pitch so the user can compare different protagonist flaws, support dynamics, and bedtime-safety strategies.',
    title: 'Start with multiple cast options',
    tone: 'info' as const,
  }
}

function parseFocusedCharacterNames(value: string) {
  return value
    .split(/[\n,]/g)
    .map((entry) => entry.trim())
    .filter(Boolean)
}

export function CharacterSelectionStage({
  onGenerateCharacterSheets,
  onPreviewStage,
  onRefineCharacterSheet,
  onRestorePlanRevision,
  onSelectCharacterSheet,
  selectedStage,
  snapshot,
}: CharacterSelectionStageProps) {
  const characterSheetBatches = useMemo(
    () => snapshot.character_sheet_batches ?? [],
    [snapshot.character_sheet_batches],
  )
  const latestBatch = characterSheetBatches[0] ?? null
  const selectedCharacterSheetId = snapshot.selected_character_sheet?.id ?? null
  const revisionHelp = buildRevisionHelp(selectedStage, snapshot)
  const [candidateCount, setCandidateCount] = useState(
    String(latestBatch?.candidate_count ?? 3),
  )
  const [guidance, setGuidance] = useState('')
  const [generationError, setGenerationError] = useState<string | null>(null)
  const [refinementInstructions, setRefinementInstructions] = useState('')
  const [refinementFocusNames, setRefinementFocusNames] = useState('')
  const [refinementChangeSummary, setRefinementChangeSummary] = useState('')
  const [refinementChangeImpact, setRefinementChangeImpact] = useState<
    'minor' | 'major'
  >('major')
  const [refinementError, setRefinementError] = useState<string | null>(null)
  const [selectionError, setSelectionError] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isRefining, setIsRefining] = useState(false)
  const [pendingCharacterSheetId, setPendingCharacterSheetId] = useState<
    string | null
  >(null)
  const [refinementBaseCharacterSheetId, setRefinementBaseCharacterSheetId] =
    useState<string | null>(selectedCharacterSheetId)

  const latestBatchCharacterSheets = useMemo(
    () => latestBatch?.character_sheets ?? [],
    [latestBatch],
  )
  const allCharacterSheets = useMemo(
    () =>
      characterSheetBatches.flatMap((batch) => batch.character_sheets ?? []),
    [characterSheetBatches],
  )
  const refinementBaseCharacterSheet =
    allCharacterSheets.find(
      (characterSheet) => characterSheet.id === refinementBaseCharacterSheetId,
    ) ?? null

  useEffect(() => {
    if (
      refinementBaseCharacterSheetId != null &&
      allCharacterSheets.some(
        (characterSheet) => characterSheet.id === refinementBaseCharacterSheetId,
      )
    ) {
      return
    }

    setRefinementBaseCharacterSheetId(
      selectedCharacterSheetId ?? allCharacterSheets[0]?.id ?? null,
    )
  }, [
    allCharacterSheets,
    refinementBaseCharacterSheetId,
    selectedCharacterSheetId,
  ])

  async function handleGenerateCharacterSheets() {
    if (selectedStage.availability === 'locked' || isGenerating) {
      return
    }

    setGenerationError(null)
    setIsGenerating(true)

    try {
      await onGenerateCharacterSheets({
        candidateCount: Number(candidateCount),
        guidance: guidance.trim() || null,
        origin: 'workspace',
      })
    } catch (error) {
      setGenerationError(
        error instanceof Error
          ? error.message
          : 'The character-sheet batch could not be generated right now.',
      )
    } finally {
      setIsGenerating(false)
    }
  }

  async function handleCharacterSheetSelection(characterSheet: {
    id: string
    revision_number: number
    title?: string | null
  }) {
    setPendingCharacterSheetId(characterSheet.id)
    setSelectionError(null)

    try {
      await onSelectCharacterSheet({
        characterSheetId: characterSheet.id,
        revisionNumber: characterSheet.revision_number,
        title: characterSheet.title ?? null,
        origin: 'workspace',
      })
    } catch (error) {
      setSelectionError(
        error instanceof Error
          ? error.message
          : 'The selected character sheet could not be saved right now.',
      )
    } finally {
      setPendingCharacterSheetId(null)
    }
  }

  async function handleCharacterSheetRefinement() {
    if (
      selectedStage.availability === 'locked' ||
      isRefining ||
      refinementBaseCharacterSheet == null ||
      refinementInstructions.trim().length === 0
    ) {
      return
    }

    setRefinementError(null)
    setIsRefining(true)

    try {
      await onRefineCharacterSheet({
        characterSheetId: refinementBaseCharacterSheet.id,
        revisionNumber: refinementBaseCharacterSheet.revision_number,
        title: refinementBaseCharacterSheet.title ?? null,
        instructions: refinementInstructions.trim(),
        focusCharacterNames: parseFocusedCharacterNames(refinementFocusNames),
        changeSummary: refinementChangeSummary.trim() || null,
        changeImpact: refinementChangeImpact,
        origin: 'workspace',
      })
      setRefinementInstructions('')
      setRefinementFocusNames('')
      setRefinementChangeSummary('')
      setRefinementChangeImpact('major')
    } catch (error) {
      setRefinementError(
        error instanceof Error
          ? error.message
          : 'The character-sheet refinement could not be saved right now.',
      )
    } finally {
      setIsRefining(false)
    }
  }

  return (
    <section
      aria-label="Character selection stage"
      className="workspace-stage-panel"
    >
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            snapshot.selected_character_sheet != null
              ? readCharacterSelectionCopy(snapshot.selected_character_sheet)
              : 'No character sheet is accepted yet. Generate a batch and choose the cast that best supports the selected pitch.'
          }
          label="Current selection"
          title={
            snapshot.selected_character_sheet?.title ?? 'Character sheet pending'
          }
          tone={
            snapshot.selected_character_sheet != null ? 'accent' : 'default'
          }
        >
          {snapshot.selected_character_sheet?.change_impact != null ? (
            <div className="workspace-stage-detail__badges">
              <Badge tone="accent">
                {snapshot.selected_character_sheet.change_impact === 'major'
                  ? 'Major refinement'
                  : 'Minor refinement'}
              </Badge>
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={
            latestBatch != null
              ? buildBatchSummary(latestBatch)
              : 'The newest durable batch will appear here once character generation runs.'
          }
          label="Latest batch"
          title={
            latestBatch != null
              ? latestBatch.generation_kind === 'refinement'
                ? 'Refined cast ready'
                : `${latestBatch.candidate_count} cast cards ready`
              : 'No character batch yet'
          }
        >
          {latestBatch != null ? (
            <div className="workspace-stage-detail__badges">
              <Badge tone="brand">{latestBatch.generation_key}</Badge>
              {latestBatch.generation_kind === 'refinement' ? (
                <Badge tone="accent">Refinement</Badge>
              ) : null}
              {latestBatch.change_impact != null ? (
                <Badge tone="neutral">
                  {latestBatch.change_impact === 'major'
                    ? 'Major change'
                    : 'Minor change'}
                </Badge>
              ) : null}
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={
            snapshot.selected_character_sheet != null
              ? 'Beat generation can now stay anchored to the accepted cast and relationship dynamics.'
              : 'Selecting a character sheet completes this stage and unlocks beat planning.'
          }
          label="Next step"
          title={
            snapshot.selected_character_sheet != null
              ? 'Beat sheet is ready next'
              : 'Choose one cast to continue'
          }
        >
          <div className="cta-row">
            <Button
              onClick={() => {
                onPreviewStage(
                  snapshot.selected_character_sheet != null
                    ? 'beats'
                    : 'pitches',
                )
              }}
              tone="ghost"
            >
              {snapshot.selected_character_sheet != null
                ? 'Preview beat stage'
                : 'Revisit pitches'}
            </Button>
          </div>
        </SummaryPanel>
      </CardGrid>

      <InlineHelp title={revisionHelp.title} tone={revisionHelp.tone}>
        {revisionHelp.body}
      </InlineHelp>

      {generationError != null ? (
        <InlineHelp title="Character generation failed" tone="warning">
          {generationError}
        </InlineHelp>
      ) : null}

      {selectionError != null ? (
        <InlineHelp title="Character selection failed" tone="warning">
          {selectionError}
        </InlineHelp>
      ) : null}

      {refinementError != null ? (
        <InlineHelp title="Character refinement failed" tone="warning">
          {refinementError}
        </InlineHelp>
      ) : null}

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Generate a character batch</h3>
            <p>
              Create several cast directions from the accepted pitch, then
              compare them as durable cards before beats are generated.
            </p>
          </div>
          <Badge tone={latestBatch != null ? 'success' : 'warning'}>
            {latestBatch != null ? 'Ready to compare' : 'Generation required'}
          </Badge>
        </div>

        <CardGrid className="character-stage__controls" columns={2}>
          <SelectField
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Character sheet count"
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
            description="Optional guidance can steer the next cast batch. For example: make the lead more cautious, add a sibling dynamic, or keep the support cast smaller."
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Optional character guidance"
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
              void handleGenerateCharacterSheets()
            }}
            tone="primary"
          >
            {isGenerating
              ? 'Generating character sheets...'
              : latestBatch != null
                ? 'Regenerate character sheets'
                : 'Generate character sheets'}
          </Button>
          <Button
            onClick={() => {
              onPreviewStage('pitches')
            }}
            tone="ghost"
          >
            Revisit pitches
          </Button>
        </div>
      </section>

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Refine a saved character sheet</h3>
            <p>
              Pick one saved cast, describe the change, and save the refined
              result as a new durable option without losing earlier sheets.
            </p>
          </div>
          <Badge
            tone={refinementBaseCharacterSheet != null ? 'brand' : 'warning'}
          >
            {refinementBaseCharacterSheet != null
              ? 'Ready to refine'
              : 'Select a base sheet'}
          </Badge>
        </div>

        <CardGrid className="character-stage__controls" columns={2}>
          <SelectField
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Character sheet to refine"
            onChange={(event) => {
              setRefinementBaseCharacterSheetId(event.currentTarget.value)
            }}
            options={allCharacterSheets.map((characterSheet) => ({
              label: `Rev ${String(characterSheet.revision_number).padStart(2, '0')} · ${characterSheet.title ?? characterSheet.protagonist_name ?? 'Untitled character sheet'}`,
              value: characterSheet.id,
            }))}
            value={refinementBaseCharacterSheetId ?? ''}
          />

          <TextArea
            description="Describe the specific cast change to apply. For example: give the lead a quieter flaw, make the support cast siblings, or add a more obvious comfort ritual."
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Refinement instructions"
            onChange={(event) => {
              setRefinementInstructions(event.currentTarget.value)
            }}
            rows={4}
            value={refinementInstructions}
          />

          <TextArea
            description="Optional. Focus the change on specific characters. Separate names with commas or line breaks."
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Focus characters"
            onChange={(event) => {
              setRefinementFocusNames(event.currentTarget.value)
            }}
            rows={3}
            value={refinementFocusNames}
          />

          <TextArea
            description="Optional. Save a concise durable summary that will show up later in chat and in the saved character history."
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Change summary"
            onChange={(event) => {
              setRefinementChangeSummary(event.currentTarget.value)
            }}
            rows={3}
            value={refinementChangeSummary}
          />

          <SelectField
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Planning impact"
            onChange={(event) => {
              setRefinementChangeImpact(
                event.currentTarget.value === 'minor' ? 'minor' : 'major',
              )
            }}
            options={[
              { label: 'Major change', value: 'major' },
              { label: 'Minor polish', value: 'minor' },
            ]}
            value={refinementChangeImpact}
          />
        </CardGrid>

        <div className="cta-row">
          <Button
            disabled={
              selectedStage.availability === 'locked' ||
              isRefining ||
              refinementBaseCharacterSheet == null ||
              refinementInstructions.trim().length === 0
            }
            onClick={() => {
              void handleCharacterSheetRefinement()
            }}
            tone="primary"
          >
            {isRefining ? 'Refining character sheet...' : 'Refine character sheet'}
          </Button>
          {refinementBaseCharacterSheet != null ? (
            <Badge tone="neutral">
              {refinementBaseCharacterSheet.title ??
                refinementBaseCharacterSheet.protagonist_name ??
                'Selected base sheet'}
            </Badge>
          ) : null}
        </div>
      </section>

      {latestBatch == null ? (
        <EmptyStateBlock
          action={
            <Button
              disabled={selectedStage.availability === 'locked' || isGenerating}
              onClick={() => {
                void handleGenerateCharacterSheets()
              }}
              tone="primary"
            >
              Generate the first batch
            </Button>
          }
          description="The character stage keeps every generated batch so the user can resume comparison later instead of losing cast options after each refresh."
          title="No character sheets have been generated yet"
        />
      ) : null}

      {latestBatch != null ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Latest character batch</h3>
              <p>
                The newest batch stays first so the strongest cast options are
                quick to compare. Earlier batches remain below for resume and
                review.
              </p>
            </div>
            <Badge tone="brand">
              {formatBatchTimestamp(latestBatch.created_at)}
            </Badge>
          </div>

          <CardGrid className="character-stage__grid" columns={2}>
            {latestBatchCharacterSheets.map((characterSheet) => {
              const selected = characterSheet.id === selectedCharacterSheetId
              const isPending = pendingCharacterSheetId === characterSheet.id

              return (
                <SelectionCard
                  key={characterSheet.id}
                  className="character-stage__card"
                  description={readCharacterSummary(characterSheet)}
                  eyebrow={`Sheet ${String(characterSheet.candidate_index ?? characterSheet.revision_number).padStart(2, '0')}`}
                  footer={
                    <div className="cta-row">
                      <Button
                        disabled={selected || isPending}
                        onClick={() => {
                          void handleCharacterSheetSelection(characterSheet)
                        }}
                        tone={selected ? 'ghost' : 'primary'}
                      >
                        {selected
                          ? 'Selected sheet'
                          : isPending
                            ? 'Saving sheet...'
                            : 'Choose cast'}
                      </Button>
                    </div>
                  }
                  meta={
                    <div className="workspace-stage-detail__badges">
                      {characterSheet.generation_key != null ? (
                        <Badge tone="neutral">
                          {characterSheet.generation_key}
                        </Badge>
                      ) : null}
                      {characterSheet.refinement_instructions != null ? (
                        <Badge tone="accent">
                          {characterSheet.change_impact === 'minor'
                            ? 'Refined · Minor'
                            : 'Refined'}
                        </Badge>
                      ) : null}
                      {selected ? <Badge tone="success">Selected</Badge> : null}
                    </div>
                  }
                  selected={selected}
                  title={
                    characterSheet.title ??
                    characterSheet.protagonist_name ??
                    'Untitled character sheet'
                  }
                >
                  <div className="character-stage__card-copy">
                    <p>
                      <strong>Lead signal.</strong>{' '}
                      {readLeadSignal(characterSheet)}
                    </p>
                    <p>
                      <strong>Supporting cast.</strong>{' '}
                      {readSupportingCastSignal(characterSheet)}
                    </p>
                    <p>
                      <strong>Bedtime notes.</strong>{' '}
                      {characterSheet.bedtime_safety_notes ??
                        characterSheet.bedtime_notes ??
                        'The bedtime-safety posture will appear here once the sheet is generated.'}
                    </p>
                  </div>
                </SelectionCard>
              )
            })}
          </CardGrid>
        </section>
      ) : null}

      {characterSheetBatches.length > 1 ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Earlier character batches</h3>
              <p>
                Older generations stay available so the user can revisit prior
                cast directions instead of losing them after each refresh.
              </p>
            </div>
            <Badge tone="neutral">
              {characterSheetBatches.length - 1} earlier batch
              {characterSheetBatches.length === 2 ? '' : 'es'}
            </Badge>
          </div>

          <div className="character-stage__history">
            {characterSheetBatches.slice(1).map((batch) => (
              <SummaryPanel
                key={batch.generation_key}
                description={buildBatchSummary(batch)}
                label="Earlier batch"
                title={
                  batch.generation_kind === 'refinement'
                    ? '1 refined option'
                    : `${batch.candidate_count} saved options`
                }
              >
                <div className="character-stage__history-titles">
                  {batch.character_sheets.map((characterSheet) => (
                    <span key={characterSheet.id}>
                      {characterSheet.title ??
                        characterSheet.protagonist_name ??
                        'Untitled character sheet'}
                    </span>
                  ))}
                </div>
              </SummaryPanel>
            ))}
          </div>
        </section>
      ) : null}

      <PlanRevisionHistoryPanel
        disabled={isGenerating || isRefining}
        onRestorePlanRevision={onRestorePlanRevision}
        snapshot={snapshot}
      />
    </section>
  )
}
