import type {
  StoryReaderBlockView,
  StoryReaderDocumentView,
  StoryReaderSpanView,
} from '../../api/sessions.ts'

type StoryReaderProps = {
  document: StoryReaderDocumentView
}

type StoryReaderSection = {
  blocks: StoryReaderBlockView[]
  heading: StoryReaderBlockView | null
}

export function StoryReader({ document }: StoryReaderProps) {
  const sections = buildStoryReaderSections(document.blocks)

  return (
    <article className="story-reader" data-format-version={document.format_version}>
      {sections.map((section, index) => (
        <section
          className={
            section.heading != null
              ? 'story-reader__chapter'
              : 'story-reader__section'
          }
          key={`story-section-${index}`}
        >
          {section.heading != null ? (
            <header className="story-reader__chapter-header">
              {renderStoryReaderHeading(section.heading)}
            </header>
          ) : null}

          <div className="story-reader__flow">
            {section.blocks.map((block, blockIndex) => {
              if (block.kind === 'paragraph') {
                return (
                  <p key={`story-block-${index}-${blockIndex}`}>
                    {renderStoryReaderSpans(block.spans)}
                  </p>
                )
              }

              return (
                <h5 key={`story-block-${index}-${blockIndex}`}>
                  {renderStoryReaderSpans(block.spans)}
                </h5>
              )
            })}
          </div>
        </section>
      ))}
    </article>
  )
}

function buildStoryReaderSections(
  blocks: StoryReaderBlockView[],
): StoryReaderSection[] {
  const sections: StoryReaderSection[] = []
  let currentSection: StoryReaderSection = {
    heading: null,
    blocks: [],
  }

  for (const block of blocks) {
    if (block.kind === 'chapter_heading') {
      if (currentSection.heading != null || currentSection.blocks.length > 0) {
        sections.push(currentSection)
      }
      currentSection = {
        heading: block,
        blocks: [],
      }
      continue
    }

    currentSection.blocks.push(block)
  }

  if (currentSection.heading != null || currentSection.blocks.length > 0) {
    sections.push(currentSection)
  }

  return sections
}

function renderStoryReaderHeading(block: StoryReaderBlockView) {
  return <h4>{renderStoryReaderSpans(block.spans)}</h4>
}

function renderStoryReaderSpans(spans: StoryReaderSpanView[]) {
  return spans.map((span, index) => {
    if (span.style === 'emphasis') {
      return <em key={`story-span-${index}`}>{span.text}</em>
    }

    if (span.style === 'strong') {
      return <strong key={`story-span-${index}`}>{span.text}</strong>
    }

    if (span.style === 'strong_emphasis') {
      return (
        <strong key={`story-span-${index}`}>
          <em>{span.text}</em>
        </strong>
      )
    }

    return <span key={`story-span-${index}`}>{span.text}</span>
  })
}
