import axios, { type AxiosRequestConfig } from 'axios'
import { storeToRefs } from 'pinia'
import {useUserStore} from "@/stores/UserStore"
import router from "@/router"
import { BadRequestError, UnauthorizedError, PermissionDeniedError, NotFoundError, ServerError } from "@/communication/exceptions"

type HTTPMethodName = 'GET' | 'POST' | 'PUT' | 'DELETE'

type Response = {
  statusCode: number
  data: any
}

const APIRequests = axios.create({ baseURL: import.meta.env.VITE_API_URL })

function isObject(value: any): boolean {
  return typeof value === 'object' && value !== null;
}

function constructErrorMessage(errorObject: any): string {
  // This function constructs an error message by recursively appending each field and its error descriptions together.
  if (typeof errorObject === 'string') {
    return `${errorObject} `;
  } else if (Array.isArray(errorObject)) {
    return errorObject.map((item) => constructErrorMessage(item)).join('');
  } else if (isObject(errorObject)) {
    return Object.entries(errorObject).map(([field, errors]) => {
      if(errors) {
        return `Field ${field}: ${constructErrorMessage(errors)}`
      } else {
        return ''
      }
    }).join('');
  } else if(errorObject === null || errorObject === undefined) {
    return '';
  } else {
    throw new TypeError('Unsupported type encountered');
  }
}

export async function makeAPIRequest(
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
        response = await APIRequests.get(url, config)
        break
      case 'POST':
        response = await APIRequests.post(url, data, config)
        break
      case 'PUT':
        response = await APIRequests.put(url, data, config)
        break
      case 'DELETE':
        response = await APIRequests.delete(url, config)
    }
    return { statusCode: response.status, data: response.data }
  } catch (error: any) {
    if(error.response.status === 401
        && error.response.data?.code === 'token_not_valid'
        && tryToUpdateTokenWhenUnauthorized) {
      return await userStore.refreshLogin().then(async () => {
        return await makeAPIRequest(url, method, useAuthorization, false, data)
      }).catch((error) => {
        userStore.logout(router)
        throw new UnauthorizedError('Your session has expired. Please sign in again.', error.response?.data)
      })
    }

    // Here, we are either using the error detail field provided by the backend or, if that is not available (e.g.
    // backend form validation errors), we construct an error message out of the form validation errors.
    const errorMessage = `Error ${error.response?.status}: ${(error.response?.data?.detail) ? error.response.data.detail : constructErrorMessage(error.response?.data?.errors)}`
    switch(error.response?.status) {
      case 400:
        throw new BadRequestError(errorMessage, error.response?.data)
      case 401:
        throw new UnauthorizedError(errorMessage, error.response?.data)
      case 403:
        throw new PermissionDeniedError(errorMessage, error.response?.data)
      case 404:
        throw new NotFoundError(errorMessage, error.response?.data)
      default:
        throw new ServerError(errorMessage, error.response?.data)
    }
  }
}
