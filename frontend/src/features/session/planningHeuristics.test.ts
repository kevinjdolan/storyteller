import { describe, expect, it } from 'vitest'
import {
  buildPlanningAssumptionsText,
  buildRuntimeHeuristicSummary,
  buildStructureHeuristicSummary,
  estimateChapterSizeFromWordCount,
  estimateRuntimeFromWordCount,
  estimateWordCountFromRuntime,
} from './planningHeuristics.ts'

describe('planningHeuristics', () => {
  it('estimates runtime and word count with the bedtime pacing band', () => {
    expect(estimateRuntimeFromWordCount(1800)).toEqual({
      targetMinutes: 13,
      minimumMinutes: 11,
      maximumMinutes: 15,
    })
    expect(estimateWordCountFromRuntime(12)).toEqual({
      targetWordCount: 1680,
      minimumWordCount: 1440,
      maximumWordCount: 1920,
    })
  })

  it('estimates chapter size with a modest drift around the average', () => {
    expect(estimateChapterSizeFromWordCount(1800, 3)).toEqual({
      averageWordsPerChapter: 600,
      minimumWordsPerChapter: 510,
      maximumWordsPerChapter: 690,
    })
  })

  it('offers an explicit runtime suggestion without auto-overwriting the field', () => {
    const summary = buildRuntimeHeuristicSummary({
      lastEditedField: 'targetWordCount',
      targetWordCount: 1800,
      targetRuntimeMinutes: null,
    })

    expect(summary.body).toContain(
      '1800 words usually reads aloud in about 13 minutes',
    )
    expect(summary.suggestion).toEqual({
      field: 'targetRuntimeMinutes',
      helpText:
        'Apply the midpoint runtime if you want the related field filled in for you.',
      label: 'Use ~13 minutes',
      value: 13,
    })
  })

  it('combines chapter sizing and scene density into one structure summary', () => {
    expect(
      buildStructureHeuristicSummary({
        approximateSceneCount: 8,
        chapterCount: 3,
        targetRuntimeMinutes: null,
        targetWordCount: 1800,
      }),
    ).toContain(
      '3 chapters at 1800 words usually lands near 600 words per chapter, often roughly 500-700. That works out to about 2.7 scenes per chapter.',
    )
  })

  it('keeps the heuristic assumptions inspectable', () => {
    expect(buildPlanningAssumptionsText()).toContain('140 words per minute')
    expect(buildPlanningAssumptionsText()).toContain('15%')
  })
})
