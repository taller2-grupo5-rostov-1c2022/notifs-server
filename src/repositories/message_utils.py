from fastapi import Depends, HTTPException

from src import schemas
from src.firebase.access import get_db
from firebase_admin import messaging


def retrieve_token(uid: str, db=Depends(get_db)):
    """Retrieve a token by its uid"""

    token = db.collection("tokens").document(uid).get()
    if token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    return token.to_dict()["token"]


def send_message(message_info: schemas.MessageBase, token: str):
    """Send a message to a user"""

    message = messaging.Message(
        data=message_info.dict(),
        token=token,
    )
    messaging.send(message)
