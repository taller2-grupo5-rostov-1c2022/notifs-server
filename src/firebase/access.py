import firebase_admin
import json
from src.constants import TESTING
from firebase_admin import credentials, auth
from src.mocks.firebase.auth import auth_mock
from firebase_admin import firestore
from src.mocks.firebase.database import db as db_mock

from dotenv import load_dotenv

load_dotenv()

db = db_mock
_auth = auth_mock

if not TESTING:
    # Use a service account
    # Si tira error porque no encuentra el archivo, copiar el google-credentials.json a /src
    with open("google-credentials.json") as json_file:
        cert_dict = json.load(json_file, strict=False)

    cred = credentials.Certificate(cert_dict)

    firebase_admin.initialize_app(
        cred, {"databaseURL": "https://rostov-spotifiuby.firebaseio.com"}
    )

    db = firestore.client()

    _auth = auth


def get_db():
    return db


def get_auth():
    return _auth
