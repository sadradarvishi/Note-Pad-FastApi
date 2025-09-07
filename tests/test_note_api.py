import uuid


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "okay"}


def test_create_note_requires_auth__unauthorized(client):
    res = client.post("/notes", json={"title": "x", "note_pad": "y"})
    assert res.status_code in (401, 403)


def test_create_note_authed_success(authed_client):
    res = authed_client.post("/notes", json={"title": "hello", "note_pad": "world"})
    assert res.status_code == 201
    note = res.json()
    uuid.UUID(note["id"])
    assert note["title"] == "hello"


def test_create_and_get_note_auth_user(authed_client, test_user):
    payload = {"title": "test", "note_pad": "some items"}
    res = authed_client.post("/notes", json=payload)
    assert res.status_code == 201
    note = res.json()
    uuid.UUID(note["id"])
    assert note["title"] == "test"
    assert note["note_pad"] == "some items"
    assert note["owner_id"] == str(test_user.id)

    res2 = authed_client.get(f"/notes/{note['id']}")
    assert res2.status_code == 200
    got = res2.json()
    assert got["id"] == note["id"]
    assert got["owner_id"] == str(test_user.id)
    assert got["title"] == "test"


def test_list_notes(authed_client):
    authed_client.post("/notes", json={"title": "test", "note_pad": "some items"})
    authed_client.post("/notes", json={"title": "test2", "note_pad": "groceries"})
    res = authed_client.get("/notes")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) >= 2


def test_delete_note(authed_client):
    res = authed_client.post("/notes", json={"title": "test2", "note_pad": "groceries"})
    note_id = res.json()["id"]
    delete_res = authed_client.delete(f"/notes/{note_id}")
    assert delete_res.status_code == 204
    not_found = authed_client.get(f"/notes/{note_id}")
    assert not_found.status_code == 404


def test_update_note(authed_client):
    res = authed_client.post("/notes", json={"title": "test2", "note_pad": "groceries"})
    note_id = res.json()["id"]
    update = authed_client.patch(
        f"/notes/{note_id}", json={"title": "test2update", "note_pad": "some new items"}
    )
    body = update.json()
    assert update.status_code == 200
    assert body["id"] == note_id
    assert body["title"] == "test2update"
    assert body["note_pad"] == "some new items"
