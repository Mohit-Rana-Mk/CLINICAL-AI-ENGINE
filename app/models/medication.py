from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    medicine_name = Column(
        String(100),
        nullable=False
    )

    dosage = Column(
        String(50)
    )

    frequency = Column(
        String(50)
    )

    patient = relationship("User")