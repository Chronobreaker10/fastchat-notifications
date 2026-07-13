from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from ..core.utils import get_msc_dt


class NotificationCreate(BaseModel):
    body: Annotated[str, Field(min_length=1, max_length=500, title="Текст уведомления")]
    created_at: Annotated[datetime, Field(title="Время отправки уведомления")]
    chat_id: Annotated[UUID, Field(title="Идентификатор связанного чата")]
    chat_name: Annotated[str, Field(title="Имя связанного чата")]
    recipient_id: Annotated[int, Field(ge=1, title="Идентификатор получателя")]

    @field_serializer("chat_id")
    def convert_chat_id(self, v: UUID) -> str:
        return str(v)


class NotificationUpdate(BaseModel):
    is_viewed: Annotated[bool, Field(title="Просмотрено ли получателем")]


class NotificationRead(NotificationCreate, NotificationUpdate):
    id: Annotated[str, Field(title="Идентификатор уведомления")]

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def created_at_to_msc_dt(self, v: datetime) -> datetime:
        return get_msc_dt(v.replace(microsecond=0))


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
