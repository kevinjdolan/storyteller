import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import {
  afterAll,
  afterEach,
  beforeAll,
  describe,
  expect,
  it,
  vi,
} from 'vitest'
import type { SessionAssetView } from '../../api/sessions.ts'
import type { AudioPlaybackMarker } from './finalizeAudioSync.ts'
import { FinalizeAudioPlayer } from './FinalizeAudioPlayer.tsx'

type TestMediaElement = HTMLMediaElement & {
  __currentTime?: number
  __duration?: number
  __ended?: boolean
  __paused?: boolean
  __playbackRate?: number
}

const baseAsset: SessionAssetView = {
  id: 'final-audio-1',
  asset_kind: 'final_audio',
  status: 'ready',
  duration_seconds: 120,
}

const baseMarkers: AudioPlaybackMarker[] = [
  {
    id: 'outline:chapter-1',
    order: 1,
    kind: 'chapter',
    label: 'Lantern Wake',
    startSeconds: 0,
    endSeconds: 45,
    segmentIndexes: [1],
    sourceOutlineCardKey: 'chapter-1',
    sourceOutlineCardTitle: 'Lantern Wake',
  },
  {
    id: 'outline:chapter-2',
    order: 2,
    kind: 'chapter',
    label: 'Moonlit Crossing',
    startSeconds: 45,
    endSeconds: 120,
    segmentIndexes: [2],
    sourceOutlineCardKey: 'chapter-2',
    sourceOutlineCardTitle: 'Moonlit Crossing',
  },
]

const originalCurrentTime = Object.getOwnPropertyDescriptor(
  HTMLMediaElement.prototype,
  'currentTime',
)
const originalDuration = Object.getOwnPropertyDescriptor(
  HTMLMediaElement.prototype,
  'duration',
)
const originalPaused = Object.getOwnPropertyDescriptor(
  HTMLMediaElement.prototype,
  'paused',
)
const originalEnded = Object.getOwnPropertyDescriptor(
  HTMLMediaElement.prototype,
  'ended',
)
const originalPlaybackRate = Object.getOwnPropertyDescriptor(
  HTMLMediaElement.prototype,
  'playbackRate',
)

beforeAll(() => {
  Object.defineProperty(HTMLMediaElement.prototype, 'currentTime', {
    configurable: true,
    get(this: TestMediaElement) {
      return this.__currentTime ?? 0
    },
    set(this: TestMediaElement, value: number) {
      this.__currentTime = value
    },
  })
  Object.defineProperty(HTMLMediaElement.prototype, 'duration', {
    configurable: true,
    get(this: TestMediaElement) {
      return this.__duration ?? Number.NaN
    },
  })
  Object.defineProperty(HTMLMediaElement.prototype, 'paused', {
    configurable: true,
    get(this: TestMediaElement) {
      return this.__paused ?? true
    },
  })
  Object.defineProperty(HTMLMediaElement.prototype, 'ended', {
    configurable: true,
    get(this: TestMediaElement) {
      return this.__ended ?? false
    },
  })
  Object.defineProperty(HTMLMediaElement.prototype, 'playbackRate', {
    configurable: true,
    get(this: TestMediaElement) {
      return this.__playbackRate ?? 1
    },
    set(this: TestMediaElement, value: number) {
      this.__playbackRate = value
    },
  })
})

afterEach(() => {
  vi.restoreAllMocks()
  window.localStorage.clear()
})

afterAll(() => {
  restoreMediaProperty('currentTime', originalCurrentTime)
  restoreMediaProperty('duration', originalDuration)
  restoreMediaProperty('paused', originalPaused)
  restoreMediaProperty('ended', originalEnded)
  restoreMediaProperty('playbackRate', originalPlaybackRate)
})

