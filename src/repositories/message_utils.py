import json
from src import schemas
from firebase_admin import messaging


def parse_message_data(notification: schemas.NotificationBase, sender_uid: str):

    """Return a message dict from a notification"""

    body = {"sender_uid": sender_uid, "type": "message"}

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
