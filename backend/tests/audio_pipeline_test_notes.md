# Audio Pipeline Test Notes

The focused audio pipeline tests split mocked and real behavior deliberately:

- Mocked:
  - The TTS provider boundary uses `RecordingTextToSpeechAdapter`.
  - Optional background-music mixing uses `RecordingAudioMixer` or `FailingAudioMixer`.
  - Object storage uses `InMemoryObjectStorage` instead of the HTTP GCS adapter.
- Real:
  - SQLAlchemy models, transactions, and job persistence.
  - `AudioJobService`, `NarrationSegmentationService`, and `FinalAudioAssemblyService`.
  - WAV assembly, pause insertion, final asset publication, superseding prior assets, and event-log writes.

Existing lower-level tests continue to cover the real Gemini request/response contract and the ffmpeg
command builder separately:

- `backend/tests/test_gemini_tts_adapter.py`
- `backend/tests/test_audio_mixing_service.py`
