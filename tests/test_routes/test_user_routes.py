from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT


def test_get_users_initial(client):
    resp = client.get("/users")
    assert resp.status_code == HTTP_200_OK
    data = resp.json()
    assert "items" in data
    assert "total" in data


def test_create_and_get_user(client):
    payload = {
        "username": "api_user",
        "email": "api@example.com",
        "description": "From API",
    }

    create_resp = client.post("/users", json=payload)
    assert create_resp.status_code in (HTTP_201_CREATED, HTTP_200_OK)
    created = create_resp.json()
    user_id = created["id"]

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == HTTP_200_OK
    got = get_resp.json()
    assert got["username"] == "api_user"
    assert got["email"] == "api@example.com"


def test_update_user_api(client):
    payload = {
        "username": "to_update",
        "email": "update@example.com",
        "description": "Old",
    }
    create_resp = client.post("/users", json=payload)
    user_id = create_resp.json()["id"]

    update_payload = {
        "username": "updated",
        "email": "update@example.com",
        "description": "New",
    }
    update_resp = client.put(f"/users/{user_id}", json=update_payload)
    assert update_resp.status_code == HTTP_200_OK

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == HTTP_200_OK
    data = get_resp.json()
    assert data["username"] == "updated"
    assert data["description"] == "New"


def test_delete_user_api(client):
    payload = {
        "username": "to_delete",
        "email": "delete@example.com",
        "description": "Delete",
    }
    create_resp = client.post("/users", json=payload)
    user_id = create_resp.json()["id"]

    del_resp = client.delete(f"/users/{user_id}")
    assert del_resp.status_code in (HTTP_204_NO_CONTENT, HTTP_200_OK)

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404