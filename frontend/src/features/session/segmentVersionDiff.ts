export type SegmentDiffKind = 'unchanged' | 'added' | 'removed'

export type SegmentDiffPart = {
  kind: SegmentDiffKind
  value: string
}

export type SegmentDiffRegion = {
  afterText: string
  beforeText: string
  kind: 'addition' | 'removal' | 'replacement'
}

export type SegmentDiffSummary = {
  addedWords: number
  changedRegionCount: number
  parts: SegmentDiffPart[]
  regions: SegmentDiffRegion[]
  removedWords: number
}

function tokenizeForDiff(value: string) {
  return value.match(/\S+\s*|\s+/gu) ?? []
}

function countWords(value: string) {
  const trimmedValue = value.trim()
  if (trimmedValue.length === 0) {
    return 0
  }

  return trimmedValue.split(/\s+/u).length
}

function mergeAdjacentParts(parts: SegmentDiffPart[]) {
  return parts.reduce<SegmentDiffPart[]>((mergedParts, part) => {
    const previousPart = mergedParts.at(-1)
    if (previousPart?.kind === part.kind) {
      previousPart.value += part.value
      return mergedParts
    }

    mergedParts.push({ ...part })
    return mergedParts
  }, [])
}

function buildDiffParts(beforeText: string, afterText: string) {
  const beforeTokens = tokenizeForDiff(beforeText)
  const afterTokens = tokenizeForDiff(afterText)
  const matrix = Array.from({ length: beforeTokens.length + 1 }, () =>
    Array<number>(afterTokens.length + 1).fill(0),
  )

  for (
    let beforeIndex = 1;
    beforeIndex <= beforeTokens.length;
    beforeIndex += 1
  ) {
    for (
      let afterIndex = 1;
      afterIndex <= afterTokens.length;
      afterIndex += 1
    ) {
      if (beforeTokens[beforeIndex - 1] === afterTokens[afterIndex - 1]) {
        matrix[beforeIndex][afterIndex] =
          matrix[beforeIndex - 1][afterIndex - 1] + 1
        continue
      }

      matrix[beforeIndex][afterIndex] = Math.max(
        matrix[beforeIndex - 1][afterIndex],
        matrix[beforeIndex][afterIndex - 1],
      )
    }
  }

  const diffParts: SegmentDiffPart[] = []
  let beforeIndex = beforeTokens.length
  let afterIndex = afterTokens.length

  while (beforeIndex > 0 || afterIndex > 0) {
    if (
      beforeIndex > 0 &&
      afterIndex > 0 &&
      beforeTokens[beforeIndex - 1] === afterTokens[afterIndex - 1]
    ) {
      diffParts.push({
        kind: 'unchanged',
        value: beforeTokens[beforeIndex - 1],
      })
      beforeIndex -= 1
      afterIndex -= 1
      continue
    }

    const leftScore =
      afterIndex > 0
        ? matrix[beforeIndex][afterIndex - 1]
        : Number.NEGATIVE_INFINITY
    const upScore =
      beforeIndex > 0
        ? matrix[beforeIndex - 1][afterIndex]
        : Number.NEGATIVE_INFINITY

    if (afterIndex > 0 && leftScore >= upScore) {
      diffParts.push({
        kind: 'added',
        value: afterTokens[afterIndex - 1],
      })
      afterIndex -= 1
      continue
    }

    if (beforeIndex > 0) {
      diffParts.push({
        kind: 'removed',
        value: beforeTokens[beforeIndex - 1],
      })
      beforeIndex -= 1
    }
  }

  return mergeAdjacentParts(diffParts.reverse())
}

function truncateSnippet(value: string, maximumLength = 180) {
  const normalizedValue = value.trim()
  if (normalizedValue.length <= maximumLength) {
    return normalizedValue
  }

  return `${normalizedValue.slice(0, maximumLength - 3).trimEnd()}...`
}

function buildDiffRegions(parts: SegmentDiffPart[], maximumRegions = 6) {
  const regions: SegmentDiffRegion[] = []
  let partIndex = 0

  while (partIndex < parts.length && regions.length < maximumRegions) {
    if (parts[partIndex]?.kind === 'unchanged') {
      partIndex += 1
      continue
    }

    let beforeText = ''
    let afterText = ''

    while (partIndex < parts.length && parts[partIndex]?.kind !== 'unchanged') {
      const part = parts[partIndex]
      if (part.kind === 'removed') {
        beforeText += part.value
      } else if (part.kind === 'added') {
        afterText += part.value
      }
      partIndex += 1
    }

    const normalizedBeforeText = truncateSnippet(beforeText)
    const normalizedAfterText = truncateSnippet(afterText)
    if (normalizedBeforeText.length === 0 && normalizedAfterText.length === 0) {
      continue
    }

    regions.push({
      beforeText: normalizedBeforeText,
      afterText: normalizedAfterText,
      kind:
        normalizedBeforeText.length === 0
          ? 'addition'
          : normalizedAfterText.length === 0
            ? 'removal'
            : 'replacement',
    })
  }

  return regions
}

export function buildSegmentDiffSummary(
  beforeText: string | null | undefined,
  afterText: string | null | undefined,
): SegmentDiffSummary {
  const normalizedBeforeText = beforeText ?? ''
  const normalizedAfterText = afterText ?? ''
  const parts = buildDiffParts(normalizedBeforeText, normalizedAfterText)

  return {
    addedWords: countWords(
      parts
        .filter((part) => part.kind === 'added')
        .map((part) => part.value)
        .join(''),
    ),
    changedRegionCount: buildDiffRegions(parts).length,
    parts,
    regions: buildDiffRegions(parts),
    removedWords: countWords(
      parts
        .filter((part) => part.kind === 'removed')
        .map((part) => part.value)
        .join(''),
    ),
  }
}
