from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(150),
        nullable=False
    )

    generic_name = Column(
        String(150)
    )

    drug_class = Column(
        String(100)
    )

    standard_dosage = Column(
        String(200)
    )

    side_effects = Column(
        String(1000)
    )

    contraindications = Column(
        String(1000)
    )

    guideline_source = Column(
        String(50)
    )