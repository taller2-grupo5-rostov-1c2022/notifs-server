import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.mocks.firebase.database import db as db_mock
from src.mocks.firebase.database import CollectionMock


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    db_mock.collections["tokens"] = CollectionMock()
    db_mock.collections["notifications"] = CollectionMock()
    db_mock.collections["messages"] = CollectionMock()
