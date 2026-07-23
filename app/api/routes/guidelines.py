from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.repositories.guideline_repository import GuidelineRepository

router = APIRouter(
    prefix="/guidelines",
    tags=["Guidelines"],
)


@router.get("/")
def get_all_guidelines(db: Session = Depends(get_db)):
    repository = GuidelineRepository(db)
    return repository.get_all_guidelines()