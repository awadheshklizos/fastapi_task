
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db
from app.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    await init_db()
    yield
    print("Application is shutting donw...")

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="/auth")


@app.get("/")
def read_root():
    return {"message": "FoR Test the code "}
    