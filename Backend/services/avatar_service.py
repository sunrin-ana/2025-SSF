from typing import Optional
from ..schemas.avatar import (
    AvatarUpdate,
    Avatar,
    AvatarOptions,
    AvatarType,
    TopClothesType,
    BottomClothesType,
)
from ..utils.db import execute, fetch_one
from ..utils.queries.avatar import AvatarQueries


class AvatarService:

    @staticmethod
    async def init_db():
        await execute(AvatarQueries.CREATE_TABLE)

    async def get_or_create_avatar(self, user_id: int) -> Avatar:
        avatar = await self.get_user_avatar(user_id)
        if not avatar:
            avatar = await self.create_default_avatar(user_id)
        return avatar

    async def get_user_avatar(self, user_id: int) -> Optional[Avatar]:
        row = await fetch_one(AvatarQueries.SELECT_USER_AVATAR, (user_id,))
        if not row:
            return None
        return Avatar(**row)

    async def create_default_avatar(self, user_id: int) -> Avatar:
        await execute(
            AvatarQueries.INSERT_AVATAR,
            (
                user_id,
                AvatarType.MALE.value,
                TopClothesType.ANA_CLOTHES.value,
                BottomClothesType.JEANS.value,
            ),
        )
        return await self.get_user_avatar(user_id)

    async def update_avatar(self, user_id: int, avatar_data: AvatarUpdate) -> Avatar:

        update_fields = []
        params = []

        if avatar_data.avatar_type is not None:
            update_fields.append("avatar_type = ?")
            params.append(avatar_data.avatar_type.value)
        if avatar_data.top_clothe_type is not None:
            update_fields.append("top_clothe_type = ?")
            params.append(avatar_data.top_clothe_type.value)
        if avatar_data.bottom_clothe_type is not None:
            update_fields.append("bottom_clothe_type = ?")
            params.append(avatar_data.bottom_clothe_type.value)

        if update_fields:
            query = AvatarQueries.UPDATE_AVATAR.format(fields=", ".join(update_fields))
            params.append(user_id)
            await execute(query, tuple(params))

        return await self.get_user_avatar(user_id)

    async def get_avatar_options(self) -> AvatarOptions:
        return AvatarOptions(
            avatar_types=list(AvatarType),
            top_clothe_types=list(TopClothesType),
            bottom_clothe_types=list(BottomClothesType),
        )
    
    async def get_avatar_by_userId(self, user_id: int) -> Optional[Avatar]:
        return await self.get_user_avatar(user_id)