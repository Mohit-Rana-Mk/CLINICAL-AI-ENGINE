from fastapi import APIRouter

router = APIRouter(
    prefix="/medical-images",
    tags=["Medical Images"]
)

@router.get("/")
def get_medical_images():
    return {
        "status": "success",
        "message": "Medical Images API is working"
    }