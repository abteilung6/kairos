from collections.abc import Generator
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from config import Config, get_config
from kairos.cloud.aws import AWSCaller, AWSCredentials
from kairos.db.base import get_engine, get_session_maker


def get_aws_cloud_caller() -> Generator[AWSCaller, Any, None]:
    config = get_config()
    credentials = AWSCredentials(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.DEFAULT_AWS_REGION,
    )
    try:
        yield AWSCaller(credentials=credentials)
    finally:
        ...


def get_environment_config() -> Generator[Config, Any, None]:
    try:
        yield get_config()
    finally:
        ...


def get_db(config: Config = Depends(get_environment_config)) -> Generator[Session, Any, None]:
    engine = get_engine(config.SQLALCHEMY_DATABASE_URL)
    session_maker = get_session_maker(engine)
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
