# from pydantic import BaseModel, field_validator
# from datetime import datetime
#
#
# class PhotoUpload(BaseModel):
#     album_name: str
#     title: str
#
#     @field_validator("album_name")
#     @classmethod
#     def validate_album_name(cls, v):
#         if len(v.strip()) < 1:
#             raise ValueError("Album name cannot be empty")
#         if len(v) > 50:
#             raise ValueError("Album name must be less than 50 characters")
#         return v.strip()
#
#     @field_validator("title")
#     @classmethod
#     def validate_title(cls, v):
#         if len(v.strip()) < 1:
#             raise ValueError("Title cannot be empty")
#         if len(v) > 100:
#             raise ValueError("Title must be less than 100 characters")
#         return v.strip()
#
#
# class PhotoResponse(BaseModel):
#     id: int
#     user_id: int
#     album_name: str
#     image_path: str
#     title: str
#     created_at: datetime
#
#
# class CommentCreate(BaseModel):
#     content: str
#
#     @field_validator("content")
#     @classmethod
#     def validate_content(cls, v):
#         if len(v.strip()) < 1:
#             raise ValueError("Comment cannot be empty")
#         if len(v) > 500:
#             raise ValueError("Comment must be less than 500 characters")
#         return v.strip()
#
#
# class CommentResponse(BaseModel):
#     id: int
#     photo_id: int
#     user_id: int
#     username: str
#     content: str
#     created_at: datetime
#
#
# class FilterRequest(BaseModel):
#     photo_id: int
#     filter_type: str
#     cover: bool
#     title: str = None
#
#
# class Photo:
#     def __init__(
#         self,
#         id: int,
#         user_id: int,
#         album_name: str,
#         image_path: str,
#         title: str,
#         created_at: datetime,
#     ):
#         self.id = id
#         self.user_id = user_id
#         self.album_name = album_name
#         self.image_path = image_path
#         self.title = title
#         self.created_at = created_at
#
#     def to_response(self) -> PhotoResponse:
#         return PhotoResponse(
#             id=self.id,
#             user_id=self.user_id,
#             album_name=self.album_name,
#             image_path=self.image_path,
#             title=self.title,
#             created_at=self.created_at,
#         )
#
#
# class PhotoComment:
#     def __init__(
#         self,
#         id: int,
#         photo_id: int,
#         user_id: int,
#         content: str,
#         created_at: datetime,
#     ):
#         self.id = id
#         self.photo_id = photo_id
#         self.user_id = user_id
#         self.content = content
#         self.created_at = created_at
#
#     def to_response(self, username: str) -> CommentResponse:
#         return CommentResponse(
#             id=self.id,
#             photo_id=self.photo_id,
#             user_id=self.user_id,
#             username=username,
#             content=self.content,
#             created_at=self.created_at,
#         )
