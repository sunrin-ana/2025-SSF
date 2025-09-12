from datetime import datetime, timezone, timedelta
from typing import Optional, List
import os
from fastapi import UploadFile
from Backend.utils.db import execute, fetch_one, fetch_all
from Backend.utils.image_processor import ImageProcessor
from Backend.utils.queries.user import UserQueries
from Backend.schemas.user import User, UserCreate, UserResponse, UserUpdate
from Backend.services.store_service import StoreService

store_service = StoreService()

class UserService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.upload_dir = "uploads/profile"
        os.makedirs(self.upload_dir, exist_ok=True)

    @staticmethod
    async def init_db():
        await execute(UserQueries.CREATE_TABLE)

    async def create_user(
        self, user_data: UserCreate, profile_file: UploadFile = None
    ) -> User:
        password_hash, salt = 

        if profile_file is not None:
            await self.image_processor.validate_image_file(
                
            )
            image_path = 
            query = UserQueries.INSERT_USER_WITH_PROFILE
            params = (
                user_data.username,
                user_data.email,
                password_hash,
                salt,
                image_path,
            )
        else:
            query = UserQueries.INSERT_USER_WITHOUT_PROFILE
            params = (user_data.username, user_data.email, password_hash, salt)

        await execute(
            query,
            params,
        )

        row = await fetch_one(
            UserQueries.SELECT_BY_USERNAME,
            (user_data.username,),
        )

        if row is None:
            raise Exception("User creation failed")

        row = dict(row)

        if isinstance(row["created_at"], str):
            datetime.fromisoformat(row["created_at"].replace("Z", "+09:00"))

        row["is_active"] = bool(row["is_active"])

        await store_service.register_user(row["id"])


        return User(**row)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        row = await fetch_one(
            UserQueries.SELECT_BY_USERNAME,
            (username,),
        )

        if row is None:
            return None

        row = dict(row)

        if isinstance(row["created_at"], str):
            datetime.fromisoformat(row["created_at"].replace("Z", "+09:00"))

        row["is_active"] = bool(row["is_active"])

        return User(**row)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        row = await fetch_one(
            UserQueries.SELECT_BY_EMAIL,
            (email,),
        )

        if row is None:
            return None

        row = dict(row)

        if isinstance(row["created_at"], str):
            datetime.fromisoformat(row["created_at"].replace("Z", "+09:00"))

        row["is_active"] = bool(row["is_active"])

        return User(**row)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = 
        if user and :
            return user
        return None

    async def delete_user(self, username: str) -> bool:
        try:
            query = UserQueries.DELETE_USER_BY_USERNAME
            await execute(query, (username,))
            return True
        except Exception:
            return False

    async def find_user(self, username: str) -> List[UserResponse]:
        query = UserQueries.SELECT_BY_USERNAME_LIKE
        rows = await fetch_all(
            query,
            ("%" + username + "%",),
        )

        return [User(**row).to_response() for row in rows]

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        row = await fetch_one(UserQueries.SELECT_BY_ID, (user_id,))
        if row is None:
            return None
        row = dict(row)
        if isinstance(row["created_at"], str):
            datetime.fromisoformat(row["created_at"].replace("Z", "+09:00"))
        row["is_active"] = bool(row["is_active"])
        return User(**row)

    async def update_user(
        self, user: User, user_data: UserUpdate, profile_file: UploadFile = None
    ) -> User:
        update_fields = {}
        if user_data.email:
            existing_user = await fetch_one(
                UserQueries.SELECT_USER_BY_EMAIL_AND_NOT_ID,
                (user_data.email, user.id),
            )
            if existing_user:
                raise ValueError("Email already registered")
            update_fields["email"] = user_data.email

        if user_data.password:
            password_hash, salt = User.hash_password(user_data.password)
            update_fields["password_hash"] = password_hash
            update_fields["salt"] = salt

        if profile_file:
            await self.image_processor.validate_image_file(
                profile_file.filename, profile_file.size
            )
            image_path = await self.image_processor.write_file_and_get_image_path(
                profile_file, upload_dir=self.upload_dir
            )
            update_fields["profile_image_path"] = image_path

        if not update_fields:
            return user

        set_clause = ", ".join(f"{key} = ?" for key in update_fields.keys())
        query = UserQueries.UPDATE_USER_BY_ID.format(set_clause)
        params = list(update_fields.values())
        params.append(user.id)

        await execute(query, tuple(params))

        return await self.get_user_by_id(user.id)
