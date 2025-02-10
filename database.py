from sqlmodel import SQLModel, create_engine
from .config import settings

postgresql_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(postgresql_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)