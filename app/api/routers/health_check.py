from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    # tags=[""],
)

@router.get("/")
def health_check():
    return 200
