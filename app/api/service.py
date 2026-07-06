from api.errors import ForbiddenError, NotificationNotFoundError
from api.schemas import NotificationCreate, NotificationRead, NotificationUpdate, User
from bson import ObjectId
from core.models import Notification


async def get_notification(notification_id: str) -> Notification:
    notification = await Notification.get(notification_id)
    if notification is None:
        raise NotificationNotFoundError(notification_id)
    return notification


async def get_notifications(notifications_ids: list[ObjectId]) -> list[Notification]:
    return await Notification.find({"_id": {"$in": notifications_ids}}).to_list()


async def create_notification(data: NotificationCreate) -> NotificationRead:
    notification = Notification(**data.model_dump())
    result = await notification.insert()
    return NotificationRead(**result.model_dump(exclude={"id"}), id=str(result.id))


async def delete_notification(notification_id: str) -> str:
    notification = await get_notification(notification_id)
    await notification.delete()
    return str(notification.id)


async def update_notifications(
    notifications_ids: list[str], data: NotificationUpdate, current_user: User
) -> None:
    object_ids = [ObjectId(id_str) for id_str in notifications_ids]
    notifications = await get_notifications(object_ids)
    for notification in notifications:
        if notification.recipient_id != current_user.id:
            raise ForbiddenError
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(notification, key, value)
    await Notification.find({"_id": {"$in": object_ids}}).update_many(
        {"$set": data.model_dump()}
    )


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
