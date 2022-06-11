from fastapi import HTTPException
import json
from src import schemas
from firebase_admin import messaging


def get_token(uid: str, db):
    token = db.collection("tokens").document(uid).get()
    if not token.exists:
        raise HTTPException(status_code=404, detail=f"Token for user {uid} not found")

    return token.to_dict()["token"]


def send_notification(
    notification: schemas.NotificationBase, token: str, sender_uid: str
):
    """Send a message to a user"""

    if not notification.extra:
        extra = {}
    else:
        extra = notification.extra
    extra["sender_uid"] = sender_uid
    message = messaging.Message(
        data={
            "body": json.dumps(extra),
            "title": notification.title,
            "message": notification.body,
        },
        token=token,
    )

    messaging.send(message)
