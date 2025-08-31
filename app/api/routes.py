from fastapi import APIRouter


router = APIRouter(prefix="")  


# Health check endpoint
@router.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}
