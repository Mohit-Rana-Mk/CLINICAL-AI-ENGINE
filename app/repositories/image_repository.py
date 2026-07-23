from sqlalchemy.orm import Session

from app.models.medical_image import MedicalImage


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(MedicalImage).offset(skip).limit(limit).all()

    def get_by_id(self, image_id: int):
        return self.db.query(MedicalImage).filter(MedicalImage.id == image_id).first()

    def search_by_filename(self, filename: str):
        return (
            self.db.query(MedicalImage)
            .filter(MedicalImage.filename.ilike(f"%{filename}%"))
            .all()
        )

    def get_by_category(self, category: str):
        return (
            self.db.query(MedicalImage)
            .filter(MedicalImage.category.ilike(f"%{category}%"))
            .all()
        )

    def create(self, data: dict):
        image = MedicalImage(**data)
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def update(self, image_id: int, data: dict):
        image = self.get_by_id(image_id)
        if image:
            for key, value in data.items():
                setattr(image, key, value)
            self.db.commit()
            self.db.refresh(image)
        return image

    def delete(self, image_id: int):
        image = self.get_by_id(image_id)
        if image:
            self.db.delete(image)
            self.db.commit()
            return True
        return False

    def count(self):
        return self.db.query(MedicalImage).count()