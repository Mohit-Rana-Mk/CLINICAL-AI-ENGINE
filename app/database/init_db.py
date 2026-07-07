from app.database.base import Base
from app.database.connection import engine

# Import all models
from app.models import *


def init_db():
    Base.metadata.create_all(bind=engine)