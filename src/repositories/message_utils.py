from src import schemas

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
)

from src.repositories import token_utils


def send_notification(
    notification: schemas.NotificationBase, recv_uid: str, sender_uid: str, db
):
    """Send a message to a user"""

    token = token_utils.get_token(recv_uid, db)

    response = PushClient().publish(
        PushMessage(to=token, body=notification.dict(), data={"sender_uid": sender_uid})
    )
    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors, so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        token_utils.delete_token(sender_uid, db)
