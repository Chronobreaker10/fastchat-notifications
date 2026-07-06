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
        if not self._subscribers.get(user):
            self._subscribers[user] = {channel: queue}
        else:
            self._subscribers[user][channel] = queue
        return queue

    async def unsubscribe(self, user: UserID, channel: ChannelID) -> None:
        self._subscribers[user].pop(channel)

    async def publish(self, notification: NotificationRead) -> None:
        if channels := self._subscribers.get(notification.recipient_id):
            for queue in channels.values():
                await queue.put(notification)
