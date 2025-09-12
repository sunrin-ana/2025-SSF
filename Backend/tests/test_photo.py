# from io import BytesIO
# import json
#
#
# def test_photo_upload_and_delete(client, authenticated_user):
#     token = authenticated_user["token"]
#     headers = {"Authorization": f"Bearer {token}"}
#
#     # Upload Photo
#     photo_data = {"album_name": "test_album", "title": "test_title"}
#     photo_data_json = json.dumps(photo_data).encode("utf-8")
#
#     response = client.post(
#         "/api/photo/upload",
#         files={
#             "photo_data": (
#                 "photo_data.json",
#                 BytesIO(photo_data_json),
#                 "application/json",
#             ),
#             "file": ("a.jpg", BytesIO(b"aaa"), "image/jpeg"),
#         },
#         headers=headers,
#     )
#     assert response.status_code == 200
#     photo_id = response.json()["id"]
#     assert response.json()["album_name"] == "test_album"
#
#     # Delete Photo
#     response = client.delete(f"/api/photo/{photo_id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Photo deleted successfully"
#
#
# def test_photo_commenting(client, two_authenticated_users):
#     user1 = two_authenticated_users["user1"]
#     user2 = two_authenticated_users["user2"]
#
#     headers1 = {"Authorization": f"Bearer {user1['token']}"}
#     headers2 = {"Authorization": f"Bearer {user2['token']}"}
#
#     # User 1 uploads a photo
#     photo_data = {"album_name": "test_album", "title": "test_title"}
#     photo_data_json = json.dumps(photo_data).encode("utf-8")
#     response = client.post(
#         "/api/photo/upload",
#         files={
#             "photo_data": (
#                 "photo_data.json",
#                 BytesIO(photo_data_json),
#                 "application/json",
#             ),
#             "file": ("a.jpg", BytesIO(b"aaa"), "image/jpeg"),
#         },
#         headers=headers1,
#     )
#     assert response.status_code == 200
#     photo_id = response.json()["id"]
#
#     # User 2 cannot comment before being friends
#     response = client.post(
#         f"/api/photo/{photo_id}/comment",
#         json={"content": "test comment"},
#         headers=headers2,
#     )
#     assert response.status_code == 400
#
#     # User 1 sends friendship request to User 2
#     response = client.post(
#         "/api/friendship/request",
#         json={"friend_username": user2["username"]},
#         headers=headers1,
#     )
#     assert response.status_code == 200
#     friendship_id = response.json()["id"]
#
#     # User 2 accepts friendship request
#     response = client.put(f"/api/friendship/{friendship_id}/accept", headers=headers2)
#     assert response.status_code == 200
#
#     # User 2 can now comment
#     response = client.post(
#         f"/api/photo/{photo_id}/comment",
#         json={"content": "test comment"},
#         headers=headers2,
#     )
#     assert response.status_code == 200
#     assert response.json()["content"] == "test comment"
#
#     # User 1 can see the comment
#     response = client.get(f"/api/photo/{photo_id}/comments", headers=headers1)
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#     assert response.json()[0]["content"] == "test comment"
