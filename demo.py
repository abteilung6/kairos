from pathlib import Path
from typing import Any, Final
from uuid import uuid4

import cv2
import requests
from boto3.session import Session
from cv2.typing import MatLike
from loguru import logger
from requests import Response

from config import get_config
from exceptions import FileFormatNotSupportedError

SAMPLE_IMAGE_FILE_NAME: Final[str] = "image.png"
ALLOWED_FILE_FORMATS: list[str] = [".png"]


def generate_object_key(filename: str) -> str:
    """The object key (or key name) uniquely identifies the object in an Amazon S3 bucket.

    See https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
    """
    path = Path(filename)
    if path.suffix not in ALLOWED_FILE_FORMATS:
        logger.error(f"File format not supported for {filename}")
        raise FileFormatNotSupportedError(f"File format not supported for {filename}")
    prefix = uuid4()
    return f"{prefix}{path.suffix}"


def create_botocore_session(
    aws_access_key_id: str, aws_secret_access_key: str, region_name: str,
) -> Session:
    return Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )


def create_presigned_post(
    session: Session, bucket_name: str, key: str,
) -> dict[str, Any]:
    s3 = session.client("s3")
    return s3.generate_presigned_post(bucket_name, key, ExpiresIn=3600)


def create_presigned_get_url(session: Session, bucket_name: str, key: str) -> str:
    s3 = session.client("s3")
    return s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=3600,
    )


def upload_file_to_s3(filename: str, presigned_post_url: str, fields: dict) -> Response:
    with open(filename, "rb") as f:
        files = {"file": (filename, f)}
        return requests.post(presigned_post_url, data=fields, files=files)


def download_file_from_url(url: str, filepath: str) -> None:
    img_data = requests.get(url).content
    with open(filepath, "wb") as handler:
        handler.write(img_data)


def read_image(filename: str) -> MatLike:
    return cv2.imread(filename)


def get_human_count(image: MatLike) -> int:
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    (humans, _) = hog.detectMultiScale(
        image, winStride=(10, 10), padding=(32, 32), scale=1.1,
    )
    return len(humans)


if __name__ == "__main__":
    config = get_config()
    session = create_botocore_session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY.get_secret_value(),
        region_name=config.DEFAULT_AWS_REGION,
    )
    bucket_name = config.BUCKET_NAME

    object_key = generate_object_key(SAMPLE_IMAGE_FILE_NAME)
    presigned_post_response = create_presigned_post(
        session=session, bucket_name=bucket_name, key=object_key,
    )
    presigned_post_url = presigned_post_response["url"]

    upload_response = upload_file_to_s3(
        filename=SAMPLE_IMAGE_FILE_NAME,
        presigned_post_url=presigned_post_url,
        fields=presigned_post_response["fields"],
    )

    presigned_get_url = create_presigned_get_url(
        session=session, bucket_name=bucket_name, key=object_key,
    )
    download_file_path = f"images/{object_key}"
    download_file_from_url(presigned_get_url, download_file_path)

    image = read_image(download_file_path)
    human_count = get_human_count(image)
    logger.info(f"Detected {human_count} humans in image {SAMPLE_IMAGE_FILE_NAME}")
