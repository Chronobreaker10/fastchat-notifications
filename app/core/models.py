from datetime import datetime

from beanie import Document, Indexed


class Notification(Document):
    body: str
    created_at: Indexed(datetime)
    chat_id: Indexed(str)
    recipient_id: Indexed(int)
    is_viewed: bool = False

    class Settings:
        name = "notifications"
