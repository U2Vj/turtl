import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

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

export const useUserStore = defineStore('UserStore', () => {
  const user = ref<User | null>(null)
  const loggedIn = computed(() => {
    return !!user.value
  })

  async function login(logininData: LoginData) {
    return await axios
      .post(import.meta.env.VITE_API_URL + '/users/login', logininData)
      .then((response) => {
        if (response.data.user.token) {
          localStorage.setItem('user', JSON.stringify(response.data.user))
          user.value = response.data.user
          console.log('true')
          return true
        }
        return false
      })
      .catch(() => {
        return false
      })
  }

  async function update(user: any) {
    return await axios.post(import.meta.env.VITE_API_URL + '/user', user).then((response) => {
      if (response.data.user.token) {
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }

      return response.data
    })
  }

  async function resetPasswordRequest(email: string) {
    return axios.post(import.meta.env.VITE_API_URL+'/request-reset-email', {
                    email: email
                })
  }

  async function logout() {
    localStorage.removeItem('user')
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

  return { user, loggedIn, login, logout, resetPasswordRequest, resetPassword }
})
