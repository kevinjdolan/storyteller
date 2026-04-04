import { useId, useMemo, useRef, useState } from 'react'
import type { SessionAssetView } from '../../api/sessions.ts'
import { Button } from '../../shared/ui/primitives.tsx'
import type { AudioPlaybackMarker } from './finalizeAudioSync.ts'

type FinalizeAudioPlayerProps = {
  asset: SessionAssetView
  currentTime: number
  markers: AudioPlaybackMarker[]
  onCurrentTimeChange: (value: number) => void
  streamUrl: string
  storageNamespace: string
}

type PersistedAudioPlaybackState = {
  assetId: string
  currentTime: number
  isPlaying: boolean
  playbackRate: number
}

const playbackSpeedOptions = [0.8, 1, 1.15, 1.3]

export function FinalizeAudioPlayer({
  asset,
  currentTime,
  markers,
  onCurrentTimeChange,
  storageNamespace,
  streamUrl,
}: FinalizeAudioPlayerProps) {
  const storageKey = useMemo(
    () => `storyteller:audio-player:${storageNamespace}:${asset.id}`,
    [asset.id, storageNamespace],
  )
  const persistedPlaybackState = useMemo(
    () => readPersistedPlaybackState(storageKey, asset.id),
    [asset.id, storageKey],
  )
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const restoredPlaybackRef = useRef<PersistedAudioPlaybackState | null>(
    persistedPlaybackState,
  )
  const lastPersistedStateRef = useRef<PersistedAudioPlaybackState | null>(null)
  const [duration, setDuration] = useState(asset.duration_seconds ?? 0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackRate, setPlaybackRate] = useState(
    persistedPlaybackState?.playbackRate ?? 1,
  )
  const [playerError, setPlayerError] = useState<string | null>(null)
  const [restoreNotice, setRestoreNotice] = useState<string | null>(null)
  const seekInputId = useId()

  function persistPlaybackState(
    nextState: PersistedAudioPlaybackState,
    options?: { force?: boolean },
  ) {
    if (typeof window === 'undefined') {
      return
    }

    const previousState = lastPersistedStateRef.current
    const shouldPersist =
      options?.force === true ||
      previousState == null ||
      previousState.assetId !== nextState.assetId ||
      previousState.isPlaying !== nextState.isPlaying ||
      previousState.playbackRate !== nextState.playbackRate ||
      Math.abs(previousState.currentTime - nextState.currentTime) >= 1

    if (!shouldPersist) {
      return
    }

    try {
      window.localStorage.setItem(storageKey, JSON.stringify(nextState))
      lastPersistedStateRef.current = nextState
    } catch {
      // Ignore storage failures so playback keeps working.
    }
  }

  function buildPlaybackStateSnapshot(
    overrides?: Partial<Omit<PersistedAudioPlaybackState, 'assetId'>>,
  ): PersistedAudioPlaybackState {
    const audioElement = audioRef.current
    return {
      assetId: asset.id,
      currentTime:
        overrides?.currentTime ??
        (audioElement != null && Number.isFinite(audioElement.currentTime)
          ? audioElement.currentTime
          : currentTime),
      isPlaying:
        overrides?.isPlaying ??
        (audioElement != null ? !audioElement.paused && !audioElement.ended : false),
      playbackRate:
        overrides?.playbackRate ??
        (audioElement != null ? audioElement.playbackRate : playbackRate),
    }
  }

  function applyPlaybackRate(nextPlaybackRate: number) {
    const audioElement = audioRef.current
    if (audioElement != null) {
      audioElement.playbackRate = nextPlaybackRate
    }
    setPlaybackRate(nextPlaybackRate)
    persistPlaybackState(
      buildPlaybackStateSnapshot({
        playbackRate: nextPlaybackRate,
      }),
      { force: true },
    )
  }

  async function togglePlayback() {
    const audioElement = audioRef.current
    if (audioElement == null) {
      return
    }

    setPlayerError(null)

    if (!audioElement.paused) {
      audioElement.pause()
      return
    }

    try {
      await audioElement.play()
    } catch (error) {
      setPlayerError(
        error instanceof Error
          ? error.message
          : 'Playback could not start in this browser session.',
      )
    }
  }

  function seekTo(nextTime: number) {
    const audioElement = audioRef.current
    if (audioElement == null) {
      return
    }

    const clampedTime = clamp(nextTime, 0, duration > 0 ? duration : nextTime)
    audioElement.currentTime = clampedTime
    onCurrentTimeChange(clampedTime)
    persistPlaybackState(
      buildPlaybackStateSnapshot({
        currentTime: clampedTime,
      }),
      { force: true },
    )
  }

  function handleLoadedMetadata() {
    const audioElement = audioRef.current
    if (audioElement == null) {
      return
    }

    const resolvedDuration =
      Number.isFinite(audioElement.duration) && audioElement.duration > 0
        ? audioElement.duration
        : (asset.duration_seconds ?? 0)

    setDuration(resolvedDuration)

    const restoredPlayback = restoredPlaybackRef.current
    if (restoredPlayback == null) {
      audioElement.playbackRate = playbackRate
      onCurrentTimeChange(audioElement.currentTime)
      return
    }

    const restoredCurrentTime = clamp(
      restoredPlayback.currentTime,
      0,
      resolvedDuration > 0 ? resolvedDuration : restoredPlayback.currentTime,
    )
    audioElement.currentTime = restoredCurrentTime
    audioElement.playbackRate = restoredPlayback.playbackRate
    setPlaybackRate(restoredPlayback.playbackRate)
    onCurrentTimeChange(restoredCurrentTime)

    if (restoredCurrentTime > 0) {
      setRestoreNotice(
        restoredPlayback.isPlaying
          ? `Playback position restored to ${formatClock(restoredCurrentTime)}. Press play to continue.`
          : `Playback position restored to ${formatClock(restoredCurrentTime)}.`,
      )
    }

    restoredPlaybackRef.current = null
    persistPlaybackState(
      {
        assetId: asset.id,
        currentTime: restoredCurrentTime,
        isPlaying: false,
        playbackRate: audioElement.playbackRate,
      },
      { force: true },
    )
  }

  function handleTimeUpdate() {
    const audioElement = audioRef.current
    if (audioElement == null) {
      return
    }

    onCurrentTimeChange(audioElement.currentTime)
    persistPlaybackState(buildPlaybackStateSnapshot())
  }

  function handlePlay() {
    setIsPlaying(true)
    setPlayerError(null)
    persistPlaybackState(
      buildPlaybackStateSnapshot({
        isPlaying: true,
      }),
      { force: true },
    )
  }

  function handlePause() {
    setIsPlaying(false)
    persistPlaybackState(
      buildPlaybackStateSnapshot({
        isPlaying: false,
      }),
      { force: true },
    )
  }

  function handleRateChange() {
    const audioElement = audioRef.current
    if (audioElement == null) {
      return
    }

    setPlaybackRate(audioElement.playbackRate)
    persistPlaybackState(
      buildPlaybackStateSnapshot({
        playbackRate: audioElement.playbackRate,
      }),
      { force: true },
    )
  }

  function handleEnded() {
    setIsPlaying(false)
    persistPlaybackState(
      buildPlaybackStateSnapshot({
        currentTime: 0,
        isPlaying: false,
      }),
      { force: true },
    )
  }

  function handleError() {
    setIsPlaying(false)
    setPlayerError('The narration file is ready, but this browser could not play it inline.')
  }

  const elapsedLabel = formatClock(currentTime)
  const durationLabel = formatClock(duration)
  const remainingLabel = formatClock(Math.max(duration - currentTime, 0))

  return (
    <div className="finalize-audio-player">
      <audio
        aria-label="Final narration preview"
        className="finalize-audio-player__media"
        onEnded={handleEnded}
        onError={handleError}
        onLoadedMetadata={handleLoadedMetadata}
        onPause={handlePause}
        onPlay={handlePlay}
        onRateChange={handleRateChange}
        onTimeUpdate={handleTimeUpdate}
        preload="metadata"
        ref={audioRef}
        src={streamUrl}
      />

      <div className="finalize-audio-player__controls">
        <div className="finalize-audio-player__transport">
          <Button
            onClick={() => {
              void togglePlayback()
            }}
            tone={isPlaying ? 'ghost' : 'primary'}
          >
            {isPlaying ? 'Pause narration' : 'Play narration'}
          </Button>

          <div className="finalize-audio-player__time-grid">
            <dl className="finalize-audio-player__time-list">
              <div>
                <dt>Elapsed</dt>
                <dd>{elapsedLabel}</dd>
              </div>
              <div>
                <dt>Remaining</dt>
                <dd>{remainingLabel}</dd>
              </div>
              <div>
                <dt>Total</dt>
                <dd>{durationLabel}</dd>
              </div>
            </dl>
          </div>
        </div>

        <div className="finalize-audio-player__seek">
          <div className="finalize-audio-player__seek-header">
            <label htmlFor={seekInputId}>Seek narration</label>
            <span>{elapsedLabel}</span>
          </div>
          <input
            id={seekInputId}
            max={duration > 0 ? duration : Math.max(currentTime, 0)}
            min={0}
            onChange={(event) => {
              seekTo(Number(event.target.value))
            }}
            step="0.1"
            type="range"
            value={Math.min(currentTime, duration > 0 ? duration : currentTime)}
          />
        </div>

        <div className="finalize-audio-player__speed">
          <span className="finalize-audio-player__speed-label">
            Review playback speed
          </span>
          <div className="finalize-audio-player__speed-options">
            {playbackSpeedOptions.map((option) => (
              <button
                aria-pressed={Math.abs(playbackRate - option) < 0.01}
                className="finalize-audio-player__speed-option"
                data-selected={Math.abs(playbackRate - option) < 0.01}
                key={option}
                onClick={() => {
                  applyPlaybackRate(option)
                }}
                type="button"
              >
                {formatPlaybackRate(option)}
              </button>
            ))}
          </div>
        </div>

        {restoreNotice != null ? (
          <p className="finalize-audio-player__note">{restoreNotice}</p>
        ) : null}

        {playerError != null ? (
          <p className="finalize-audio-player__error">{playerError}</p>
        ) : null}
      </div>

      {markers.length > 0 ? (
        <div className="finalize-audio-player__markers">
          <div className="finalize-audio-player__markers-header">
            <strong>Playback markers</strong>
            <span>Jump to the next chapter or rendered segment.</span>
          </div>
          <div className="finalize-audio-player__marker-list">
            {markers.map((marker) => (
              <button
                className="finalize-audio-player__marker"
                data-active={
                  currentTime >= marker.startSeconds &&
                  currentTime < marker.endSeconds
                }
                key={marker.id}
                onClick={() => {
                  seekTo(marker.startSeconds)
                }}
                type="button"
              >
                <span>{formatClock(marker.startSeconds)}</span>
                <strong>{marker.label}</strong>
                <em>
                  {marker.kind === 'chapter'
                    ? `Chapter marker${marker.segmentIndexes.length > 1 ? 's' : ''}`
                    : `Segment ${marker.segmentIndexes.join(', ')}`}
                </em>
              </button>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  )
}

function clamp(value: number, minimum: number, maximum: number) {
  return Math.min(Math.max(value, minimum), maximum)
}

function formatClock(value: number) {
  if (!Number.isFinite(value) || value <= 0) {
    return '0:00'
  }

  const roundedSeconds = Math.floor(value)
  const hours = Math.floor(roundedSeconds / 3600)
  const minutes = Math.floor((roundedSeconds % 3600) / 60)
  const seconds = roundedSeconds % 60

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds
      .toString()
      .padStart(2, '0')}`
  }

  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

function formatPlaybackRate(value: number) {
  if (Number.isInteger(value)) {
    return `${value.toFixed(0)}x`
  }

  if (Number.isInteger(value * 10)) {
    return `${value.toFixed(1)}x`
  }

  return `${value.toFixed(2)}x`
}

function readPersistedPlaybackState(
  storageKey: string,
  assetId: string,
): PersistedAudioPlaybackState | null {
  if (typeof window === 'undefined') {
    return null
  }

  try {
    const rawValue = window.localStorage.getItem(storageKey)
    if (rawValue == null) {
      return null
    }

    const parsedValue = JSON.parse(rawValue) as Partial<PersistedAudioPlaybackState>
    if (
      parsedValue.assetId !== assetId ||
      typeof parsedValue.currentTime !== 'number' ||
      !Number.isFinite(parsedValue.currentTime)
    ) {
      return null
    }

    return {
      assetId,
      currentTime: Math.max(parsedValue.currentTime, 0),
      isPlaying: parsedValue.isPlaying === true,
      playbackRate:
        typeof parsedValue.playbackRate === 'number' &&
        Number.isFinite(parsedValue.playbackRate)
          ? parsedValue.playbackRate
          : 1,
    }
  } catch {
    return null
  }
}
