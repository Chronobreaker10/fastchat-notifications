import asyncio
import uuid
from collections.abc import AsyncIterable
from typing import Annotated

from fastapi import Body, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent
from faststream import AckPolicy
from faststream.kafka.fastapi.fastapi import KafkaRouter

from ..core.config import settings
from . import service
from .dependencies import CurrentUserDep, PubSubNotificationsDep
from .schemas import (
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
    StatusResponse,
)

router = KafkaRouter(
    bootstrap_servers=settings.kafka.bootstrap_servers,
    prefix="/notifications",
    tags=["Уведомления"],
)


@router.get(
    "/",
    summary="Получение уведомлений текущего пользователя",
    response_model=list[NotificationRead],
)
async def get_user_notifications(
    current_user: CurrentUserDep,
) -> list[NotificationRead]:
    return await service.get_user_unviewed_notifications(current_user.id)


@router.patch(
    "/", summary="Отметка уведомлений как просмотренных", response_model=StatusResponse
)
async def view_notifications(
    notifications_ids: Annotated[list[str], Body(embed=True)],
    current_user: CurrentUserDep,
) -> StatusResponse:
    await service.update_notifications(
        notifications_ids, NotificationUpdate(is_viewed=True), current_user
    )
    return StatusResponse(success=True)


@router.get(
    "/events",
    summary="Получение новых уведомлений через SSE",
    response_class=EventSourceResponse,
)
async def get_notifications_events(
    current_user: CurrentUserDep, pubsub: PubSubNotificationsDep, request: Request
) -> AsyncIterable[ServerSentEvent]:
    channel_id = uuid.uuid7()
    queue = await pubsub.subscribe(current_user.id, channel_id)
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                data = await asyncio.wait_for(queue.get(), timeout=1)
                yield ServerSentEvent(data=data, event="new_notification")
            except TimeoutError:
                continue
    finally:
        await pubsub.unsubscribe(current_user.id, channel_id)


@router.subscriber(
    settings.kafka.notifications_topic,
    group_id=settings.kafka.notifications_group,
    ack_policy=AckPolicy.ACK,
)
@router.publisher(settings.kafka.fanout_notifications_topic)
async def receive_notification(notification: NotificationCreate) -> NotificationRead:
    return await service.create_notification(notification)


@router.subscriber(settings.kafka.fanout_notifications_topic)
async def send_notification(
    notification: NotificationRead, pubsub: PubSubNotificationsDep
) -> None:
    await pubsub.publish(notification)
