from fastapi import (
    FastAPI,
    Depends,
)
from src.app import tokens, messages
from src.middleware.utils import get_api_key

API_VERSION_PREFIX = "/api/v3"

app = FastAPI(
    title="Notifs API",
    description="Spotifiuby's API to manage notifications",
    version="0.0.1",
    dependencies=[Depends(get_api_key)],
)

app.include_router(tokens.router, prefix=API_VERSION_PREFIX)
app.include_router(messages.router, prefix=API_VERSION_PREFIX)
