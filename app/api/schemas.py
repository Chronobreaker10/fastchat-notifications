import uuid
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class NotificationCreate(BaseModel):
    body: Annotated[str, Field(min_length=1, max_length=500, title="Текст уведомления")]
    created_at: Annotated[datetime, Field(title="Время отправки уведомления")]
    chat_id: Annotated[UUID, Field(title="Идентификатор связанного чата")]
    recipient_id: Annotated[int, Field(ge=1, title="Идентификатор получателя")]

    @field_serializer("chat_id")
    def convert_chat_id(self, value: UUID) -> str:
        return str(value)


class NotificationUpdate(BaseModel):
    is_viewed: Annotated[bool, Field(title="Просмотрено ли получателем")]


class NotificationRead(NotificationCreate, NotificationUpdate):
    id: Annotated[str, Field(title="Идентификатор уведомления")]

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    sub: Annotated[int | uuid.UUID, Field(title="Уникальный идентификатор сущности")]
    iss: Annotated[int | None, Field(title="Издатель токена", ge=1)] = None
    username: Annotated[str | None, Field(title="Имя пользователя")] = None
    user_registered_at: Annotated[
        str | None, Field(title="Дата регистрации пользователя")
    ] = None


class User(BaseModel):
    id: Annotated[int, Field(ge=1, title="ID", description="ID пользователя")]
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            title="Имя пользователя",
            description="Имя пользователя",
        ),
    ]
    created_at: Annotated[
        datetime,
        Field(
            title="Зарегистрировался",
            description="Зарегистрировался",
        ),
    ]


class StatusResponse(BaseModel):
    success: Annotated[bool, Field(title="Статус ответа")]
