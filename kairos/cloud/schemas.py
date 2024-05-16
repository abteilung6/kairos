from pydantic import BaseModel, Field, HttpUrl


class PresignedFields(BaseModel):
    key: str = Field(
        title="File gets upload to the bucket key",
        examples=["sample.png"],
    )
    AWSAccessKeyId: str = Field(title="AWS access key id")
    policy: str = Field(title="Base64 encoded policy")
    signature: str = Field(title="Account signature")


class PresignedPostUrlResponse(BaseModel):
    url: HttpUrl = Field(
        title="A generated presigned URL",
        description="Using a presigned URL will allow an upload without requiring another party to have AWS security credentials or permissions.",  # noqa: E501
    )
    fields: PresignedFields
