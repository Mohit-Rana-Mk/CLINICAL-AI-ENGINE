from sqlalchemy.orm import Session
from app.models.lab_reference import LabReference


class LabRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(LabReference).offset(skip).limit(limit).all()

    def get_by_id(self, lab_id: int):
        return self.db.query(LabReference).filter(LabReference.id == lab_id).first()

    def get_by_test_name(self, test_name: str):
        return self.db.query(LabReference).filter(LabReference.test_name.ilike(f"%{test_name}%")).first()

    def search_by_test_name(self, test_name: str):
        return self.db.query(LabReference).filter(LabReference.test_name.ilike(f"%{test_name}%")).all()

    def get_by_gender(self, gender_specific: str):
        return self.db.query(LabReference).filter(LabReference.gender_specific == gender_specific).all()

    def create(self, data: dict) -> LabReference:
        lab_ref = LabReference(**data)
        self.db.add(lab_ref)
        self.db.commit()
        self.db.refresh(lab_ref)
        return lab_ref

    def update(self, lab_id: int, data: dict):
        lab_ref = self.get_by_id(lab_id)
        if lab_ref:
            for key, value in data.items():
                setattr(lab_ref, key, value)
            self.db.commit()
            self.db.refresh(lab_ref)
        return lab_ref

    def delete(self, lab_id: int) -> bool:
        lab_ref = self.get_by_id(lab_id)
        if lab_ref:
            self.db.delete(lab_ref)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        return self.db.query(LabReference).count()
