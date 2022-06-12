from src import schemas
from google.cloud import firestore

def get_notifications(uid: str, db):
    """Get all notifications for a user"""

    notifications = db.collection("notifications").document(uid).get()
    if not notifications.exists:
        return []

    return notifications.to_dict()["notifications"]

def store_notification(notification: schemas.NotificationBase, receiver_uid: str, db):
    """Store a notification in the database"""

    user_notifications = db.collection("notifications").document(receiver_uid)
    user_notifications.update({'notifications': firestore.ArrayUnion([notification.dict()])})

def clear_notifications(uid: str, db):
    """Clear all notifications for a user"""

    db.collection("notifications").document(uid).set({'notifications': []})