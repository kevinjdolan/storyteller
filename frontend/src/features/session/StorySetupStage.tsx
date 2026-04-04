import { useEffect, useState } from 'react'
import type {
  SessionHistoryEvent,
  SessionSnapshot,
  StoryOutlineCard,
} from '../../api/sessions.ts'
import {
  Badge,
  Button,
  TextArea,
  TextInput,
} from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  FormColumns,
  InlineHelp,
  NumberField,
  StickySummaryLayout,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import { PlanRevisionHistoryPanel } from './PlanRevisionHistoryPanel.tsx'
import {
  buildPlanningAssumptionsText,
  buildRuntimeHeuristicSummary,
  buildStructureHeuristicSummary,
  type HeuristicSuggestion,
  type PlanningFieldId,
} from './planningHeuristics.ts'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'
import {
  getWorkflowStageLabel,
  type WorkflowStageId,
} from './workflowStages.ts'

type StorySetupStageProps = {
  onPreviewStage: (stageId: 'beats' | 'composition') => void
  onSaveStorySetup: (input: {
    targetWordCount?: number | null
    targetRuntimeMinutes?: number | null
    chapterCount?: number | null
    approximateSceneCount?: number | null
    guidanceNotes?: string | null
    origin: string
    previewCurrentStage?: boolean
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  onSaveStoryOutline: (input: {
    outlineId?: string | null
    summary?: string | null
    cards: StoryOutlineCard[]
    regenerateCardKeys?: string[]
    origin: string
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  onRestorePlanRevision: (input: {
    origin: string
    revisionNumber: number
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

type StorySetupFormState = {
  targetWordCount: string
  targetRuntimeMinutes: string
  chapterCount: string
  approximateSceneCount: string
  guidanceNotes: string
}

type ParsedNumberField = {
  value: number | null
  error: string | null
}

type StoryOutlineEditorCardState = {
  cardKey: string
  cardType: StoryOutlineCard['card_type']
  position: number
  title: string
  purpose: string
  summary: string
  beatKeys: string[]
  beatLabels: string[]
  emotionalShift: string
  targetWordCount?: number | null
  targetRuntimeMinutes?: number | null
  targetSceneCount?: number | null
  toneDirection?: string | null
  bedtimeGuardrail?: string | null
  draftingBrief: string
}

type OutlineEditPreview = {
  changeImpact: 'minor' | 'major'
  changedCardKeys: string[]
  reordered: boolean
  summary: string
}

type HeuristicSuggestionCalloutProps = {
  disabled: boolean
  onApply: (suggestion: HeuristicSuggestion) => void
  suggestion: HeuristicSuggestion | null
}

const savedAtFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function normalizeText(value: string) {
  return value.trim()
}

function toNullableText(value: string) {
  const normalized = normalizeText(value)
  return normalized.length > 0 ? normalized : null
}

function formatNullableNumber(value: number | null | undefined) {
  return value != null ? String(value) : ''
}

function buildFormState(snapshot: SessionSnapshot): StorySetupFormState {
  return {
    targetWordCount: formatNullableNumber(
      snapshot.selected_story_setup?.target_word_count,
    ),
    targetRuntimeMinutes: formatNullableNumber(
      snapshot.selected_story_setup?.target_runtime_minutes,
    ),
    chapterCount: formatNullableNumber(
      snapshot.selected_story_setup?.chapter_count,
    ),
    approximateSceneCount: formatNullableNumber(
      snapshot.selected_story_setup?.approximate_scene_count,
    ),
    guidanceNotes: snapshot.selected_story_setup?.guidance_notes ?? '',
  }
}

function getOutlineCardLabel(
  card:
    | Pick<StoryOutlineCard, 'card_type' | 'position'>
    | Pick<StoryOutlineEditorCardState, 'cardType' | 'position'>,
) {
  const cardType = 'card_type' in card ? card.card_type : card.cardType

  return `${cardType === 'chapter' ? 'Chapter' : 'Scene'} ${card.position}`
}

function buildFallbackOutlinePurpose(card: StoryOutlineCard) {
  if (card.beat_labels.length > 1) {
    return `Bridge ${card.beat_labels[0]} into ${card.beat_labels.at(-1)} without losing the bedtime rhythm.`
  }

  if (card.beat_labels.length === 1) {
    return `Deliver the ${card.beat_labels[0]} turn clearly enough that composition can keep moving.`
  }

  return 'Clarify the main story turn this card needs to carry before composition begins.'
}

function getSelectedStoryOutline(snapshot: SessionSnapshot) {
  return (
    snapshot.selected_story_outline ??
    snapshot.story_outline_revisions?.[0] ??
    null
  )
}

function buildOutlineEditorState(
  snapshot: SessionSnapshot,
): StoryOutlineEditorCardState[] {
  return (getSelectedStoryOutline(snapshot)?.cards ?? []).map((card) => ({
    cardKey: card.card_key,
    cardType: card.card_type,
    position: card.position,
    title: card.title,
    purpose: card.purpose ?? buildFallbackOutlinePurpose(card),
    summary: card.summary,
    beatKeys: [...card.beat_keys],
    beatLabels: [...card.beat_labels],
    emotionalShift: card.emotional_shift,
    targetWordCount: card.target_word_count,
    targetRuntimeMinutes: card.target_runtime_minutes,
    targetSceneCount: card.target_scene_count,
    toneDirection: card.tone_direction ?? null,
    bedtimeGuardrail: card.bedtime_guardrail ?? null,
    draftingBrief: card.drafting_brief ?? '',
  }))
}

function buildOutlineComparableState(values: StoryOutlineEditorCardState[]) {
  return values.map((card) => ({
    cardKey: card.cardKey,
    cardType: card.cardType,
    position: card.position,
    title: normalizeText(card.title),
    purpose: normalizeText(card.purpose),
    summary: normalizeText(card.summary),
    beatKeys: [...card.beatKeys],
    beatLabels: [...card.beatLabels],
    emotionalShift: normalizeText(card.emotionalShift),
    targetWordCount: card.targetWordCount ?? null,
    targetRuntimeMinutes: card.targetRuntimeMinutes ?? null,
    targetSceneCount: card.targetSceneCount ?? null,
    toneDirection: card.toneDirection ?? null,
    bedtimeGuardrail: card.bedtimeGuardrail ?? null,
    draftingBrief: normalizeText(card.draftingBrief),
  }))
}

function storyOutlineStatesMatch(
  current: StoryOutlineEditorCardState[],
  saved: StoryOutlineEditorCardState[],
) {
  return (
    JSON.stringify(buildOutlineComparableState(current)) ===
    JSON.stringify(buildOutlineComparableState(saved))
  )
}

function moveOutlineDraftCard(
  cards: StoryOutlineEditorCardState[],
  cardKey: string,
  direction: -1 | 1,
) {
  const currentIndex = cards.findIndex((card) => card.cardKey === cardKey)
  const nextIndex = currentIndex + direction

  if (currentIndex < 0 || nextIndex < 0 || nextIndex >= cards.length) {
    return cards
  }

  const reordered = [...cards]
  const [movedCard] = reordered.splice(currentIndex, 1)
  reordered.splice(nextIndex, 0, movedCard)

  return reordered.map((card, index) => {
    const nextPosition = index + 1
    const prefix = card.cardType === 'chapter' ? 'Chapter' : 'Scene'

    return {
      ...card,
      position: nextPosition,
      title: card.title.replace(
        new RegExp(`^${prefix} \\d+:\\s+`),
        `${prefix} ${nextPosition}: `,
      ),
    }
  })
}

function buildOutlineEditPreview(
  draft: StoryOutlineEditorCardState[],
  saved: StoryOutlineEditorCardState[],
  invalidatedStages: ReadonlyArray<WorkflowStageId>,
): OutlineEditPreview | null {
  if (storyOutlineStatesMatch(draft, saved)) {
    return null
  }

  const savedByKey = new Map(saved.map((card) => [card.cardKey, card]))
  const changedCardKeys = draft
    .filter((card) => {
      const savedCard = savedByKey.get(card.cardKey)

      return (
        savedCard == null ||
        JSON.stringify(buildOutlineComparableState([card])[0]) !==
          JSON.stringify(buildOutlineComparableState([savedCard])[0])
      )
    })
    .map((card) => card.cardKey)
  const reordered =
    draft.map((card) => card.cardKey).join('|') !==
    saved.map((card) => card.cardKey).join('|')
  const invalidatedLabels = invalidatedStages.map(getWorkflowStageLabel)
  const impact = reordered || changedCardKeys.length > 1 ? 'major' : 'minor'
  const stagesLabel =
    invalidatedLabels.length > 0
      ? invalidatedLabels.join(', ')
      : 'No downstream stages'

  if (impact === 'major') {
    return {
      changeImpact: impact,
      changedCardKeys,
      reordered,
      summary: reordered
        ? `This becomes a structural outline revision because card order changed. ${stagesLabel} will need regeneration after save.`
        : `This revision changes ${changedCardKeys.length} cards at once. ${stagesLabel} will need regeneration after save.`,
    }
  }

  return {
    changeImpact: impact,
    changedCardKeys,
    reordered,
    summary: `This is a light outline revision. ${stagesLabel} should refresh before reuse after save.`,
  }
}

function validateOutlineDraft(cards: StoryOutlineEditorCardState[]) {
  for (const card of cards) {
    if (normalizeText(card.title).length === 0) {
      return `${getOutlineCardLabel(card)} needs a title before it can be saved.`
    }

    if (normalizeText(card.purpose).length === 0) {
      return `${getOutlineCardLabel(card)} needs a purpose before it can be saved.`
    }

    if (normalizeText(card.summary).length === 0) {
      return `${getOutlineCardLabel(card)} needs a summary before it can be saved.`
    }

    if (normalizeText(card.emotionalShift).length === 0) {
      return `${getOutlineCardLabel(card)} needs an emotional shift before it can be saved.`
    }
  }

  return null
}

function parseOptionalInteger(
  value: string,
  {
    label,
    min,
    max,
  }: {
    label: string
    min: number
    max: number
  },
): ParsedNumberField {
  const normalized = normalizeText(value)

  if (normalized.length === 0) {
    return {
      value: null,
      error: null,
    }
  }

  if (!/^\d+$/.test(normalized)) {
    return {
      value: null,
      error: `${label} must be a whole number.`,
    }
  }

  const parsed = Number.parseInt(normalized, 10)

  if (parsed < min || parsed > max) {
    return {
      value: null,
      error: `${label} should stay between ${min} and ${max}.`,
    }
  }

  return {
    value: parsed,
    error: null,
  }
}

function toComparableNumericString(value: string) {
  const normalized = normalizeText(value)

  if (!/^\d+$/.test(normalized)) {
    return normalized
  }

  return String(Number.parseInt(normalized, 10))
}

function buildComparableState(values: StorySetupFormState) {
  return {
    targetWordCount: toComparableNumericString(values.targetWordCount),
    targetRuntimeMinutes: toComparableNumericString(
      values.targetRuntimeMinutes,
    ),
    chapterCount: toComparableNumericString(values.chapterCount),
    approximateSceneCount: toComparableNumericString(
      values.approximateSceneCount,
    ),
    guidanceNotes: normalizeText(values.guidanceNotes),
  }
}

function storySetupStatesMatch(
  current: StorySetupFormState,
  saved: StorySetupFormState,
) {
  const currentComparable = buildComparableState(current)
  const savedComparable = buildComparableState(saved)

  return (
    currentComparable.targetWordCount === savedComparable.targetWordCount &&
    currentComparable.targetRuntimeMinutes ===
      savedComparable.targetRuntimeMinutes &&
    currentComparable.chapterCount === savedComparable.chapterCount &&
    currentComparable.approximateSceneCount ===
      savedComparable.approximateSceneCount &&
    currentComparable.guidanceNotes === savedComparable.guidanceNotes
  )
}

function formatSavedAt(value: string | null | undefined) {
  if (value == null) {
    return 'Not saved yet'
  }

  return `Saved ${savedAtFormatter.format(new Date(value))}`
}

function buildSavedTargetSummary(snapshot: SessionSnapshot) {
  const setup = snapshot.selected_story_setup

  if (setup == null) {
    return 'No soft targets saved yet'
  }

  const parts = buildTargetSummaryParts({
    targetRuntimeMinutes: setup.target_runtime_minutes ?? null,
    targetWordCount: setup.target_word_count ?? null,
    chapterCount: setup.chapter_count ?? null,
    approximateSceneCount: setup.approximate_scene_count ?? null,
  })

  return parts.length > 0 ? parts.join(', ') : 'Story setup preferences'
}

function buildStoryOutlineSummary(snapshot: SessionSnapshot) {
  const outline = getSelectedStoryOutline(snapshot)

  if (outline == null) {
    return 'No draftable outline saved yet'
  }

  const cardLabel = outline.outline_kind === 'chapter' ? 'chapters' : 'scenes'
  return `${outline.cards.length} ${cardLabel} ready for composition`
}

function buildDraftTargetSummary(values: {
  targetWordCount: number | null
  targetRuntimeMinutes: number | null
  chapterCount: number | null
  approximateSceneCount: number | null
}) {
  const parts = buildTargetSummaryParts(values)

  return parts.length > 0 ? parts.join(', ') : 'No targets drafted yet'
}

function isSavedOutlineCard(
  card:
    | StoryOutlineCard
    | Pick<
        StoryOutlineEditorCardState,
        'targetWordCount' | 'targetRuntimeMinutes' | 'targetSceneCount'
      >,
): card is StoryOutlineCard {
  return 'target_word_count' in card
}

function buildOutlineCardScope(
  card:
    | StoryOutlineCard
    | Pick<
        StoryOutlineEditorCardState,
        'targetWordCount' | 'targetRuntimeMinutes' | 'targetSceneCount'
      >,
) {
  const targetWordCount = isSavedOutlineCard(card)
    ? card.target_word_count
    : card.targetWordCount
  const targetRuntimeMinutes = isSavedOutlineCard(card)
    ? card.target_runtime_minutes
    : card.targetRuntimeMinutes
  const targetSceneCount = isSavedOutlineCard(card)
    ? card.target_scene_count
    : card.targetSceneCount

  return [
    targetWordCount != null ? `${targetWordCount} words` : null,
    targetRuntimeMinutes != null ? `~${targetRuntimeMinutes} min` : null,
    targetSceneCount != null
      ? `${targetSceneCount} scene${targetSceneCount === 1 ? '' : 's'}`
      : null,
  ]
    .filter((part): part is string => part != null)
    .join(' / ')
}

function buildTargetSummaryParts(values: {
  targetWordCount: number | null
  targetRuntimeMinutes: number | null
  chapterCount: number | null
  approximateSceneCount: number | null
}) {
  return [
    values.targetRuntimeMinutes != null
      ? `~${values.targetRuntimeMinutes} minutes`
      : null,
    values.targetWordCount != null ? `${values.targetWordCount} words` : null,
    values.chapterCount != null ? `${values.chapterCount} chapters` : null,
    values.approximateSceneCount != null
      ? `about ${values.approximateSceneCount} scenes`
      : null,
  ].filter((part): part is string => part != null)
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  snapshot: SessionSnapshot,
) {
  if (selectedStage.availability === 'locked') {
    return {
      body: 'Accept a beat sheet first. This panel stays visible so the pacing plan is easy to preview, but saving waits until the story structure is settled.',
      title: 'Beat sheet comes first',
      tone: 'warning' as const,
    }
  }

  if (
    selectedStage.availability === 'revisitable' &&
    snapshot.selected_story_setup != null
  ) {
    return {
      body: 'Updating these targets creates a fresh saved revision. Composition, audio, and finalize may need another pass afterward, because they treat these as planning input.',
      title: 'Edits refresh later production work',
      tone: 'warning' as const,
    }
  }

  return {
    body: 'Use these as calm planning guides. The final story may land a little above or below them if that keeps the bedtime arc coherent and restful.',
    title: 'Guides, not guarantees',
    tone: 'info' as const,
  }
}

function HeuristicSuggestionCallout({
  disabled,
  onApply,
  suggestion,
}: HeuristicSuggestionCalloutProps) {
  if (suggestion == null) {
    return null
  }

  return (
    <div className="story-setup-stage__suggestion">
      <p>{suggestion.helpText}</p>
      <Button
        disabled={disabled}
        onClick={() => {
          onApply(suggestion)
        }}
        size="compact"
        tone="secondary"
      >
        {suggestion.label}
      </Button>
    </div>
  )
}

export function StorySetupStage({
  onPreviewStage,
  onRestorePlanRevision,
  onSaveStorySetup,
  onSaveStoryOutline,
  selectedStage,
  snapshot,
}: StorySetupStageProps) {
  const [formState, setFormState] = useState<StorySetupFormState>(() =>
    buildFormState(snapshot),
  )
  const [outlineDraft, setOutlineDraft] = useState<
    StoryOutlineEditorCardState[]
  >(() => buildOutlineEditorState(snapshot))
  const [selectedOutlineCardKey, setSelectedOutlineCardKey] = useState<
    string | null
  >(() => buildOutlineEditorState(snapshot)[0]?.cardKey ?? null)
  const [formError, setFormError] = useState<string | null>(null)
  const [outlineError, setOutlineError] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [outlineAction, setOutlineAction] = useState<
    'save' | 'regenerate' | null
  >(null)
  const [lastEditedField, setLastEditedField] =
    useState<PlanningFieldId | null>(null)

  useEffect(() => {
    setFormState(buildFormState(snapshot))
    const nextOutlineState = buildOutlineEditorState(snapshot)
    setOutlineDraft(nextOutlineState)
    setSelectedOutlineCardKey(nextOutlineState[0]?.cardKey ?? null)
    setFormError(null)
    setOutlineError(null)
    setOutlineAction(null)
    setLastEditedField(null)
  }, [snapshot])

  const selectedOutline = getSelectedStoryOutline(snapshot)
  const savedState = buildFormState(snapshot)
  const savedOutlineState = buildOutlineEditorState(snapshot)
  const isLocked = selectedStage.availability === 'locked'
  const revisionHelp = buildRevisionHelp(selectedStage, snapshot)
  const targetWordCount = parseOptionalInteger(formState.targetWordCount, {
    label: 'Target word count',
    min: 100,
    max: 10000,
  })
  const targetRuntimeMinutes = parseOptionalInteger(
    formState.targetRuntimeMinutes,
    {
      label: 'Target read-aloud duration',
      min: 1,
      max: 180,
    },
  )
  const chapterCount = parseOptionalInteger(formState.chapterCount, {
    label: 'Chapter count',
    min: 1,
    max: 24,
  })
  const approximateSceneCount = parseOptionalInteger(
    formState.approximateSceneCount,
    {
      label: 'Approximate scene count',
      min: 1,
      max: 48,
    },
  )
  const comparableState = buildComparableState(formState)
  const fieldErrors = [
    targetWordCount.error,
    targetRuntimeMinutes.error,
    chapterCount.error,
    approximateSceneCount.error,
  ].filter((error): error is string => error != null)
  const isDirty = !storySetupStatesMatch(formState, savedState)
  const isOutlineDirty = !storyOutlineStatesMatch(
    outlineDraft,
    savedOutlineState,
  )
  const outlineValidationError = validateOutlineDraft(outlineDraft)
  const hasSavedSetup = snapshot.selected_story_setup != null
  const hasSavedOutline = selectedOutline != null
  const hasAnyConfiguredTarget =
    comparableState.targetWordCount.length > 0 ||
    comparableState.targetRuntimeMinutes.length > 0 ||
    comparableState.chapterCount.length > 0 ||
    comparableState.approximateSceneCount.length > 0 ||
    comparableState.guidanceNotes.length > 0
  const saveDisabled =
    isLocked ||
    isSaving ||
    !isDirty ||
    fieldErrors.length > 0 ||
    (!hasAnyConfiguredTarget && !hasSavedSetup)
  const activeOutlineDraft =
    outlineDraft.find((card) => card.cardKey === selectedOutlineCardKey) ??
    outlineDraft[0] ??
    null
  const outlineEditPreview = buildOutlineEditPreview(
    outlineDraft,
    savedOutlineState,
    selectedStage.invalidatesOnEdit,
  )
  const downstreamLabels = selectedStage.invalidatesOnEdit.map(
    getWorkflowStageLabel,
  )
  const saveOutlineDisabled =
    selectedOutline == null ||
    outlineAction != null ||
    !isOutlineDirty ||
    outlineValidationError != null
  const regenerateOutlineDisabled =
    selectedOutline == null ||
    activeOutlineDraft == null ||
    outlineAction != null ||
    outlineValidationError != null
  const runtimeHeuristic = buildRuntimeHeuristicSummary({
    lastEditedField,
    targetWordCount: targetWordCount.value,
    targetRuntimeMinutes: targetRuntimeMinutes.value,
  })
  const structureHeuristic = buildStructureHeuristicSummary({
    approximateSceneCount: approximateSceneCount.value,
    chapterCount: chapterCount.value,
    targetRuntimeMinutes: targetRuntimeMinutes.value,
    targetWordCount: targetWordCount.value,
  })

  function applyHeuristicSuggestion(suggestion: HeuristicSuggestion) {
    setFormState((current) => ({
      ...current,
      [suggestion.field]: String(suggestion.value),
    }))
    setLastEditedField(null)
    setFormError(null)
  }

  function updateOutlineDraft(
    cardKey: string,
    updates: Partial<StoryOutlineEditorCardState>,
  ) {
    setOutlineDraft((current) =>
      current.map((card) =>
        card.cardKey === cardKey ? { ...card, ...updates } : card,
      ),
    )
    setOutlineError(null)
  }

  function buildOutlineSavePayload() {
    return outlineDraft.map((card) => ({
      card_key: card.cardKey,
      card_type: card.cardType,
      position: card.position,
      title: normalizeText(card.title),
      purpose: toNullableText(card.purpose),
      summary: normalizeText(card.summary),
      beat_keys: [...card.beatKeys],
      beat_labels: [...card.beatLabels],
      emotional_shift: normalizeText(card.emotionalShift),
      target_word_count: card.targetWordCount ?? null,
      target_runtime_minutes: card.targetRuntimeMinutes ?? null,
      target_scene_count: card.targetSceneCount ?? null,
      tone_direction: card.toneDirection ?? null,
      bedtime_guardrail: card.bedtimeGuardrail ?? null,
      drafting_brief: toNullableText(card.draftingBrief),
    }))
  }

  function handleMoveOutlineCard(cardKey: string, direction: -1 | 1) {
    setOutlineDraft((current) =>
      moveOutlineDraftCard(current, cardKey, direction),
    )
    setOutlineError(null)
  }

  async function handleSave() {
    if (saveDisabled) {
      return
    }

    setIsSaving(true)
    setFormError(null)

    try {
      const requestBody: Parameters<typeof onSaveStorySetup>[0] = {
        origin: 'workspace',
        previewCurrentStage: false,
      }
      const currentComparable = buildComparableState(formState)
      const savedComparable = buildComparableState(savedState)

      if (
        currentComparable.targetWordCount !== savedComparable.targetWordCount
      ) {
        requestBody.targetWordCount = targetWordCount.value
      }
      if (
        currentComparable.targetRuntimeMinutes !==
        savedComparable.targetRuntimeMinutes
      ) {
        requestBody.targetRuntimeMinutes = targetRuntimeMinutes.value
      }
      if (currentComparable.chapterCount !== savedComparable.chapterCount) {
        requestBody.chapterCount = chapterCount.value
      }
      if (
        currentComparable.approximateSceneCount !==
        savedComparable.approximateSceneCount
      ) {
        requestBody.approximateSceneCount = approximateSceneCount.value
      }
      if (currentComparable.guidanceNotes !== savedComparable.guidanceNotes) {
        requestBody.guidanceNotes = toNullableText(formState.guidanceNotes)
      }

      await onSaveStorySetup(requestBody)
    } catch (error) {
      setFormError(
        error instanceof Error
          ? error.message
          : 'The story setup could not be saved right now.',
      )
    } finally {
      setIsSaving(false)
    }
  }

  async function handleSaveOutline(regenerateCardKeys: string[] = []) {
    if (
      selectedOutline == null ||
      outlineAction != null ||
      outlineValidationError != null ||
      (regenerateCardKeys.length === 0 && !isOutlineDirty)
    ) {
      return
    }

    setOutlineAction(regenerateCardKeys.length > 0 ? 'regenerate' : 'save')
    setOutlineError(null)

    try {
      await onSaveStoryOutline({
        outlineId: selectedOutline.id,
        summary: selectedOutline.summary ?? null,
        cards: buildOutlineSavePayload(),
        regenerateCardKeys,
        origin: 'workspace',
      })
    } catch (error) {
      setOutlineError(
        error instanceof Error
          ? error.message
          : 'The story outline could not be saved right now.',
      )
    } finally {
      setOutlineAction(null)
    }
  }

  return (
    <section aria-label="Story setup stage" className="workspace-stage-panel">
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            snapshot.selected_story_setup?.guidance_notes ??
            'Save a calm set of targets here, then revisit them whenever the beat sheet or writing direction changes.'
          }
          label="Current setup"
          title={buildSavedTargetSummary(snapshot)}
          tone={snapshot.selected_story_setup != null ? 'accent' : 'default'}
        >
          <div className="workspace-stage-detail__badges">
            {snapshot.selected_story_setup != null ? (
              <Badge tone="brand">
                Revision {snapshot.selected_story_setup.revision_number}
              </Badge>
            ) : (
              <Badge tone="warning">Not saved yet</Badge>
            )}
            <Badge tone="neutral">
              {formatSavedAt(snapshot.selected_story_setup?.accepted_at)}
            </Badge>
          </div>
        </SummaryPanel>

        <SummaryPanel
          description="These numbers help the planner balance pacing, chapter shape, and read-aloud feel. They are honest suggestions, not hard guarantees."
          label="Expectation setting"
          title="Guides, not guarantees"
        >
          <div className="workspace-stage-detail__badges">
            <Badge tone="brand">Soft targets</Badge>
            <Badge tone="neutral">Bedtime-first</Badge>
          </div>
        </SummaryPanel>

        <SummaryPanel
          description={
            downstreamLabels.length > 0
              ? `${downstreamLabels.join(', ')} may need another pass after these targets change.`
              : 'No later stages depend on this step.'
          }
          label="Next step"
          title={
            hasSavedOutline
              ? 'Composition can use this outline'
              : snapshot.selected_story_setup != null
                ? 'Save targets to rebuild the outline'
                : 'Save to unlock composition planning'
          }
        >
          <div className="cta-row">
            <Button
              disabled={!hasSavedOutline}
              onClick={() => {
                onPreviewStage('composition')
              }}
              tone="ghost"
            >
              Preview composition
            </Button>
          </div>
        </SummaryPanel>
      </CardGrid>

      <InlineHelp title={revisionHelp.title} tone={revisionHelp.tone}>
        {revisionHelp.body}
      </InlineHelp>

      {isLocked ? (
        <EmptyStateBlock
          action={
            <Button
              onClick={() => {
                onPreviewStage('beats')
              }}
              tone="ghost"
            >
              Return to beat sheet
            </Button>
          }
          description="Story setup follows the accepted Save-the-Cat outline so the pacing targets have something durable to sit on top of."
          title="Story setup is locked"
        />
      ) : null}

      <StickySummaryLayout
        summary={
          <SummaryPanel
            description="This rail shows the current pacing plan the backend will carry into composition prompts and later runtime estimates."
            label="Planner summary"
            sticky
            title={
              hasAnyConfiguredTarget
                ? buildDraftTargetSummary({
                    targetWordCount: targetWordCount.value,
                    targetRuntimeMinutes: targetRuntimeMinutes.value,
                    chapterCount: chapterCount.value,
                    approximateSceneCount: approximateSceneCount.value,
                  })
                : 'No targets drafted yet'
            }
            tone={snapshot.selected_story_setup != null ? 'accent' : 'default'}
          >
            <div className="workspace-stage-detail__badges">
              {isDirty ? (
                <Badge tone="accent">Unsaved changes</Badge>
              ) : snapshot.selected_story_setup != null ? (
                <Badge tone="success">Saved</Badge>
              ) : (
                <Badge tone="warning">Draft only</Badge>
              )}
            </div>

            <dl>
              <div>
                <dt>Story lane</dt>
                <dd>
                  {snapshot.selected_genre?.label ?? 'Genre pending'} /{' '}
                  {snapshot.selected_tone_profile?.label ?? 'Tone pending'}
                </dd>
              </div>
              <div>
                <dt>Beat sheet</dt>
                <dd>
                  {snapshot.selected_beat_sheet != null
                    ? `Revision ${snapshot.selected_beat_sheet.revision_number}`
                    : 'Needs selection'}
                </dd>
              </div>
              <div>
                <dt>Saved state</dt>
                <dd>
                  {formatSavedAt(snapshot.selected_story_setup?.accepted_at)}
                </dd>
              </div>
              <div>
                <dt>Outline</dt>
                <dd>{buildStoryOutlineSummary(snapshot)}</dd>
              </div>
            </dl>

            <InlineHelp title="Word count and runtime" tone="info">
              <div className="story-setup-stage__heuristic">
                <p>{runtimeHeuristic.body}</p>
                <HeuristicSuggestionCallout
                  disabled={isLocked}
                  onApply={applyHeuristicSuggestion}
                  suggestion={runtimeHeuristic.suggestion}
                />
              </div>
            </InlineHelp>

            <InlineHelp title="Chapter sizing" tone="info">
              <div className="story-setup-stage__heuristic">
                <p>{structureHeuristic}</p>
              </div>
            </InlineHelp>

            <InlineHelp title="Assumptions" tone="info">
              <div className="story-setup-stage__heuristic">
                <p>{buildPlanningAssumptionsText()}</p>
              </div>
            </InlineHelp>
          </SummaryPanel>
        }
      >
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Planning targets</h3>
              <p>
                Set the rough length and structure you want the writing stage to
                aim for. The planner will treat these as nearby targets, not
                strict requirements.
              </p>
            </div>
            <Badge
              tone={
                isDirty
                  ? 'accent'
                  : snapshot.selected_story_setup != null
                    ? 'success'
                    : 'warning'
              }
            >
              {isDirty
                ? 'Unsaved edits'
                : snapshot.selected_story_setup != null
                  ? 'Saved'
                  : 'Optional'}
            </Badge>
          </div>

          <FormColumns>
            <NumberField
              description="A soft word target helps later composition estimate density and pacing without forcing an exact final count."
              disabled={isLocked}
              error={targetWordCount.error}
              label="Target word count"
              min={100}
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  targetWordCount: value,
                }))
                setLastEditedField('targetWordCount')
                setFormError(null)
              }}
              step={100}
              value={formState.targetWordCount}
            />

            <NumberField
              description="Use the read-aloud duration you would like to land near. The written story may be a little shorter or longer."
              disabled={isLocked}
              error={targetRuntimeMinutes.error}
              label="Target read-aloud duration (minutes)"
              min={1}
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  targetRuntimeMinutes: value,
                }))
                setLastEditedField('targetRuntimeMinutes')
                setFormError(null)
              }}
              step={1}
              value={formState.targetRuntimeMinutes}
            />

            <NumberField
              description="Chapter count sets the broad pacing shape for the reading experience."
              disabled={isLocked}
              error={chapterCount.error}
              label="Chapter count"
              min={1}
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  chapterCount: value,
                }))
                setLastEditedField('chapterCount')
                setFormError(null)
              }}
              step={1}
              value={formState.chapterCount}
            />

            <NumberField
              description="Scene count is optional. Use it when you want a rough sense of how many distinct story turns the plan should hold."
              disabled={isLocked}
              error={approximateSceneCount.error}
              label="Approximate scene count"
              min={1}
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  approximateSceneCount: value,
                }))
                setLastEditedField('approximateSceneCount')
                setFormError(null)
              }}
              step={1}
              value={formState.approximateSceneCount}
            />
          </FormColumns>

          <TextArea
            description="Use this for pacing or structural guidance that does not fit neatly into a number, such as 'keep each chapter ending calmer than it began.'"
            disabled={isLocked}
            label="Pacing notes"
            onChange={(event) => {
              const value = event.currentTarget.value

              setFormState((current) => ({
                ...current,
                guidanceNotes: value,
              }))
              setLastEditedField('guidanceNotes')
              setFormError(null)
            }}
            rows={5}
            value={formState.guidanceNotes}
          />

          {formError != null ? (
            <InlineHelp title="Story setup save failed" tone="warning">
              {formError}
            </InlineHelp>
          ) : null}

          <div className="cta-row">
            <Button
              disabled={saveDisabled}
              onClick={() => {
                void handleSave()
              }}
              tone="primary"
            >
              {isSaving ? 'Saving story setup...' : 'Save story setup'}
            </Button>
            <Button
              disabled={isLocked || !isDirty || isSaving}
              onClick={() => {
                setFormState(savedState)
                setFormError(null)
                setLastEditedField(null)
              }}
              tone="ghost"
            >
              Reset
            </Button>
            <Button
              onClick={() => {
                onPreviewStage('beats')
              }}
              tone="ghost"
            >
              Review beat sheet
            </Button>
            <p className="cta-note">
              {formatSavedAt(snapshot.selected_story_setup?.accepted_at)}
            </p>
          </div>
        </section>

        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Draftable outline</h3>
              <p>
                These chapter or scene cards bridge the beat sheet into the
                actual writing segments composition can execute next.
              </p>
            </div>
            <Badge tone={hasSavedOutline ? 'success' : 'warning'}>
              {hasSavedOutline
                ? `${outlineDraft.length} cards ready`
                : 'Outline pending'}
            </Badge>
          </div>

          {selectedOutline != null ? (
            <>
              <CardGrid className="workspace-stage-detail__cards" columns={3}>
                <SummaryPanel
                  description={
                    selectedOutline.summary ??
                    'No saved outline summary is available yet.'
                  }
                  label="Current outline"
                  title={buildStoryOutlineSummary(snapshot)}
                  tone="accent"
                >
                  <div className="workspace-stage-detail__badges">
                    <Badge tone="brand">
                      Revision {selectedOutline.revision_number}
                    </Badge>
                    <Badge tone="neutral">
                      {selectedOutline.outline_kind === 'chapter'
                        ? 'Chapter cards'
                        : 'Scene cards'}
                    </Badge>
                    {selectedOutline.change_impact != null ? (
                      <Badge
                        tone={
                          selectedOutline.change_impact === 'major'
                            ? 'warning'
                            : 'accent'
                        }
                      >
                        {selectedOutline.change_impact === 'major'
                          ? 'Structural revision'
                          : 'Light revision'}
                      </Badge>
                    ) : null}
                  </div>
                </SummaryPanel>

                <SummaryPanel
                  description="Each card keeps beat coverage explicit so later segment writing can stay grounded in the accepted arc."
                  label="Beat coverage"
                  title={`${outlineDraft.reduce((count, card) => count + card.beatKeys.length, 0)} beats mapped`}
                />

                <SummaryPanel
                  description={
                    outlineEditPreview?.summary ??
                    selectedOutline.last_change_summary ??
                    'Reordering or editing multiple cards at once becomes a structural revision and makes downstream invalidation explicit before composition starts.'
                  }
                  label="Change propagation"
                  title={
                    outlineEditPreview != null
                      ? outlineEditPreview.changeImpact === 'major'
                        ? 'Structural draft pending save'
                        : 'Light draft pending save'
                      : selectedOutline.refreshes_downstream
                        ? 'Saved outline refreshes downstream work'
                        : 'No unsaved outline changes'
                  }
                />
              </CardGrid>

              {outlineEditPreview != null ? (
                <InlineHelp
                  title={
                    outlineEditPreview.changeImpact === 'major'
                      ? 'Structural outline revision'
                      : 'Light outline revision'
                  }
                  tone={
                    outlineEditPreview.changeImpact === 'major'
                      ? 'warning'
                      : 'info'
                  }
                >
                  {outlineEditPreview.summary}
                </InlineHelp>
              ) : selectedOutline.last_change_summary != null ? (
                <InlineHelp
                  title="Latest saved outline change"
                  tone={
                    selectedOutline.change_impact === 'major'
                      ? 'warning'
                      : 'info'
                  }
                >
                  {selectedOutline.last_change_summary}
                </InlineHelp>
              ) : null}

              {outlineValidationError != null ? (
                <InlineHelp
                  title="Outline draft needs attention"
                  tone="warning"
                >
                  {outlineValidationError}
                </InlineHelp>
              ) : null}

              {outlineError != null ? (
                <InlineHelp title="Outline save failed" tone="warning">
                  {outlineError}
                </InlineHelp>
              ) : null}

              <div className="story-outline-stage__editor">
                <ol className="story-outline-stage__cards">
                  {outlineDraft.map((card, index) => {
                    const isActive =
                      activeOutlineDraft?.cardKey === card.cardKey
                    const isChanged =
                      savedOutlineState.find(
                        (savedCard) => savedCard.cardKey === card.cardKey,
                      ) == null ||
                      JSON.stringify(buildOutlineComparableState([card])[0]) !==
                        JSON.stringify(
                          buildOutlineComparableState(
                            savedOutlineState.filter(
                              (savedCard) => savedCard.cardKey === card.cardKey,
                            ),
                          )[0],
                        )

                    return (
                      <li key={card.cardKey}>
                        <article
                          className={`story-outline-stage__card${isActive ? ' story-outline-stage__card--active' : ''}${isChanged ? ' story-outline-stage__card--changed' : ''}`}
                        >
                          <div className="story-outline-stage__card-header">
                            <div>
                              <div className="workspace-stage-detail__badges">
                                <Badge tone={isActive ? 'accent' : 'neutral'}>
                                  {getOutlineCardLabel(card)}
                                </Badge>
                                {isChanged ? (
                                  <Badge tone="warning">Draft changed</Badge>
                                ) : null}
                              </div>
                              <h4>
                                <button
                                  className="story-outline-stage__card-select"
                                  onClick={() => {
                                    setSelectedOutlineCardKey(card.cardKey)
                                    setOutlineError(null)
                                  }}
                                  type="button"
                                >
                                  {card.title}
                                </button>
                              </h4>
                            </div>
                            <div className="workspace-stage-detail__badges">
                              {buildOutlineCardScope(card).length > 0 ? (
                                <Badge tone="brand">
                                  {buildOutlineCardScope(card)}
                                </Badge>
                              ) : null}
                            </div>
                          </div>

                          <p>
                            <strong>Purpose.</strong> {card.purpose}
                          </p>
                          <p>{card.summary}</p>
                          <p>
                            <strong>Linked beats.</strong>{' '}
                            {card.beatLabels.join(', ')}
                          </p>
                          <p>
                            <strong>Emotional shift.</strong>{' '}
                            {card.emotionalShift}
                          </p>

                          <div className="cta-row">
                            <Button
                              disabled={outlineAction != null || index === 0}
                              onClick={() => {
                                handleMoveOutlineCard(card.cardKey, -1)
                              }}
                              size="compact"
                              tone="ghost"
                            >
                              Move earlier
                            </Button>
                            <Button
                              disabled={
                                outlineAction != null ||
                                index === outlineDraft.length - 1
                              }
                              onClick={() => {
                                handleMoveOutlineCard(card.cardKey, 1)
                              }}
                              size="compact"
                              tone="ghost"
                            >
                              Move later
                            </Button>
                          </div>
                        </article>
                      </li>
                    )
                  })}
                </ol>

                {activeOutlineDraft != null ? (
                  <section className="story-outline-stage__editor-panel">
                    <div className="panel-heading">
                      <div>
                        <h3>Outline editor</h3>
                        <p>
                          Adjust one card at a time, or reorder the full list.
                          Saving creates a new outline revision without wiping
                          the accepted beat sheet.
                        </p>
                      </div>
                      <Badge tone={isOutlineDirty ? 'warning' : 'success'}>
                        {isOutlineDirty ? 'Unsaved card edits' : 'Saved'}
                      </Badge>
                    </div>

                    <CardGrid
                      className="workspace-stage-detail__cards"
                      columns={2}
                    >
                      <SummaryPanel
                        description={activeOutlineDraft.beatLabels.join(', ')}
                        label="Linked beats"
                        title={`${activeOutlineDraft.beatLabels.length} beats`}
                      />
                      <SummaryPanel
                        description={
                          buildOutlineCardScope(activeOutlineDraft) ||
                          'No explicit target length is attached to this card.'
                        }
                        label="Target length"
                        title={getOutlineCardLabel(activeOutlineDraft)}
                      />
                    </CardGrid>

                    <FormColumns>
                      <TextInput
                        description="Use a concise title that still reads clearly in the card rail."
                        label="Card title"
                        onChange={(event) => {
                          updateOutlineDraft(activeOutlineDraft.cardKey, {
                            title: event.currentTarget.value,
                          })
                        }}
                        value={activeOutlineDraft.title}
                      />

                      <TextArea
                        description="Purpose should explain why this card exists in the composition plan."
                        label="Card purpose"
                        onChange={(event) => {
                          updateOutlineDraft(activeOutlineDraft.cardKey, {
                            purpose: event.currentTarget.value,
                          })
                        }}
                        rows={3}
                        value={activeOutlineDraft.purpose}
                      />
                    </FormColumns>

                    <TextArea
                      description="Keep the summary practical enough that composition can draft from it."
                      label="Card summary"
                      onChange={(event) => {
                        updateOutlineDraft(activeOutlineDraft.cardKey, {
                          summary: event.currentTarget.value,
                        })
                      }}
                      rows={4}
                      value={activeOutlineDraft.summary}
                    />

                    <TextArea
                      description="Capture the emotional movement this card needs to carry."
                      label="Emotional shift"
                      onChange={(event) => {
                        updateOutlineDraft(activeOutlineDraft.cardKey, {
                          emotionalShift: event.currentTarget.value,
                        })
                      }}
                      rows={3}
                      value={activeOutlineDraft.emotionalShift}
                    />

                    <TextArea
                      description="This is the segment-ready brief composition will inherit if no custom redirect overrides it."
                      label="Drafting brief"
                      onChange={(event) => {
                        updateOutlineDraft(activeOutlineDraft.cardKey, {
                          draftingBrief: event.currentTarget.value,
                        })
                      }}
                      rows={4}
                      value={activeOutlineDraft.draftingBrief}
                    />

                    <InlineHelp title="Locked structure" tone="info">
                      Beat coverage and target length stay fixed here so this
                      remains a structured card editor rather than turning into
                      a free-form outliner.
                    </InlineHelp>

                    <InlineHelp title="Regenerate this card" tone="info">
                      Regenerating saves the current outline draft as a new
                      revision, then rebuilds only this card from its linked
                      beats and saved targets.
                    </InlineHelp>

                    <div className="cta-row">
                      <Button
                        disabled={saveOutlineDisabled}
                        onClick={() => {
                          void handleSaveOutline()
                        }}
                        tone="primary"
                      >
                        {outlineAction === 'save'
                          ? 'Saving outline...'
                          : 'Save outline revision'}
                      </Button>
                      <Button
                        disabled={regenerateOutlineDisabled}
                        onClick={() => {
                          void handleSaveOutline([activeOutlineDraft.cardKey])
                        }}
                        tone="secondary"
                      >
                        {outlineAction === 'regenerate'
                          ? 'Regenerating card...'
                          : 'Regenerate this card'}
                      </Button>
                      <Button
                        disabled={outlineAction != null || !isOutlineDirty}
                        onClick={() => {
                          setOutlineDraft(savedOutlineState)
                          setSelectedOutlineCardKey(
                            savedOutlineState[0]?.cardKey ?? null,
                          )
                          setOutlineError(null)
                        }}
                        tone="ghost"
                      >
                        Reset outline edits
                      </Button>
                    </div>
                  </section>
                ) : null}
              </div>
            </>
          ) : (
            <EmptyStateBlock
              description={
                snapshot.selected_story_setup != null
                  ? 'This session has saved targets, but the outline has not been regenerated yet. Save the setup again to rebuild draftable cards from the latest beat sheet.'
                  : 'Save story setup targets to generate the first chapter or scene card plan.'
              }
              title="Outline not ready"
            />
          )}
        </section>

        <PlanRevisionHistoryPanel
          disabled={isSaving || outlineAction != null}
          onRestorePlanRevision={onRestorePlanRevision}
          snapshot={snapshot}
        />
      </StickySummaryLayout>
    </section>
  )
}
