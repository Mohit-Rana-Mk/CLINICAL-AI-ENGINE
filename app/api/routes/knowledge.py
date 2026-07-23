from fastapi import APIRouter

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)

@router.get("/")
def get_knowledge():
    return {
        "status": "success",
        "message": "Knowledge API is working"
    }