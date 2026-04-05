import { describe, expect, it } from 'vitest'
import {
  buildSessionArtifactDownloadUrl,
  resolveSessionAssetDownloadUrl,
  resolveSessionAssetStreamUrl,
} from './sessionArtifacts.ts'

describe('sessionArtifacts', () => {
  it('resolves backend-relative asset paths through the configured API base', () => {
    const asset = {
      id: 'asset-1',
      asset_kind: 'final_audio',
      status: 'ready',
      access: {
        download_path:
          '/api/v1/sessions/moonlit/assets/asset-1/content?disposition=attachment',
        filename: 'story.mp3',
        stream_path:
          '/api/v1/sessions/moonlit/assets/asset-1/content?disposition=inline',
      },
    }

    expect(resolveSessionAssetStreamUrl(asset)).toBe(
      '/api/v1/sessions/moonlit/assets/asset-1/content?disposition=inline',
    )
    expect(resolveSessionAssetDownloadUrl(asset)).toBe(
      '/api/v1/sessions/moonlit/assets/asset-1/content?disposition=attachment',
    )
  })

  it('builds named artifact downloads through the backend API', () => {
    expect(
      buildSessionArtifactDownloadUrl('moonlit-harbor', 'story-docx'),
    ).toBe('/api/v1/sessions/moonlit-harbor/artifacts/story-docx')
  })

  it('ignores non-backend asset URLs even if legacy fields are present', () => {
    const asset = {
      id: 'asset-2',
      asset_kind: 'final_audio',
      status: 'ready',
      access: {
        download_path: 'https://example.com/story.mp3',
        filename: 'story.mp3',
        stream_path: 'https://example.com/story.mp3',
      },
      public_url: 'https://example.com/story.mp3',
    }

    expect(resolveSessionAssetStreamUrl(asset)).toBeNull()
    expect(resolveSessionAssetDownloadUrl(asset)).toBeNull()
  })
})
