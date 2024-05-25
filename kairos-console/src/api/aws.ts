import { UseMutationOptions, useMutation } from '@tanstack/react-query'
import {} from 'generated-api'
import api from './api'
import { UploadFileToS3Request } from './awsApi'

export const useUploadFileToS3 = (
  options?: Omit<
    UseMutationOptions<void, Error, UploadFileToS3Request>,
    'mutationFn'
  >
) => {
  return useMutation<void, Error, UploadFileToS3Request>({
    ...options,
    mutationFn: async (uploadFileToS3Request) => {
      const { data } = await api.Aws.uploadFileToS3(uploadFileToS3Request)
      return data
    }
  })
}
