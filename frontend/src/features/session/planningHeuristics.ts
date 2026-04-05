export const DEFAULT_BEDTIME_WORDS_PER_MINUTE = 140
export const MIN_BEDTIME_WORDS_PER_MINUTE = 120
export const MAX_BEDTIME_WORDS_PER_MINUTE = 160
export const DEFAULT_CHAPTER_VARIANCE_RATIO = 0.15

const WORD_COUNT_SUGGESTION_INCREMENT = 100
const CHAPTER_WORD_COUNT_INCREMENT = 50

export type PlanningFieldId =
  | 'targetWordCount'
  | 'targetRuntimeMinutes'
  | 'chapterCount'
  | 'approximateSceneCount'
  | 'guidanceNotes'

export type RuntimeEstimate = {
  targetMinutes: number
  minimumMinutes: number
  maximumMinutes: number
}

export type WordCountEstimate = {
  targetWordCount: number
  minimumWordCount: number
  maximumWordCount: number
}

export type ChapterSizeEstimate = {
  averageWordsPerChapter: number
  minimumWordsPerChapter: number
  maximumWordsPerChapter: number
}

export type HeuristicSuggestion = {
  field: 'targetWordCount' | 'targetRuntimeMinutes'
  helpText: string
  label: string
  value: number
}

type RuntimeHeuristicInput = {
  lastEditedField: PlanningFieldId | null
  targetRuntimeMinutes: number | null
  targetWordCount: number | null
}

type StructureHeuristicInput = {
  approximateSceneCount: number | null
  chapterCount: number | null
  targetRuntimeMinutes: number | null
  targetWordCount: number | null
}

type RuntimeHeuristicSummary = {
  body: string
  suggestion: HeuristicSuggestion | null
}

function clampMinimum(value: number, minimum = 1) {
  return Math.max(minimum, value)
}

function roundToIncrement(value: number, increment: number) {
  return clampMinimum(Math.round(value / increment) * increment, increment)
}

export function estimateRuntimeFromWordCount(
  wordCount: number,
): RuntimeEstimate {
  if (wordCount <= 0) {
    return {
      targetMinutes: 0,
      minimumMinutes: 0,
      maximumMinutes: 0,
    }
  }

  return {
    targetMinutes: clampMinimum(
      Math.round(wordCount / DEFAULT_BEDTIME_WORDS_PER_MINUTE),
    ),
    minimumMinutes: clampMinimum(
      Math.floor(wordCount / MAX_BEDTIME_WORDS_PER_MINUTE),
    ),
    maximumMinutes: clampMinimum(
      Math.ceil(wordCount / MIN_BEDTIME_WORDS_PER_MINUTE),
    ),
  }
}

export function estimateWordCountFromRuntime(
  runtimeMinutes: number,
): WordCountEstimate {
  if (runtimeMinutes <= 0) {
    return {
      targetWordCount: 0,
      minimumWordCount: 0,
      maximumWordCount: 0,
    }
  }

  return {
    targetWordCount: clampMinimum(
      Math.round(runtimeMinutes * DEFAULT_BEDTIME_WORDS_PER_MINUTE),
    ),
    minimumWordCount: clampMinimum(
      Math.floor(runtimeMinutes * MIN_BEDTIME_WORDS_PER_MINUTE),
    ),
    maximumWordCount: clampMinimum(
      Math.ceil(runtimeMinutes * MAX_BEDTIME_WORDS_PER_MINUTE),
    ),
  }
}

export function estimateChapterSizeFromWordCount(
  totalWordCount: number,
  chapterCount: number,
): ChapterSizeEstimate {
  if (totalWordCount <= 0 || chapterCount <= 0) {
    return {
      averageWordsPerChapter: 0,
      minimumWordsPerChapter: 0,
      maximumWordsPerChapter: 0,
    }
  }

  const averageWordsPerChapter = clampMinimum(
    Math.round(totalWordCount / chapterCount),
  )
  const chapterVariance =
    averageWordsPerChapter * DEFAULT_CHAPTER_VARIANCE_RATIO

  return {
    averageWordsPerChapter,
    minimumWordsPerChapter: clampMinimum(
      Math.floor(averageWordsPerChapter - chapterVariance),
    ),
    maximumWordsPerChapter: clampMinimum(
      Math.ceil(averageWordsPerChapter + chapterVariance),
      averageWordsPerChapter,
    ),
  }
}

