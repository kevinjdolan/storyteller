import { useEffect, useMemo, useState } from 'react'
import type {
  BeatSheetView,
  SessionBeatSheetGenerationResponse,
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
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'
import { getWorkflowStageLabel } from './workflowStages.ts'

type BeatSheetStageProps = {
  onEditBeatSheet: (input: {
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
    origin: string
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  onGenerateBeatSheet: (input: {
    guidance?: string | null
    focusBeats?: string[]
    bedtimeGoal?: string | null
    origin: string
  }) => Promise<SessionBeatSheetGenerationResponse>
  onPreviewStage: (stageId: 'characters' | 'story_setup') => void
  onRefineBeatSheet: (selection: {
    beatSheetId?: string | null
    revisionNumber?: number | null
    instructions: string
    beatNames?: string[]
    bedtimeGoal?: string | null
    origin: string
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  onSelectBeatSheet: (selection: {
    beatSheetId?: string | null
    revisionNumber?: number | null
    origin: string
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

type BeatEditorBeatDraft = {
  summary: string
  emotionalIntent: string
  bedtimeSofteningNote: string
}

type BeatEditorDraft = {
  summary: string
  bedtimeGoal: string
  bedtimeNotes: string
  beats: Record<string, BeatEditorBeatDraft>
}

const revisionTimestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function formatRevisionTimestamp(value: string) {
  return `Saved ${revisionTimestampFormatter.format(new Date(value))}`
}

function humanizeBeatName(value: string) {
  return value
    .replace(/[_-]+/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function formatHumanizedList(values: string[]) {
  if (values.length === 0) {
    return ''
  }

  if (values.length === 1) {
    return values[0]
  }

  if (values.length === 2) {
    return `${values[0]} and ${values[1]}`
  }

  return `${values.slice(0, -1).join(', ')}, and ${values.at(-1)}`
}

function parseBeatNames(value: string) {
  return value
    .split(/[\n,]/g)
    .map((entry) => entry.trim())
    .filter(Boolean)
}

function readBeatSelectionCopy(beatSheet: {
  summary?: string | null
  selection_rationale?: string | null
}) {
  return (
    beatSheet.selection_rationale ??
    beatSheet.summary ??
    'The accepted Save-the-Cat revision will appear here once one is chosen.'
  )
}

function buildBeatRevisionSummary(beatSheet: BeatSheetView) {
  if (
    beatSheet.generation_kind === 'refinement' &&
    beatSheet.source_beat_sheet_revision_number != null &&
    beatSheet.refinement_instructions != null
  ) {
    return `Refined from revision ${beatSheet.source_beat_sheet_revision_number}. ${beatSheet.refinement_instructions}`
  }

  if (
    beatSheet.generation_kind === 'refinement' &&
    beatSheet.source_beat_sheet_revision_number != null
  ) {
    return `Refined from revision ${beatSheet.source_beat_sheet_revision_number}.`
  }

  if (beatSheet.updated_at != null) {
    return formatRevisionTimestamp(beatSheet.updated_at)
  }

  return 'Fresh Save-the-Cat outline ready for review.'
}

function buildFocusBeatSummary(beatSheet: BeatSheetView) {
  if (beatSheet.focus_beats.length === 0) {
    return 'No focus beats were called out for this revision.'
  }

  return beatSheet.focus_beats.map(humanizeBeatName).join(', ')
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  snapshot: SessionSnapshot,
  beatSheetRevisions: BeatSheetView[],
) {
  if (selectedStage.availability === 'locked') {
    return {
      body: 'Accept a character sheet first. The beat stage stays visible, but generation is disabled until the cast is durable.',
      title: 'Character selection comes first',
      tone: 'warning' as const,
    }
  }

  if (
    selectedStage.availability === 'revisitable' &&
    snapshot.selected_beat_sheet
  ) {
    return {
      body: 'Generating or refining beats reopens downstream planning. The accepted revision stays visible while you compare new structures.',
      title: 'New beat revisions refresh later work',
      tone: 'warning' as const,
    }
  }

  if (beatSheetRevisions.length > 0) {
    return {
      body: 'Keep the structure high level. Each beat should anchor the emotional turn, show bedtime softening, and preserve the full Save-the-Cat order.',
      title: 'Compare the arc before accepting it',
      tone: 'success' as const,
    }
  }

  return {
    body: 'Generate the first beat-sheet revision from the selected pitch and character sheet, then review the full fifteen-beat progression before moving on.',
    title: 'Start with a full Save-the-Cat outline',
    tone: 'info' as const,
  }
}

function buildBeatEditorDraft(beatSheet: BeatSheetView): BeatEditorDraft {
  return {
    summary: beatSheet.summary ?? '',
    bedtimeGoal: beatSheet.bedtime_goal ?? '',
    bedtimeNotes: beatSheet.bedtime_notes ?? '',
    beats: Object.fromEntries(
      beatSheet.beats.map((beat) => [
        beat.key,
        {
          summary: beat.summary,
          emotionalIntent: beat.emotional_intent ?? '',
          bedtimeSofteningNote: beat.bedtime_softening_note ?? '',
        },
      ]),
    ),
  }
}

function readPreferredEditorBeatKey(beatSheet: BeatSheetView | null) {
  if (beatSheet == null || beatSheet.beats.length === 0) {
    return ''
  }

  const preferredFocusBeat = beatSheet.focus_beats.find((focusBeat) =>
    beatSheet.beats.some(
      (beat) =>
        beat.key.toLowerCase() === focusBeat.toLowerCase() ||
        beat.label.toLowerCase() === focusBeat.toLowerCase(),
    ),
  )
  if (preferredFocusBeat != null) {
    const matchingBeat = beatSheet.beats.find(
      (beat) =>
        beat.key.toLowerCase() === preferredFocusBeat.toLowerCase() ||
        beat.label.toLowerCase() === preferredFocusBeat.toLowerCase(),
    )
    if (matchingBeat != null) {
      return matchingBeat.key
    }
  }

  return beatSheet.beats[0]?.key ?? ''
}

function countBeatEditorChanges(
  beatSheet: BeatSheetView | null,
  draft: BeatEditorDraft | null,
) {
  if (beatSheet == null || draft == null) {
    return 0
  }

  let changeCount = 0
  if ((beatSheet.summary ?? '') !== draft.summary) {
    changeCount += 1
  }
  if ((beatSheet.bedtime_notes ?? '') !== draft.bedtimeNotes) {
    changeCount += 1
  }
  if ((beatSheet.bedtime_goal ?? '') !== draft.bedtimeGoal) {
    changeCount += 1
  }

  for (const beat of beatSheet.beats) {
    const beatDraft = draft.beats[beat.key]
    if (beatDraft == null) {
      continue
    }
    if (beatDraft.summary !== beat.summary) {
      changeCount += 1
    }
    if (beatDraft.emotionalIntent !== (beat.emotional_intent ?? '')) {
      changeCount += 1
    }
    if (
      beatDraft.bedtimeSofteningNote !== (beat.bedtime_softening_note ?? '')
    ) {
      changeCount += 1
    }
  }

  return changeCount
}

function buildBeatEditorUpdateRequest(
  beatSheet: BeatSheetView,
  draft: BeatEditorDraft,
) {
  const beatUpdates: Array<{
    key: string
    summary?: string | null
    emotionalIntent?: string | null
    bedtimeSofteningNote?: string | null
  }> = []

  const summary = draft.summary.trim()
  const bedtimeNotes = draft.bedtimeNotes.trim()
  const bedtimeGoal = draft.bedtimeGoal.trim()

  if (draft.summary !== (beatSheet.summary ?? '') && summary.length === 0) {
    return {
      error: 'Arc summary cannot be cleared from the beat editor.',
    }
  }
  if (
    draft.bedtimeNotes !== (beatSheet.bedtime_notes ?? '') &&
    bedtimeNotes.length === 0
  ) {
    return {
      error: 'Overall bedtime notes cannot be cleared from the beat editor.',
    }
  }
  if (
    draft.bedtimeGoal !== (beatSheet.bedtime_goal ?? '') &&
    bedtimeGoal.length === 0
  ) {
    return {
      error: 'Saved bedtime goal cannot be cleared from the beat editor.',
    }
  }

  for (const beat of beatSheet.beats) {
    const beatDraft = draft.beats[beat.key]
    if (beatDraft == null) {
      continue
    }

    const nextSummary = beatDraft.summary.trim()
    const nextEmotionalIntent = beatDraft.emotionalIntent.trim()
    const nextBedtimeSofteningNote = beatDraft.bedtimeSofteningNote.trim()

    if (beatDraft.summary !== beat.summary && nextSummary.length === 0) {
      return {
        error: `${beat.label} summary cannot be cleared from the beat editor.`,
      }
    }
    if (
      beatDraft.emotionalIntent !== (beat.emotional_intent ?? '') &&
      nextEmotionalIntent.length === 0
    ) {
      return {
        error: `${beat.label} emotional intent cannot be cleared from the beat editor.`,
      }
    }
    if (
      beatDraft.bedtimeSofteningNote !== (beat.bedtime_softening_note ?? '') &&
      nextBedtimeSofteningNote.length === 0
    ) {
      return {
        error: `${beat.label} bedtime softening note cannot be cleared from the beat editor.`,
      }
    }

    const beatUpdate: {
      key: string
      summary?: string | null
      emotionalIntent?: string | null
      bedtimeSofteningNote?: string | null
    } = {
      key: beat.key,
    }

    if (beatDraft.summary !== beat.summary) {
      beatUpdate.summary = nextSummary
    }
    if (beatDraft.emotionalIntent !== (beat.emotional_intent ?? '')) {
      beatUpdate.emotionalIntent = nextEmotionalIntent
    }
    if (
      beatDraft.bedtimeSofteningNote !== (beat.bedtime_softening_note ?? '')
    ) {
      beatUpdate.bedtimeSofteningNote = nextBedtimeSofteningNote
    }

    if (
      beatUpdate.summary != null ||
      beatUpdate.emotionalIntent != null ||
      beatUpdate.bedtimeSofteningNote != null
    ) {
      beatUpdates.push(beatUpdate)
    }
  }

  const request = {
    summary:
      draft.summary !== (beatSheet.summary ?? '') ? summary : (null as string | null),
    bedtimeNotes:
      draft.bedtimeNotes !== (beatSheet.bedtime_notes ?? '')
        ? bedtimeNotes
        : (null as string | null),
    bedtimeGoal:
      draft.bedtimeGoal !== (beatSheet.bedtime_goal ?? '')
        ? bedtimeGoal
        : (null as string | null),
    beatUpdates,
  }

  if (
    request.summary == null &&
    request.bedtimeNotes == null &&
    request.bedtimeGoal == null &&
    beatUpdates.length === 0
  ) {
    return {
      error: 'No beat-sheet changes are waiting to be saved.',
    }
  }

  return {
    request,
  }
}

function buildEditHistoryFocusCopy(entry: {
  beat_keys?: string[] | null
  changed_fields?: string[] | null
}) {
  const beatKeys = entry.beat_keys ?? []
  if (beatKeys.length > 0) {
    return `Focus beats: ${formatHumanizedList(
      beatKeys.map(humanizeBeatName),
    )}.`
  }

  const changedFields = entry.changed_fields ?? []
  if (changedFields.includes('summary') || changedFields.includes('bedtime_notes')) {
    return 'This edit changed the overall arc framing for the revision.'
  }

  return 'This edit stayed at the revision level without targeting a named beat.'
}

export function BeatSheetStage({
  onEditBeatSheet,
  onGenerateBeatSheet,
  onPreviewStage,
  onRefineBeatSheet,
  onSelectBeatSheet,
  selectedStage,
  snapshot,
}: BeatSheetStageProps) {
  const beatSheetRevisions = useMemo(
    () => snapshot.beat_sheet_revisions ?? [],
    [snapshot.beat_sheet_revisions],
  )
  const latestBeatSheet = beatSheetRevisions[0] ?? null
  const selectedBeatSheetId = snapshot.selected_beat_sheet?.id ?? null
  const revisionHelp = buildRevisionHelp(
    selectedStage,
    snapshot,
    beatSheetRevisions,
  )
  const [guidance, setGuidance] = useState('')
  const [generationFocusBeats, setGenerationFocusBeats] = useState('')
  const [generationBedtimeGoal, setGenerationBedtimeGoal] = useState('')
  const [generationError, setGenerationError] = useState<string | null>(null)
  const [refinementInstructions, setRefinementInstructions] = useState('')
  const [refinementFocusBeats, setRefinementFocusBeats] = useState('')
  const [refinementBedtimeGoal, setRefinementBedtimeGoal] = useState('')
  const [refinementError, setRefinementError] = useState<string | null>(null)
  const [selectionError, setSelectionError] = useState<string | null>(null)
  const [editorError, setEditorError] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isRefining, setIsRefining] = useState(false)
  const [isSavingEditor, setIsSavingEditor] = useState(false)
  const [pendingBeatSheetId, setPendingBeatSheetId] = useState<string | null>(
    null,
  )
  const [refinementBaseBeatSheetId, setRefinementBaseBeatSheetId] = useState<
    string | null
  >(selectedBeatSheetId ?? latestBeatSheet?.id ?? null)
  const [inspectedBeatSheetId, setInspectedBeatSheetId] = useState<
    string | null
  >(selectedBeatSheetId ?? latestBeatSheet?.id ?? null)
  const [editorBeatKey, setEditorBeatKey] = useState('')
  const [editorDraft, setEditorDraft] = useState<BeatEditorDraft | null>(null)

  const refinementBaseBeatSheet =
    beatSheetRevisions.find(
      (beatSheet) => beatSheet.id === refinementBaseBeatSheetId,
    ) ?? null
  const inspectedBeatSheet =
    beatSheetRevisions.find(
      (beatSheet) => beatSheet.id === inspectedBeatSheetId,
    ) ??
    snapshot.selected_beat_sheet ??
    latestBeatSheet
  const editorBeat =
    inspectedBeatSheet?.beats.find((beat) => beat.key === editorBeatKey) ??
    inspectedBeatSheet?.beats[0] ??
    null
  const editorBeatDraft =
    editorBeat != null && editorDraft != null
      ? editorDraft.beats[editorBeat.key] ?? null
      : null
  const editHistory = inspectedBeatSheet?.edit_history ?? []
  const editorChangeCount = countBeatEditorChanges(inspectedBeatSheet, editorDraft)
  const editorDirty = editorChangeCount > 0
  const downstreamEditImpactLabels = selectedStage.invalidatesOnEdit.map(
    getWorkflowStageLabel,
  )

  useEffect(() => {
    if (
      refinementBaseBeatSheetId != null &&
      beatSheetRevisions.some(
        (beatSheet) => beatSheet.id === refinementBaseBeatSheetId,
      )
    ) {
      return
    }

    setRefinementBaseBeatSheetId(
      selectedBeatSheetId ?? latestBeatSheet?.id ?? null,
    )
  }, [
    beatSheetRevisions,
    latestBeatSheet?.id,
    refinementBaseBeatSheetId,
    selectedBeatSheetId,
  ])

  useEffect(() => {
    if (
      inspectedBeatSheetId != null &&
      beatSheetRevisions.some(
        (beatSheet) => beatSheet.id === inspectedBeatSheetId,
      )
    ) {
      return
    }

    setInspectedBeatSheetId(selectedBeatSheetId ?? latestBeatSheet?.id ?? null)
  }, [
    beatSheetRevisions,
    inspectedBeatSheetId,
    latestBeatSheet?.id,
    selectedBeatSheetId,
  ])

  useEffect(() => {
    if (inspectedBeatSheet == null) {
      setEditorDraft(null)
      setEditorBeatKey('')
      setEditorError(null)
      return
    }

    setEditorDraft(buildBeatEditorDraft(inspectedBeatSheet))
    setEditorBeatKey(readPreferredEditorBeatKey(inspectedBeatSheet))
    setEditorError(null)
  }, [inspectedBeatSheet])

  async function handleGenerateBeatSheet() {
    if (selectedStage.availability === 'locked' || isGenerating) {
      return
    }

    setGenerationError(null)
    setIsGenerating(true)

    try {
      await onGenerateBeatSheet({
        guidance: guidance.trim() || null,
        focusBeats: parseBeatNames(generationFocusBeats),
        bedtimeGoal: generationBedtimeGoal.trim() || null,
        origin: 'workspace',
      })
      setGuidance('')
      setGenerationFocusBeats('')
      setGenerationBedtimeGoal('')
    } catch (error) {
      setGenerationError(
        error instanceof Error
          ? error.message
          : 'The beat-sheet revision could not be generated right now.',
      )
    } finally {
      setIsGenerating(false)
    }
  }

  async function handleBeatSheetSelection(beatSheet: BeatSheetView) {
    setPendingBeatSheetId(beatSheet.id)
    setSelectionError(null)

    try {
      await onSelectBeatSheet({
        beatSheetId: beatSheet.id,
        revisionNumber: beatSheet.revision_number,
        origin: 'workspace',
      })
    } catch (error) {
      setSelectionError(
        error instanceof Error
          ? error.message
          : 'The selected beat sheet could not be saved right now.',
      )
    } finally {
      setPendingBeatSheetId(null)
    }
  }

  async function handleBeatSheetRefinement() {
    if (
      selectedStage.availability === 'locked' ||
      isRefining ||
      refinementBaseBeatSheet == null ||
      refinementInstructions.trim().length === 0
    ) {
      return
    }

    setRefinementError(null)
    setIsRefining(true)

    try {
      await onRefineBeatSheet({
        beatSheetId: refinementBaseBeatSheet.id,
        revisionNumber: refinementBaseBeatSheet.revision_number,
        instructions: refinementInstructions.trim(),
        beatNames: parseBeatNames(refinementFocusBeats),
        bedtimeGoal: refinementBedtimeGoal.trim() || null,
        origin: 'workspace',
      })
      setRefinementInstructions('')
      setRefinementFocusBeats('')
      setRefinementBedtimeGoal('')
    } catch (error) {
      setRefinementError(
        error instanceof Error
          ? error.message
          : 'The beat-sheet refinement could not be saved right now.',
      )
    } finally {
      setIsRefining(false)
    }
  }

  async function handleBeatSheetEditSave() {
    if (inspectedBeatSheet == null || editorDraft == null || isSavingEditor) {
      return
    }

    const nextUpdate = buildBeatEditorUpdateRequest(inspectedBeatSheet, editorDraft)
    if ('error' in nextUpdate && nextUpdate.error != null) {
      setEditorError(nextUpdate.error)
      return
    }

    setEditorError(null)
    setIsSavingEditor(true)

    try {
      await onEditBeatSheet({
        beatSheetId: inspectedBeatSheet.id,
        revisionNumber: inspectedBeatSheet.revision_number,
        summary: nextUpdate.request.summary,
        bedtimeNotes: nextUpdate.request.bedtimeNotes,
        bedtimeGoal: nextUpdate.request.bedtimeGoal,
        beatUpdates: nextUpdate.request.beatUpdates,
        origin: 'workspace',
      })
    } catch (error) {
      setEditorError(
        error instanceof Error
          ? error.message
          : 'The beat-sheet edit could not be saved right now.',
      )
    } finally {
      setIsSavingEditor(false)
    }
  }

  function resetBeatEditor() {
    if (inspectedBeatSheet == null) {
      return
    }

    setEditorDraft(buildBeatEditorDraft(inspectedBeatSheet))
    setEditorBeatKey(readPreferredEditorBeatKey(inspectedBeatSheet))
    setEditorError(null)
  }

  const editorDisabled =
    selectedStage.availability === 'locked' ||
    inspectedBeatSheet == null ||
    editorDraft == null ||
    isSavingEditor

  return (
    <section aria-label="Beat sheet stage" className="workspace-stage-panel">
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            snapshot.selected_beat_sheet != null
              ? readBeatSelectionCopy(snapshot.selected_beat_sheet)
              : 'No beat revision is accepted yet. Generate or refine one, then choose the version that gives composition the clearest bedtime-safe arc.'
          }
          label="Current selection"
          title={
            snapshot.selected_beat_sheet != null
              ? `Revision ${snapshot.selected_beat_sheet.revision_number}`
              : 'Beat sheet pending'
          }
          tone={snapshot.selected_beat_sheet != null ? 'accent' : 'default'}
        />

        <SummaryPanel
          description={
            latestBeatSheet != null
              ? buildBeatRevisionSummary(latestBeatSheet)
              : 'The newest durable beat revision will appear here once generation runs.'
          }
          label="Latest revision"
          title={
            latestBeatSheet != null
              ? latestBeatSheet.generation_kind === 'refinement'
                ? `Revision ${latestBeatSheet.revision_number} refined`
                : `Revision ${latestBeatSheet.revision_number} ready`
              : 'No beat revision yet'
          }
        >
          {latestBeatSheet != null ? (
            <div className="workspace-stage-detail__badges">
              <Badge tone="brand">{latestBeatSheet.beats.length} beats</Badge>
              {latestBeatSheet.generation_kind === 'refinement' ? (
                <Badge tone="accent">Refinement</Badge>
              ) : null}
              {latestBeatSheet.focus_beats.length > 0 ? (
                <Badge tone="neutral">
                  {latestBeatSheet.focus_beats.length} focus beat
                  {latestBeatSheet.focus_beats.length === 1 ? '' : 's'}
                </Badge>
              ) : null}
              {(latestBeatSheet.edit_history?.length ?? 0) > 0 ? (
                <Badge tone="warning">
                  {latestBeatSheet.edit_history?.length} edit
                  {latestBeatSheet.edit_history?.length === 1 ? '' : 's'}
                </Badge>
              ) : null}
            </div>
          ) : null}
        </SummaryPanel>

        <SummaryPanel
          description={
            snapshot.selected_beat_sheet != null
              ? 'Story setup can now inherit a durable structure for pacing, runtime, and chapter planning.'
              : 'Accepting a beat revision completes this stage and unlocks story setup.'
          }
          label="Next step"
          title={
            snapshot.selected_beat_sheet != null
              ? 'Story setup is ready next'
              : 'Choose one revision to continue'
          }
        >
          <div className="cta-row">
            <Button
              onClick={() => {
                onPreviewStage(
                  snapshot.selected_beat_sheet != null
                    ? 'story_setup'
                    : 'characters',
                )
              }}
              tone="ghost"
            >
              {snapshot.selected_beat_sheet != null
                ? 'Preview story setup'
                : 'Revisit characters'}
            </Button>
          </div>
        </SummaryPanel>
      </CardGrid>

      <InlineHelp title={revisionHelp.title} tone={revisionHelp.tone}>
        {revisionHelp.body}
      </InlineHelp>

      {generationError != null ? (
        <InlineHelp title="Beat generation failed" tone="warning">
          {generationError}
        </InlineHelp>
      ) : null}

      {selectionError != null ? (
        <InlineHelp title="Beat selection failed" tone="warning">
          {selectionError}
        </InlineHelp>
      ) : null}

      {refinementError != null ? (
        <InlineHelp title="Beat refinement failed" tone="warning">
          {refinementError}
        </InlineHelp>
      ) : null}

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Generate a beat sheet revision</h3>
            <p>
              Create or refresh the Save-the-Cat outline from the accepted pitch
              and character sheet, keeping the structure high level and
              bedtime-safe.
            </p>
          </div>
          <Badge tone={latestBeatSheet != null ? 'success' : 'warning'}>
            {latestBeatSheet != null ? 'Revision ready' : 'Generation required'}
          </Badge>
        </div>

        <CardGrid className="beat-stage__controls" columns={2}>
          <TextArea
            description="Optional guidance can steer the next revision. For example: soften the midpoint, make the catalyst more luminous, or keep the finale quieter."
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Optional beat guidance"
            onChange={(event) => {
              setGuidance(event.currentTarget.value)
            }}
            rows={4}
            value={guidance}
          />

          <TextArea
            description="Optional. Focus specific beats by key or label. Separate entries with commas or line breaks."
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Focus beats"
            onChange={(event) => {
              setGenerationFocusBeats(event.currentTarget.value)
            }}
            rows={4}
            value={generationFocusBeats}
          />

          <TextArea
            description="Optional. Capture the bedtime landing you want the outline to protect all the way through the final image."
            disabled={selectedStage.availability === 'locked' || isGenerating}
            label="Bedtime goal"
            onChange={(event) => {
              setGenerationBedtimeGoal(event.currentTarget.value)
            }}
            rows={3}
            value={generationBedtimeGoal}
          />
        </CardGrid>

        <div className="cta-row">
          <Button
            disabled={selectedStage.availability === 'locked' || isGenerating}
            onClick={() => {
              void handleGenerateBeatSheet()
            }}
            tone="primary"
          >
            {isGenerating
              ? 'Generating beat sheet...'
              : latestBeatSheet != null
                ? 'Regenerate beat sheet'
                : 'Generate beat sheet'}
          </Button>
          <Button
            onClick={() => {
              onPreviewStage('characters')
            }}
            tone="ghost"
          >
            Revisit characters
          </Button>
        </div>
      </section>

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Refine a saved beat revision</h3>
            <p>
              Pick one saved revision, describe the structural change, and save
              the result as a new durable option without losing earlier beats.
            </p>
          </div>
          <Badge tone={refinementBaseBeatSheet != null ? 'brand' : 'warning'}>
            {refinementBaseBeatSheet != null
              ? 'Ready to refine'
              : 'Generate a base revision'}
          </Badge>
        </div>

        <CardGrid className="beat-stage__controls" columns={2}>
          <SelectField
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Beat revision to refine"
            onChange={(event) => {
              setRefinementBaseBeatSheetId(event.currentTarget.value)
            }}
            options={
              beatSheetRevisions.length > 0
                ? beatSheetRevisions.map((beatSheet) => ({
                    label: `Revision ${beatSheet.revision_number} · ${beatSheet.summary ?? 'Untitled beat sheet'}`,
                    value: beatSheet.id,
                  }))
                : [
                    {
                      disabled: true,
                      label: 'No saved beat revisions',
                      value: '',
                    },
                  ]
            }
            value={refinementBaseBeatSheetId ?? ''}
          />

          <TextArea
            description="Describe the structural change to make. For example: soften all-is-lost, add more wonder to the midpoint, or make the finale land more sleepily."
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Refinement instructions"
            onChange={(event) => {
              setRefinementInstructions(event.currentTarget.value)
            }}
            rows={4}
            value={refinementInstructions}
          />

          <TextArea
            description="Optional. Focus the refinement on specific beats. Separate entries with commas or line breaks."
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Focus beats"
            onChange={(event) => {
              setRefinementFocusBeats(event.currentTarget.value)
            }}
            rows={3}
            value={refinementFocusBeats}
          />

          <TextArea
            description="Optional. Save the bedtime outcome this revision should protect, especially across the low points and the final image."
            disabled={selectedStage.availability === 'locked' || isRefining}
            label="Bedtime goal"
            onChange={(event) => {
              setRefinementBedtimeGoal(event.currentTarget.value)
            }}
            rows={3}
            value={refinementBedtimeGoal}
          />
        </CardGrid>

        <div className="cta-row">
          <Button
            disabled={
              selectedStage.availability === 'locked' ||
              isRefining ||
              refinementBaseBeatSheet == null ||
              refinementInstructions.trim().length === 0
            }
            onClick={() => {
              void handleBeatSheetRefinement()
            }}
            tone="primary"
          >
            {isRefining ? 'Refining beat sheet...' : 'Refine beat sheet'}
          </Button>
          {refinementBaseBeatSheet != null ? (
            <Badge tone="neutral">
              Revision {refinementBaseBeatSheet.revision_number}
            </Badge>
          ) : null}
        </div>
      </section>

      {beatSheetRevisions.length === 0 ? (
        <EmptyStateBlock
          action={
            <Button
              disabled={selectedStage.availability === 'locked' || isGenerating}
              onClick={() => {
                void handleGenerateBeatSheet()
              }}
              tone="primary"
            >
              Generate the first revision
            </Button>
          }
          description="The beat stage keeps every revision so the user can revisit earlier structures before composition begins."
          title="No beat-sheet revisions have been generated yet"
        />
      ) : null}

      {beatSheetRevisions.length > 0 ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Saved beat revisions</h3>
              <p>
                Compare the summary, focus beats, and bedtime landing of each
                saved revision before accepting one for downstream planning.
              </p>
            </div>
            <Badge tone="brand">
              {beatSheetRevisions.length} revision
              {beatSheetRevisions.length === 1 ? '' : 's'}
            </Badge>
          </div>

          <CardGrid className="beat-stage__grid" columns={2}>
            {beatSheetRevisions.map((beatSheet) => {
              const selected = beatSheet.id === selectedBeatSheetId
              const isPending = pendingBeatSheetId === beatSheet.id
              const isPreviewed = beatSheet.id === inspectedBeatSheet?.id

              return (
                <SelectionCard
                  key={beatSheet.id}
                  className="beat-stage__card"
                  description={buildBeatRevisionSummary(beatSheet)}
                  eyebrow={`Revision ${String(beatSheet.revision_number).padStart(2, '0')}`}
                  footer={
                    <div className="cta-row">
                      <Button
                        onClick={() => {
                          setInspectedBeatSheetId(beatSheet.id)
                        }}
                        tone="ghost"
                      >
                        {isPreviewed ? 'Previewing outline' : 'Preview outline'}
                      </Button>
                      <Button
                        disabled={selected || isPending}
                        onClick={() => {
                          void handleBeatSheetSelection(beatSheet)
                        }}
                        tone={selected ? 'ghost' : 'primary'}
                      >
                        {selected
                          ? 'Accepted revision'
                          : isPending
                            ? 'Saving revision...'
                            : 'Accept beat sheet'}
                      </Button>
                    </div>
                  }
                  meta={
                    <div className="workspace-stage-detail__badges">
                      <Badge tone="neutral">
                        {beatSheet.beats.length} beats
                      </Badge>
                      {beatSheet.generation_kind === 'refinement' ? (
                        <Badge tone="accent">Refined</Badge>
                      ) : null}
                      {(beatSheet.edit_history?.length ?? 0) > 0 ? (
                        <Badge tone="warning">
                          {beatSheet.edit_history?.length} edit
                          {beatSheet.edit_history?.length === 1 ? '' : 's'}
                        </Badge>
                      ) : null}
                      {isPreviewed ? (
                        <Badge tone="brand">Previewed</Badge>
                      ) : null}
                      {selected ? <Badge tone="success">Accepted</Badge> : null}
                    </div>
                  }
                  selected={selected}
                  title={
                    beatSheet.summary ??
                    `Beat sheet revision ${beatSheet.revision_number}`
                  }
                >
                  <div className="beat-stage__card-copy">
                    <p>
                      <strong>Bedtime notes.</strong>{' '}
                      {beatSheet.bedtime_notes ??
                        'Bedtime softening notes will appear here once the revision is generated.'}
                    </p>
                    <p>
                      <strong>Focus beats.</strong>{' '}
                      {buildFocusBeatSummary(beatSheet)}
                    </p>
                    <p>
                      <strong>Bedtime goal.</strong>{' '}
                      {beatSheet.bedtime_goal ??
                        'No explicit bedtime goal was saved for this revision.'}
                    </p>
                  </div>
                </SelectionCard>
              )
            })}
          </CardGrid>
        </section>
      ) : null}

      {inspectedBeatSheet != null ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Beat outline preview</h3>
              <p>
                This preview shows the full Save-the-Cat progression that
                composition will consume once the revision is accepted.
              </p>
            </div>
            <Badge tone="brand">
              Revision {inspectedBeatSheet.revision_number}
            </Badge>
          </div>

          <CardGrid className="workspace-stage-detail__cards" columns={3}>
            <SummaryPanel
              description={
                inspectedBeatSheet.summary ?? 'High-level beat summary pending.'
              }
              label="Arc summary"
              title={
                inspectedBeatSheet.generation_kind === 'refinement'
                  ? 'Refined revision'
                  : 'Generated revision'
              }
            />

            <SummaryPanel
              description={buildFocusBeatSummary(inspectedBeatSheet)}
              label="Focus beats"
              title={
                inspectedBeatSheet.focus_beats.length > 0
                  ? `${inspectedBeatSheet.focus_beats.length} focus beat${inspectedBeatSheet.focus_beats.length === 1 ? '' : 's'}`
                  : 'No focus beats'
              }
            />

            <SummaryPanel
              description={
                inspectedBeatSheet.bedtime_goal ??
                inspectedBeatSheet.bedtime_notes ??
                'No explicit bedtime goal was saved for this revision.'
              }
              label="Bedtime landing"
              title="Soft ending target"
            />
          </CardGrid>

          <ol className="beat-stage__outline">
            {inspectedBeatSheet.beats.map((beat) => (
              <li key={beat.key} className="beat-stage__outline-item">
                <div className="beat-stage__outline-header">
                  <Badge tone="neutral">
                    Beat {String(beat.order).padStart(2, '0')}
                  </Badge>
                  <h4>{beat.label}</h4>
                </div>
                <p>{beat.summary}</p>
                {beat.emotional_intent != null ? (
                  <p>
                    <strong>Emotional intent.</strong> {beat.emotional_intent}
                  </p>
                ) : null}
                {beat.bedtime_softening_note != null ? (
                  <p>
                    <strong>Bedtime softening.</strong>{' '}
                    {beat.bedtime_softening_note}
                  </p>
                ) : null}
              </li>
            ))}
          </ol>
        </section>
      ) : null}

      {inspectedBeatSheet != null &&
      editorDraft != null &&
      editorBeat != null &&
      editorBeatDraft != null ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Beat editor</h3>
              <p>
                Shape this saved revision directly. Saved edits stay in durable
                history and keep the outline feeling like a living plan instead
                of a frozen artifact.
              </p>
            </div>
            <Badge tone={editorDirty ? 'warning' : 'success'}>
              {editorDirty
                ? `${editorChangeCount} unsaved change${editorChangeCount === 1 ? '' : 's'}`
                : 'Saved'}
            </Badge>
          </div>

          <InlineHelp
            title={
              inspectedBeatSheet.id === selectedBeatSheetId
                ? 'Editing the accepted plan refreshes later work'
                : 'Editing an unaccepted revision stays local to this option'
            }
            tone={
              inspectedBeatSheet.id === selectedBeatSheetId ? 'warning' : 'info'
            }
          >
            {inspectedBeatSheet.id === selectedBeatSheetId
              ? `Saving this revision refreshes ${formatHumanizedList(downstreamEditImpactLabels)} when those stages already exist.`
              : 'This revision can be tuned safely before you accept it. Downstream planning will stay pointed at the currently accepted beat sheet.'}
          </InlineHelp>

          {editorError != null ? (
            <InlineHelp title="Beat edit failed" tone="warning">
              {editorError}
            </InlineHelp>
          ) : null}

          <CardGrid className="beat-stage__editor-grid" columns={2}>
            <SelectField
              disabled={editorDisabled}
              label="Beat to edit"
              onChange={(event) => {
                setEditorBeatKey(event.currentTarget.value)
              }}
              options={inspectedBeatSheet.beats.map((beat) => ({
                label: `Beat ${String(beat.order).padStart(2, '0')} · ${beat.label}`,
                value: beat.key,
              }))}
              value={editorBeat.key}
            />

            <TextArea
              description="Keep the one-line arc readable for the story setup and composition stages that inherit this plan."
              disabled={editorDisabled}
              label="Arc summary"
              onChange={(event) => {
                const nextValue = event.currentTarget.value
                setEditorDraft((currentDraft) =>
                  currentDraft == null
                    ? currentDraft
                    : {
                        ...currentDraft,
                        summary: nextValue,
                      },
                )
              }}
              rows={3}
              value={editorDraft.summary}
            />

            <TextArea
              description="These overall bedtime notes stay above any single beat and help later prompts protect the right landing."
              disabled={editorDisabled}
              label="Overall bedtime notes"
              onChange={(event) => {
                const nextValue = event.currentTarget.value
                setEditorDraft((currentDraft) =>
                  currentDraft == null
                    ? currentDraft
                    : {
                        ...currentDraft,
                        bedtimeNotes: nextValue,
                      },
                )
              }}
              rows={4}
              value={editorDraft.bedtimeNotes}
            />

            <TextArea
              description="This saved target should still describe the bedtime feeling you want the whole outline to protect."
              disabled={editorDisabled}
              label="Saved bedtime goal"
              onChange={(event) => {
                const nextValue = event.currentTarget.value
                setEditorDraft((currentDraft) =>
                  currentDraft == null
                    ? currentDraft
                    : {
                        ...currentDraft,
                        bedtimeGoal: nextValue,
                      },
                )
              }}
              rows={3}
              value={editorDraft.bedtimeGoal}
            />

            <TextArea
              description={`Beat ${String(editorBeat.order).padStart(2, '0')} should stay concise, visual, and easy for later writing prompts to inherit.`}
              disabled={editorDisabled}
              label="Beat summary"
              onChange={(event) => {
                const nextValue = event.currentTarget.value
                setEditorDraft((currentDraft) =>
                  currentDraft == null
                    ? currentDraft
                    : {
                        ...currentDraft,
                        beats: {
                          ...currentDraft.beats,
                          [editorBeat.key]: {
                            ...currentDraft.beats[editorBeat.key],
                            summary: nextValue,
                          },
                        },
                      },
                )
              }}
              rows={4}
              value={editorBeatDraft.summary}
            />

            <TextArea
              description="This describes the emotional turn that the composition stage should feel in the scene, not draft prose."
              disabled={editorDisabled}
              label="Emotional intent"
              onChange={(event) => {
                const nextValue = event.currentTarget.value
                setEditorDraft((currentDraft) =>
                  currentDraft == null
                    ? currentDraft
                    : {
                        ...currentDraft,
                        beats: {
                          ...currentDraft.beats,
                          [editorBeat.key]: {
                            ...currentDraft.beats[editorBeat.key],
                            emotionalIntent: nextValue,
                          },
                        },
                      },
                )
              }}
              rows={3}
              value={editorBeatDraft.emotionalIntent}
            />

            <TextArea
              description="Use this note to keep pressure beats bedtime-safe and to give later prompts a concrete softening move."
              disabled={editorDisabled}
              label="Bedtime softening note"
              onChange={(event) => {
                const nextValue = event.currentTarget.value
                setEditorDraft((currentDraft) =>
                  currentDraft == null
                    ? currentDraft
                    : {
                        ...currentDraft,
                        beats: {
                          ...currentDraft.beats,
                          [editorBeat.key]: {
                            ...currentDraft.beats[editorBeat.key],
                            bedtimeSofteningNote: nextValue,
                          },
                        },
                      },
                )
              }}
              rows={3}
              value={editorBeatDraft.bedtimeSofteningNote}
            />
          </CardGrid>

          <div className="cta-row">
            <Button
              disabled={editorDisabled || !editorDirty}
              onClick={() => {
                void handleBeatSheetEditSave()
              }}
              tone="primary"
            >
              {isSavingEditor ? 'Saving beat changes...' : 'Save beat changes'}
            </Button>
            <Button
              disabled={editorDisabled || !editorDirty}
              onClick={() => {
                resetBeatEditor()
              }}
              tone="ghost"
            >
              Reset editor
            </Button>
            <Badge tone="neutral">{editorBeat.label}</Badge>
            {inspectedBeatSheet.id === selectedBeatSheetId ? (
              <Badge tone="accent">Accepted revision</Badge>
            ) : (
              <Badge tone="neutral">Unaccepted revision</Badge>
            )}
          </div>
        </section>
      ) : null}

      {inspectedBeatSheet != null ? (
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Change tracking</h3>
              <p>
                Generated revisions keep the broader refinement history, while
                this log shows direct edits made to the currently previewed
                revision.
              </p>
            </div>
            <Badge tone={editHistory.length > 0 ? 'brand' : 'neutral'}>
              {editHistory.length} edit{editHistory.length === 1 ? '' : 's'}
            </Badge>
          </div>

          {editHistory.length > 0 ? (
            <ol className="beat-stage__history">
              {editHistory.map((entry) => (
                <li key={entry.id} className="beat-stage__history-item">
                  <div className="beat-stage__history-header">
                    <div>
                      <p className="eyebrow">{formatRevisionTimestamp(entry.created_at)}</p>
                      <h4>{entry.summary_text}</h4>
                    </div>
                    <div className="workspace-stage-detail__badges">
                      <Badge tone="neutral">
                        {entry.origin === 'chat' ? 'Chat edit' : 'Workspace edit'}
                      </Badge>
                      {entry.material_change ? (
                        <Badge tone="warning">Material change</Badge>
                      ) : null}
                      {entry.refreshes_downstream ? (
                        <Badge tone="accent">Refreshes downstream</Badge>
                      ) : null}
                    </div>
                  </div>
                  <p>{buildEditHistoryFocusCopy(entry)}</p>
                </li>
              ))}
            </ol>
          ) : (
            <InlineHelp title="No direct edits yet" tone="info">
              Save beat changes here or refine through chat to build an audit
              trail on this revision.
            </InlineHelp>
          )}
        </section>
      ) : null}
    </section>
  )
}
