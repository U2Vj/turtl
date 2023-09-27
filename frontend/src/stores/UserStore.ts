import { StorageSerializers, useStorage } from '@vueuse/core'
import axios from 'axios'
import jwt_decode from 'jwt-decode'
import { defineStore, storeToRefs } from 'pinia'
import { computed, type Ref } from 'vue'
import type { Router } from 'vue-router'
import { useAuthStore } from './AuthStore'
import { makeAxiosRequest } from './AxiosInstance'
import {useToast} from "vue-toastification";

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
  role: string
  role_display: string
  email: string
}

const toast = useToast()

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

  async function login(loginData: LoginData) {
    const data = {
      email: loginData.user.email,
      password: loginData.user.password
    }

    const response = await makeAxiosRequest('/users/login', 'POST', false, false, data)
    if (response.success) {
      refreshToken.value = response.data.refresh
      accessToken.value = response.data.access
      toast.info("Welcome back!")
      return true
    }
    toast.error(response.message)
    return false
  }

  async function refreshLogin() {
    const data = {
      refresh: refreshToken.value
    }
    const response = await makeAxiosRequest('/users/login/refresh', 'POST', false, false, data)
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
      .post(import.meta.env.TURTL_API_URL + '/users/request-reset-email', {
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
    await makeAxiosRequest('/users/logout', 'POST', false, false, data)
    refreshToken.value = null
    accessToken.value = null
    toast.info("You have been signed out")
    router.push('/signin')
  }

  async function testLogin() {
    console.log(await makeAxiosRequest('/users/login/test', 'GET', true, true))
  }

  async function resetPassword(email: string, newPassword: string) {
    return await axios
      .post(import.meta.env.TURTL_API_URL + '/users/reset-password', {
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
    resetPasswordRequest,
    resetPassword,
    refreshLogin,
    userIsSignedIn,
    refreshTokenPayload,
    testLogin
  }
})
