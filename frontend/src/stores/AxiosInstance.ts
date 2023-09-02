import { useAuthStore } from './AuthStore'
import axios, { type AxiosRequestConfig } from 'axios'
import { storeToRefs } from 'pinia'
import {useUserStore} from "@/stores/UserStore";
import router from "@/router";

type HTTPMethodName = 'GET' | 'POST' | 'PUT' | 'DELETE'

type SuccessfulResponse = {
  success: true
  data: any
}

type UnsuccessfulResponse = {
  success: false
  message: string
}

type Response = SuccessfulResponse | UnsuccessfulResponse

const axiosInstance = axios.create({ baseURL: import.meta.env.VITE_API_URL })

export async function makeAxiosRequest(
  url: string,
  method: HTTPMethodName,
  useAuthorization: boolean,
  tryToUpdateTokenWhenUnauthorized: boolean,
  data?: any
): Promise<Response> {
  // TODO: find out why this can't be used outside of the function.
  const authStore = useAuthStore()
  const { accessToken } = storeToRefs(authStore)

  const config: AxiosRequestConfig = {}

  if (useAuthorization) {
    config.headers = { Authorization: `Bearer ${accessToken.value}` }
  }

  try {
    let response
    switch (method) {
      case 'GET':
        response = await axiosInstance.get(url, config)
        break
      case 'POST':
        response = await axiosInstance.post(url, data, config)
        break
      case 'PUT':
        response = await axiosInstance.put(url, data, config)
        break
      case 'DELETE':
        response = await axiosInstance.delete(url, config)
    }
    return { success: true, data: response.data }
  } catch (error) {
    if(tryToUpdateTokenWhenUnauthorized) {
      const userStore = useUserStore()
      return await userStore.refreshLogin().then(async (success) => {
        if (success) {
          return await makeAxiosRequest(url, method, useAuthorization, false, data)
        }
        await userStore.signOut(router)
        return {
          success: false,
          message: 'Could not obtain new access token, logging out...'
        }
      })
    }
    return {
      success: false,
      message: 'An error occurred'
    }
  }
}
