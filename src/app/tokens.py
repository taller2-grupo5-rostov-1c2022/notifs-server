from fastapi import APIRouter
from fastapi import Depends, HTTPException, UploadFile

from src import schemas
from src.firebase.access import get_db

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
    document = db.collection("tokens").document(uid)
    if document.get().exists:
        document.delete()
    else:
        raise HTTPException(status_code=404, detail=f"Token for {uid} not found")
