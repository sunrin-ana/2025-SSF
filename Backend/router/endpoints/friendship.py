from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ...schemas.friendship import (
    FriendshipRequest,
    FriendshipResponse,
)
from ...services.friendship_service import FriendshipService
from ...core.security import get_current_user
from ...schemas.user import User

router = APIRouter(prefix="/friendship", tags=["friendship"])
friendship_service = FriendshipService()


@router.post("/request", response_model=FriendshipResponse)
async def send_friendship_request(
    request_data: FriendshipRequest, current_user: User = Depends(get_current_user)
) -> FriendshipResponse:
    try:
        friendship = await friendship_service.send_friendship_request(
            current_user.id, request_data.friend_username
        )
        return friendship
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{friendship_id}/accept", response_model=FriendshipResponse)
async def accept_friendship_request(
    friendship_id: int, current_user: User = Depends(get_current_user)
) -> FriendshipResponse:
    try:
        friendship = await friendship_service.accept_friendship_request(
            friendship_id, current_user.id
        )
        if not friendship:
            raise HTTPException(status_code=404, detail="Friendship request not found")
        return friendship
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[FriendshipResponse])
async def get_friendships(
    status: Optional[str] = None, current_user: User = Depends(get_current_user)
) -> List[FriendshipResponse]:
    try:
        friendships = await friendship_service.get_user_friendships(
            current_user.id, status
        )
        return friendships
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{friendship_id}")
async def delete_friendship(
    friendship_id: int, current_user: User = Depends(get_current_user)
) -> dict:
    try:
        success = await friendship_service.delete_friendship(
            friendship_id, current_user.id
        )
        if not success:
            raise HTTPException(status_code=404, detail="Friendship not found")
        return {"message": "Friendship deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pending", response_model=List[FriendshipResponse])
async def get_pending_requests(
    current_user: User = Depends(get_current_user),
) -> List[FriendshipResponse]:
    try:
        pending_requests = await friendship_service.get_pending_requests(
            current_user.id
        )
        return pending_requests
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
