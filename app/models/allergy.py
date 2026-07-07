from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    allergen = Column(
        String(100),
        nullable=False
    )

    severity = Column(
        String(30)
    )

    patient = relationship("User")