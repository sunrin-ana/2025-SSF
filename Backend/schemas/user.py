from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import hashlib
import secrets
from fastapi import Form


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
    ) -> "UserCreate":
        return cls(username=username, email=email, password=password)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        email: Optional[EmailStr] = Form(default=None),
        password: Optional[str] = Form(default=None),
    ) -> "UserUpdate":
        return cls(email=email, password=password)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    profile_image_path: str
    is_active: bool


class User:
    def __init__(
        self,
        id: int,
        username: str,
        email: str,
        password_hash: str,
        salt: str,
        created_at: datetime,
        profile_image_path: str,
        is_active: bool = True,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.salt = salt
        self.created_at = created_at
        self.profile_image_path = profile_image_path
        self.is_active = is_active

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        if salt is None:
            salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return password_hash.hex(), salt

    def verify_password(self, password: str) -> bool:
        password_hash, _ = self.hash_password(password, self.salt)
        return password_hash == self.password_hash

    def to_response(self) -> UserResponse:
        return UserResponse(
            id=self.id,
            username=self.username,
            email=self.email,
            created_at=self.created_at,
            profile_image_path=self.profile_image_path,
            is_active=self.is_active,
        )
