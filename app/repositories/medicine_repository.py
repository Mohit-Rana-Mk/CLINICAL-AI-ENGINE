from sqlalchemy.orm import Session
from app.models.medicine import Medicine


class MedicineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Medicine).offset(skip).limit(limit).all()

    def get_by_id(self, medicine_id: int):
        return self.db.query(Medicine).filter(Medicine.id == medicine_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Medicine).filter(Medicine.name.ilike(f"%{name}%")).first()

    def search_by_name(self, name: str):
        return self.db.query(Medicine).filter(Medicine.name.ilike(f"%{name}%")).all()

    def get_by_generic_name(self, generic_name: str):
        return self.db.query(Medicine).filter(Medicine.generic_name.ilike(f"%{generic_name}%")).all()

    def get_by_drug_class(self, drug_class: str):
        return self.db.query(Medicine).filter(Medicine.drug_class.ilike(f"%{drug_class}%")).all()

    def create(self, data: dict) -> Medicine:
        medicine = Medicine(**data)
        self.db.add(medicine)
        self.db.commit()
        self.db.refresh(medicine)
        return medicine

    def update(self, medicine_id: int, data: dict):
        medicine = self.get_by_id(medicine_id)
        if medicine:
            for key, value in data.items():
                setattr(medicine, key, value)
            self.db.commit()
            self.db.refresh(medicine)
        return medicine

    def delete(self, medicine_id: int) -> bool:
        medicine = self.get_by_id(medicine_id)
        if medicine:
            self.db.delete(medicine)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        return self.db.query(Medicine).count()
