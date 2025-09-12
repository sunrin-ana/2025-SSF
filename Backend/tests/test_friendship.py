def test_friendship_flow(client, two_authenticated_users):
    user1 = two_authenticated_users["user1"]
    user2 = two_authenticated_users["user2"]

    headers1 = {"Authorization": f"Bearer {user1['token']}"}
    headers2 = {"Authorization": f"Bearer {user2['token']}"}

    # User 1 sends friendship request to User 2
    response = client.post(
        "/api/friendship/request",
        json={"friend_username": user2["username"]},
        headers=headers1,
    )
    assert response.status_code == 200
    friendship_id = response.json()["id"]
    assert response.json()["status"] == "pending"

    # User 2 accepts friendship request
    response = client.put(f"/api/friendship/{friendship_id}/accept", headers=headers2)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"

    # User 1 lists friends
    response = client.get("/api/friendship", headers=headers1)
    assert response.status_code == 200
    assert any(f["id"] == friendship_id for f in response.json())

    # User 2 lists friends
    response = client.get("/api/friendship", headers=headers2)
    assert response.status_code == 200
    assert any(f["id"] == friendship_id for f in response.json())

    # User 1 deletes friendship
    response = client.delete(f"/api/friendship/{friendship_id}", headers=headers1)
    assert response.status_code == 200
    assert response.json()["message"] == "Friendship deleted successfully"

    # Verify deletion for both users
    response = client.get("/api/friendship", headers=headers1)
    assert response.status_code == 200
    assert not any(f["id"] == friendship_id for f in response.json())

    response = client.get("/api/friendship", headers=headers2)
    assert response.status_code == 200
    assert not any(f["id"] == friendship_id for f in response.json())
