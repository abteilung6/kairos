from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: SecretStr
    DEFAULT_AWS_REGION: str = "eu-west-1"
    BUCKET_NAME: str
    SQLALCHEMY_DATABASE_URL: str
    KAIROS_CONSOLE_REMOTE: str | None


def get_config() -> Config:
    return Config()
