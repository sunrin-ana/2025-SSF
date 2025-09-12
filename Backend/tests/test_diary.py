from io import BytesIO


def test_diary_operations(client, authenticated_user):
    token = authenticated_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Diary
    diary_data = {
        "title": "test title",
        "content": "test content",
        "category": "test category",
    }
    response = client.post(
        "/api/diary",
        data=diary_data,
        files={"file": ("a.jpg", BytesIO(b"aaa"), "image/jpeg")},
        headers=headers,
    )
    assert response.status_code == 200
    diary_id = response.json()["id"]
    assert response.json()["title"] == "test title"

    # Get Diary
    response = client.get(f"/api/diary/{diary_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == diary_id

    # List Diaries
    response = client.get("/api/diary", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Update Diary
    updated_diary_data = {"title": "updated title", "content": "updated content"}
    response = client.put(
        f"/api/diary/{diary_id}",
        data=updated_diary_data,
        files={"file": ("b.jpg", BytesIO(b"bbb"), "image/jpeg")},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "updated title"

    # Delete Diary
    response = client.delete(f"/api/diary/{diary_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Diary deleted successfully"

    # Verify Deletion
    response = client.get(f"/api/diary/{diary_id}", headers=headers)
    assert response.status_code == 400
