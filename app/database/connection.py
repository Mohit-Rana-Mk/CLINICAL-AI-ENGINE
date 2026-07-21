import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    host=settings.MYSQL_HOST,
    port=int(settings.MYSQL_PORT),
    database=settings.MYSQL_DATABASE,
)

logger.info(
    "Initializing MySQL database connection."
)

engine = create_engine(

    DATABASE_URL,

    echo=settings.DEBUG,

    future=True,

    pool_pre_ping=True,

    pool_recycle=3600,

    pool_size=10,

    max_overflow=20,

    pool_timeout=30,

    pool_reset_on_return="rollback",

)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

logger.info(
    "Database engine initialized successfully."
)