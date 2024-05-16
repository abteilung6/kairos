from pathlib import Path
from typing import Any, Final, Literal
from uuid import uuid4

from boto3 import Session
from mypy_boto3_s3 import S3Client
from pydantic import BaseModel, SecretStr

from kairos.cloud.schemas import PresignedPostUrlResponse

OBJECT_EXPIRATION_SECONDS: Final[int] = 31557600 # this project wont survive 100 years

JsonObject = dict[str, Any]


class AWSCredentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: SecretStr
    region_name: str


class AWSCaller:
    def __init__(self, credentials: AWSCredentials) -> None:
        self.credentials = credentials
        self._botocore_session: Session | None = None
        self._s3_client: S3Client | None = None

    def _create_botocore_session(self) -> None:
        if self._botocore_session is None:
            self._botocore_session = Session(
                aws_access_key_id=self.credentials.aws_access_key_id,
                aws_secret_access_key=self.credentials.aws_secret_access_key.get_secret_value(),
                region_name=self.credentials.region_name,
            )

    def _create_botocore_client(self, service_name: Literal["s3"]) -> S3Client:
        self._create_botocore_session()
        assert self._botocore_session is not None
        return self._botocore_session.client(
            service_name,
            region_name=self.credentials.region_name,
        )

    @property
    def s3_client(self) -> S3Client:
        s3_client = self._s3_client
        if s3_client is None:
            s3_client = self._create_botocore_client("s3")
            self._s3_client = s3_client
        return s3_client

    def create_presigned_post(self, bucket_name: str, key: str) -> PresignedPostUrlResponse:
        """Builds the url and the form fields used for a presigned s3 post"""
        # TODO: conditions e.g ['starts-with', '$Content-Type', 'image']
        raw_response = self.s3_client.generate_presigned_post(bucket_name, key, ExpiresIn=3600)
        return PresignedPostUrlResponse.model_validate(
            raw_response,
        )

    def create_presigned_get_url(self, bucket_name: str, key: str) -> str:
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": key},
            ExpiresIn=OBJECT_EXPIRATION_SECONDS,
        )

    # TODO: check bucket during state transition
    def get_bucket_object_metadata(self, bucket: str, object_key: str) -> JsonObject | None:
        """Retrieves metadata from an object without returning the object itself."""
        return self.s3_client.head_object(Bucket=bucket, Key=object_key)



def generate_object_key(filename: str) -> str:
    """The object key (or key name) uniquely identifies the object in an Amazon S3 bucket.

    See https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
    """
    path = Path(filename)
    prefix = uuid4()
    return f"{prefix}{path.suffix}"
