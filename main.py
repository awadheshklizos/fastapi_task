from fastapi import FastAPI
from app.core.database import init_db
from app.routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth")

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI MongoDB Example"}

    