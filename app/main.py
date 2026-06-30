from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from api.errors import setup_exceptions
from api.router import router
from core.config import settings
from core.database import setup_beanie
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    await setup_beanie()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
setup_exceptions(app)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.run_config.host, port=settings.run_config.port)
