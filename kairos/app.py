from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_config
from kairos.api.api import api_router
from kairos.db.base import Base, get_engine


def get_app(*, skip_db: bool = False, skip_cors: bool = False) -> FastAPI:
    if not skip_db:
        config = get_config()
        engine = get_engine(config.SQLALCHEMY_DATABASE_URL)
        Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="Kairos API",
        description="This specification descibes the Kairos API.",
    )
    app.include_router(api_router)

    if not skip_cors:
        origins = [config.KAIROS_CONSOLE_REMOTE] if config.KAIROS_CONSOLE_REMOTE else []

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return app
