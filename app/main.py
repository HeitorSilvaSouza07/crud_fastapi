from fastapi import FastAPI
from .router import router as teste_router
from .user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(teste_router)