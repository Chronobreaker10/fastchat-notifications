from beanie import init_beanie
from core.config import settings
from core.models import Notification
from pymongo import AsyncMongoClient


async def setup_beanie() -> None:
    client = AsyncMongoClient(str(settings.database.dev_dsn))
    await init_beanie(
        database=client[settings.database.name], document_models=[Notification]
    )
