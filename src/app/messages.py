from fastapi import APIRouter
from fastapi import Depends, HTTPException, UploadFile, Header
from firebase_admin import messaging
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

    token = message_utils.get_token(target_uid, db)

    message_utils.send_notification(notification, token, uid)
