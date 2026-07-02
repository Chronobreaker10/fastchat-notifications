from api.errors import ForbiddenError, NotificationNotFoundError
from api.schemas import NotificationCreate, NotificationRead, NotificationUpdate, User
from core.models import Notification


async def get_notification(notification_id: str) -> Notification:
    notification = await Notification.get(notification_id)
    if notification is None:
        raise NotificationNotFoundError(notification_id)
    return notification


async def create_notification(notification: NotificationCreate) -> NotificationRead:
    notification = Notification(**notification.model_dump())
    result = await notification.insert()
    return NotificationRead(**result.model_dump(exclude={"id"}), id=str(result.id))


async def delete_notification(notification_id: str) -> str:
    notification = await get_notification(notification_id)
    await notification.delete()
    return str(notification.id)


async def update_notification(
    notification_id: str, data: NotificationUpdate, current_user: User
) -> NotificationRead:
    notification = await get_notification(notification_id)
    if notification.recipient_id != current_user.id:
        raise ForbiddenError
    result = await notification.set(data.model_dump())
    return NotificationRead(**result.model_dump(exclude={"id"}), id=str(result.id))


async def get_user_unviewed_notifications(user_id: int) -> list[NotificationRead]:
    notifications = (
        await Notification.find({"recipient_id": user_id, "is_viewed": False})
        .sort("-created_at")
        .to_list(length=10)
    )
    return [
        NotificationRead(**item.model_dump(exclude={"id"}), id=str(item.id))
        for item in notifications
    ]
