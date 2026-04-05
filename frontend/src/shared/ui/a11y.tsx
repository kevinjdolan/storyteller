import { type AriaAttributes, useEffect, useRef } from 'react'

type LiveRegionPoliteness = 'polite' | 'assertive'

type LiveRegionProps = {
  announceOnMount?: boolean
  announcementKey?: number | string | null
  atomic?: boolean
  politeness?: LiveRegionPoliteness
  relevant?: AriaAttributes['aria-relevant']
  text: string | null
}

export function LiveRegion({
  announceOnMount = false,
  announcementKey = null,
  atomic = true,
  politeness = 'polite',
  relevant = 'additions text',
  text,
}: LiveRegionProps) {
  const regionRef = useRef<HTMLDivElement | null>(null)
  const hasMountedRef = useRef(false)

  useEffect(() => {
    const region = regionRef.current

    if (region == null) {
      return
    }

    if (!hasMountedRef.current) {
      hasMountedRef.current = true
      region.textContent = announceOnMount ? (text ?? '') : ''

      return () => {
        region.textContent = ''
      }
    }

    region.textContent = ''

    if (text == null || text.trim().length === 0) {
      return () => {
        region.textContent = ''
      }
    }

    const timeoutId = window.setTimeout(() => {
      if (regionRef.current != null) {
        regionRef.current.textContent = text
      }
    }, 20)

    return () => {
      window.clearTimeout(timeoutId)
      region.textContent = ''
    }
  }, [announceOnMount, announcementKey, text])

  return (
    <div
      aria-atomic={atomic}
      aria-live={politeness}
      aria-relevant={relevant}
      className="visually-hidden"
      ref={regionRef}
      role={politeness === 'assertive' ? 'alert' : 'status'}
    />
  )
}
