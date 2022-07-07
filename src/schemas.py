from typing import Optional

from pydantic.main import BaseModel


class TokenPost(BaseModel):
    token: str


class NotificationInfo(BaseModel):
    sender_uid: str
    type: str


class NotificationGet(BaseModel):
    title: str
    message: str
    body: NotificationInfo


class NotificationBase(BaseModel):
    title: str
    body: str
    extra: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Message Title",
                "body": "Message",
                "extra": "Optional Data (Currently Unused)",
            }
        }
