import type { SessionSnapshot } from '../../api/sessions.ts'
import { Badge, ProgressBar, TextArea } from '../../shared/ui/primitives.tsx'
import {
  CardGrid,
  EmptyStateBlock,
  FormColumns,
  InlineHelp,
  NumberField,
  SelectField,
  SelectionCard,
  SliderField,
  SplitCard,
  StickySummaryLayout,
  SummaryPanel,
  ToggleField,
} from '../../shared/ui/workflow.tsx'
import type { SessionWorkspaceStageView } from './sessionStageScaffold.ts'

function toDisplayLabel(value: string) {
  const withSpaces = value.replace(/_/g, ' ')

  return withSpaces.charAt(0).toUpperCase() + withSpaces.slice(1)
}

function buildProgressLabel(snapshot: SessionSnapshot) {
  const { completed_stages: completedStages, total_stages: totalStages } =
    snapshot.progress
  const percentage = Math.round((completedStages / totalStages) * 100)

  return {
    percentage,
    valueText: `${completedStages} of ${totalStages} stages`,
  }
}

type SessionStageEditorPreviewProps = {
  invalidationLabels: ReadonlyArray<string>
  selectedStage: SessionWorkspaceStageView
  snapshot: SessionSnapshot
}

export function SessionStageEditorPreview({
  invalidationLabels,
  selectedStage,
  snapshot,
}: SessionStageEditorPreviewProps) {
  const progress = buildProgressLabel(snapshot)
  const chosenGenre = snapshot.selected_genre?.label ?? 'Quest Fantasy'
  const chosenTone = snapshot.selected_tone_profile?.label ?? 'Hushed Wonder'
  const pitchTitle = snapshot.selected_pitch?.title ?? 'Lantern Ferry Promise'
  const pitchLogline =
    snapshot.selected_pitch?.logline ??
    'A harbor child helps a shy ferry keeper return wandering lights to their sleeping boats before moonrise.'
  const beatFeedback =
    selectedStage.stage === 'beats'
      ? 'Keep the midpoint adventurous, then let the low point resolve into comfort within a page or two.'
      : 'Validation messages, helper copy, and soft constraints should remain visually consistent across later stages.'
  const summaryTone =
    selectedStage.availability === 'locked' ? 'accent' : 'default'

  return (
    <section
      aria-label="Workflow component kit"
      className="workspace-stage-panel"
    >
      <div className="panel-heading">
        <div>
          <h3>Workflow component kit</h3>
          <p>
            These shared cards, form controls, and rail layouts are the building
            blocks future prompts can compose instead of shipping one-off stage
            markup.
          </p>
        </div>
      </div>

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Choice cards</h3>
            <p>
              Selection states now read cleanly for genres, tones, and any other
              chooser that needs a chosen versus available option.
            </p>
          </div>
        </div>

        <CardGrid className="workflow-choice-grid" columns={2}>
          <SelectionCard
            description="Warm curiosity, safe tension, and enough wonder to keep the room feeling hushed."
            eyebrow="Selected tone"
            meta={
              <>
                <Badge tone="success">Chosen</Badge>
                <Badge tone="brand">{chosenGenre}</Badge>
              </>
            }
            selected
            title={chosenTone}
          >
            Bedtime-safe stakes and a reassuring cadence stay visible before the
            user commits to writing.
          </SelectionCard>

          <SelectionCard
            description="A slightly brighter, more curious option that still closes with emotional repair."
            eyebrow="Alternative"
            meta={<Badge tone="neutral">Preview</Badge>}
            title="Moonlit Mischief"
          >
            Unselected cards keep the same information density without pulling
            focus away from the accepted choice.
          </SelectionCard>

          <EmptyStateBlock
            description="When chat asks for more options, regenerated cards can land here without collapsing the layout rhythm."
            title="Option batch can expand in place"
          />
        </CardGrid>
      </section>

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Pitch and character cards</h3>
            <p>
              Split cards give pitches and character sheets a stronger content
              lane plus a summary lane for quick scanning.
            </p>
          </div>
        </div>

        <CardGrid columns={2}>
          <SplitCard
            aside={
              <>
                <Badge tone="success">Accepted pitch</Badge>
                <dl>
                  <div>
                    <dt>Promise</dt>
                    <dd>Soft harbor quest</dd>
                  </div>
                  <div>
                    <dt>Landing beat</dt>
                    <dd>Calm reunion</dd>
                  </div>
                </dl>
              </>
            }
            description={pitchLogline}
            eyebrow="Pitch card"
            meta={<Badge tone="brand">Lead option</Badge>}
            selected
            title={pitchTitle}
          >
            <ul className="split-card__list">
              <li>Gentle mystery with motion across lantern-lit water.</li>
              <li>Companion energy stays supportive rather than sarcastic.</li>
              <li>Conflict resolves into rest, not escalation.</li>
            </ul>
          </SplitCard>

          <SplitCard
            aside={
              <>
                <Badge tone="accent">Character sheet</Badge>
                <dl>
                  <div>
                    <dt>Need</dt>
                    <dd>Trust quiet instincts</dd>
                  </div>
                  <div>
                    <dt>Comfort note</dt>
                    <dd>Always return home safely</dd>
                  </div>
                </dl>
              </>
            }
            description="Character cards can balance bio details with the traits later stages need at a glance."
            eyebrow="Character card"
            title="Mina and the otter ferry keeper"
          >
            <ul className="split-card__list">
              <li>Mina notices soft sounds before anyone else does.</li>
              <li>
                The ferry keeper steadies scenes when the world feels large.
              </li>
              <li>Both characters value home, warmth, and gentle bravery.</li>
            </ul>
          </SplitCard>
        </CardGrid>
      </section>

      <section className="workspace-stage-panel">
        <div className="panel-heading">
          <div>
            <h3>Editor layout + side summary</h3>
            <p>
              Two-column forms, inline help, and a sticky rail make beat-sheet
              editors and setup screens reusable without crowding the canvas.
            </p>
          </div>
        </div>

        <StickySummaryLayout
          summary={
            <SummaryPanel
              description={selectedStage.scaffoldSummary}
              label="Sticky summary"
              sticky
              title={`${selectedStage.label} preview`}
              tone={summaryTone}
            >
              <div className="workspace-stage-detail__badges">
                <Badge tone="brand">
                  {toDisplayLabel(selectedStage.status)}
                </Badge>
                <Badge tone="accent">
                  {toDisplayLabel(selectedStage.availability)}
                </Badge>
              </div>

              <ProgressBar
                aria-label="Workflow progress"
                hint={`Resume at ${snapshot.resume_stage.replace(/_/g, ' ')} after this stage settles.`}
                label="Workflow progress"
                value={progress.percentage}
                valueText={progress.valueText}
              />

              <dl>
                <div>
                  <dt>Current route</dt>
                  <dd>?stage={selectedStage.stage}</dd>
                </div>
                <div>
                  <dt>Invalidates on edit</dt>
                  <dd>
                    {invalidationLabels.length > 0
                      ? invalidationLabels.join(', ')
                      : 'No later stages'}
                  </dd>
                </div>
              </dl>
            </SummaryPanel>
          }
        >
          <InlineHelp
            title="Inline guidance"
            tone={selectedStage.availability === 'locked' ? 'warning' : 'info'}
          >
            {selectedStage.availability === 'locked'
              ? 'Locked stages can still show preview controls, helper text, and downstream impact without implying they are editable yet.'
              : 'Unlocked stages can swap these mock controls for durable backend data without changing the surrounding layout.'}
          </InlineHelp>

          <FormColumns>
            <SelectField
              defaultValue="quiet-quest"
              description="Selects stay visually aligned with other fields and reserve room for helper copy."
              label="Narrative posture"
              options={[
                {
                  label: 'Quiet quest',
                  value: 'quiet-quest',
                },
                {
                  label: 'Restful mystery',
                  value: 'restful-mystery',
                },
                {
                  label: 'Comforting adventure',
                  value: 'comforting-adventure',
                },
              ]}
            />

            <NumberField
              defaultValue={
                snapshot.selected_story_setup?.target_word_count ?? 1500
              }
              description="Numeric targets work as soft guides rather than strict constraints."
              label="Target word count"
            />

            <SliderField
              defaultValue={
                snapshot.selected_story_setup?.target_runtime_minutes ?? 12
              }
              description="Slider labels can carry a readable value without extra one-off markup."
              label="Read-aloud runtime"
              max={20}
              min={6}
              step={1}
              valueText={`${snapshot.selected_story_setup?.target_runtime_minutes ?? 12} min`}
            />

            <ToggleField
              defaultChecked
              description="Toggles match the same label, description, and validation rules as other fields."
              label="Background music"
              stateLabel="Keep music soft and subordinate to narration."
            />
          </FormColumns>

          <TextArea
            defaultValue={selectedStage.detail ?? ''}
            description="Text areas inherit the same helper and validation treatment, so long-form stage notes still feel consistent."
            error={beatFeedback}
            label={`${selectedStage.label} notes`}
          />
        </StickySummaryLayout>
      </section>
    </section>
  )
}
