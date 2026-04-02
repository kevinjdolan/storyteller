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
  SelectField,
  StickySummaryLayout,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import {
  buildPlanningAssumptionsText,
  buildRuntimeHeuristicSummary,
  buildStructureHeuristicSummary,
  type HeuristicSuggestion,
  type PlanningFieldId,
} from './planningHeuristics.ts'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'
import { getWorkflowStageLabel } from './workflowStages.ts'

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
    origin: string
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
  title: string
  summary: string
  emotionalShift: string
  draftingBrief: string
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

function getSelectedStoryOutline(snapshot: SessionSnapshot) {
  return (
    snapshot.selected_story_outline ?? snapshot.story_outline_revisions?.[0] ?? null
  )
}

function buildOutlineEditorState(
  snapshot: SessionSnapshot,
): StoryOutlineEditorCardState[] {
  return (getSelectedStoryOutline(snapshot)?.cards ?? []).map((card) => ({
    cardKey: card.card_key,
    title: card.title,
    summary: card.summary,
    emotionalShift: card.emotional_shift,
    draftingBrief: card.drafting_brief ?? '',
  }))
}

function buildOutlineComparableState(values: StoryOutlineEditorCardState[]) {
  return values.map((card) => ({
    cardKey: card.cardKey,
    title: normalizeText(card.title),
    summary: normalizeText(card.summary),
    emotionalShift: normalizeText(card.emotionalShift),
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
    targetRuntimeMinutes: toComparableNumericString(values.targetRuntimeMinutes),
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

function buildOutlineCardScope(card: StoryOutlineCard) {
  return [
    card.target_word_count != null ? `${card.target_word_count} words` : null,
    card.target_runtime_minutes != null
      ? `~${card.target_runtime_minutes} min`
      : null,
    card.target_scene_count != null
      ? `${card.target_scene_count} scene${card.target_scene_count === 1 ? '' : 's'}`
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
  onSaveStorySetup,
  onSaveStoryOutline,
  selectedStage,
  snapshot,
}: StorySetupStageProps) {
  const [formState, setFormState] = useState<StorySetupFormState>(() =>
    buildFormState(snapshot),
  )
  const [outlineDraft, setOutlineDraft] = useState<StoryOutlineEditorCardState[]>(
    () => buildOutlineEditorState(snapshot),
  )
  const [selectedOutlineCardKey, setSelectedOutlineCardKey] = useState<
    string | null
  >(() => buildOutlineEditorState(snapshot)[0]?.cardKey ?? null)
  const [formError, setFormError] = useState<string | null>(null)
  const [outlineError, setOutlineError] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [isSavingOutline, setIsSavingOutline] = useState(false)
  const [lastEditedField, setLastEditedField] = useState<PlanningFieldId | null>(
    null,
  )

  useEffect(() => {
    setFormState(buildFormState(snapshot))
    const nextOutlineState = buildOutlineEditorState(snapshot)
    setOutlineDraft(nextOutlineState)
    setSelectedOutlineCardKey(nextOutlineState[0]?.cardKey ?? null)
    setFormError(null)
    setOutlineError(null)
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
  const isOutlineDirty = !storyOutlineStatesMatch(outlineDraft, savedOutlineState)
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
  const activeOutlineCard =
    selectedOutline?.cards.find((card) => card.card_key === selectedOutlineCardKey) ??
    selectedOutline?.cards[0] ??
    null
  const activeOutlineDraft =
    outlineDraft.find((card) => card.cardKey === selectedOutlineCardKey) ??
    outlineDraft[0] ??
    null
  const downstreamLabels = selectedStage.invalidatesOnEdit.map(
    getWorkflowStageLabel,
  )
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

  async function handleSaveOutline() {
    if (
      selectedOutline == null ||
      activeOutlineCard == null ||
      activeOutlineDraft == null ||
      isSavingOutline ||
      !isOutlineDirty
    ) {
      return
    }

    setIsSavingOutline(true)
    setOutlineError(null)

    try {
      const cards = selectedOutline.cards.map((card) => {
        const draft = outlineDraft.find(
          (draftCard) => draftCard.cardKey === card.card_key,
        )

        return {
          ...card,
          title: draft?.title ?? card.title,
          summary: draft?.summary ?? card.summary,
          emotional_shift: draft?.emotionalShift ?? card.emotional_shift,
          drafting_brief:
            toNullableText(draft?.draftingBrief ?? card.drafting_brief ?? '') ??
            null,
        }
      })

      await onSaveStoryOutline({
        outlineId: selectedOutline.id,
        summary: selectedOutline.summary ?? null,
        cards,
        origin: 'workspace',
      })
    } catch (error) {
      setOutlineError(
        error instanceof Error
          ? error.message
          : 'The story outline could not be saved right now.',
      )
    } finally {
      setIsSavingOutline(false)
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
                <dd>{formatSavedAt(snapshot.selected_story_setup?.accepted_at)}</dd>
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
                ? `${selectedOutline?.cards.length ?? 0} cards ready`
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
                  </div>
                </SummaryPanel>

                <SummaryPanel
                  description="Each card keeps beat coverage explicit so later segment writing can stay grounded in the accepted arc."
                  label="Beat coverage"
                  title={`${selectedOutline.cards.reduce((count, card) => count + card.beat_keys.length, 0)} beats mapped`}
                />

                <SummaryPanel
                  description={
                    selectedOutline.guidance_notes ??
                    snapshot.selected_story_setup?.guidance_notes ??
                    'No extra pacing note is attached beyond the saved targets.'
                  }
                  label="Planner carry-through"
                  title={
                    selectedOutline.tone_label != null
                      ? `${selectedOutline.genre_label ?? 'Story lane'} / ${selectedOutline.tone_label}`
                      : 'Lane context'
                  }
                />
              </CardGrid>

              <ol className="story-outline-stage__cards">
                {selectedOutline.cards.map((card) => (
                  <li key={card.card_key} className="story-outline-stage__card">
                    <div className="story-outline-stage__card-header">
                      <div>
                        <Badge tone="neutral">
                          {card.card_type === 'chapter' ? 'Chapter' : 'Scene'}{' '}
                          {card.position}
                        </Badge>
                        <h4>{card.title}</h4>
                      </div>
                      <div className="workspace-stage-detail__badges">
                        {buildOutlineCardScope(card).length > 0 ? (
                          <Badge tone="brand">{buildOutlineCardScope(card)}</Badge>
                        ) : null}
                      </div>
                    </div>
                    <p>{card.summary}</p>
                    <p>
                      <strong>Supports beats.</strong>{' '}
                      {card.beat_labels.join(', ')}
                    </p>
                    <p>
                      <strong>Emotional shift.</strong> {card.emotional_shift}
                    </p>
                    {card.tone_direction != null ? (
                      <p>
                        <strong>Tone direction.</strong> {card.tone_direction}
                      </p>
                    ) : null}
                    {card.bedtime_guardrail != null ? (
                      <p>
                        <strong>Bedtime guardrail.</strong>{' '}
                        {card.bedtime_guardrail}
                      </p>
                    ) : null}
                    {card.drafting_brief != null ? (
                      <p>
                        <strong>Drafting brief.</strong> {card.drafting_brief}
                      </p>
                    ) : null}
                  </li>
                ))}
              </ol>
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

        {selectedOutline != null &&
        activeOutlineCard != null &&
        activeOutlineDraft != null ? (
          <section className="workspace-stage-panel">
            <div className="panel-heading">
              <div>
                <h3>Outline editor</h3>
                <p>
                  Edit the saved cards directly. Saving creates a new outline
                  revision and refreshes later production work without wiping
                  the accepted beat sheet.
                </p>
              </div>
              <Badge tone={isOutlineDirty ? 'warning' : 'success'}>
                {isOutlineDirty ? 'Unsaved card edits' : 'Saved'}
              </Badge>
            </div>

            <FormColumns>
              <SelectField
                description="Choose which draftable card to edit."
                label="Outline card"
                onChange={(event) => {
                  setSelectedOutlineCardKey(event.currentTarget.value)
                  setOutlineError(null)
                }}
                options={selectedOutline.cards.map((card) => ({
                  label: `${card.card_type === 'chapter' ? 'Chapter' : 'Scene'} ${card.position}: ${card.title}`,
                  value: card.card_key,
                }))}
                value={activeOutlineCard.card_key}
              />

              <TextInput
                description="Use a concise title that still reads well in the card rail."
                label="Card title"
                onChange={(event) => {
                  updateOutlineDraft(activeOutlineCard.card_key, {
                    title: event.currentTarget.value,
                  })
                }}
                value={activeOutlineDraft.title}
              />
            </FormColumns>

            <TextArea
              description="Keep the card summary practical enough that composition can draft from it."
              label="Card summary"
              onChange={(event) => {
                updateOutlineDraft(activeOutlineCard.card_key, {
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
                updateOutlineDraft(activeOutlineCard.card_key, {
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
                updateOutlineDraft(activeOutlineCard.card_key, {
                  draftingBrief: event.currentTarget.value,
                })
              }}
              rows={4}
              value={activeOutlineDraft.draftingBrief}
            />

            <InlineHelp title="Locked structure" tone="info">
              Beat coverage and card targets stay fixed here so edits can stay
              focused on clearer drafting direction rather than reshuffling the
              whole plan.
            </InlineHelp>

            {outlineError != null ? (
              <InlineHelp title="Outline save failed" tone="warning">
                {outlineError}
              </InlineHelp>
            ) : null}

            <div className="cta-row">
              <Button
                disabled={isSavingOutline || !isOutlineDirty}
                onClick={() => {
                  void handleSaveOutline()
                }}
                tone="primary"
              >
                {isSavingOutline ? 'Saving outline...' : 'Save outline revision'}
              </Button>
              <Button
                disabled={isSavingOutline || !isOutlineDirty}
                onClick={() => {
                  setOutlineDraft(savedOutlineState)
                  setOutlineError(null)
                }}
                tone="ghost"
              >
                Reset outline edits
              </Button>
            </div>
          </section>
        ) : null}
      </StickySummaryLayout>
    </section>
  )
}
