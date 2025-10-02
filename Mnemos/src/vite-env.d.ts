/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_APP_VERSION: string
  readonly VITE_DEV_MODE: string
  readonly VITE_LOG_LEVEL: string
  readonly VITE_MOBILE_MODE: string
  readonly VITE_ENABLE_VUE_COMPONENTS: string
  readonly VITE_ENABLE_PWA: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}