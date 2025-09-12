from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from Backend.core.security import get_current_user
from Backend.schemas.guestbook import (
    GuestBookCreate,
    GuestbookUpdate,
    GuestbookResponse,
)
from Backend.schemas.user import User
from Backend.services.guestbook_service import GuestbookService

router = APIRouter(prefix="/guestbook", tags=["guestbook"])

guestbook_service = GuestbookService()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GuestbookResponse)
async def create_guestbook(
    guestbook: GuestBookCreate, current_user: User = Depends(get_current_user)
) -> GuestbookResponse:
    try:
        response = await guestbook_service.create_guestbook(guestbook, current_user)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{target_user_id}", response_model=List[GuestbookResponse])
async def get_guestbook(target_user_id: int):
    try:
        response = await guestbook_service.get_target_user_guestbooks(target_user_id)
        response.reverse()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=GuestbookResponse)
async def update_guestbook(
    id: int,
    guestbook: GuestbookUpdate,
) -> GuestbookResponse:
    try:
        response = await guestbook_service.update_guestbook_by_id(id, guestbook.content)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
async def delete_guestbook(
    id: int,
    user: User = Depends(get_current_user),
) -> dict:
    try:
        is_success = await guestbook_service.delete_guestbook_by_id(id, user.id)
        if is_success:
            return {"detail": "success"}
        else:
            raise HTTPException(status_code=404, detail="guestbook not found")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
