from fastapi import APIRouter
from fastapi import Depends, Header
from src import schemas
from src.firebase.access import get_db
from src.repositories import message_utils

router = APIRouter(tags=["messages"])


@router.post("/messages/")
def post_message(
    notification: schemas.NotificationBase,
    target_uid: str = Header(...),
    uid: str = Header(...),
    db=Depends(get_db),
):
    """Send a message notification to a user"""

    message_utils.send_notification(notification, target_uid, uid, db)
