import { screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import type { StoryReaderDocumentView } from '../../api/sessions.ts'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import { StoryReader } from './StoryReader.tsx'

const document: StoryReaderDocumentView = {
  format_version: 'story_reader.v1',
  asset_id: 'story-asset-1',
  word_count: 29,
  chapter_count: 2,
  has_structure: true,
  blocks: [
    {
      kind: 'chapter_heading',
      level: 1,
      text: 'Chapter 1: Lantern Wake',
      spans: [{ text: 'Chapter 1: Lantern Wake', style: 'plain' }],
    },
    {
      kind: 'paragraph',
      text: 'Mira carried a soft lantern home.',
      spans: [
        { text: 'Mira carried a ', style: 'plain' },
        { text: 'soft', style: 'emphasis' },
        { text: ' lantern home.', style: 'plain' },
      ],
    },
    {
      kind: 'heading',
      level: 3,
      text: 'A Quiet Promise',
      spans: [{ text: 'A Quiet Promise', style: 'plain' }],
    },
    {
      kind: 'paragraph',
      text: 'Otis whispered the harbor was safe.',
      spans: [
        { text: 'Otis whispered the harbor was ', style: 'plain' },
        { text: 'safe', style: 'strong' },
        { text: '.', style: 'plain' },
      ],
    },
    {
      kind: 'chapter_heading',
      level: 1,
      text: 'Chapter 2: Bell Water',
      spans: [{ text: 'Chapter 2: Bell Water', style: 'plain' }],
    },
    {
      kind: 'paragraph',
      text: 'The cove felt deeply calm.',
      spans: [
        { text: 'The cove felt ', style: 'plain' },
        { text: 'deeply calm', style: 'strong_emphasis' },
        { text: '.', style: 'plain' },
      ],
    },
  ],
}

describe('StoryReader', () => {
  it('renders chapter sections and inline emphasis from the reader document', () => {
    renderWithAppProviders(<StoryReader document={document} />)

    expect(
      screen.getByRole('heading', { name: 'Chapter 1: Lantern Wake' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'Chapter 2: Bell Water' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'A Quiet Promise' }),
    ).toBeInTheDocument()

    const emphasizedWord = screen.getByText('soft')
    expect(emphasizedWord.tagName).toBe('EM')

    const strongWord = screen.getByText('safe')
    expect(strongWord.tagName).toBe('STRONG')

    const strongEmphasisText = screen.getByText('deeply calm')
    expect(strongEmphasisText.tagName).toBe('EM')
    expect(strongEmphasisText.parentElement?.tagName).toBe('STRONG')
  })
})
