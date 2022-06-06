from fastapi import APIRouter
from fastapi import Depends, HTTPException, UploadFile, Header
from firebase_admin import messaging
from src import schemas
from src.firebase.access import get_db
from src.repositories import message_utils

router = APIRouter(tags=["messages"])


@router.post("/messages/")
def post_message(
    message_info: schemas.MessageBase,
    target_uid: str = Header(...),
    uid: str = Header(...),
):
    """Send a message notification to a user"""

    message_info.uid = uid
    token = message_utils.retrieve_token(target_uid)
    message_utils.send_message(message_info, token)
