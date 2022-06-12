from fastapi import HTTPException
import json
from src import schemas
from firebase_admin import messaging
from google.cloud import firestore
from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def get_token(uid: str, db):
    token = db.collection("tokens").document(uid).get()
    if not token.exists:
        raise HTTPException(status_code=404, detail=f"Token for user {uid} not found")

    return token.to_dict()["token"]

def store_notification(notification: schemas.NotificationBase, receiver_uid: str, db):
    """Store a notification in the database"""

    user_notifications = db.collection("notifications").document(receiver_uid)
    user_notifications.update({'notifications': firestore.ArrayUnion([notification.dict()])})

def clear_notifications(uid: str, db):
    """Clear all notifications for a user"""

    db.collection("notifications").document(uid).set({'notifications': []})

def send_notification(
    notification: schemas.NotificationBase, token: str, sender_uid: str
):
    """Send a message to a user"""

    if not notification.extra:
        extra = {}
    else:
        extra = json.loads(notification.extra)
    extra["sender_uid"] = sender_uid
    extra["type"] = "message"
    message = messaging.Message(
        data={
            "body": json.dumps(extra),
            "title": notification.title,
            "message": notification.body,
        },
        token=token,
    )

    messaging.send(message)