describe('FinalizeAudioPlayer', () => {
  it('supports play, seek, speed changes, and marker jumps', async () => {
    const onCurrentTimeChange = vi.fn()
    const playMock = vi
      .spyOn(HTMLMediaElement.prototype, 'play')
      .mockImplementation(function (this: TestMediaElement) {
        this.__paused = false
        this.dispatchEvent(new Event('play'))
        return Promise.resolve()
      })
    const pauseMock = vi
      .spyOn(HTMLMediaElement.prototype, 'pause')
      .mockImplementation(function (this: TestMediaElement) {
        this.__paused = true
        this.dispatchEvent(new Event('pause'))
      })

    render(
      <FinalizeAudioPlayer
        asset={baseAsset}
        currentTime={0}
        markers={baseMarkers}
        onCurrentTimeChange={onCurrentTimeChange}
        storageNamespace="session-1"
        streamUrl="http://localhost/audio.wav"
      />,
    )

    const audio = screen.getByLabelText(
      'Final narration preview',
    ) as TestMediaElement
    audio.__duration = 120
    fireEvent.loadedMetadata(audio)

    fireEvent.click(screen.getByRole('button', { name: 'Play narration' }))
    await waitFor(() => {
      expect(playMock).toHaveBeenCalledTimes(1)
      expect(
        screen.getByRole('button', { name: 'Pause narration' }),
      ).toBeInTheDocument()
    })

    fireEvent.click(screen.getByRole('button', { name: '1.3x' }))
    expect(audio.playbackRate).toBe(1.3)

    const seekInput = screen.getByLabelText(
      'Seek narration',
    ) as HTMLInputElement
    fireEvent.change(seekInput, { target: { value: '32.5' } })
    expect(audio.currentTime).toBe(32.5)

    audio.currentTime = 32.5
    fireEvent.timeUpdate(audio)
    expect(onCurrentTimeChange).toHaveBeenLastCalledWith(32.5)

    fireEvent.click(screen.getByRole('button', { name: /Moonlit Crossing/ }))
    expect(audio.currentTime).toBe(45)
    expect(
      window.localStorage.getItem(
        'storyteller:audio-player:session-1:final-audio-1',
      ),
    ).toContain('"playbackRate":1.3')

    fireEvent.click(screen.getByRole('button', { name: 'Pause narration' }))
    expect(pauseMock).toHaveBeenCalledTimes(1)
  })

  it('restores the saved playback position and rate after reload', () => {
    const onCurrentTimeChange = vi.fn()
    window.localStorage.setItem(
      'storyteller:audio-player:session-1:final-audio-1',
      JSON.stringify({
        assetId: 'final-audio-1',
        currentTime: 72.5,
        isPlaying: true,
        playbackRate: 1.15,
      }),
    )

    render(
      <FinalizeAudioPlayer
        asset={baseAsset}
        currentTime={0}
        markers={baseMarkers}
        onCurrentTimeChange={onCurrentTimeChange}
        storageNamespace="session-1"
        streamUrl="http://localhost/audio.wav"
      />,
    )

    const audio = screen.getByLabelText(
      'Final narration preview',
    ) as TestMediaElement
    audio.__duration = 120
    fireEvent.loadedMetadata(audio)

    expect(audio.currentTime).toBe(72.5)
    expect(audio.playbackRate).toBe(1.15)
    expect(onCurrentTimeChange).toHaveBeenCalledWith(72.5)
    expect(
      screen.getByText(
        'Playback position restored to 1:12. Press play to continue.',
      ),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '1.15x' })).toHaveAttribute(
      'aria-pressed',
      'true',
    )
  })
})

function restoreMediaProperty(
  property: 'currentTime' | 'duration' | 'paused' | 'ended' | 'playbackRate',
  descriptor: PropertyDescriptor | undefined,
) {
  if (descriptor == null) {
    Reflect.deleteProperty(HTMLMediaElement.prototype, property)
    return
  }

  Object.defineProperty(HTMLMediaElement.prototype, property, descriptor)
}
