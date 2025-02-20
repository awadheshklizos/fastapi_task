from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import init_db, close_db
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="/auth")


@app.get("/")
def read_root():
    return {"message": "FoR Test the code "}
