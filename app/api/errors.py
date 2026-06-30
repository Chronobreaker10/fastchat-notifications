from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class BaseHTTPError(Exception):
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Произошла непредвиденная ошибка"
    headers: dict | None = None

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message


class NotificationNotFoundError(BaseHTTPError):
    code: int = status.HTTP_404_NOT_FOUND

    def __init__(self, notification_id: str) -> None:
        self.message = f"Уведомление с ID {notification_id} не найдено"


async def handle_base_http_error(_: Request, exc: BaseHTTPError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message},
        headers=getattr(exc, "headers", None),
    )


def setup_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(BaseHTTPError, handle_base_http_error)
