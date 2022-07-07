from fastapi import HTTPException


def delete_token(uid: str, db):
    """Delete a token"""

    document = db.collection("tokens").document(uid)
    if document.get().exists:
        document.delete()
    else:
        raise HTTPException(status_code=404, detail=f"Token for {uid} not found")


def get_token(uid: str, db):
    """Get a token"""

    document = db.collection("tokens").document(uid)
    if document.get().exists:
        return document.get().to_dict()["token"]
    else:
        raise HTTPException(status_code=404, detail=f"Token for {uid} not found")
