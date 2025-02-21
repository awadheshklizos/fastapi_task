from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import init_db, close_db
from app.routers import auth
from beanie import init_beanie

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        yield 
    except Exception as e:
        
        raise
    finally:
        await close_db()

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "FoR Test the code "}
