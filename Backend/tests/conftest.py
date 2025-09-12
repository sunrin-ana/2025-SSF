import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add Backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from Backend import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def authenticated_user(client):
    user_data = {
        "username": "testuser_authenticated",
        "email": "test_auth@example.com",
        "password": "testpassword123",
    }
    # Register user
    response = client.post("/api/user/register", data=user_data)

    # Login to get token
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/api/user/login", json=login_data)
    token = response.json()["access_token"]

    yield {"token": token, "user_data": user_data}

    # Cleanup: delete user via API
    headers = {"Authorization": f"Bearer {token}"}
    client.delete(f"/api/user/{user_data['username']}", headers=headers)


@pytest.fixture
def two_authenticated_users(client):
    user1_data = {
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "testpassword123",
    }
    user2_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123",
    }

    # Register users
    client.post("/api/user/register", data=user1_data)
    client.post("/api/user/register", data=user2_data)

    # Login users
    login1_data = {
        "username": user1_data["username"],
        "password": user1_data["password"],
    }
    response1 = client.post("/api/user/login", json=login1_data)
    token1 = response1.json()["access_token"]

    login2_data = {
        "username": user2_data["username"],
        "password": user2_data["password"],
    }
    response2 = client.post("/api/user/login", json=login2_data)
    token2 = response2.json()["access_token"]

    yield {
        "user1": {"token": token1, "username": user1_data["username"]},
        "user2": {"token": token2, "username": user2_data["username"]},
    }

    # Cleanup
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}
    client.delete(f"/api/user/{user1_data['username']}", headers=headers1)
    client.delete(f"/api/user/{user2_data['username']}", headers=headers2)
