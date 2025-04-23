from fastapi import APIRouter

# Create Router
router = APIRouter()

@router.get("/pymentorbot")
async def pymentorbot_interface():
    return {"message": "Welcome to PyMentorBot!"}
