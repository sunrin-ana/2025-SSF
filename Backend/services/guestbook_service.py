from datetime import datetime
from typing import List
from fastapi import HTTPException
from Backend.utils.db import execute, fetch_one, fetch_all
from Backend.utils.queries.guestbook import GuestBookQueries
from Backend.schemas.guestbook import GuestBook, GuestBookCreate, GuestbookResponse
from Backend.schemas.user import User
from Backend.utils.queries.user import UserQueries


class GuestbookService:
    def __init__(self):
        pass

    @staticmethod
    async def init_db():
        await execute(GuestBookQueries.CREATE_TABLE)

    async def create_guestbook(
        self, data: GuestBookCreate, user: User
    ) -> GuestbookResponse:
        user_exist = await fetch_one(UserQueries.SELECT_BY_ID, (data.target_user_id,))
        if user_exist is None:
            raise HTTPException(status_code=404, detail="User not found")

        ex_row = await fetch_one(
            GuestBookQueries.SELECT_GUEST_BOOK_BY_USER_ID, (user.id,)
        )
        created_at = datetime.now()
        query = GuestBookQueries.INSERT_GUEST_BOOK
        await execute(query, (data.target_user_id, user.id, data.content, created_at))

        query = GuestBookQueries.SELECT_GUEST_BOOK_BY_USER_ID
        row = await fetch_one(query, (user.id,))

        if not (ex_row is None):
            if row is None or ex_row["id"] == row["id"]:
                raise HTTPException(
                    status_code=400, detail="Failed to create guest book"
                )

        return GuestbookResponse(
            id=row["id"],
            content=row["content"],
            target_user_id=row["target_user_id"],
            user_id=row["user_id"],
            user_profile_path=user.profile_image_path,
            username=user.username,
            created_at=row["created_at"],
        )

    async def get_target_user_guestbooks(
        self, target_user_id: int, limit: int = 20, offset: int = 0
    ) -> List[GuestbookResponse]:
        query = GuestBookQueries.SELECT_TARGET_USER_GUEST_BOOKS

        rows = await fetch_all(query, (target_user_id, limit, offset))

        response_list = []
        for row in rows:
            user = await fetch_one(UserQueries.SELECT_BY_ID, (row["user_id"],))

            response_list.append(
                GuestbookResponse(
                    id=row["id"],
                    content=row["content"],
                    target_user_id=row["target_user_id"],
                    user_id=row["user_id"],
                    user_profile_path=user["profile_image_path"],
                    username=user["username"],
                    created_at=row["created_at"],
                )
            )

        return response_list

    async def update_guestbook_by_id(self, id: int, content: str) -> GuestbookResponse:
        query = GuestBookQueries.SELECT_GUEST_BOOK_BY_ID

        row = await fetch_one(query, (id,))

        if row is None:
            raise HTTPException(status_code=404, detail="Guest book not found")

        query = GuestBookQueries.UPDATE_GUEST_BOOK_BY_ID
        await execute(query, (content, id))

        query = GuestBookQueries.SELECT_GUEST_BOOK_BY_ID

        row = await fetch_one(query, (id,))

        user = await fetch_one(UserQueries.SELECT_BY_ID, (row["user_id"],))

        return GuestbookResponse(
            id=row["id"],
            content=row["content"],
            target_user_id=row["target_user_id"],
            user_id=row["user_id"],
            user_profile_path=user["profile_image_path"],
            username=user["username"],
            created_at=row["created_at"],
        )

    async def delete_guestbook_by_id(self, id: int, user_id: int) -> bool:
        try:
            query = GuestBookQueries.DELETE_GUEST_BOOK
            await execute(query, (id, user_id))
            return True
        except Exception:
            return False
