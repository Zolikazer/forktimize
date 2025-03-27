from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

from settings import SETTINGS

engine = create_engine(SETTINGS.DATABASE_CONNECTION_STRING, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
