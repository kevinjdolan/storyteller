import { useEffect, useState } from 'react'
import type {
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { Badge, Button, TextArea } from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  FormColumns,
  InlineHelp,
  NumberField,
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

function buildDraftTargetSummary(values: {
  targetWordCount: number | null
  targetRuntimeMinutes: number | null
  chapterCount: number | null
  approximateSceneCount: number | null
}) {
  const parts = buildTargetSummaryParts(values)

  return parts.length > 0 ? parts.join(', ') : 'No targets drafted yet'
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
  selectedStage,
  snapshot,
}: StorySetupStageProps) {
  const [formState, setFormState] = useState<StorySetupFormState>(() =>
    buildFormState(snapshot),
  )
  const [formError, setFormError] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [lastEditedField, setLastEditedField] = useState<PlanningFieldId | null>(
    null,
  )

  useEffect(() => {
    setFormState(buildFormState(snapshot))
    setFormError(null)
    setLastEditedField(null)
  }, [snapshot])

  const savedState = buildFormState(snapshot)
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
  const hasSavedSetup = snapshot.selected_story_setup != null
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
            snapshot.selected_story_setup != null
              ? 'Composition can use this plan'
              : 'Save to unlock composition planning'
          }
        >
          <div className="cta-row">
            <Button
              disabled={snapshot.selected_story_setup == null}
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
      </StickySummaryLayout>
    </section>
  )
}
