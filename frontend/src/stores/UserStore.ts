import axios from 'axios'
import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useStorage, StorageSerializers } from '@vueuse/core'
import type { Router } from 'vue-router'
import { axiosInstance } from './AxiosInstance'

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

export const useUserStore = defineStore('user', () => {
  // see https://github.com/vueuse/vueuse/issues/1307 and https://vueuse.org/core/useStorage/#custom-serialization
  const user = useStorage<User | null>('user', null, undefined, {
    serializer: StorageSerializers.object
  })
  const loggedIn = computed(() => {
    return !!user.value
  })

  async function login(logininData: LoginData) {
    const response = await axiosInstance.post('/users/login', {
      email: logininData.user.email,
      password: logininData.user.password
    })
    return response.status === 200
  }

  async function update(email: string, password: string) {
    return await axiosInstance.post('/user', { email, password })
  }

  async function resetPasswordRequest(email: string) {
    return await axios
      .post(import.meta.env.VITE_API_URL + '/request-reset-email', {
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
  async function logout(router: Router) {
    user.value = null
    router.push('/signin')
  }

  async function register(user: any) {
    return await axios.post(import.meta.env.VITE_API_URL + '/users/register', user)
  }

  async function resetPassword(email: string, newPassword: string) {
    console.log('hier')
    return await axios
      .post(import.meta.env.VITE_API_URL + '/reset-password', {
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

  return { user, loggedIn, login, logout, update, register, resetPasswordRequest, resetPassword }
})
