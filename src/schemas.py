from typing import Optional

from pydantic.main import BaseModel


class TokenPost(BaseModel):
    token: str


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
