import { resolveApiUrl } from '../../api/client.ts'
import type { SessionAssetView } from '../../api/sessions.ts'

export type SessionArtifactHandle = 'story-docx' | 'final-audio'

export function resolveSessionAssetStreamUrl(
  asset: SessionAssetView | null | undefined,
) {
  const streamPath = asset?.access?.stream_path ?? null
  if (streamPath == null) {
    return null
  }
  return resolveBackendAssetUrl(streamPath)
}

export function resolveSessionAssetDownloadUrl(
  asset: SessionAssetView | null | undefined,
) {
  const downloadPath = asset?.access?.download_path ?? null
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

export async function fetchSessionAssetText(
  asset: SessionAssetView | null | undefined,
) {
  const textUrl =
    resolveSessionAssetStreamUrl(asset) ?? resolveSessionAssetDownloadUrl(asset)
  if (textUrl == null) {
    throw new Error('The requested text asset is not readable yet.')
  }

  const response = await fetch(textUrl)
  if (!response.ok) {
    throw new Error(`Unexpected status code: ${response.status}`)
  }

  return response.text()
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
  if (!url.startsWith('/')) {
    return null
  }
  return resolveApiUrl(url as `/${string}`)
}
