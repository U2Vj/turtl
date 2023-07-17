import axios, { type AxiosRequestConfig } from 'axios'
import { storeToRefs } from 'pinia'
import { useAuthStore } from './AuthStore'

type HTTPMethodName = 'GET' | 'POST' | 'PUT' | 'DELETE'

type SuccessfullResponse = {
  success: true
  data: any
}

type UnsuccessfullResponse = {
  success: false
  message: string
}

type Response = SuccessfullResponse | UnsuccessfullResponse

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
  const { refreshToken, accessToken } = storeToRefs(authStore)

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
    if (tryToUpdateTokenWhenUnauthorized) {
      const data = { refresh: refreshToken.value }
      const responseToRefreshRequest = await makeAxiosRequest(
        'users/login/refresh',
        'POST',
        false,
        false,
        data
      )

      if (responseToRefreshRequest.success) {
        accessToken.value = responseToRefreshRequest?.data.access
        refreshToken.value = responseToRefreshRequest?.data.refresh

        const response = await makeAxiosRequest(url, method, useAuthorization, false, data)
        return response
      }
    }
    if (axios.isAxiosError(error) && error.response?.data.message) {
      return { success: false, message: error.response.data.message }
    }

    return {
      success: false,
      message: 'An error occured'
    }
  }
}
