from fastapi import Depends, HTTPException

from src import schemas
from src.firebase.access import get_db
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

    message = messaging.Message(
        notification=messaging.Notification(
            title=notification.title, body=notification.body
        ),
        data={"sender_uid": sender_uid},
        token=token,
    )

    messaging.send(message)
