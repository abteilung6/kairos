import { AxiosResponse } from 'axios'
import { PresignedFields } from 'generated-api'
import { BaseAPI } from 'generated-api/base'

export type UploadFileToS3Request = {
  bucket_post_url: string
  fields: PresignedFields
  file: File
}

export class AwsApi extends BaseAPI {
  public uploadFileToS3({
    bucket_post_url,
    fields,
    file
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  }: UploadFileToS3Request): Promise<AxiosResponse<any, any>> {
    const form = new FormData()
    form.append('key', fields.key)
    form.append('AWSAccessKeyId', fields.AWSAccessKeyId)
    form.append('policy', fields.policy)
    form.append('signature', fields.signature)
    form.append('file', file)
    return this.axios.post(bucket_post_url, form)
  }
}
