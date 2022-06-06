from pydantic.main import BaseModel


class TokenPost(BaseModel):
    token: str
    uid: str


class NotificationBase(BaseModel):
    title: str
    body: str
