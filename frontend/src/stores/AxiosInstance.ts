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
  message: string,
  data?: any
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
  const userStore = useUserStore()
  const { accessToken } = storeToRefs(userStore)

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
  } catch (error: any) {
    if(error.response.status === 401
        && error.response.data?.code === 'token_not_valid'
        && tryToUpdateTokenWhenUnauthorized) {
      return await userStore.refreshLogin().then(async (success) => {
        if (success) {
          return await makeAxiosRequest(url, method, useAuthorization, false, data)
        }
        await userStore.logout(router)
        return {
          success: false,
          message: 'Your session has expired. Please sign in again.'
        }
      })
    }
    // This section constructs an error message either by getting the error detail or, if that is not available (e.g.
    // backend form validation errors), by adding each error description of each form field to the error message returned
    // by this function.
    let errorMessage: string = `Error ${error?.response.status}`
    if(error?.response.data?.detail) {
      errorMessage += `: ${error?.response.data?.detail}`
    } else if(error?.response.data?.errors) {
      errorMessage += ": "
      for(const [field, errorDescriptions] of Object.entries<string[]>(error.response.data.errors)) {
        errorMessage += `Field ${field}: `
        for(const errorDescription of errorDescriptions) {
          errorMessage += `${errorDescription} `
        }
        errorMessage = errorMessage.slice(0,-1)
        errorMessage += ", "
      }
      errorMessage = errorMessage.slice(0, -2)
    }
    return {
      success: false,
      message: errorMessage,
      data: error?.response?.data
    }
  }
}
