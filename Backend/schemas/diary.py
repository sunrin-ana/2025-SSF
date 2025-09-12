from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from fastapi import Form


class DiaryCreate(BaseModel):
    title: str
    content: str
    category: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        content: str = Form(...),
        category: str = Form(...),
    ) -> "DiaryCreate":
        return cls(title=title, content=content, category=category)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if len(v.strip()) < 1:
            raise ValueError("Title cannot be empty")
        if len(v) > 100:
            raise ValueError("Title must be less than 100 characters")
        return v.strip()

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if len(v.strip()) < 1:
            raise ValueError("Content cannot be empty")
        if len(v) > 5000:
            raise ValueError("Content must be less than 5000 characters")
        return v.strip()


class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(None),
        content: Optional[str] = Form(None),
        category: Optional[str] = Form(None),
    ) -> "DiaryUpdate":
        return cls(title=title, content=content, category=category)


class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    images: List[str]
    category: str
    created_at: datetime
    is_submitted: bool
    email_sent: bool


class Diary:
    def __init__(
        self,
        id: int,
        user_id: int,
        title: str,
        content: str,
        images: str,  # JSON string
        category: str,
        created_at: datetime,
        is_submitted: bool = False,
        email_sent: bool = False,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.images = images
        self.category = category
        self.created_at = created_at
        self.is_submitted = is_submitted
        self.email_sent = email_sent

    @property
    def image_list(self) -> List[str]:
        return (
            [img.strip() for img in self.images.split(",") if img.strip()]
            if self.images
            else []
        )

    def to_response(self) -> DiaryResponse:
        return DiaryResponse(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            content=self.content,
            images=self.image_list,
            category=self.category,
            created_at=self.created_at,
            is_submitted=self.is_submitted,
            email_sent=self.email_sent,
        )
