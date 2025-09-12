from fastapi import APIRouter, Depends, HTTPException
from ...core.security import get_current_user
from ...schemas.user import User
from Backend.services.store_service import StoreService
from ...services.room_service import RoomService

router = APIRouter(prefix="/store", tags=["store"])
store_service = StoreService()
room_service = RoomService()


@router.get("")
async def get_dotory(
    current_user: User = Depends(get_current_user),
):
    try:
        dotory = await store_service.get_dotory_by_id(current_user.id)
        return {"dotory": dotory}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{product_id}")
async def buy_product(
    product_id: int,
    product_name: str,
    current_user: User = Depends(get_current_user),
):
    try:
        response = await store_service.buy_product(product_id, current_user.id)
        if response["isSuccess"]:
            await room_service.add_furniture(current_user.id, product_name)
            return {"dotory": response["dotory"]}
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("")
async def update_dotory(
    dotory_num: int,
    current_user: User = Depends(get_current_user),
):
    try:
        dotory = await store_service.update_user_dotory(current_user.id, dotory_num)
        return {"dotory": dotory}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
