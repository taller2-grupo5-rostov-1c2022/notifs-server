from fastapi import APIRouter
from fastapi import Depends, Header
from src import schemas


from src.firebase.access import get_db
from src.repositories import message_utils, notifications_utils, token_utils

router = APIRouter(tags=["messages"])


@router.post("/messages/")
def post_message(
    notification: schemas.NotificationBase,
    target_uid: str = Header(...),
    uid: str = Header(...),
    db=Depends(get_db),
):
    """Send a message notification to a user"""

    token = token_utils.get_token(target_uid, db)

    message_data = message_utils.parse_message_data(notification, uid)

    notifications_utils.store_notification(message_data, target_uid, db)

    message_utils.send_message(message_data, token)
