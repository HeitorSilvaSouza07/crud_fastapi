from fastapi import APIRouter

router = APIRouter(
    prefix='/teste'
)

@router.get("/")
def hello_word():
    return {"message": "teste!"}