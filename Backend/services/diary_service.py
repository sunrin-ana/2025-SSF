import os
from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
from ..schemas.diary import DiaryCreate, DiaryUpdate, Diary
from ..utils.db import execute, fetch_one, fetch_all
from ..utils.image_processor import ImageProcessor
from ..utils.queries.diary import DiaryQueries


class DiaryService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.upload_dir = "uploads/diary"
        os.makedirs(self.upload_dir, exist_ok=True)

    @staticmethod
    async def init_db():
        await execute(DiaryQueries.CREATE_TABLE)

    async def create_diary(
        self, user_id: int, diary_data: DiaryCreate, files: List[UploadFile]
    ) -> Diary:
        # image_path 는 ,로 구분 되어 있음
        image_path = ""
        if files is not None:
            for file in files:
                image_path += (
                    ","
                    + await self.image_processor.write_file_and_get_image_path(
                        file, self.upload_dir
                    )
                )
            image_path = image_path[1:]

        query = DiaryQueries.INSERT_DIARY

        created_at = datetime.now()
        await execute(
            query,
            (
                user_id,
                diary_data.title,
                diary_data.content,
                image_path,
                diary_data.category,
                created_at,
                False,
                False,
            ),
        )

        row = await fetch_one(
            DiaryQueries.SELECT_LATEST_USER_DIARY,
            (user_id,),
        )

        return Diary(**row)

    async def get_user_diaries(
        self, user_id: int, skip: int = 0, limit: int = 20, category: str = None
    ) -> List[Diary]:
        if category:
            query = DiaryQueries.SELECT_USER_DIARIES_BY_CATEGORY
            rows = await fetch_all(query, (user_id, category, limit, skip))
        else:
            query = DiaryQueries.SELECT_USER_DIARIES
            rows = await fetch_all(query, (user_id, limit, skip))

        return [Diary(**row) for row in rows]

    async def get_diary_by_id(self, diary_id: int) -> Optional[Diary]:
        query = DiaryQueries.SELECT_BY_ID
        row = await fetch_one(query, (diary_id,))

        if not row:
            return None

        return Diary(**row)

    async def get_diary_with_user_id(
        self, diary_id: int, user_id: int
    ) -> Optional[Diary]:
        query = DiaryQueries.SELECT_BY_ID_WITH_USER_ID
        row = await fetch_one(query, (diary_id, user_id))

        if not row:
            return None

        return Diary(**row)

    async def update_diary(
        self,
        diary_id: int,
        user_id: int,
        diary_data: DiaryUpdate,
        files: List[UploadFile],
    ) -> Optional[Diary]:
        diary = await self.get_diary_with_user_id(diary_id, user_id)
        if not diary:
            return None

        update_fields = []
        params = []

        if diary_data.title is not None:
            update_fields.append("title = ?")
            params.append(diary_data.title)

        if diary_data.content is not None:
            update_fields.append("content = ?")
            params.append(diary_data.content)

        if diary_data.category is not None:
            update_fields.append("category = ?")
            params.append(diary_data.category)

        if files is not None:
            update_fields.append("images = ?")
            image_paths = ""
            for file in files:
                image_paths += (
                    ","
                    + await self.image_processor.write_file_and_get_image_path(
                        file, self.upload_dir
                    )
                )
            image_paths = image_paths[1:]
            params.append(image_paths)

        if update_fields:
            query = DiaryQueries.UPDATE_DIARY.format(fields=", ".join(update_fields))
            params.extend([diary_id, user_id])
            await execute(query, tuple(params))

        return await self.get_diary_with_user_id(diary_id, user_id)

    async def delete_diary(self, diary_id: int, user_id: int) -> bool:
        try:
            query = DiaryQueries.DELETE_DIARY
            await execute(query, (diary_id, user_id))
            return True
        except Exception:
            return False
