from sqlmodel import SQLModel, create_engine, Session

from settings import SETTINGS

engine = create_engine(SETTINGS.DATABASE_LOCATION, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
