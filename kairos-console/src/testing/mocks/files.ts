export const createMockFile = ({
  fileName,
  content = [{ key: 'value' }]
}: {
  fileName: string
  content?: Array<Record<string, string>>
}) => {
  const str = JSON.stringify(content)
  const blob = new Blob([str])
  const file = new File([blob], fileName, {
    type: 'application/JSON'
  })
  return file
}
