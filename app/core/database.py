from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user_model import User
from app.models.trash_model import Trash
from .config import settings


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User, Trash]
    ) 

