from src.mocks.firebase.database import db as db_mock
from src.main import API_VERSION_PREFIX


def test_post_one_token(client):
    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_my_uid", "uid": "my_uid"},
        headers={"api_key": "key"},
    )

    document = db_mock.collection("tokens").document("my_uid").get()
    assert document.exists is True
    assert document.to_dict()["token"] == "token_for_my_uid"
    assert response.status_code == 200


def test_post_two_tokens(client):

    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_my_uid", "uid": "my_uid"},
        headers={"api_key": "key"},
    )
    assert response.status_code == 200

    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_another_uid", "uid": "another_uid"},
        headers={"api_key": "key"},
    )
    assert response.status_code == 200

    document_1 = db_mock.collection("tokens").document("my_uid").get()
    document_2 = db_mock.collection("tokens").document("another_uid").get()

    assert document_1.exists is True
    assert document_1.to_dict()["token"] == "token_for_my_uid"
    assert document_2.exists is True
    assert document_2.to_dict()["token"] == "token_for_another_uid"


def test_post_token_for_the_same_uid_twice_replaces_old_token(client):
    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_my_uid", "uid": "my_uid"},
        headers={"api_key": "key"},
    )
    assert response.status_code == 200

    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "new_token", "uid": "my_uid"},
        headers={"api_key": "key"},
    )
    assert response.status_code == 200

    document = db_mock.collection("tokens").document("my_uid").get()
    assert document.exists is True
    assert document.to_dict()["token"] == "new_token"


def test_delete_token(client):
    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_my_uid", "uid": "my_uid"},
        headers={"api_key": "key"},
    )
    assert response.status_code == 200

    response = client.delete(
        f"{API_VERSION_PREFIX}/tokens/my_uid", headers={"api_key": "key"}
    )
    assert response.status_code == 200

    document = db_mock.collection("tokens").document("my_uid").get()
    assert document.exists is False


def test_delete_token_for_non_existing_uid(client):
    response = client.delete(
        f"{API_VERSION_PREFIX}/tokens/my_uid", headers={"api_key": "key"}
    )
    assert response.status_code == 404
