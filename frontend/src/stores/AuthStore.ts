import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', () => {
  const refreshToken = useStorage<string | null>('refreshToken', null)
  const accessToken = useStorage<string | null>('accessToken', null)

  return { refreshToken, accessToken }
})
