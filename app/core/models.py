from datetime import datetime
from typing import Annotated

from beanie import Document, Indexed


class Notification(Document):
    body: str
    created_at: Annotated[datetime, Indexed()]
    chat_id: str
    chat_name: str
    recipient_id: Annotated[int, Indexed()]
    is_viewed: Indexed(bool) = False

    class Settings:
        name = "notifications"
