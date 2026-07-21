from sqlalchemy import Column, Integer, String, Text

from app.database.base import Base


class MedicalImage(Base):
    __tablename__ = "medical_images"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    category = Column(String(100))

    image_type = Column(String(100))

    diagnosis = Column(Text)

    findings = Column(Text)

    image_path = Column(String(500))