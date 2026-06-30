from api import service
from api.schemas import NotificationCreate, NotificationRead, NotificationUpdate
from core.config import settings
from faststream.kafka.fastapi.fastapi import KafkaRouter

router = KafkaRouter(
    bootstrap_servers=settings.kafka.bootstrap_servers,
    prefix="/notifications",
    tags=["Уведомления"],
)


@router.post("/notifications", response_model=NotificationRead)
async def create_notification(notification: NotificationCreate) -> NotificationRead:
    return await service.create_notification(notification)


@router.get("/notifications/{user_id}", response_model=list[NotificationRead])
async def get_user_notifications(user_id: int) -> list[NotificationRead]:
    return await service.get_user_unviewed_notifications(user_id)


@router.patch("/notifications/{notification_id}", response_model=NotificationRead)
async def view_notification(notification_id: str) -> NotificationRead:
    return await service.update_notification(
        notification_id, NotificationUpdate(is_viewed=True)
    )


@router.subscriber(settings.kafka.notifications_topic)
async def receive_notification(notification: NotificationCreate) -> None:
    await service.create_notification(notification)
