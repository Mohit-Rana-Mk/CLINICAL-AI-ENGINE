from sqlalchemy.orm import Session
from app.models.disease import Disease


class DiseaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Disease).offset(skip).limit(limit).all()

    def get_by_id(self, disease_id: int):
        return self.db.query(Disease).filter(Disease.id == disease_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Disease).filter(Disease.name.ilike(f"%{name}%")).first()

    def search_by_name(self, name: str):
        return self.db.query(Disease).filter(Disease.name.ilike(f"%{name}%")).all()

    def get_by_category(self, category: str):
        return self.db.query(Disease).filter(Disease.category.ilike(f"%{category}%")).all()

    def get_by_severity(self, severity_level: str):
        return self.db.query(Disease).filter(Disease.severity_level == severity_level).all()

    def create(self, data: dict) -> Disease:
        disease = Disease(**data)
        self.db.add(disease)
        self.db.commit()
        self.db.refresh(disease)
        return disease

    def update(self, disease_id: int, data: dict):
        disease = self.get_by_id(disease_id)
        if disease:
            for key, value in data.items():
                setattr(disease, key, value)
            self.db.commit()
            self.db.refresh(disease)
        return disease

    def delete(self, disease_id: int) -> bool:
        disease = self.get_by_id(disease_id)
        if disease:
            self.db.delete(disease)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        return self.db.query(Disease).count()
