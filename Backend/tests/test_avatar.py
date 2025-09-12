from fastapi.testclient import TestClient
from Backend.schemas.avatar import (
    AvatarUpdate,
    AvatarType,
    TopClothesType,
    BottomClothesType,
)


def test_get_my_avatar(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    response = client.get("/api/avatar", headers=headers)
    assert response.status_code == 200
    avatar_data = response.json()
    assert "id" in avatar_data
    assert "user_id" in avatar_data
    assert avatar_data["avatar_type"]["name"] == AvatarType.MALE.value


def test_update_my_avatar(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    response = client.get("/api/avatar", headers=headers)
    assert response.status_code == 200
    update_data = AvatarUpdate(
        avatar_type=AvatarType.FEMALE,
        top_clothe_type=TopClothesType.SCHOOL_CLOTHES,
        bottom_clothe_type=BottomClothesType.SCHOOL_CLOTHES_2,
    )
    response = client.put(
        "/api/avatar", json=update_data.model_dump(mode="json"), headers=headers
    )

    assert response.status_code == 200
    avatar_data = response.json()
    assert avatar_data["avatar_type"]["name"] == update_data.avatar_type.value
    assert avatar_data["top_clothe_type"]["name"] == update_data.top_clothe_type.value
    assert (
        avatar_data["bottom_clothe_type"]["name"]
        == update_data.bottom_clothe_type.value
    )


def test_get_avatar_options(client: TestClient):
    response = client.get("/api/avatar/options")
    assert response.status_code == 200
    options = response.json()
    assert "avatar_types" in options
    assert "top_clothe_types" in options
    assert "bottom_clothe_types" in options
    assert all(isinstance(item, str) for item in options["avatar_types"])
    assert all(isinstance(item, str) for item in options["top_clothe_types"])
    assert all(isinstance(item, str) for item in options["bottom_clothe_types"])


def test_get_avatar_by_user_id(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    response = client.get("/api/avatar", headers=headers)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    response = client.get(f"/api/avatar/{user_id}", headers=headers)
    assert response.status_code == 200
    avatar_data = response.json()
    assert "id" in avatar_data
    assert avatar_data["user_id"] == user_id
    assert avatar_data["avatar_type"]["name"] == AvatarType.MALE.value

    # Test for a non-existent user
    response = client.get("/api/avatar/9999", headers=headers)
    assert response.status_code == 404