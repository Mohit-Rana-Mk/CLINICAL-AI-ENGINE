from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.core.config import settings

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    host=settings.MYSQL_HOST,
    port=int(settings.MYSQL_PORT),
    database=settings.MYSQL_DATABASE,
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)