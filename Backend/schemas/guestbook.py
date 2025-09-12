from datetime import datetime
from pydantic import BaseModel, field_validator


class GuestBookCreate(BaseModel):
    content: str
    target_user_id: int

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if len(v.strip()) < 1:
            raise ValueError("GuestBook content cannot be empty")
        if len(v) > 2000:
            raise ValueError("GuestBook content must be less than 2000 characters")
        return v.strip()


class GuestbookUpdate(BaseModel):
    content: str


class GuestbookResponse(BaseModel):
    id: int
    content: str
    target_user_id: int
    user_id: int
    user_profile_path: str
    username: str
    created_at: datetime


class GuestBook:
    def __init__(
        self,
        id: int,
        target_user_id: int,
        user_id,
        content,
        created_at: datetime,
    ):
        self.id = id
        self.target_user_id = target_user_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
