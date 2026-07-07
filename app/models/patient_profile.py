from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    gender = Column(String(20))

    date_of_birth = Column(Date)

    blood_group = Column(String(10))

    phone = Column(String(20))

    emergency_contact = Column(String(20))

    address = Column(String(255))

    user = relationship("User")