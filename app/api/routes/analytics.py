from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/")
def get_analytics():

    return {
        "total_diseases": 0,
        "total_medicines": 0,
        "total_guidelines": 0,
        "total_lab_tests": 0,
        "total_images": 0,
        "total_sources": 0,
        "coverage": "100%",
        "dataset_quality": "Good",
        "last_update": "Available",
    }