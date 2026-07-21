from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.disease_repository import DiseaseRepository

router = APIRouter(
    prefix="/diseases",
    tags=["Diseases"],
)


@router.get("/")
def get_all_diseases(db: Session = Depends(get_db)):
    repository = DiseaseRepository(db)
    return repository.get_all()