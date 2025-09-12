# from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query, Form
# from typing import List
# from ...schemas.photo import (
#     PhotoUpload,
#     PhotoResponse,
#     CommentCreate,
#     CommentResponse,
#     FilterRequest,
# )
# from ...services.photo_service import PhotoService
# from ...core.security import get_current_user
# from ...schemas.user import User
# from pydantic import ValidationError
#
# router = APIRouter(prefix="/photo", tags=["photo"])
# photo_service = PhotoService()
#
#
# @router.post("/upload", response_model=PhotoResponse)
# async def upload_photo(
#     photo_data: UploadFile = Form(...),
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user),
# ) -> PhotoResponse:
#     import json
#
#     try:
#         photo_data_bytes = await photo_data.read()
#         photo_info = json.loads(photo_data_bytes.decode("utf-8"))
#         photo_data = PhotoUpload(**photo_info)
#     except (json.JSONDecodeError, ValidationError) as e:
#         raise HTTPException(status_code=400, detail="Invalid photo data format")
#     try:
#         photo = await photo_service.upload_photo(current_user.id, photo_data, file)
#         return photo.to_response()
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.get("", response_model=List[PhotoResponse])
# async def get_user_photos(
#     skip: int = 0,
#     limit: int = 20,
#     album_name: str = None,
#     current_user: User = Depends(get_current_user),
# ) -> List[PhotoResponse]:
#     try:
#         photos = await photo_service.get_user_photos(
#             current_user.id, skip, limit, album_name
#         )
#         return [photo.to_response() for photo in photos]
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.post("/{photo_id}/comment", response_model=CommentResponse)
# async def add_photo_comment(
#     photo_id: int,
#     comment_data: CommentCreate,
#     current_user: User = Depends(get_current_user),
# ) -> CommentResponse:
#     try:
#         is_friend = await photo_service.check_friendship(current_user.id, photo_id)
#         if not is_friend:
#             raise HTTPException(
#                 status_code=403, detail="Only friends can comment on photos"
#             )
#
#         comment = await photo_service.add_comment(
#             photo_id, current_user.id, comment_data
#         )
#         return comment.to_response(current_user.username)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.get("/{photo_id}/comments", response_model=List[CommentResponse])
# async def get_photo_comments(
#     photo_id: int, current_user: User = Depends(get_current_user)
# ) -> List[CommentResponse]:
#     try:
#         comments = await photo_service.get_photo_comments(photo_id)
#         return comments
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.post("/edit-filter")
# async def apply_photo_filter(
#     filter_request: FilterRequest, current_user: User = Depends(get_current_user)
# ) -> dict:
#     if filter_request.cover and filter_request.title is None:
#         raise HTTPException(status_code=400, detail="title must be Not Null")
#     try:
#         filtered_image_path = await photo_service.apply_filter(
#             filter_request.photo_id,
#             filter_request.filter_type,
#             current_user.id,
#             filter_request.cover,
#             filter_request.title,
#         )
#         return {"filtered_image_path": filtered_image_path}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.delete("/{photo_id}")
# async def delete_photo(
#     photo_id: int, current_user: User = Depends(get_current_user)
# ) -> dict:
#     try:
#         success = await photo_service.delete_photo(photo_id, current_user.id)
#         if not success:
#             raise HTTPException(status_code=404, detail="Photo not found")
#         return {"message": "Photo deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
