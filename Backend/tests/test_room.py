from fastapi.testclient import TestClient
from Backend.schemas.room import Furniture, RoomTypes


def test_get_furniture_catalog(client: TestClient):
    response = client.get("/api/room/catalog")
    assert response.status_code == 200
    catalog = response.json()
    assert isinstance(catalog, list)
    assert len(catalog) > 0
    for item in catalog:
        assert "name" in item
        assert "image_path" in item
        assert "width" in item


def test_get_room_types(client: TestClient):
    response = client.get("/api/room/types")
    assert response.status_code == 200
    types = response.json()
    assert isinstance(types, list)
    assert len(types) > 0
    for room_type in types:
        assert "type" in room_type
        assert "image_path" in room_type


def test_get_my_room(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    response = client.get("/api/room/", headers=headers)
    assert response.status_code == 200
    room_data = response.json()
    assert "id" in room_data
    assert "room_name" in room_data
    assert "room_type" in room_data
    assert "room_image_path" in room_data


def test_update_room_name(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    response = client.get("/api/room/", headers=headers)
    new_name = "My Awesome Room"
    response = client.put("/api/room/", json={"new_name": new_name}, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Room name updated successfully"}

    # Verify the change
    response = client.get("/api/room/", headers=headers)
    assert response.status_code == 200
    assert response.json()["room_name"] == new_name


def test_update_room_type(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    response = client.get("/api/room/", headers=headers)
    new_type = RoomTypes.ROOM_2.value

    response = client.patch("/api/room/", json={"type": new_type}, headers=headers)
    assert response.status_code == 200
    updated_room = response.json()
    assert updated_room["room_type"] == new_type


def test_get_my_room_layout(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    response = client.get("/api/room/layout", headers=headers)
    assert response.status_code == 200
    layout_data = response.json()
    assert "room" in layout_data
    assert "furniture" in layout_data
    assert isinstance(layout_data["furniture"], list)


def test_place_furniture(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    placement_data = {
        "furniture_name": Furniture.SOFA_0.value,
        "x": 5,
        "y": 5,
    }
    response = client.post("/api/room/furniture", json=placement_data, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Furniture placed successfully"}

    # Verify placement
    layout_response = client.get("/api/room/layout", headers=headers)
    assert layout_response.status_code == 200
    new_layout = layout_response.json()
    assert any(
        item["furniture_name"] == placement_data["furniture_name"]
        and item["x"] == placement_data["x"]
        and item["y"] == placement_data["y"]
        for item in new_layout["furniture"]
    )

    # Cleanup
    client.delete(
        f"/api/room/furniture?x={placement_data['x']}&y={placement_data['y']}&furniture_name={placement_data['furniture_name']}",
        headers=headers,
    )


def test_remove_furniture(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}
    placement_data = {
        "furniture_name": Furniture.CHAIR_0.value,
        "x": 1,
        "y": 1,
    }
    # Place furniture first
    client.post("/api/room/furniture", json=placement_data, headers=headers)

    # Remove furniture
    response = client.delete(
        f"/api/room/furniture?x={placement_data['x']}&y={placement_data['y']}&furniture_name={placement_data['furniture_name']}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Furniture removed successfully"}

    # Verify removal
    final_layout_response = client.get("/api/room/layout", headers=headers)
    assert final_layout_response.status_code == 200
    final_layout = final_layout_response.json()
    assert not any(
        item["furniture_name"] == placement_data["furniture_name"]
        and item["x"] == placement_data["x"]
        and item["y"] == placement_data["y"]
        for item in final_layout["furniture"]
    )


def test_invalid_furniture_placement(client: TestClient, authenticated_user):
    headers = {"Authorization": f"Bearer {authenticated_user['token']}"}

    # Test with invalid coordinates (out of bounds)
    invalid_coords_data = {
        "furniture_name": Furniture.CHAIR_0.value,
        "x": 11,
        "y": -1,
    }
    response = client.post(
        "/api/room/furniture", json=invalid_coords_data, headers=headers
    )
    assert response.status_code == 422  # Pydantic validation error

    # Test collision
    placement_data = {"furniture_name": Furniture.CHAIR_0.value, "x": 1, "y": 1}
    # Place once
    client.post("/api/room/furniture", json=placement_data, headers=headers)
    # Try to place again in the same spot
    response = client.post("/api/room/furniture", json=placement_data, headers=headers)
    assert response.status_code == 400
    assert "already placed" in response.json()["detail"]

    # Cleanup
    client.delete(
        f"/api/room/furniture?x={placement_data['x']}&y={placement_data['y']}&furniture_name={placement_data['furniture_name']}",
        headers=headers,
    )
