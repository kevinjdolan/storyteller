import { useEffect, useState } from 'react'
import type {
  NormalizedBriefPreferencesView,
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../api/sessions.ts'
import { Badge, Button, TextArea } from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  FormColumns,
  InlineHelp,
  StickySummaryLayout,
  SummaryPanel,
} from '../../shared/ui/workflow.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

type StoryBriefStageProps = {
  onPreviewStage: (stageId: 'pitches' | 'tone') => void
  onSaveStoryBrief: (input: {
    audienceNotes?: string | null
    desiredThemes?: string | null
    keyImages?: string | null
    mustHaveElements?: string | null
    normalizedPreferences?: NormalizedBriefPreferencesView | null
    normalizedSummary?: string | null
    origin: string
    storyIdea?: string | null
  }) => Promise<{
    event: SessionHistoryEvent
    snapshot: SessionSnapshot
  }>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

type StoryBriefFormState = {
  audienceNotes: string
  bedtimeSafetyConcerns: string
  candidateMotifs: string
  constraintNotes: string
  desiredThemes: string
  emotionalGoal: string
  keyImages: string
  mustHaveElements: string
  normalizedSummary: string
  protagonistType: string
  setting: string
  storyIdea: string
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

function normalizeListText(value: string) {
  return value
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
}

function formatListText(values: string[] | null | undefined) {
  return values?.join('\n') ?? ''
}

function buildFormState(snapshot: SessionSnapshot): StoryBriefFormState {
  return {
    storyIdea: snapshot.story_brief?.story_idea ?? '',
    desiredThemes: snapshot.story_brief?.desired_themes ?? '',
    keyImages: snapshot.story_brief?.key_images ?? '',
    audienceNotes: snapshot.story_brief?.audience_notes ?? '',
    mustHaveElements: snapshot.story_brief?.must_have_elements ?? '',
    normalizedSummary: snapshot.story_brief?.normalized_summary ?? '',
    protagonistType:
      snapshot.story_brief?.normalized_preferences?.protagonist_type ?? '',
    setting: snapshot.story_brief?.normalized_preferences?.setting ?? '',
    emotionalGoal:
      snapshot.story_brief?.normalized_preferences?.emotional_goal ?? '',
    constraintNotes: formatListText(
      snapshot.story_brief?.normalized_preferences?.constraint_notes,
    ),
    bedtimeSafetyConcerns: formatListText(
      snapshot.story_brief?.normalized_preferences?.bedtime_safety_concerns,
    ),
    candidateMotifs: formatListText(
      snapshot.story_brief?.normalized_preferences?.candidate_motifs,
    ),
  }
}

function buildCanonicalBriefPreview(values: StoryBriefFormState) {
  const sections: string[] = []

  if (normalizeText(values.storyIdea).length > 0) {
    sections.push(normalizeText(values.storyIdea))
  }

  for (const [label, value] of [
    ['Desired themes', values.desiredThemes],
    ['Key images', values.keyImages],
    ['Target audience notes', values.audienceNotes],
    ['Must-have elements', values.mustHaveElements],
  ] as const) {
    const normalized = normalizeText(value)

    if (normalized.length > 0) {
      sections.push(`${label}: ${normalized}`)
    }
  }

  return sections.join('\n\n')
}

function buildSpecificityCount(values: StoryBriefFormState) {
  return [
    values.desiredThemes,
    values.keyImages,
    values.audienceNotes,
    values.mustHaveElements,
  ].filter((value) => normalizeText(value).length > 0).length
}

function buildInterpretationFieldCount(values: StoryBriefFormState) {
  return [
    values.normalizedSummary,
    values.protagonistType,
    values.setting,
    values.emotionalGoal,
    values.constraintNotes,
    values.bedtimeSafetyConcerns,
    values.candidateMotifs,
  ].filter((value) => normalizeText(value).length > 0).length
}

function buildBriefTitle(
  values: StoryBriefFormState,
  snapshot: SessionSnapshot,
) {
  const preview =
    normalizeText(values.normalizedSummary) ||
    normalizeText(values.storyIdea) ||
    snapshot.story_brief?.normalized_summary ||
    snapshot.story_brief?.story_idea ||
    ''

  if (preview.length === 0) {
    return 'Brief not saved yet'
  }

  if (preview.length <= 92) {
    return preview
  }

  return `${preview.slice(0, 89).trimEnd()}...`
}

function buildRevisionHelp(
  selectedStage: SessionWorkspaceStageView,
  snapshot: SessionSnapshot,
) {
  if (selectedStage.availability === 'locked') {
    return {
      body: 'Finish genre and tone first. The brief stays previewable, but saving is disabled until the bedtime lane is fully chosen.',
      title: 'Brief saving unlocks after tone',
      tone: 'warning' as const,
    }
  }

  if (
    selectedStage.availability === 'revisitable' &&
    snapshot.story_brief != null
  ) {
    return {
      body: 'Editing a saved brief creates a new revision, keeps the latest version active, and refreshes pitches plus any later planning that depends on it.',
      title: 'Revisions refresh downstream planning',
      tone: 'warning' as const,
    }
  }

  return {
    body: 'Start with one or two natural sentences. Use the optional fields only when they add helpful specificity for later pitch generation.',
    title: 'Keep the brief open-ended, not rigid',
    tone: 'info' as const,
  }
}

function formatUpdatedAt(value: string | null | undefined) {
  if (value == null) {
    return 'Not saved yet'
  }

  return `Saved ${savedAtFormatter.format(new Date(value))}`
}

function normalizeFormState(values: StoryBriefFormState) {
  return {
    storyIdea: normalizeText(values.storyIdea),
    desiredThemes: normalizeText(values.desiredThemes),
    keyImages: normalizeText(values.keyImages),
    audienceNotes: normalizeText(values.audienceNotes),
    mustHaveElements: normalizeText(values.mustHaveElements),
    normalizedSummary: normalizeText(values.normalizedSummary),
    protagonistType: normalizeText(values.protagonistType),
    setting: normalizeText(values.setting),
    emotionalGoal: normalizeText(values.emotionalGoal),
    constraintNotes: normalizeListText(values.constraintNotes),
    bedtimeSafetyConcerns: normalizeListText(values.bedtimeSafetyConcerns),
    candidateMotifs: normalizeListText(values.candidateMotifs),
  }
}

function formStatesMatch(
  left: StoryBriefFormState,
  right: StoryBriefFormState,
) {
  const normalizedLeft = normalizeFormState(left)
  const normalizedRight = normalizeFormState(right)

  return (
    normalizedLeft.storyIdea === normalizedRight.storyIdea &&
    normalizedLeft.desiredThemes === normalizedRight.desiredThemes &&
    normalizedLeft.keyImages === normalizedRight.keyImages &&
    normalizedLeft.audienceNotes === normalizedRight.audienceNotes &&
    normalizedLeft.mustHaveElements === normalizedRight.mustHaveElements &&
    normalizedLeft.normalizedSummary === normalizedRight.normalizedSummary &&
    normalizedLeft.protagonistType === normalizedRight.protagonistType &&
    normalizedLeft.setting === normalizedRight.setting &&
    normalizedLeft.emotionalGoal === normalizedRight.emotionalGoal &&
    normalizedLeft.constraintNotes.join('\n') ===
      normalizedRight.constraintNotes.join('\n') &&
    normalizedLeft.bedtimeSafetyConcerns.join('\n') ===
      normalizedRight.bedtimeSafetyConcerns.join('\n') &&
    normalizedLeft.candidateMotifs.join('\n') ===
      normalizedRight.candidateMotifs.join('\n')
  )
}

function briefStatesMatch(
  left: StoryBriefFormState,
  right: StoryBriefFormState,
) {
  const normalizedLeft = normalizeFormState(left)
  const normalizedRight = normalizeFormState(right)

  return (
    normalizedLeft.storyIdea === normalizedRight.storyIdea &&
    normalizedLeft.desiredThemes === normalizedRight.desiredThemes &&
    normalizedLeft.keyImages === normalizedRight.keyImages &&
    normalizedLeft.audienceNotes === normalizedRight.audienceNotes &&
    normalizedLeft.mustHaveElements === normalizedRight.mustHaveElements
  )
}

function interpretationStatesMatch(
  left: StoryBriefFormState,
  right: StoryBriefFormState,
) {
  const normalizedLeft = normalizeFormState(left)
  const normalizedRight = normalizeFormState(right)

  return (
    normalizedLeft.normalizedSummary === normalizedRight.normalizedSummary &&
    normalizedLeft.protagonistType === normalizedRight.protagonistType &&
    normalizedLeft.setting === normalizedRight.setting &&
    normalizedLeft.emotionalGoal === normalizedRight.emotionalGoal &&
    normalizedLeft.constraintNotes.join('\n') ===
      normalizedRight.constraintNotes.join('\n') &&
    normalizedLeft.bedtimeSafetyConcerns.join('\n') ===
      normalizedRight.bedtimeSafetyConcerns.join('\n') &&
    normalizedLeft.candidateMotifs.join('\n') ===
      normalizedRight.candidateMotifs.join('\n')
  )
}

function buildNormalizedPreferences(
  values: StoryBriefFormState,
): NormalizedBriefPreferencesView | null {
  const normalized = normalizeFormState(values)
  const preferences: NormalizedBriefPreferencesView = {
    protagonist_type: normalized.protagonistType || null,
    setting: normalized.setting || null,
    emotional_goal: normalized.emotionalGoal || null,
    constraint_notes: normalized.constraintNotes,
    bedtime_safety_concerns: normalized.bedtimeSafetyConcerns,
    candidate_motifs: normalized.candidateMotifs,
  }

  return hasNormalizedPreferences(preferences) ? preferences : null
}

function hasNormalizedPreferences(
  preferences: NormalizedBriefPreferencesView | null | undefined,
) {
  if (preferences == null) {
    return false
  }

  return Boolean(
    preferences.protagonist_type ||
    preferences.setting ||
    preferences.emotional_goal ||
    (preferences.constraint_notes?.length ?? 0) > 0 ||
    (preferences.bedtime_safety_concerns?.length ?? 0) > 0 ||
    (preferences.candidate_motifs?.length ?? 0) > 0,
  )
}

export function StoryBriefStage({
  onPreviewStage,
  onSaveStoryBrief,
  selectedStage,
  snapshot,
}: StoryBriefStageProps) {
  const [formState, setFormState] = useState<StoryBriefFormState>(() =>
    buildFormState(snapshot),
  )
  const [formError, setFormError] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    setFormState(buildFormState(snapshot))
    setFormError(null)
  }, [snapshot])

  const savedState = buildFormState(snapshot)
  const isLocked = selectedStage.availability === 'locked'
  const specificityCount = buildSpecificityCount(formState)
  const interpretationFieldCount = buildInterpretationFieldCount(formState)
  const briefTitle = buildBriefTitle(formState, snapshot)
  const canonicalPreview = buildCanonicalBriefPreview(formState)
  const normalizedPreferences = buildNormalizedPreferences(formState)
  const hasInterpretation =
    normalizeText(formState.normalizedSummary).length > 0 ||
    hasNormalizedPreferences(normalizedPreferences)
  const revisionHelp = buildRevisionHelp(selectedStage, snapshot)
  const storyIdeaError =
    !isLocked && normalizeText(formState.storyIdea).length === 0
      ? 'Start with the bedtime story idea in your own words.'
      : null
  const briefDirty = !briefStatesMatch(formState, savedState)
  const interpretationDirty = !interpretationStatesMatch(formState, savedState)
  const isDirty = !formStatesMatch(formState, savedState)

  async function handleSave() {
    if (isLocked || storyIdeaError != null || isSaving || !isDirty) {
      return
    }

    setIsSaving(true)
    setFormError(null)

    try {
      const requestBody: Parameters<typeof onSaveStoryBrief>[0] = {
        storyIdea: toNullableText(formState.storyIdea),
        desiredThemes: toNullableText(formState.desiredThemes),
        keyImages: toNullableText(formState.keyImages),
        audienceNotes: toNullableText(formState.audienceNotes),
        mustHaveElements: toNullableText(formState.mustHaveElements),
        origin: 'workspace',
      }

      if (interpretationDirty) {
        requestBody.normalizedSummary = toNullableText(
          formState.normalizedSummary,
        )
        requestBody.normalizedPreferences = normalizedPreferences
      }

      await onSaveStoryBrief(requestBody)
    } catch (error) {
      setFormError(
        error instanceof Error
          ? error.message
          : 'The story brief could not be saved right now.',
      )
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <section aria-label="Story brief stage" className="workspace-stage-panel">
      <CardGrid className="workspace-stage-detail__cards" columns={3}>
        <SummaryPanel
          description={
            snapshot.story_brief?.normalized_summary ??
            'This is the durable bedtime prompt that later pitch generation will inherit.'
          }
          label="Current brief"
          title={briefTitle}
          tone={snapshot.story_brief != null ? 'accent' : 'default'}
        >
          <div className="workspace-stage-detail__badges">
            {snapshot.story_brief != null ? (
              <Badge tone="brand">
                Revision {snapshot.story_brief.revision_number}
              </Badge>
            ) : (
              <Badge tone="warning">Unsaved</Badge>
            )}
          </div>
        </SummaryPanel>

        <SummaryPanel
          description={
            hasInterpretation
              ? 'The backend stores this editable interpretation alongside the raw brief so later planning can use structured preferences directly.'
              : 'The backend will generate an interpretation on save, then the user can correct it instead of treating it as hidden magic.'
          }
          label="Structured interpretation"
          title={
            interpretationFieldCount > 0
              ? `${interpretationFieldCount} interpretation field${interpretationFieldCount === 1 ? '' : 's'} filled`
              : 'Generated on first save'
          }
        >
          <div className="workspace-stage-detail__badges">
            <Badge tone={hasInterpretation ? 'brand' : 'warning'}>
              {hasInterpretation ? 'Editable' : 'Pending'}
            </Badge>
            <Badge tone="neutral">
              {specificityCount} cue{specificityCount === 1 ? '' : 's'}
            </Badge>
          </div>
        </SummaryPanel>

        <SummaryPanel
          description={
            snapshot.story_brief != null
              ? 'Pitch generation can now synthesize multiple directions from this saved bedtime brief.'
              : 'Save the brief once it feels right, then move into pitch generation.'
          }
          label="Next step"
          title={
            snapshot.story_brief != null
              ? 'Pitch options come next'
              : 'Save to unlock pitches'
          }
        >
          <div className="cta-row">
            <Button
              disabled={snapshot.story_brief == null}
              onClick={() => {
                onPreviewStage('pitches')
              }}
              tone="ghost"
            >
              Preview pitches
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
                onPreviewStage('tone')
              }}
              tone="ghost"
            >
              Return to tone
            </Button>
          }
          description="The brief is the bridge between tone selection and generative planning, so the workspace keeps it read-only until the tone is saved."
          title="Brief editing is locked"
        />
      ) : null}

      <StickySummaryLayout
        summary={
          <SummaryPanel
            description="This is the compiled prompt text that the backend persists for downstream planning."
            label="Planner preview"
            sticky
            title={briefTitle}
            tone={snapshot.story_brief != null ? 'accent' : 'default'}
          >
            <div className="workspace-stage-detail__badges">
              {snapshot.story_brief != null ? (
                <Badge tone="brand">
                  Revision {snapshot.story_brief.revision_number}
                </Badge>
              ) : (
                <Badge tone="warning">Draft only</Badge>
              )}
              <Badge tone="neutral">
                {formatUpdatedAt(snapshot.story_brief?.updated_at)}
              </Badge>
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
                <dt>Optional cues filled</dt>
                <dd>{specificityCount}</dd>
              </div>
              <div>
                <dt>Interpretation fields</dt>
                <dd>{interpretationFieldCount}</dd>
              </div>
            </dl>

            <div className="story-brief-stage__preview">
              {canonicalPreview.length > 0 ? (
                canonicalPreview.split('\n\n').map((section) => (
                  <div
                    key={section}
                    className="story-brief-stage__preview-section"
                  >
                    {section}
                  </div>
                ))
              ) : (
                <p className="story-brief-stage__preview-empty">
                  The compiled prompt preview will appear here as the brief
                  takes shape.
                </p>
              )}
            </div>

            <div className="story-brief-stage__interpretation-summary">
              <h4>Structured interpretation</h4>
              {formState.normalizedSummary.length > 0 ? (
                <p className="story-brief-stage__interpretation-text">
                  {formState.normalizedSummary}
                </p>
              ) : (
                <p className="story-brief-stage__preview-empty">
                  Save the brief to extract a reusable interpretation, then
                  correct it here if needed.
                </p>
              )}

              <dl className="story-brief-stage__interpretation-grid">
                <div>
                  <dt>Protagonist type</dt>
                  <dd>{formState.protagonistType || 'Not extracted yet'}</dd>
                </div>
                <div>
                  <dt>Setting</dt>
                  <dd>{formState.setting || 'Not extracted yet'}</dd>
                </div>
                <div>
                  <dt>Emotional goal</dt>
                  <dd>{formState.emotionalGoal || 'Not extracted yet'}</dd>
                </div>
              </dl>

              <div className="story-brief-stage__interpretation-groups">
                <div>
                  <h5>Constraint notes</h5>
                  {normalizeListText(formState.constraintNotes).length > 0 ? (
                    <ul>
                      {normalizeListText(formState.constraintNotes).map(
                        (item) => (
                          <li key={item}>{item}</li>
                        ),
                      )}
                    </ul>
                  ) : (
                    <p className="story-brief-stage__preview-empty">
                      No explicit constraints captured yet.
                    </p>
                  )}
                </div>
                <div>
                  <h5>Bedtime guardrails</h5>
                  {normalizeListText(formState.bedtimeSafetyConcerns).length >
                  0 ? (
                    <ul>
                      {normalizeListText(formState.bedtimeSafetyConcerns).map(
                        (item) => (
                          <li key={item}>{item}</li>
                        ),
                      )}
                    </ul>
                  ) : (
                    <p className="story-brief-stage__preview-empty">
                      No special guardrails captured yet.
                    </p>
                  )}
                </div>
                <div>
                  <h5>Candidate motifs</h5>
                  {normalizeListText(formState.candidateMotifs).length > 0 ? (
                    <ul>
                      {normalizeListText(formState.candidateMotifs).map(
                        (item) => (
                          <li key={item}>{item}</li>
                        ),
                      )}
                    </ul>
                  ) : (
                    <p className="story-brief-stage__preview-empty">
                      No recurring motifs captured yet.
                    </p>
                  )}
                </div>
              </div>
            </div>
          </SummaryPanel>
        }
      >
        <section className="workspace-stage-panel">
          <div className="panel-heading">
            <div>
              <h3>Free-form bedtime brief</h3>
              <p>
                Capture the story in natural language first, then add optional
                cues only if they will sharpen later pitch generation.
              </p>
            </div>
            <Badge
              tone={
                briefDirty
                  ? 'accent'
                  : snapshot.story_brief != null
                    ? 'success'
                    : 'warning'
              }
            >
              {briefDirty
                ? 'Unsaved edits'
                : snapshot.story_brief != null
                  ? 'Saved'
                  : 'Required'}
            </Badge>
          </div>

          <TextArea
            description="One or two vivid sentences is enough. Write this the way you would explain the story idea to a calm human collaborator."
            disabled={isLocked}
            error={storyIdeaError}
            label="Story idea"
            onChange={(event) => {
              const value = event.currentTarget.value

              setFormState((current) => ({
                ...current,
                storyIdea: value,
              }))
            }}
            rows={6}
            value={formState.storyIdea}
          />

          <FormColumns>
            <TextArea
              description="Themes can stay broad or emotional: belonging, gentle courage, grief repair, wonder, and so on."
              disabled={isLocked}
              label="Desired themes"
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  desiredThemes: value,
                }))
              }}
              rows={4}
              value={formState.desiredThemes}
            />
            <TextArea
              description="Call out the images or motifs you want the story to keep returning to."
              disabled={isLocked}
              label="Key images"
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  keyImages: value,
                }))
              }}
              rows={4}
              value={formState.keyImages}
            />
            <TextArea
              description="Audience notes can cover age, sensitivity, family context, or read-aloud preferences."
              disabled={isLocked}
              label="Target audience notes"
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  audienceNotes: value,
                }))
              }}
              rows={4}
              value={formState.audienceNotes}
            />
            <TextArea
              description="Use this for non-negotiables: a calm ending, a dragon friend, a lighthouse, or any image that must appear."
              disabled={isLocked}
              label="Must-have elements"
              onChange={(event) => {
                const value = event.currentTarget.value

                setFormState((current) => ({
                  ...current,
                  mustHaveElements: value,
                }))
              }}
              rows={4}
              value={formState.mustHaveElements}
            />
          </FormColumns>

          <section className="story-brief-stage__interpretation-panel">
            <div className="panel-heading">
              <div>
                <h3>Editable interpretation</h3>
                <p>
                  This is the backend&apos;s structured read of the brief. If
                  the extraction misses the user&apos;s intent, correct it here
                  before later generators inherit it.
                </p>
              </div>
              <Badge
                tone={
                  interpretationDirty
                    ? 'accent'
                    : hasInterpretation
                      ? 'success'
                      : 'warning'
                }
              >
                {interpretationDirty
                  ? 'Unsaved interpretation'
                  : hasInterpretation
                    ? 'Reviewable'
                    : 'Generated on save'}
              </Badge>
            </div>

            <InlineHelp title="Tied to the current brief" tone="info">
              If the story text changes and these interpretation fields stay
              untouched, the backend will regenerate them on save. If you edit
              them here, your corrections are saved as the durable
              interpretation for this revision.
            </InlineHelp>

            <FormColumns>
              <TextArea
                description="A compact, calm planning summary that later stages can reuse directly."
                disabled={isLocked}
                label="Normalized summary"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    normalizedSummary: value,
                  }))
                }}
                rows={4}
                value={formState.normalizedSummary}
              />
              <TextArea
                description="Describe the likely main protagonist role, creature, or duo the brief implies."
                disabled={isLocked}
                label="Protagonist type"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    protagonistType: value,
                  }))
                }}
                rows={3}
                value={formState.protagonistType}
              />
              <TextArea
                description="Capture the main environment or location that later planning should keep returning to."
                disabled={isLocked}
                label="Setting"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    setting: value,
                  }))
                }}
                rows={3}
                value={formState.setting}
              />
              <TextArea
                description="Describe the bedtime-facing emotional destination or repair the story should aim toward."
                disabled={isLocked}
                label="Emotional goal"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    emotionalGoal: value,
                  }))
                }}
                rows={3}
                value={formState.emotionalGoal}
              />
              <TextArea
                description="One note per line. Use this for non-negotiables or strong implied constraints from the brief."
                disabled={isLocked}
                label="Constraint notes"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    constraintNotes: value,
                  }))
                }}
                rows={5}
                value={formState.constraintNotes}
              />
              <TextArea
                description="One note per line. Capture guardrails that keep the story bedtime-safe for this brief."
                disabled={isLocked}
                label="Bedtime-safety concerns"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    bedtimeSafetyConcerns: value,
                  }))
                }}
                rows={5}
                value={formState.bedtimeSafetyConcerns}
              />
              <TextArea
                description="One motif per line. These are recurring images or symbols worth carrying forward."
                disabled={isLocked}
                label="Candidate motifs"
                onChange={(event) => {
                  const value = event.currentTarget.value

                  setFormState((current) => ({
                    ...current,
                    candidateMotifs: value,
                  }))
                }}
                rows={5}
                value={formState.candidateMotifs}
              />
            </FormColumns>
          </section>

          {formError != null ? (
            <InlineHelp title="Story brief save failed" tone="warning">
              {formError}
            </InlineHelp>
          ) : null}

          <div className="cta-row">
            <Button
              disabled={
                isLocked || storyIdeaError != null || !isDirty || isSaving
              }
              onClick={() => {
                void handleSave()
              }}
              tone="primary"
            >
              {isSaving ? 'Saving brief...' : 'Save brief'}
            </Button>
            <Button
              disabled={isLocked || !isDirty || isSaving}
              onClick={() => {
                setFormState(savedState)
                setFormError(null)
              }}
              tone="ghost"
            >
              Reset
            </Button>
            <p className="cta-note">
              {formatUpdatedAt(snapshot.story_brief?.updated_at)}
            </p>
          </div>
        </section>
      </StickySummaryLayout>
    </section>
  )
}
