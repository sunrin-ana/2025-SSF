# def test_letter_operations(client, authenticated_user):
#     token = authenticated_user["token"]
#     headers = {"Authorization": f"Bearer {token}"}
#
#     # Create Letter
#     letter_data = {"content": "test content"}
#     response = client.post("/api/letter", json=letter_data, headers=headers)
#     assert response.status_code == 200
#     letter_id = response.json()["id"]
#     assert response.json()["content"] == "test content"
#
#     # Get Letter
#     response = client.get(f"/api/letter/{letter_id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["id"] == letter_id
#
#     # Update Letter
#     updated_letter_data = {"content": "updated content"}
#     response = client.put(
#         f"/api/letter/{letter_id}", json=updated_letter_data, headers=headers
#     )
#     assert response.status_code == 200
#     assert response.json()["content"] == "updated content"
#
#     # Delete Letter
#     response = client.delete(f"/api/letter/{letter_id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["detail"] == "Letter deleted"
#
#     # Verify Deletion
#     response = client.get(f"/api/letter/{letter_id}", headers=headers)
#     assert response.status_code == 400
