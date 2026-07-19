from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(150),
        nullable=False
    )

    category = Column(
        String(100)
    )

    description = Column(
        String(1000)
    )

    common_symptoms = Column(
        String(500)
    )

    severity_level = Column(
        String(30)
    )

    guideline_source = Column(
        String(50)
    )