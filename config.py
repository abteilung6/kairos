from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: SecretStr
    DEFAULT_AWS_REGION: str = "eu-west-1"
    BUCKET_NAME: str


def get_config() -> Config:
    return Config()
