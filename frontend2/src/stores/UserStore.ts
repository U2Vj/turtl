import axios from 'axios'
import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useStorage, StorageSerializers } from '@vueuse/core'
// importing router directly is recommended. See https://github.com/vuejs/pinia/discussions/1717
import router from '@/router'

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
  // see https://github.com/vueuse/vueuse/issues/1307 and https://vueuse.org/core/useStorage/#custom-serialization
  const user = useStorage<User | null>('user', null, undefined, {
    serializer: StorageSerializers.object
  })
  const loggedIn = computed(() => {
    return !!user.value
  })

  async function login(logininData: LoginData) {
    return await axios
      .post(import.meta.env.VITE_API_URL + '/users/login', logininData)
      .then((response) => {
        if (response.data.user.token) {
          user.value = response.data.user
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

  async function logout() {
    user.value = null
    router.push('/signin')
  }

  async function register(user: any) {
    return await axios.post(import.meta.env.VITE_API_URL + '/users/register', user)
  }

  return { user, loggedIn, login, logout, resetPasswordRequest }
})