export function inferWordsPerMinute(
  targetWordCount: number,
  targetRuntimeMinutes: number,
) {
  if (targetWordCount <= 0 || targetRuntimeMinutes <= 0) {
    return 0
  }

  return clampMinimum(Math.round(targetWordCount / targetRuntimeMinutes))
}

export function classifyNarrationPacing(wordsPerMinute: number) {
  if (wordsPerMinute <= 0) {
    return 'balanced' as const
  }
  if (wordsPerMinute < MIN_BEDTIME_WORDS_PER_MINUTE) {
    return 'roomy' as const
  }
  if (wordsPerMinute > MAX_BEDTIME_WORDS_PER_MINUTE) {
    return 'brisk' as const
  }
  return 'balanced' as const
}

export function buildRuntimeHeuristicSummary({
  lastEditedField,
  targetRuntimeMinutes,
  targetWordCount,
}: RuntimeHeuristicInput): RuntimeHeuristicSummary {
  if (targetWordCount != null && targetRuntimeMinutes != null) {
    const wordsPerMinute = inferWordsPerMinute(
      targetWordCount,
      targetRuntimeMinutes,
    )
    const pacing = classifyNarrationPacing(wordsPerMinute)

    if (lastEditedField === 'targetWordCount') {
      const estimate = estimateRuntimeFromWordCount(targetWordCount)

      if (
        targetRuntimeMinutes < estimate.minimumMinutes ||
        targetRuntimeMinutes > estimate.maximumMinutes
      ) {
        return {
          body: `${targetWordCount} words in ${targetRuntimeMinutes} minutes implies about ${wordsPerMinute} words per minute, which sits outside the usual bedtime range of ${MIN_BEDTIME_WORDS_PER_MINUTE}-${MAX_BEDTIME_WORDS_PER_MINUTE}.`,
          suggestion: {
            field: 'targetRuntimeMinutes',
            helpText:
              'If you want runtime to follow this word target more closely, use the midpoint estimate.',
            label: `Use ~${estimate.targetMinutes} minutes`,
            value: estimate.targetMinutes,
          },
        }
      }
    }

    if (lastEditedField === 'targetRuntimeMinutes') {
      const estimate = estimateWordCountFromRuntime(targetRuntimeMinutes)

      if (
        targetWordCount < estimate.minimumWordCount ||
        targetWordCount > estimate.maximumWordCount
      ) {
        const suggestedWordCount = roundToIncrement(
          estimate.targetWordCount,
          WORD_COUNT_SUGGESTION_INCREMENT,
        )

        return {
          body: `${targetWordCount} words in ${targetRuntimeMinutes} minutes implies about ${wordsPerMinute} words per minute, which sits outside the usual bedtime range of ${MIN_BEDTIME_WORDS_PER_MINUTE}-${MAX_BEDTIME_WORDS_PER_MINUTE}.`,
          suggestion: {
            field: 'targetWordCount',
            helpText:
              'If you want word count to follow this runtime more closely, use the midpoint estimate.',
            label: `Use ${suggestedWordCount} words`,
            value: suggestedWordCount,
          },
        }
      }
    }

    if (pacing === 'brisk') {
      return {
        body: `${targetWordCount} words in ${targetRuntimeMinutes} minutes implies about ${wordsPerMinute} words per minute, which may feel brisk for bedtime narration.`,
        suggestion: null,
      }
    }

    if (pacing === 'roomy') {
      return {
        body: `${targetWordCount} words in ${targetRuntimeMinutes} minutes implies about ${wordsPerMinute} words per minute, which leaves a very roomy read-aloud pace.`,
        suggestion: null,
      }
    }

    return {
      body: `${targetWordCount} words in ${targetRuntimeMinutes} minutes implies about ${wordsPerMinute} words per minute, which stays inside the usual bedtime range.`,
      suggestion: null,
    }
  }

  if (targetWordCount != null) {
    const estimate = estimateRuntimeFromWordCount(targetWordCount)

    return {
      body: `${targetWordCount} words usually reads aloud in about ${estimate.targetMinutes} minutes, often somewhere near ${estimate.minimumMinutes}-${estimate.maximumMinutes}.`,
      suggestion:
        lastEditedField === 'targetWordCount'
          ? {
              field: 'targetRuntimeMinutes',
              helpText:
                'Apply the midpoint runtime if you want the related field filled in for you.',
              label: `Use ~${estimate.targetMinutes} minutes`,
              value: estimate.targetMinutes,
            }
          : null,
    }
  }

  if (targetRuntimeMinutes != null) {
    const estimate = estimateWordCountFromRuntime(targetRuntimeMinutes)
    const suggestedWordCount = roundToIncrement(
      estimate.targetWordCount,
      WORD_COUNT_SUGGESTION_INCREMENT,
    )

    return {
      body: `${targetRuntimeMinutes} minutes usually lands near ${suggestedWordCount} words, often somewhere around ${roundToIncrement(estimate.minimumWordCount, WORD_COUNT_SUGGESTION_INCREMENT)}-${roundToIncrement(estimate.maximumWordCount, WORD_COUNT_SUGGESTION_INCREMENT)}.`,
      suggestion:
        lastEditedField === 'targetRuntimeMinutes'
          ? {
              field: 'targetWordCount',
              helpText:
                'Apply the midpoint word count if you want the related field filled in for you.',
              label: `Use ${suggestedWordCount} words`,
              value: suggestedWordCount,
            }
          : null,
    }
  }

  return {
    body: 'Word count and runtime can stay approximate. The goal is a believable bedtime pace, not exact numeric compliance.',
    suggestion: null,
  }
}

