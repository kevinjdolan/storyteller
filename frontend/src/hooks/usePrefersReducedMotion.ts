import { useEffect, useState } from 'react'

const reducedMotionQuery = '(prefers-reduced-motion: reduce)'

function getInitialPreference() {
  if (
    typeof window === 'undefined' ||
    typeof window.matchMedia !== 'function'
  ) {
    return false
  }

  return window.matchMedia(reducedMotionQuery).matches
}

export function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] =
    useState(getInitialPreference)

  useEffect(() => {
    if (
      typeof window === 'undefined' ||
      typeof window.matchMedia !== 'function'
    ) {
      return
    }

    const mediaQueryList = window.matchMedia(reducedMotionQuery)
    const updatePreference = () => {
      setPrefersReducedMotion(mediaQueryList.matches)
    }

    updatePreference()

    if (typeof mediaQueryList.addEventListener === 'function') {
      mediaQueryList.addEventListener('change', updatePreference)

      return () => {
        mediaQueryList.removeEventListener('change', updatePreference)
      }
    }

    mediaQueryList.addListener(updatePreference)

    return () => {
      mediaQueryList.removeListener(updatePreference)
    }
  }, [])

  return prefersReducedMotion
}
