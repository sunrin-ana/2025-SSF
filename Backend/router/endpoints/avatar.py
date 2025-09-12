from fastapi import APIRouter, HTTPException, Depends
from ...schemas.avatar import (
    AvatarUpdate,
    AvatarResponse,
    AvatarOptions,
)
from ...services.avatar_service import AvatarService
from ...core.security import get_current_user
from ...schemas.user import User

router = APIRouter(prefix="/avatar", tags=["avatar"])
avatar_service = AvatarService()


@router.get("", response_model=AvatarResponse)
async def get_my_avatar(
    current_user: User = Depends(get_current_user),
) -> AvatarResponse:
    try:
        avatar = await avatar_service.get_or_create_avatar(current_user.id)
        return avatar.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("", response_model=AvatarResponse)
async def update_avatar(
    avatar_data: AvatarUpdate, current_user: User = Depends(get_current_user)
) -> AvatarResponse:
    try:
        avatar = await avatar_service.update_avatar(current_user.id, avatar_data)
        return avatar.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/options", response_model=AvatarOptions)
async def get_avatar_options() -> AvatarOptions:
    try:
        return await avatar_service.get_avatar_options()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=AvatarResponse)
async def get_avatar_by_userId(user_id: int) -> AvatarResponse:
    avatar = await avatar_service.get_avatar_by_userId(user_id)
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return avatar.to_response()
