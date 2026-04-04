/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_SESSION_EVENTS_WS_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
