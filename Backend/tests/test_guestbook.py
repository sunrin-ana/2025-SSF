def test_guest_book(client, authenticated_user):
    token = authenticated_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_data = {
        "username": "testtarget",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = client.post("/api/user/register", data=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    username = response.json()["username"]

    response = client.post(
        "/api/guestbook",
        json={"target_user_id": user_id, "content": "test"},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["content"] == "test"
    id = response.json()["id"]

    response = client.get(f"/api/guestbook/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]["content"] == "test"

    response = client.put(
        f"/api/guestbook/{id}", json={"content": "test2"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["content"] == "test2"

    response = client.delete(f"/api/guestbook/{id}", headers=headers)
    assert response.status_code == 200

    client.delete(f"/api/user/{username}", headers=headers)
    assert response.status_code == 200
