from sqlalchemy import Column, Integer, String

from app.database.base import Base


class LabReference(Base):
    __tablename__ = "lab_references"

    id = Column(Integer, primary_key=True)

    test_name = Column(
        String(150),
        nullable=False
    )

    unit = Column(
        String(50)
    )

    normal_range_min = Column(
        String(50)
    )

    normal_range_max = Column(
        String(50)
    )

    gender_specific = Column(
        String(20)
    )

    description = Column(
        String(500)
    )

    guideline_source = Column(
        String(50)
    )