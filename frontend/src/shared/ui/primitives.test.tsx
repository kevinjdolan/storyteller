import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import {
  Panel,
  ProgressBar,
  StackedList,
  StackedListItem,
  TextArea,
  TextInput,
} from './primitives.tsx'

describe('shared ui primitives', () => {
  it('connects text inputs to labels, descriptions, and errors', () => {
    render(
      <TextInput
        description="Shown in the session library."
        error="A title is required."
        label="Story title"
      />,
    )

    const input = screen.getByLabelText('Story title')
    const description = screen.getByText('Shown in the session library.')
    const error = screen.getByRole('alert')
    const describedBy = input.getAttribute('aria-describedby') ?? ''

    expect(input).toHaveAttribute('aria-invalid', 'true')
    expect(describedBy).toContain(description.id)
    expect(describedBy).toContain(error.id)
  })

  it('connects text areas to labels, descriptions, and errors', () => {
    render(
      <TextArea
        description="Visible to the story-planning assistant."
        error="Message cannot be blank."
        label="Chat message"
      />,
    )

    const textarea = screen.getByLabelText('Chat message')
    const description = screen.getByText(
      'Visible to the story-planning assistant.',
    )
    const error = screen.getByRole('alert')
    const describedBy = textarea.getAttribute('aria-describedby') ?? ''

    expect(textarea).toHaveAttribute('aria-invalid', 'true')
    expect(describedBy).toContain(description.id)
    expect(describedBy).toContain(error.id)
  })

  it('renders panel headings and progress bars with semantic metadata', () => {
    render(
      <Panel
        description="Shared surfaces for the story studio."
        headingLevel={3}
        title="Workflow foundation"
      >
        <ProgressBar
          aria-label="Workflow progress"
          label="Workflow progress"
          value={45}
          valueText="45% complete"
        />
      </Panel>,
    )

    expect(
      screen.getByRole('heading', { level: 3, name: 'Workflow foundation' }),
    ).toBeInTheDocument()

    const progress = screen.getByRole('progressbar', {
      name: 'Workflow progress',
    })

    expect(progress).toHaveAttribute('aria-valuenow', '45')
    expect(progress).toHaveAttribute('aria-valuetext', '45% complete')
  })

  it('preserves ordered list semantics for stacked lists', () => {
    render(
      <StackedList as="ol">
        <StackedListItem>Genre</StackedListItem>
        <StackedListItem>Beat sheet</StackedListItem>
      </StackedList>,
    )

    expect(document.querySelector('ol.stacked-list')).not.toBeNull()
    expect(screen.getAllByRole('listitem')).toHaveLength(2)
    expect(screen.getByText('Beat sheet')).toBeInTheDocument()
  })
})
