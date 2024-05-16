from fastapi import FastAPI

from config import get_config
from kairos.api.api import api_router
from kairos.db.base import Base, get_engine


def get_app(*, skip_db: bool = False) -> FastAPI:
    if not skip_db:
        config = get_config()
        engine = get_engine(config.SQLALCHEMY_DATABASE_URL)
        Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="Kairos API",
        description="This specification descibes the Kairos API.",
    )
    app.include_router(api_router)
    return app
