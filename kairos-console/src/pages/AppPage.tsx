import { useS3FileUpload } from 'hooks/useS3FileUpload'
import { useState } from 'react'
import { noop } from 'utils'

const AppPage: React.FC = () => {
  const { uploadFile, isLoading, isError, error } = useS3FileUpload()
  const [file, setFile] = useState<File | undefined>()

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event?.preventDefault()
    if (file === undefined) {
      return
    }
    uploadFile(file)
      .then(() => {
        setFile(undefined)
      })
      .catch(noop)
  }

  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFile(event?.target?.files?.[0])
  }

  return (
    <div>
      <h1 className="text-gray-600">AppPage</h1>
      {isError && <div>{error?.message}</div>}
      {file && `File: ${file.name}`}
      <form onSubmit={onSubmit}>
        <input
          data-testid="file-input-id"
          type="file"
          onChange={onFileChange}
        />
        <button type="submit" disabled={file === undefined || isLoading}>
          Upload
        </button>
      </form>
    </div>
  )
}

export default AppPage
