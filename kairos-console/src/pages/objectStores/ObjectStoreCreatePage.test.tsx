import { screen, fireEvent, waitFor } from '@testing-library/react'

import ObjectStoreCreatePage from './ObjectStoreCreatePage'
import api from 'api/api'
import {
  createMockObjectStore,
  createMockObjectStoreCreateResponse
} from 'testing/mocks/objectStores'
import {
  createMockAxiosError,
  createMockAxiosResponse
} from 'testing/mocks/axios'
import { createMockFile } from 'testing/mocks/files'
import { customRender } from 'testing/utils'

const fileName = 'mock.json'
const mockContent = [{ key: 'value' }]
const mockFile = createMockFile({
  fileName: fileName,
  content: mockContent
})

describe(ObjectStoreCreatePage.name, () => {
  beforeEach(() => {
    vi.resetAllMocks()
    customRender(<ObjectStoreCreatePage />)
  })

  const selectInputFile = () => {
    const mockFileText = vi.fn().mockResolvedValue(JSON.stringify(mockContent))
    File.prototype.text = mockFileText
    const fileInput = screen.getByTestId('file-input-id')
    fireEvent.change(fileInput, { target: { files: [mockFile] } })
    screen.getByText(/mock.json/)
  }

  describe('Page', () => {
    it('should render the header AppPage', () => {
      expect(
        screen.getByRole('heading', {
          name: 'ObjectStoreCreatePage'
        })
      ).toBeInTheDocument()
    })
  })

  describe('Form', () => {
    it('should disabled upload button, when file is not selected', async () => {
      const button = screen.getByRole('button', { name: 'Upload' })
      expect(button).toBeDisabled()
    })

    it('should enable upload button, when file is selected', async () => {
      selectInputFile()
      const button = screen.getByRole('button', { name: 'Upload' })
      expect(button).toBeEnabled()
    })
  })

  describe('Actions', () => {
    it('should submit form values', async () => {
      const spyOnObjectStoreCreateObjectStorePost = vi
        .spyOn(api.ObjectStores, 'objectStoreCreateObjectStorePost')
        .mockResolvedValueOnce(
          createMockAxiosResponse({
            data: createMockObjectStoreCreateResponse()
          })
        )
      const spyUploadFileToS3 = vi
        .spyOn(api.Aws, 'uploadFileToS3')
        .mockResolvedValueOnce(
          createMockAxiosResponse({
            data: {}
          })
        )
      const spyObjectStoreUpdateObjectStoreObjectStoreIdPatch = vi
        .spyOn(
          api.ObjectStores,
          'objectStoreUpdateObjectStoreObjectStoreIdPatch'
        )
        .mockResolvedValueOnce(
          createMockAxiosResponse({ data: createMockObjectStore() })
        )
      selectInputFile()
      const button = screen.getByRole('button', { name: 'Upload' })
      fireEvent.click(button)

      await waitFor(() => {
        expect(spyOnObjectStoreCreateObjectStorePost).toHaveBeenCalledTimes(1)
        expect(spyUploadFileToS3).toHaveBeenCalledTimes(1)
        expect(
          spyObjectStoreUpdateObjectStoreObjectStoreIdPatch
        ).toHaveBeenCalledTimes(1)
      })
    })

    it('should display an alert, when any request failed', async () => {
      const spyOnObjectStoreCreateObjectStorePost = vi
        .spyOn(api.ObjectStores, 'objectStoreCreateObjectStorePost')
        .mockRejectedValue(
          createMockAxiosError({
            response: { data: {} },
            message: 'Something went wrong'
          })
        )

      selectInputFile()
      const button = screen.getByRole('button', { name: 'Upload' })
      fireEvent.click(button)

      await waitFor(() => {
        expect(spyOnObjectStoreCreateObjectStorePost).toHaveBeenCalledTimes(1)
      })
      await screen.findByText('Something went wrong')
    })
  })
})
