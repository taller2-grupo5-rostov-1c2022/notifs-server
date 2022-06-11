from typing import Optional

from pydantic.main import BaseModel


class TokenPost(BaseModel):
    token: str


class NotificationBase(BaseModel):
    title: str
    body: str
    extra: Optional[dict]
