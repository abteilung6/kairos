from collections.abc import Generator
from typing import Any, Literal

import pytest
from boto3 import Session
from botocore.stub import Stubber
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session as DBSession

from config import Config
from kairos.api.deps import get_aws_cloud_caller, get_db, get_environment_config
from kairos.app import get_app
from kairos.cloud.aws import AWSCaller, AWSCredentials
from kairos.db.base import Base, format_sqlite_url, get_engine, get_session_maker

SQLALCHEMY_TEST_DATABASE_URL = format_sqlite_url(suffix="testing")
ENGINE_TEST = get_engine(SQLALCHEMY_TEST_DATABASE_URL)


class AWSCallerMock(AWSCaller):
    def __init__(self, credentials: AWSCredentials) -> None:
        super().__init__(credentials)
        self.stubbers: dict[str, Stubber] = {}

    def _create_botocore_session(self) -> None:
        if self._botocore_session is None:
            self._botocore_session = Session()

    def _create_botocore_client(self, service_name: Literal["s3"]):  # noqa: ANN202
        if service_name not in self.stubbers:
            stubber = Stubber(super()._create_botocore_client(service_name=service_name))
            self.stubbers[service_name] = stubber
            stubber.activate()
        return self.stubbers[service_name].client

    def get_stubber(self, service_name: Literal["s3"]) -> Stubber:
        if service_name not in self.stubbers:
            self._create_botocore_client(service_name=service_name)
        return self.stubbers[service_name]


@pytest.fixture(name="aws_fake_credentials")
def fixture_aws_fake_credentials() -> AWSCredentials:
    return AWSCredentials(
        aws_access_key_id="fake_aws_access_key_id",
        aws_secret_access_key="fake_aws_secret_access_key",
        region_name="eu-west-1",
    )


@pytest.fixture(name="db_session")
def fixture_db_session() -> Generator[DBSession, Any, None]:
    Base.metadata.drop_all(bind=ENGINE_TEST)
    Base.metadata.create_all(bind=ENGINE_TEST)
    session_maker = get_session_maker(ENGINE_TEST)

    db = session_maker()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(name="app")
def fixture_app(aws_fake_credentials: AWSCredentials, db_session: DBSession) -> tuple[TestClient, AWSCallerMock]:
    app = get_app(skip_db=True, skip_cors=True)
    config = Config(
        AWS_ACCESS_KEY_ID=aws_fake_credentials.aws_access_key_id,
        AWS_SECRET_ACCESS_KEY=aws_fake_credentials.aws_secret_access_key.get_secret_value(),
        DEFAULT_AWS_REGION="eu-west-1",
        BUCKET_NAME="fake_bucket",
        SQLALCHEMY_DATABASE_URL=SQLALCHEMY_TEST_DATABASE_URL,
        KAIROS_CONSOLE_REMOTE="http://127.0.0.1:5173",
    )
    aws_caller_mock = AWSCallerMock(credentials=aws_fake_credentials)

    def override_get_aws_cloud_caller() -> Generator[AWSCallerMock, Any, None]:
        try:
            yield aws_caller_mock
        finally:
            ...

    def override_get_environment_config() -> Generator[Config, Any, None]:
        try:
            yield config
        finally:
            ...

    def override_get_db() -> Generator[DBSession, Any, None]:
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_environment_config] = override_get_environment_config
    app.dependency_overrides[get_aws_cloud_caller] = override_get_aws_cloud_caller
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app), aws_caller_mock
