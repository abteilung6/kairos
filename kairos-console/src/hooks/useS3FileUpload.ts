import { useUploadFileToS3 } from 'api/aws'
import { useCreateObjectStore, useUpdateObjectStore } from 'api/objectStores'
import { ObjectStore, ObjectStoreState } from 'generated-api'
import { useCallback } from 'react'

export const useS3FileUpload = () => {
  const createObjectStoreMutation = useCreateObjectStore()
  const uploadFileToS3Mutation = useUploadFileToS3()
  const updateObjectStoreMutation = useUpdateObjectStore()
  const error =
    createObjectStoreMutation.error ||
    updateObjectStoreMutation.error ||
    updateObjectStoreMutation.error

  const uploadFile = useCallback(
    async (file: File): Promise<ObjectStore> => {
      const response = await createObjectStoreMutation.mutateAsync({
        file_name: file.name
      })
      if (response.bucket_post_url === null) {
        return Promise.reject(Error('Field bucket_post_url is required'))
      }
      await uploadFileToS3Mutation.mutateAsync({
        bucket_post_url: response.bucket_post_url,
        fields: response.fields,
        file: file
      })
      return await updateObjectStoreMutation.mutateAsync({
        objectStoreId: response.id,
        objectStoreUpdateRequest: {
          state: ObjectStoreState.Occupied
        }
      })
    },
    [
      createObjectStoreMutation,
      updateObjectStoreMutation,
      uploadFileToS3Mutation
    ]
  )

  return {
    uploadFile,
    isLoading:
      createObjectStoreMutation.isPending ||
      updateObjectStoreMutation.isPending ||
      updateObjectStoreMutation.isPending,
    isError: error !== null,
    error: error
  }
}
