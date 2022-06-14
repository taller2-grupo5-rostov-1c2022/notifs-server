from fastapi import HTTPException
import json
from src import schemas
from firebase_admin import messaging


def get_token(uid: str, db):
    token = db.collection("tokens").document(uid).get()
    if not token.exists:
        raise HTTPException(status_code=404, detail=f"Token for user {uid} not found")

    return token.to_dict()["token"]


def parse_message_data(notification: schemas.NotificationBase, sender_uid: str):

    """Return a message dict from a notification"""

    body = {
        "sender_uid": sender_uid,
        "type": "message"
    }
    
    data = {
        "body": json.dumps(body),
        "title": notification.title,
        "message": notification.body,
    }

    return data


def send_message(data: dict, token: str):

    """Return a message dict from a notification"""

    message = messaging.Message(
        data=data,
        token=token,
    )

    messaging.send(message)
