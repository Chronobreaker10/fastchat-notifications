import asyncio
from uuid import UUID

from api.schemas import NotificationRead

type ChannelID = UUID
type UserID = int


class PubSubNotifications:
    def __init__(self) -> None:
        self._subscribers: dict[UserID, dict[ChannelID, asyncio.Queue]] = {}

    async def subscribe(self, user: UserID, channel: ChannelID) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._subscribers[user][channel] = queue
        return queue

    async def unsubscribe(self, user: UserID, channel: ChannelID) -> None:
        self._subscribers[user].pop(channel)

    async def publish(self, notification: NotificationRead) -> None:
        for queue in self._subscribers[notification.recipient_id].values():
            await queue.put(notification)