function buildSceneDensityHint(
  chapterCount: number | null,
  approximateSceneCount: number | null,
) {
  if (chapterCount != null && approximateSceneCount != null) {
    const scenesPerChapter = approximateSceneCount / chapterCount
    const rounded =
      Number.isInteger(scenesPerChapter) || Math.abs(scenesPerChapter) >= 10
        ? String(Math.round(scenesPerChapter))
        : scenesPerChapter.toFixed(1)

    return `That works out to about ${rounded} scene${rounded === '1' ? '' : 's'} per chapter.`
  }

  if (chapterCount != null) {
    return 'Chapter count sets the broad pacing shape; chapter lengths can still breathe a little.'
  }

  if (approximateSceneCount != null) {
    return 'Scene count can stay loose. Chapters can be grouped later once the writing finds its rhythm.'
  }

  return 'Chapters and scenes are planning containers. They help shape pacing without locking the story into equal slices.'
}

export function buildStructureHeuristicSummary({
  approximateSceneCount,
  chapterCount,
  targetRuntimeMinutes,
  targetWordCount,
}: StructureHeuristicInput) {
  const structureBits: string[] = []

  if (chapterCount != null && targetWordCount != null) {
    const estimate = estimateChapterSizeFromWordCount(
      targetWordCount,
      chapterCount,
    )

    structureBits.push(
      `${chapterCount} chapter${chapterCount === 1 ? '' : 's'} at ${targetWordCount} words usually lands near ${roundToIncrement(estimate.averageWordsPerChapter, CHAPTER_WORD_COUNT_INCREMENT)} words per chapter, often roughly ${roundToIncrement(estimate.minimumWordsPerChapter, CHAPTER_WORD_COUNT_INCREMENT)}-${roundToIncrement(estimate.maximumWordsPerChapter, CHAPTER_WORD_COUNT_INCREMENT)}.`,
    )
  } else if (chapterCount != null && targetRuntimeMinutes != null) {
    const wordEstimate = estimateWordCountFromRuntime(targetRuntimeMinutes)
    const chapterEstimate = estimateChapterSizeFromWordCount(
      wordEstimate.targetWordCount,
      chapterCount,
    )

    structureBits.push(
      `At a calm pace, ${targetRuntimeMinutes} minutes across ${chapterCount} chapter${chapterCount === 1 ? '' : 's'} often means about ${roundToIncrement(chapterEstimate.averageWordsPerChapter, CHAPTER_WORD_COUNT_INCREMENT)} words per chapter.`,
    )
  }

  structureBits.push(buildSceneDensityHint(chapterCount, approximateSceneCount))

  return structureBits.join(' ')
}

export function buildPlanningAssumptionsText() {
  return `Read-aloud estimates assume about ${DEFAULT_BEDTIME_WORDS_PER_MINUTE} words per minute, with most bedtime narration landing between ${MIN_BEDTIME_WORDS_PER_MINUTE} and ${MAX_BEDTIME_WORDS_PER_MINUTE}. Chapter sizing assumes individual chapters can drift by about ${Math.round(DEFAULT_CHAPTER_VARIANCE_RATIO * 100)}% around the average rather than matching perfectly.`
}
