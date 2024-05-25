import {
  ObjectStore,
  ObjectStoreCreateResponse,
  ObjectStoreState
} from 'generated-api'

const mockObjectStoreCreateResponse: ObjectStoreCreateResponse = {
  object_key: 'objekt_key',
  claimed_time: '2011-10-05T14:48:00.000Z',
  occupied_time: null,
  bucket_get_url: null,
  id: 'd5071b04-3055-40e2-8123-277ee807ad11',
  bucket_post_url: 'https://foo',
  fields: {
    key: 'key',
    AWSAccessKeyId: 'AWSAccessKeyId',
    policy: 'policy',
    signature: 'signature'
  },
  state: ObjectStoreState.Claimed
}

export const createMockObjectStoreCreateResponse = (
  overrides: Partial<ObjectStoreCreateResponse> = {}
): ObjectStoreCreateResponse => {
  return {
    ...mockObjectStoreCreateResponse,
    ...overrides
  }
}

const mockObjectStore: ObjectStore = {
  object_key: 'objekt_key',
  claimed_time: '2011-10-05T14:48:00.000Z',
  occupied_time: null,
  bucket_get_url: null,
  id: 'd5071b04-3055-40e2-8123-277ee807ad11',
  state: ObjectStoreState.Claimed
}

export const createMockObjectStore = (
  overrides: Partial<ObjectStore> = {}
): ObjectStore => {
  return {
    ...mockObjectStore,
    ...overrides
  }
}
