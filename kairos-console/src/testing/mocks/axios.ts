import { AxiosError, AxiosHeaders, AxiosResponse } from 'axios'

interface MockAxiosResponseOptions<T> {
  data: T
  status?: number
  statusText?: string
  headers?: Record<string, string>
}

export const createMockAxiosResponse = <T>({
  data,
  status = 200,
  statusText = 'OK',
  headers = {}
}: MockAxiosResponseOptions<T>): AxiosResponse => {
  return {
    data,
    status,
    statusText,
    headers,
    config: { headers: new AxiosHeaders() }
  }
}

export const createMockAxiosError = <T>({
  message,
  response
}: {
  message?: string
  response: MockAxiosResponseOptions<T>
}): AxiosError<T> => {
  const error = new Error(message)

  return Object.assign(error, {
    config: undefined,
    response: createMockAxiosResponse<T>(response),
    isAxiosError: true,
    toJSON: () => ({})
  }) as unknown as AxiosError<T>
}
