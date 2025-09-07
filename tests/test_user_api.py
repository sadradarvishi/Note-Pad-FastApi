import uuid


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "okay"}


def test_create_user_and_get_user(client):
    res = client.post(
        "/users",
        json={
            "firstname": "user",
            "lastname": "test",
            "username": "user_test",
            "password": "Sadra-1379",
        },
    )
    assert res.status_code == 201
    user = res.json()
    uuid.UUID(user["id"])
    assert user["firstname"] == "user"

    res2 = client.get(f"/users/{user['id']}")
    assert res2.status_code == 200
    got = res2.json()
    assert got["id"] == user["id"]
    assert got["firstname"] == "user"


def test_user_list(client):
    client.post(
        "/users",
        json={
            "firstname": "user",
            "lastname": "test",
            "username": "user_test",
            "password": "Sadra-1379",
        },
    )
    client.post(
        "/users",
        json={
            "firstname": "user2",
            "lastname": "test2",
            "username": "user_test2",
            "password": "Sadra-1379",
        },
    )
    res = client.get("/users")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) >= 2


def test_edit_user(client):
    res = client.post(
        "/users",
        json={
            "firstname": "user",
            "lastname": "test",
            "username": "user_test",
            "password": "Sadra-1379",
        },
    )
    user_id = res.json()["id"]
    update = client.patch(
        f"/users/{user_id}", json={"firstname": "user2", "password": "Sadra-13799"}
    )
    assert update.status_code == 200
    body = update.json()
    assert body["id"] == user_id
    assert body["firstname"] == "user2"

    got = client.get(f"/users/{user_id}")
    assert got.status_code == 200
    data = got.json()
    assert data["id"] == user_id
    assert data["firstname"] == "user2"
    assert "password" not in data
