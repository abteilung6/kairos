import axios from 'axios'
import { Configuration, ObjectStoresApi } from 'generated-api'
import { AwsApi } from './awsApi'

const KARIOS_API_BASE_URL = 'http://127.0.0.1:8000' // TODO: move to environment variables
const kairosAxiosInstance = axios.create({
  baseURL: KARIOS_API_BASE_URL
})

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const handleErrorResponse = (errorResponse: any) => {
  if (errorResponse.response && errorResponse.response.data) {
    // TODO: apply schema validation, when a library is introduced
    return Promise.reject(Error(errorResponse.response.data.detail))
  }
  return Promise.reject(errorResponse)
}

kairosAxiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    return handleErrorResponse(error)
  }
)

const awsAxiosInstance = axios.create({})
const configuration = new Configuration({})

export default {
  ObjectStores: new ObjectStoresApi(configuration, '', kairosAxiosInstance),
  Aws: new AwsApi(configuration, '', awsAxiosInstance)
}
