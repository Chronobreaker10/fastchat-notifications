from beanie import init_beanie
from pymongo import AsyncMongoClient

from .config import settings
from .models import Notification


async def setup_beanie() -> None:
    client = AsyncMongoClient(str(settings.database.dev_dsn))
    await init_beanie(
        database=client[settings.database.name], document_models=[Notification]
    )
