import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import {
  CardGrid,
  EmptyStateBlock,
  InlineHelp,
  SelectField,
  SelectionCard,
  SliderField,
  StickySummaryLayout,
  SummaryPanel,
  ToggleField,
} from './workflow.tsx'

describe('shared workflow ui', () => {
  it('connects select fields to descriptions and errors', () => {
    render(
      <SelectField
        description="Choose the emotional posture for the stage."
        error="A tone is required."
        label="Tone"
        options={[
          { label: 'Quiet quest', value: 'quiet-quest' },
          { label: 'Restful mystery', value: 'restful-mystery' },
        ]}
      />,
    )

    const select = screen.getByLabelText('Tone')
    const description = screen.getByText(
      'Choose the emotional posture for the stage.',
    )
    const error = screen.getByRole('alert')
    const describedBy = select.getAttribute('aria-describedby') ?? ''

    expect(select).toHaveAttribute('aria-invalid', 'true')
    expect(describedBy).toContain(description.id)
    expect(describedBy).toContain(error.id)
  })

  it('renders sliders with a visible value and toggles as switches', () => {
    render(
      <>
        <SliderField
          defaultValue={12}
          label="Runtime"
          max={20}
          min={6}
          valueText="12 min"
        />
        <ToggleField
          defaultChecked
          description="Keep music subordinate to narration."
          label="Background music"
          stateLabel="Soft instrumental bed."
        />
      </>,
    )

    expect(screen.getByRole('slider', { name: 'Runtime' })).toBeInTheDocument()
    expect(screen.getByText('12 min')).toBeInTheDocument()
    expect(
      screen.getByRole('switch', { name: 'Background music' }),
    ).toBeChecked()
  })

  it('renders selected cards inside sticky summary layouts', () => {
    render(
      <StickySummaryLayout
        summary={
          <SummaryPanel label="Summary" sticky title="Beat sheet preview">
            Keep the rail pinned while the editor scrolls.
          </SummaryPanel>
        }
      >
        <CardGrid columns={2}>
          <SelectionCard
            description="Chosen example for a stage option."
            selected
            title="Hushed Wonder"
          />
        </CardGrid>
      </StickySummaryLayout>,
    )

    expect(document.querySelector('.selection-card--selected')).not.toBeNull()
    expect(
      screen.getByRole('heading', { level: 3, name: 'Beat sheet preview' }),
    ).toBeInTheDocument()
    expect(document.querySelector('.summary-panel--sticky')).not.toBeNull()
  })

  it('supports reusable help and empty-state blocks', () => {
    render(
      <>
        <InlineHelp title="Guidance">
          Use helper copy for lightweight notes.
        </InlineHelp>
        <EmptyStateBlock
          description="Fresh options can land here without shifting the surrounding grid."
          title="Waiting for another batch"
        />
      </>,
    )

    expect(screen.getByText('Guidance')).toBeInTheDocument()
    expect(screen.getByText('Waiting for another batch')).toBeInTheDocument()
  })
})
