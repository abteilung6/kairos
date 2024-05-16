from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


def format_sqlite_url(suffix: str) -> str:
    return f"sqlite:///./sqlite_{suffix}.db"


def get_engine(sqlite_url: str) -> Engine:
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session_maker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
