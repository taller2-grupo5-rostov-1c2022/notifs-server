from fastapi import APIRouter
from fastapi import Depends, Header

from src.firebase.access import get_db
from src.repositories import notifications_utils

router = APIRouter(tags=["notifications"])

@router.get("/notifications/")
def get_notifications(uid: str = Header(...), db=Depends(get_db)):
    """Get all notifications for a user"""

    return notifications_utils.get_notifications(uid, db)

@router.delete("/notifications/")
def clear_notifications(uid: str = Header(...), db=Depends(get_db)):
    """Clear all notifications for a user"""

    notifications_utils.clear_notifications(uid, db)
