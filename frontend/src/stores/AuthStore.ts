import { useStorage } from '@vueuse/core'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const refreshToken = useStorage<string | null>('refreshToken', null)
  const accessToken = useStorage<string | null>('accessToken', null)

  return { refreshToken, accessToken }
})
