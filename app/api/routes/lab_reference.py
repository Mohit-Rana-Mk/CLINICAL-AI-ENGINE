from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.lab_repository import LabRepository

router = APIRouter(
    prefix="/lab-reference",
    tags=["Lab Reference"],
)


@router.get("/")
def get_all_lab_references(db: Session = Depends(get_db)):
    repository = LabRepository(db)
    return repository.get_all()