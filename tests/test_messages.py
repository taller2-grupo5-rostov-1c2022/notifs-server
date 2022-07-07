from src.mocks.firebase.database import db as db_mock
from src.main import API_VERSION_PREFIX


def test_send_message_to_user_without_token_should_fail(client):
    response = client.post(
        f"{API_VERSION_PREFIX}/messages/",
        json={"title": "title", "body": "body"},
        headers={"api_key": "key", "uid": "my_uid", "target-uid": "nonexistent_uid"},
    )
    assert response.status_code == 404


def test_send_message_to_user_with_token(client, mocker):
    mocker.patch("firebase_admin.messaging.send", return_value=None)

    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_my_uid"},
        headers={"api_key": "key", "uid": "my_uid"},
    )
    assert response.status_code == 200

    response = client.post(
        f"{API_VERSION_PREFIX}/messages/",
        json={"title": "title", "body": "body"},
        headers={"api_key": "key", "uid": "my_uid", "target-uid": "my_uid"},
    )
    assert response.status_code == 200

    document = db_mock.collection("notifications").document("my_uid").get()
    assert document.exists is True
    notifications = document.to_dict()["notifications"]

    assert len(notifications) == 1
    assert notifications[0]["title"] == "title"
    assert notifications[0]["message"] == "body"
    assert notifications[0]["body"] == '{"sender_uid": "my_uid", "type": "message"}'


def test_get_notifications_for_user(client, mocker):
    mocker.patch("firebase_admin.messaging.send", return_value=None)

    response = client.post(
        f"{API_VERSION_PREFIX}/tokens/",
        json={"token": "token_for_my_uid"},
        headers={"api_key": "key", "uid": "my_uid"},
    )
    assert response.status_code == 200

    response = client.post(
        f"{API_VERSION_PREFIX}/messages/",
        json={"title": "title", "body": "body"},
        headers={"api_key": "key", "uid": "my_uid", "target-uid": "my_uid"},
    )
    assert response.status_code == 200

    response = client.get(
        f"{API_VERSION_PREFIX}/notifications/",
        headers={"api_key": "key", "uid": "my_uid"},
    )
    assert response.status_code == 200
    notifications = response.json()

    assert len(notifications) == 1
    assert notifications[0]["title"] == "title"
    assert notifications[0]["message"] == "body"
    assert notifications[0]["body"] == '{"sender_uid": "my_uid", "type": "message"}'
