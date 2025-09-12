from pydantic import BaseModel, field_validator
from datetime import datetime
import enum


class FriendshipStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class FriendshipRequest(BaseModel):
    friend_username: str

    @field_validator("friend_username")
    @classmethod
    def validate_friend_username(cls, v):
        if len(v.strip()) < 1:
            raise ValueError("Friend username cannot be empty")
        return v.strip()


class FriendshipResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    friend_username: str
    status: FriendshipStatus
    created_at: datetime


class FriendshipUpdate(BaseModel):
    status: FriendshipStatus


class Friendship:
    def __init__(
        self,
        id: int,
        user_id: int,
        friend_id: int,
        status: str,
        created_at: datetime,
    ):
        self.id = id
        self.user_id = user_id
        self.friend_id = friend_id
        self.status = status
        self.created_at = created_at

    def to_response(self, friend_username: str) -> FriendshipResponse:
        return FriendshipResponse(
            id=self.id,
            user_id=self.user_id,
            friend_id=self.friend_id,
            friend_username=friend_username,
            status=FriendshipStatus(self.status),
            created_at=self.created_at,
        )
