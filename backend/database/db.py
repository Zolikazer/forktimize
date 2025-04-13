from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

from settings import SETTINGS

ENGINE = create_engine(SETTINGS.database_connection_string, echo=False)


def init_db():
    SQLModel.metadata.create_all(ENGINE)


def get_session() -> Generator[Session, None, None]:
    with Session(ENGINE) as session:
        yield session
