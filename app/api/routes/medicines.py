from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.medicine_repository import MedicineRepository

router = APIRouter(
    prefix="/medicines",
    tags=["Medicines"],
)


@router.get("/")
def get_all_medicines(db: Session = Depends(get_db)):
    repository = MedicineRepository(db)
    return repository.get_all()