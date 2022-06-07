from fastapi import APIRouter
from fastapi import Depends, HTTPException, UploadFile

from src import schemas
from src.firebase.access import get_db
from src.repositories import token_utils

router = APIRouter(tags=["tokens"])


@router.post("/tokens/")
def post_token(
    token_info: schemas.TokenPost,
    db=Depends(get_db),
):
    """Associate a token with a user"""

    db.collection("tokens").document(token_info.uid).set(
        {
            "token": token_info.token,
        }
    )


@router.delete("/tokens/{uid}")
def delete_token(uid: str, db=Depends(get_db)):
    """Delete a token"""

    token_utils.delete_token(uid, db)
