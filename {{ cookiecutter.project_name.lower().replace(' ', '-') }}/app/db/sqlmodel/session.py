from sqlmodel import SQLModel, create_engine, Session
from app.config.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
