from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Vital(Base):
    __tablename__ = "vitals"

    id = Column(Integer, primary_key=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    temperature = Column(Float)

    pulse = Column(Integer)

    spo2 = Column(Integer)

    systolic_bp = Column(Integer)

    diastolic_bp = Column(Integer)

    patient = relationship("User")