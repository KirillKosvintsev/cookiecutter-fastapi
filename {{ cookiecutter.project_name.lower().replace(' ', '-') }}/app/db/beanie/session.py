from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.config import settings
from app.models.example_model import User


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.DATABASE_NAME], document_models=[User])
