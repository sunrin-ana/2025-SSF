from typing import List, Optional
from datetime import datetime
from ..schemas.friendship import Friendship, FriendshipResponse, FriendshipStatus
from ..utils.db import execute, fetch_one, fetch_all
from ..utils.queries.friendship import FriendshipQueries


class FriendshipService:

    @staticmethod
    async def init_db():
        await execute(FriendshipQueries.CREATE_TABLE)

    async def send_friendship_request(
        self, user_id: int, friend_username: str
    ) -> FriendshipResponse:
        friend_query = FriendshipQueries.SELECT_USER_BY_USERNAME
        friend_row = await fetch_one(friend_query, (friend_username,))

        if not friend_row:
            raise ValueError("User not found")

        friend_id = friend_row["id"]

        if user_id == friend_id:
            raise ValueError("Cannot send friendship request to yourself")

        existing_query = FriendshipQueries.SELECT_EXISTING_FRIENDSHIP
        existing_row = await fetch_one(
            existing_query, (user_id, friend_id, friend_id, user_id)
        )

        if existing_row:
            raise ValueError("Friendship request already exists")

        created_at = datetime.now()

        query = FriendshipQueries.INSERT_FRIENDSHIP

        await execute(
            query, (user_id, friend_id, FriendshipStatus.PENDING.value, created_at)
        )

        friendship_row = await fetch_one(
            FriendshipQueries.SELECT_FRIENDSHIP_BY_IDS,
            (user_id, friend_id),
        )

        if not friendship_row:
            raise ValueError("Friendship not found after creation")

        friendship = Friendship(
            id=friendship_row["id"],
            user_id=friendship_row["user_id"],
            friend_id=friendship_row["friend_id"],
            status=friendship_row["status"],
            created_at=friendship_row["created_at"],
        )

        return friendship.to_response(friend_username)

    async def accept_friendship_request(
        self, friendship_id: int, user_id: int
    ) -> Optional[FriendshipResponse]:
        friendship_query = FriendshipQueries.SELECT_FRIENDSHIP_FOR_ACCEPT

        friendship_row = await fetch_one(
            friendship_query,
            (friendship_id, user_id, FriendshipStatus.PENDING.value),
        )

        if not friendship_row:
            return None

        update_query = FriendshipQueries.UPDATE_FRIENDSHIP_STATUS
        await execute(update_query, (FriendshipStatus.ACCEPTED.value, friendship_id))

        friendship = Friendship(
            id=friendship_row["id"],
            user_id=friendship_row["user_id"],
            friend_id=friendship_row["friend_id"],
            status=FriendshipStatus.ACCEPTED.value,
            created_at=friendship_row["created_at"],
        )

        return friendship.to_response(friendship_row["username"])

    async def get_user_friendships(
        self, user_id: int, status: Optional[str] = None
    ) -> List[FriendshipResponse]:
        if status:
            query = FriendshipQueries.SELECT_USER_FRIENDSHIPS_BY_STATUS
            rows = await fetch_all(query, (user_id, user_id, user_id, status))
        else:
            query = FriendshipQueries.SELECT_USER_FRIENDSHIPS
            rows = await fetch_all(
                query, (user_id, user_id, user_id, FriendshipStatus.ACCEPTED.value)
            )

        friendships = []
        for row in rows:
            friendship = Friendship(
                id=row["id"],
                user_id=row["user_id"],
                friend_id=row["friend_id"],
                status=row["status"],
                created_at=row["created_at"],
            )
            friendships.append(friendship.to_response(row["username"]))

        return friendships

    async def delete_friendship(self, friendship_id: int, user_id: int) -> bool:
        query = FriendshipQueries.DELETE_FRIENDSHIP
        await execute(query, (friendship_id, user_id, user_id))
        return True

    async def get_pending_requests(self, user_id: int) -> List[FriendshipResponse]:
        query = FriendshipQueries.SELECT_PENDING_REQUESTS

        rows = await fetch_all(query, (user_id, FriendshipStatus.PENDING.value))

        friendships = []
        for row in rows:
            friendship = Friendship(
                id=row["id"],
                user_id=row["user_id"],
                friend_id=row["friend_id"],
                status=row["status"],
                created_at=row["created_at"],
            )
            friendships.append(friendship.to_response(row["username"]))

        return friendships

    async def check_friendship(self, user_id1: int, user_id2: int) -> bool:
        friendship_query = FriendshipQueries.CHECK_FRIENDSHIP_STATUS
        friendship_row = await fetch_one(
            friendship_query, (user_id1, user_id2, user_id2, user_id1)
        )

        return friendship_row is not None
