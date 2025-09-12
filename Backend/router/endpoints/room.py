from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Backend.schemas.room import (
    FurnitureItem,
    RoomFurniturePlacement,
    FurniturePlacementRequest,
    RoomNameUpdateRequest,
    UpdateRoomTypeRequest,
    RoomResponse,
    RoomTypeResponse,
    RoomFurnitureResponse,
)
from Backend.schemas.user import User
from Backend.core.security import get_current_user
from Backend.services.room_service import RoomService

router = APIRouter(prefix="/room", tags=["room"])
room_service = RoomService()


@router.get("/catalog", response_model=List[FurnitureItem])
async def get_furniture_catalog() -> List[FurnitureItem]:
    return await room_service.get_furniture_catalog()


@router.get("/layout", response_model=RoomFurnitureResponse)
async def get_my_room_layout(current_user: User = Depends(get_current_user)):
    room_id = await room_service.get_or_create_room(current_user.id)
    return await room_service.get_room_furnitures(room_id)


@router.get("/layout/{user_id}", response_model=RoomFurnitureResponse)
async def get_user_room_layout(user_id: int) -> RoomFurnitureResponse:
    room_id = await room_service.get_or_create_room(user_id)
    return await room_service.get_room_furnitures(room_id)


@router.post("/furniture")
async def place_furniture(
    request: FurniturePlacementRequest, current_user: User = Depends(get_current_user)
):
    room_id = await room_service.get_or_create_room(current_user.id)
    try:
        await room_service.place_furniture(room_id, request)
        return {"message": "Furniture placed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/furniture")
async def remove_furniture(
    x: int, y: int, furniture_name: str, current_user: User = Depends(get_current_user)
):
    room_id = await room_service.get_or_create_room(current_user.id)
    await room_service.remove_furniture(room_id, x, y, furniture_name)
    return {"message": "Furniture removed successfully"}


@router.put("/")
async def update_room_name(
    data: RoomNameUpdateRequest, current_user: User = Depends(get_current_user)
):
    try:
        room_id = await room_service.get_or_create_room(current_user.id)
        await room_service.update_room_name(room_id, data.new_name)
        return {"message": "Room name updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def get_my_room(current_user: User = Depends(get_current_user)) -> RoomResponse:
    try:
        room_id = await room_service.get_or_create_room(current_user.id)
        return (await room_service.get_room_by_id(room_id)).to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/types")
async def get_room_types() -> List[RoomTypeResponse]:
    return await room_service.get_room_types()


@router.patch("/")
async def update_room_type(
    data: UpdateRoomTypeRequest, current_user: User = Depends(get_current_user)
) -> RoomResponse:
    try:
        room_id = await room_service.get_or_create_room(current_user.id)
        return (await room_service.update_room_type(room_id, data.type)).to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my")
async def get_my_furniture(current_user: User = Depends(get_current_user)):
    try:
        list_ = await room_service.get_user_furniture(current_user.id)
        return list_
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{user_id}", response_model=RoomResponse)
async def get_room_by_userId(user_id: int) -> RoomResponse:
    try:
        room = await room_service.get_room_by_userId(user_id)
        return room.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))