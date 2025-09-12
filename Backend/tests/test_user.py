from io import BytesIO


def test_user_registration_and_login(client):
    # Registration
    user_data = {
        "username": "testuser999",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = client.post(
        "/api/user/register",
        data=user_data,
        files={"file": ("a.jpg", BytesIO(b"aaa"), "image/jpeg")},
    )

    assert response.status_code == 201
    assert response.json()["username"] == "testuser999"

    # Duplicate registration
    response = client.post(
        "/api/user/register",
        data=user_data,
        files={"file": ("a.jpg", BytesIO(b"aaa"), "image/jpeg")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

    # Login
    login_data = {
        "username": "testuser999",
        "password": "testpassword123",
    }
    response = client.post("/api/user/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Login with wrong password
    login_data["password"] = "wrongpassword"
    response = client.post("/api/user/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

    # delete
    response = client.delete(f"/api/user/{user_data['username']}")
    assert response.status_code == 200


def test_get_user_profile(client, authenticated_user):
    token = authenticated_user["token"]
    username = authenticated_user["user_data"]["username"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/api/user/profile/{username}", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == username


def test_user_delete(client, authenticated_user):
    token = authenticated_user["token"]
    username = authenticated_user["user_data"]["username"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/user/{username}", headers=headers)

    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"
