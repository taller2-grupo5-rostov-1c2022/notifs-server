from google.cloud import firestore


def get_notifications(uid: str, db):
    """Get all notifications for a user"""

    notifications = db.collection("notifications").document(uid).get()
    if not notifications.exists:
        return []

    return notifications.to_dict()["notifications"]


def store_notification(message_data: dict, receiver_uid: str, db):
    """Store a notification in the database"""

    user_notifications_document = db.collection("notifications").document(receiver_uid)
    user_notifications = user_notifications_document.get()
    if not user_notifications.exists:
        user_notifications_document.set({"notifications": [message_data]})
    else:
        user_notifications_document.set(
            {
                "notifications": user_notifications.to_dict()["notifications"]
                + [message_data]
            }
        )


def clear_notifications(uid: str, db):
    """Clear all notifications for a user"""

    db.collection("notifications").document(uid).set({"notifications": []})
