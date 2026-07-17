from collections.abc import Generator

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.database.connection import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI database dependency.

    Creates a new SQLAlchemy session for each request
    and ensures it is always closed after use.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()