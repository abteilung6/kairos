import { screen, waitFor, within } from '@testing-library/react'

import ObjectStoreListPage from './ObjectStoreListPage'
import api from 'api/api'
import { createMockObjectStore } from 'testing/mocks/objectStores'
import { createMockAxiosResponse } from 'testing/mocks/axios'
import { customRender } from 'testing/utils'

const imageObjectStore = createMockObjectStore({
  id: 'e7eb09ef-cc61-4adc-841c-9933647e4edb',
  object_key: 'image-key'
})
const videoObjectStore = createMockObjectStore({
  id: '3277900f-7f7e-4587-8fbd-88eae1d5b7ce',
  object_key: 'video-key'
})

describe(ObjectStoreListPage.name, () => {
  beforeEach(() => {
    vi.resetAllMocks()
    vi.spyOn(
      api.ObjectStores,
      'objectStoreListObjectStoreGet'
    ).mockResolvedValueOnce(
      createMockAxiosResponse({
        data: {
          object_stores: [imageObjectStore, videoObjectStore]
        }
      })
    )

    customRender(<ObjectStoreListPage />)
  })

  describe('Page', () => {
    it('should render the header ObjectStoreListPage', () => {
      expect(
        screen.getByRole('heading', {
          name: 'ObjectStoreListPage'
        })
      ).toBeInTheDocument()
    })
  })

  describe('Table', () => {
    it('should display object stores as rows', async () => {
      const table = screen.getByRole('table')
      await waitFor(() => {
        expect(within(table).getAllByRole('row').length).toBe(3)
      })

      // TODO: row matching, when table component is extracted
      within(table).getByText(imageObjectStore.id)
      within(table).getByText(imageObjectStore.object_key)
    })
  })
})
