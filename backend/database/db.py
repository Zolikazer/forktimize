from sqlmodel import SQLModel, create_engine, Session

from settings import SETTINGS

DATABASE_URL = "sqlite:///:memory:" if SETTINGS.TEST_MODE else SETTINGS.DATABASE_LOCATION

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
