import { describe, expect, it } from 'vitest'
import { buildSegmentDiffSummary } from './segmentVersionDiff.ts'

describe('buildSegmentDiffSummary', () => {
  it('captures replacement regions and word counts', () => {
    const diff = buildSegmentDiffSummary(
      'Mira followed the bell toward the quieter cove.',
      'Mira followed the bell into the lantern cove.',
    )

    expect(diff.addedWords).toBe(2)
    expect(diff.removedWords).toBe(2)
    expect(diff.changedRegionCount).toBe(2)
    expect(diff.regions).toEqual([
      {
        beforeText: 'toward',
        afterText: 'into',
        kind: 'replacement',
      },
      {
        beforeText: 'quieter',
        afterText: 'lantern',
        kind: 'replacement',
      },
    ])
  })

  it('captures additions and removals separately', () => {
    const added = buildSegmentDiffSummary(
      'The harbor settled into silence.',
      'The harbor settled into a softer silence beside Pip.',
    )
    expect(added.regions).toEqual([
      {
        beforeText: 'silence.',
        afterText: 'a softer silence beside Pip.',
        kind: 'replacement',
      },
    ])

    const removed = buildSegmentDiffSummary(
      'Pip stayed close while Mira crossed the dock.',
      'Mira crossed the dock.',
    )
    expect(removed.regions[0]).toEqual({
      beforeText: 'Pip stayed close while',
      afterText: '',
      kind: 'removal',
    })
  })
})
