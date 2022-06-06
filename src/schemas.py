from pydantic.main import BaseModel


class TokenPost(BaseModel):
    token: str
    uid: str


class NotifyBase(BaseModel):
    title: str
    body: str


class MessageBase(BaseModel):
    message: str
    notify: NotifyBase
