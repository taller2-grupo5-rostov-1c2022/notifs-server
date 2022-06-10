from fastapi import APIRouter, Header, Depends, HTTPException

from src import schemas
from src.firebase.access import get_db
from src.repositories import token_utils

router = APIRouter(tags=["tokens"])


@router.post("/tokens/")
def post_token(
    token_info: schemas.TokenPost,
    uid: str = Header(...),
    db=Depends(get_db),
):
    """Associate a token with a user"""

    db.collection("tokens").document(uid).set(
        {
            "token": token_info.token,
        }
    )


@router.delete("/tokens/")
def delete_token(uid: str = Header(...), db=Depends(get_db)):
    """Delete a token"""
    token_utils.delete_token(uid, db)
