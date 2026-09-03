from beanie import init_beanie
from pymongo import AsyncMongoClient

from .config import settings
from .models import Notification


async def setup_beanie() -> None:
    client = AsyncMongoClient(settings.database.url)
    await init_beanie(
        database=client[settings.database.name], document_models=[Notification]
    )
