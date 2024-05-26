import {
  UseMutationOptions,
  UseQueryOptions,
  useMutation,
  useQuery
} from '@tanstack/react-query'
import {
  ObjectStore,
  ObjectStoreCreateRequest,
  ObjectStoreCreateResponse,
  ObjectStoreUpdateRequest
} from 'generated-api'
import api from './api'

export const useObjectStoreListQuery = (
  options?: Omit<UseQueryOptions<ObjectStore[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery<ObjectStore[], Error>({
    ...options,
    queryKey: ['object_stores'],
    queryFn: async () => {
      const { data } = await api.ObjectStores.objectStoreListObjectStoreGet()
      return data.object_stores
    }
  })
}

export const useCreateObjectStore = (
  options?: Omit<
    UseMutationOptions<
      ObjectStoreCreateResponse,
      Error,
      ObjectStoreCreateRequest
    >,
    'mutationFn'
  >
) => {
  return useMutation<
    ObjectStoreCreateResponse,
    Error,
    ObjectStoreCreateRequest
  >({
    ...options,
    mutationFn: async (objectStoreCreateRequest) => {
      const { data } = await api.ObjectStores.objectStoreCreateObjectStorePost(
        objectStoreCreateRequest
      )
      return data
    }
  })
}

export const useUpdateObjectStore = (
  options?: Omit<
    UseMutationOptions<
      ObjectStore,
      Error,
      {
        objectStoreId: string
        objectStoreUpdateRequest: ObjectStoreUpdateRequest
      }
    >,
    'mutationFn'
  >
) => {
  return useMutation<
    ObjectStore,
    Error,
    {
      objectStoreId: string
      objectStoreUpdateRequest: ObjectStoreUpdateRequest
    }
  >({
    ...options,
    mutationFn: async ({ objectStoreId, objectStoreUpdateRequest }) => {
      const { data } =
        await api.ObjectStores.objectStoreUpdateObjectStoreObjectStoreIdPatch(
          objectStoreId,
          objectStoreUpdateRequest
        )
      return data
    }
  })
}
