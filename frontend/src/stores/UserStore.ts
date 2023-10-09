import { useStorage } from '@vueuse/core'
import axios from 'axios'
import jwt_decode from 'jwt-decode'
import { defineStore } from 'pinia'
import { computed, type Ref } from 'vue'
import type { Router } from 'vue-router'
import { makeAPIRequest } from '@/communication/APIRequests'

type LoginData = {
  email: string
  password: string
}

type RefreshTokenPayload = {
  token_type: string
  exp: number
  iat: number
  jti: string
  user_id: number
  username: string | null
  email: string
  role: string
  role_display: string
}

export type User = {
  id: number,
  username: string | null
  email: string
  role?: string
  role_display?: string
}

export const useUserStore = defineStore('user', () => {
  const refreshToken = useStorage<string | null>('refreshToken', null)
  const accessToken = useStorage<string | null>('accessToken', null)

  const refreshTokenPayload: Ref<RefreshTokenPayload | null> = computed(() => {
    try {
      if (refreshToken.value) {
        return jwt_decode(refreshToken.value)
      }
      return null
    } catch (e) {
      return null
    }
  })

  const user: Ref<User | null> = computed(() => {
    if(refreshTokenPayload.value === null) {
      return null
    }
    return {
      id: refreshTokenPayload.value.user_id,
      username: refreshTokenPayload.value.username,
      email: refreshTokenPayload.value.email,
      role: refreshTokenPayload.value.role,
      role_display: refreshTokenPayload.value.role_display
    }
  })

  async function login(data: LoginData) {
    const response = await makeAPIRequest('/users/login', 'POST', false, false, data)
    refreshToken.value = response.data.refresh
    accessToken.value = response.data.access
  }

  async function refreshLogin() {
    const data = {
      refresh: refreshToken.value
    }
    const response = await makeAPIRequest('/users/login/refresh', 'POST', false, false, data)
    refreshToken.value = response.data.refresh
    accessToken.value = response.data.access
  }

  async function userIsSignedIn() {
    // token is in seconds while Date.now() returns timestamp in milliseconds
    return refreshTokenPayload.value
      ? refreshTokenPayload.value.exp > Math.floor(Date.now() / 1000)
      : false
  }

  async function resetPasswordRequest(email: string) {
    return await axios
      .post(import.meta.env.VITE_API_URL + '/users/request-reset-email', {
        email: email
      })
      .then(() => {
        return true
      })
      .catch(() => {
        return false
      })
  }

  async function logout(router: Router) {
    const data = { refresh: refreshToken.value }
    try {
      await makeAPIRequest('/users/logout', 'POST', false, false, data)
    } catch(e: any) {
      if(e.name !== "UnauthorizedError") {
        console.error(e)
      }
    }
    refreshToken.value = null
    accessToken.value = null
    await router.push('/signin')
  }

  async function testLogin() {
    console.log(await makeAPIRequest('/users/login/test', 'GET', true, true))
  }

  async function resetPassword(email: string, newPassword: string) {
    return await axios
      .post(import.meta.env.VITE_API_URL + '/users/reset-password', {
        email: email,
        newPassword: newPassword
      })
      .then((response) => {
        // Erfolgreiche Passwortrücksetzung, handle die Antwort entsprechend
        console.log('Passwort wurde erfolgreich zurückgesetzt:', response.data)
        return true
      })
      .catch((error) => {
        // Optional: Du kannst hier Fehlerbehandlung durchführen und entsprechende Fehler zurückgeben
        console.error('Fehler beim Zurücksetzen des Passworts:', error)
        throw error
      })
  }

  return {
    accessToken,
    user,
    login,
    logout,
    resetPasswordRequest,
    resetPassword,
    refreshLogin,
    userIsSignedIn,
    testLogin
  }
})
