from __future__ import annotations

from datetime import datetime
from functools import cache
from typing import Annotated

from fastapi import Cookie, Depends

from ..core.config import settings
from ..core.pubsub_notifications import PubSubNotifications
from ..core.security import validate_token
from .errors import UnauthorizedError
from .schemas import User


async def get_current_user(
    auth_cookie: Annotated[
        str | None, Cookie(alias=settings.security.access_token_cookie_name)
    ] = None,
) -> User:
    if auth_cookie is None:
        raise UnauthorizedError
    token_data = validate_token(auth_cookie)
    if token_data.username is None or token_data.user_registered_at is None:
        raise UnauthorizedError
    return User(
        id=int(token_data.sub),
        username=token_data.username,
        created_at=datetime.fromisoformat(token_data.user_registered_at),
    )


@cache
def get_pubsub() -> PubSubNotifications:
    return PubSubNotifications()


CurrentUserDep = Annotated[User, Depends(get_current_user)]
PubSubNotificationsDep = Annotated[PubSubNotifications, Depends(get_pubsub)]
