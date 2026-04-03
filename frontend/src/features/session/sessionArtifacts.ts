import { resolveApiUrl } from '../../api/client.ts'
import type { SessionAssetView } from '../../api/sessions.ts'

export type SessionArtifactHandle = 'story-docx' | 'final-audio'

export function resolveSessionAssetStreamUrl(
  asset: SessionAssetView | null | undefined,
) {
  const streamPath = asset?.access?.stream_path ?? asset?.public_url ?? null
  if (streamPath == null) {
    return null
  }
  return resolveBackendAssetUrl(streamPath)
}

export function resolveSessionAssetDownloadUrl(
  asset: SessionAssetView | null | undefined,
) {
  const downloadPath = asset?.access?.download_path ?? asset?.public_url ?? null
  if (downloadPath == null) {
    return null
  }
  return resolveBackendAssetUrl(downloadPath)
}

export function buildSessionArtifactDownloadUrl(
  sessionId: string,
  artifactHandle: SessionArtifactHandle,
) {
  return resolveApiUrl(
    `/api/v1/sessions/${encodeURIComponent(sessionId)}/artifacts/${encodeURIComponent(artifactHandle)}` as `/${string}`,
  )
}

export function triggerArtifactDownload(url: string) {
  const link = document.createElement('a')
  link.href = url
  link.rel = 'noopener'
  link.style.display = 'none'
  document.body.append(link)
  link.click()
  link.remove()
}

function resolveBackendAssetUrl(url: string) {
  if (/^https?:\/\//i.test(url)) {
    return url
  }
  return resolveApiUrl(url as `/${string}`)
}
