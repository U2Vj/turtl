import { useAuthStore } from './AuthStore'
import { makeAxiosRequest } from './AxiosInstance'
import { StorageSerializers, useStorage } from '@vueuse/core'
import axios from 'axios'
import jwt_decode from 'jwt-decode'
import { defineStore, storeToRefs } from 'pinia'
import { computed, type Ref } from 'vue'
import type { Router } from 'vue-router'

type LoginData = {
  user: {
    email: string
    password: string
  }
}

type User = {
  email: string
  username: string
  token: string
}

type RefreshTokenPayload = {
  token_type: 'refresh'
  exp: number
  iat: number
  jti: string
  user_id: number
  username: string
  role: 'ADMINISTRATOR'
  email: string
}

export const useUserStore = defineStore('api/user', () => {
  const authStore = useAuthStore()
  const { refreshToken, accessToken } = storeToRefs(authStore)

  // see https://github.com/vueuse/vueuse/issues/1307 and https://vueuse.org/core/useStorage/#custom-serialization
  const user = useStorage<User | null>('api/user', null, undefined, {
    serializer: StorageSerializers.object
  })

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

  async function login(logininData: LoginData) {
    const data = {
      email: logininData.user.email,
      password: logininData.user.password
    }

    const response = await makeAxiosRequest('api/users/login', 'POST', false, false, data)
    if (response.success) {
      refreshToken.value = response.data.refresh
      accessToken.value = response.data.access
      return true
    }
    return false
  }

  async function getNewRefreshAndAccessToken() {
    const data = {
      refresh: refreshToken.value
    }
    const response = await makeAxiosRequest('/api/users/login/refresh', 'POST', false, true, data)
    if (response.success && response.data.access && response.data.refresh) {
      refreshToken.value = response.data.refresh
      accessToken.value = response.data.access
      return true
    }
    return false
  }

  async function userIsSignedIn() {
    // token is in seconds while Date.now() returns timestamp in milliseconds
    return refreshTokenPayload.value
      ? refreshTokenPayload.value.exp > Math.floor(Date.now() / 1000)
      : false
  }

  async function resetPasswordRequest(email: string) {
    return await axios
      .post(import.meta.env.VITE_API_URL + 'api/request-reset-email', {
        email: email
      })
      .then(() => {
        return true
      })
      .catch(() => {
        return false
      })
  }

  // see https://github.com/vuejs/pinia/discussions/1092#discussioncomment-5408576.
  // Cant use direct import because https://github.com/vitejs/vite/issues/4430#issuecomment-979013114.
  async function signOut(router: Router) {
    const data = { refresh: refreshToken.value }
    await makeAxiosRequest('api/users/logout', 'POST', true, true, data)
    refreshToken.value = null
    accessToken.value = null
    router.push('/signin')
  }

  async function register(user: any) {
    return await axios.post(import.meta.env.VITE_API_URL + 'api/users/register', user)
  }

  async function testLogin() {
    console.log(await makeAxiosRequest('api/users/login/test', 'GET', true, true))
  }

  async function resetPassword(email: string, newPassword: string) {
    return await axios
      .post(import.meta.env.VITE_API_URL + 'api/reset-password', {
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
    user,
    login,
    signOut,
    register,
    resetPasswordRequest,
    resetPassword,
    getNewRefreshAndAccessToken,
    userIsSignedIn,
    refreshTokenPayload,
    testLogin
  }
})
