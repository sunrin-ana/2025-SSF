# import os
# from datetime import datetime
# from typing import List
# from fastapi import UploadFile
# from ..schemas.photo import (
#     PhotoUpload,
#     Photo,
#     PhotoComment,
#     CommentCreate,
#     CommentResponse,
# )
# from ..utils.db import execute, fetch_one, fetch_all
# from ..utils.default_queries import PhotoQueries
# from ..utils.image_processor import ImageProcessor
#
#
# class PhotoService:
#     def __init__(self):
#         self.image_processor = ImageProcessor()
#         self.upload_dir = "uploads/photos"
#         os.makedirs(self.upload_dir, exist_ok=True)
#
#     @staticmethod
#     async def init_db():
#         await execute(PhotoQueries.CREATE_TABLE)
#         await execute(PhotoQueries.CREATE_COMMENTS_TABLE)
#
#     async def upload_photo(
#         self, user_id: int, photo_data: PhotoUpload, file: UploadFile
#     ) -> Photo:
#         if not file.content_type.startswith("image/"):
#             raise ValueError("File must be an image")
#
#         self.image_processor.validate_image_file(file.filename, file.size)
#
#         created_at = datetime.now()
#
#         image_path = await self.image_processor.write_file_and_get_image_path(
#             file, self.upload_dir
#         )
#
#         query = PhotoQueries.INSERT_PHOTO
#
#         await execute(
#             query,
#             (user_id, photo_data.album_name, image_path, photo_data.title, created_at),
#         )
#
#         row = await fetch_one(
#             PhotoQueries.SELECT_LATEST_USER_PHOTO,
#             (user_id,),
#         )
#
#         return Photo(**row)
#
#     async def get_user_photos(
#         self, user_id: int, skip: int = 0, limit: int = 20, album_name: str = None
#     ) -> List[Photo]:
#         if album_name:
#             query = PhotoQueries.SELECT_USER_PHOTOS_BY_ALBUM
#             rows = await fetch_all(query, (user_id, album_name, limit, skip))
#         else:
#             query = PhotoQueries.SELECT_USER_PHOTOS
#             rows = await fetch_all(query, (user_id, limit, skip))
#
#         return [Photo(**row) for row in rows]
#
#     async def check_friendship(self, user_id: int, photo_id: int) -> bool:
#         photo_query = PhotoQueries.SELECT_PHOTO_OWNER
#         photo_row = await fetch_one(photo_query, (photo_id,))
#
#         if not photo_row:
#             return False
#
#         photo_owner_id = photo_row["user_id"]
#
#         if user_id == photo_owner_id:
#             return True
#
#         from ..services.friendship_service import FriendshipService
#
#         friendship_service = FriendshipService()
#         return await friendship_service.check_friendship(user_id, photo_owner_id)
#
#     async def add_comment(
#         self, photo_id: int, user_id: int, comment_data: CommentCreate
#     ) -> PhotoComment:
#         if not await self.check_friendship(user_id, photo_id):
#             raise ValueError("Cannot add comment before being friends")
#         created_at = datetime.now()
#
#         query = PhotoQueries.INSERT_COMMENT
#
#         await execute(query, (photo_id, user_id, comment_data.content, created_at))
#
#         row = await fetch_one(
#             PhotoQueries.SELECT_LATEST_COMMENT,
#             (photo_id, user_id),
#         )
#
#         return PhotoComment(**row)
#
#     async def get_photo_comments(self, photo_id: int) -> List[CommentResponse]:
#         query = PhotoQueries.SELECT_PHOTO_COMMENTS
#
#         rows = await fetch_all(query, (photo_id,))
#
#         return [CommentResponse(**row) for row in rows]
#
#     async def apply_filter(
#         self,
#         photo_id: int,
#         filter_type: str,
#         user_id: int,
#         cover: bool = False,
#         title: str = None,
#     ) -> str:
#         photo_query = PhotoQueries.SELECT_PHOTO_BY_ID
#         row = await fetch_one(photo_query, (photo_id, user_id))
#
#         if not row:
#             raise ValueError("Photo not found")
#
#         original_path = row["image_path"]
#         filtered_path = await self.image_processor.apply_filter(
#             original_path, filter_type
#         )
#
#         if cover:
#             photo_update_query = PhotoQueries.UPDATE_PHOTO_PATH
#             await execute(photo_update_query, (filtered_path, photo_id, user_id))
#         else:
#             row = await fetch_one(
#                 PhotoQueries.SELECT_PHOTO_ALBUM_NAME, (photo_id, user_id)
#             )
#             photo_create_query = PhotoQueries.INSERT_PHOTO
#             await execute(
#                 photo_create_query,
#                 (user_id, row["album_name"], filtered_path, title, datetime.now()),
#             )
#
#         return filtered_path
#
#     async def delete_photo(self, photo_id: int, user_id: int) -> bool:
#         try:
#             query = PhotoQueries.DELETE_PHOTO
#             await execute(query, (photo_id, user_id))
#             return True
#         except Exception:
#             return False
