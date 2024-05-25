from dataclasses import dataclass
from unittest.mock import MagicMock, Mock

from botocore.exceptions import ClientError
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from kairos import crud
from kairos.cloud.schemas import PresignedPostUrlResponse
from kairos.schemas.object_store import ObjectStoreCreate, ObjectStoreState, PresignedFields
from kairos.utils.date import now
from tests.api.conftest import AWSCallerMock
from tests.types import TestCase

FAKE_OBJECT_STORE_RESPONSE = PresignedPostUrlResponse(
    url="https://s3.eu-west-1.amazonaws.com/fake_bucket",
    fields=PresignedFields(
        key="fake-key.png",
        AWSAccessKeyId="fake-aws-access-key-id",
        policy="fake-policy",
        signature="fake-signature",
    ),
)

def test_object_store_list(
    app: tuple[TestClient, AWSCallerMock],
    db_session: Session,
) -> None:
    client, _ = app
    object_store_create = ObjectStoreCreate(object_key="object_key", claimed_time=now(), occupied_time=now(), bucket_get_url=HttpUrl("http://localhost/"))
    crud.object_store_create(db=db_session, obj=object_store_create) # TODO: fixture, yield with removal

    response = client.get(
        "/object-store",
    )

    assert response.status_code == 200
    content = response.json()
    assert len(content["object_stores"]) == 1
    assert content["object_stores"][0]["object_key"] == object_store_create.object_key
    assert content["object_stores"][0]["bucket_get_url"] == str(object_store_create.bucket_get_url)


@dataclass
class ObjectStoreCreateTestCase(TestCase):
    create_presigned_post_return_value: PresignedPostUrlResponse | Exception
    expected_status_code: status
    expected_object_key: str | None
    expected_bucket_post_url: str | None
    expected_error_message: str | None


OBJECT_STORE_CREATE_TEST_CASES = (
    ObjectStoreCreateTestCase(
        test_name="Generates presigned POST url for object",
        create_presigned_post_return_value=FAKE_OBJECT_STORE_RESPONSE,
        expected_status_code=status.HTTP_200_OK,
        expected_object_key=FAKE_OBJECT_STORE_RESPONSE.fields.key,
        expected_bucket_post_url=str(FAKE_OBJECT_STORE_RESPONSE.url),
        expected_error_message=None,
    ),
    ObjectStoreCreateTestCase(
        test_name="Internal server error, create_presigned_post raised ClientError",
        create_presigned_post_return_value=ClientError({}, ""),
        expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        expected_object_key=None,
        expected_bucket_post_url=None,
        expected_error_message="Unable to fully process this request because of an internal server error.",
    ),
)


@TestCase.parametrize(*OBJECT_STORE_CREATE_TEST_CASES)
def test_object_store_create(
    test_case: ObjectStoreCreateTestCase,
    app: tuple[TestClient, AWSCallerMock],
) -> None:
    client, aws_caller = app

    match test_case.create_presigned_post_return_value:
        case Exception():
            aws_caller.create_presigned_post = Mock(side_effect=test_case.create_presigned_post_return_value)
        case _:
            aws_caller.create_presigned_post = Mock(
                return_value=test_case.create_presigned_post_return_value,
            )

    response = client.post(
        "/object-store",
        json={"file_name": "sample.png"},
    )

    assert response.status_code == test_case.expected_status_code
    content = response.json()

    if response.status_code == status.HTTP_200_OK:
        assert content["bucket_get_url"] is None
        assert content["bucket_post_url"] == test_case.expected_bucket_post_url
        assert content["fields"]["key"] == test_case.expected_object_key
        assert content["state"] == "claimed"
        assert content["claimed_time"]
        assert content["occupied_time"] is None
    else:
        assert content["detail"] == test_case.expected_error_message


# TODO: exception handling test case, state transition
def test_object_store_update(
    app: tuple[TestClient, AWSCallerMock],
    db_session: Session,
) -> None:
    fake_presigned_get_url = (
        "https://s3.eu-west-1.amazonaws.com/fake_bucket/my-key?AWSAccessKeyId=X&Signature=Y&Expires=123"
    )
    client, aws_caller = app
    aws_caller.create_presigned_get_url = MagicMock(
        return_value=fake_presigned_get_url,
    )
    db_object_store = crud.object_store_create(
        db=db_session,
        obj=ObjectStoreCreate(object_key="object_key", claimed_time=now(), occupied_time=None, bucket_get_url=None),
    )

    response = client.patch(
        f"/object-store/{db_object_store.id}",
        json={"state": ObjectStoreState.occupied.value},
    )

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["state"] == ObjectStoreState.occupied.value
    assert content["occupied_time"]
    assert content["object_key"] == "object_key"
    assert content["bucket_get_url"] == fake_presigned_get_url
