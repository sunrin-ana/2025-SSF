from fastapi import HTTPException
from typing import List
from Backend.utils.queries.room import RoomQueries
from Backend.schemas.room import (
    FurnitureItem,
    RoomFurniturePlacement,
    FurniturePlacementRequest,
    Room,
    RoomTypes,
    RoomTypeResponse,
    room_path,
    Furniture,
    furniture_path,
    RoomFurnitureResponse,
    FurniturePlacementResponse,
    RoomResponse,
)
from Backend.utils.db import fetch_all, fetch_one, execute


class RoomService:

    @staticmethod
    async def init_db():
        await execute(RoomQueries.CREATE_TABLE)
        await execute(RoomQueries.CREATE_TABLE_ROOM_FURNITURE)
        await execute(RoomQueries.CREATE_TABLE_USER_FURNITURE)

    async def get_or_create_room(self, user_id: int) -> int:
        row = await fetch_one(RoomQueries.SELECT_ROOM_ID_BY_USER_ID, (user_id,))
        if row:
            return row["id"]

        await execute(RoomQueries.INSERT_ROOM, (user_id, "My Room", "room_1"))
        new_row = await fetch_one(RoomQueries.SELECT_ROOM_ID_BY_USER_ID, (user_id,))

        return new_row["id"]

    async def get_room_by_id(self, id: int) -> Room:
        row = await fetch_one(RoomQueries.SELECT_ROOM_BY_ID, (id,))
        if row is None:
            raise HTTPException(status_code=404, detail="Room not found")

        return Room(**row)
    
    async def get_room_by_userId(self, id: int) -> Room:
        row = await fetch_one(RoomQueries.SELECT_ROOM_BY_USER_ID, (id,))
        if row is None:
            raise HTTPException(status_code=404, detail="Room not found")

        return Room(**row)

    async def get_room_types(self) -> List[RoomTypeResponse]:
        return [
            RoomTypeResponse(type=rt.value, image_path=room_path[rt.value])
            for rt in RoomTypes
        ]

    async def update_room_name(self, room_id: int, new_name: str):
        await execute(RoomQueries.UPDATE_ROOM_NAME, (new_name, room_id))

    async def update_room_type(self, room_id: int, new_type: RoomTypes):
        query = RoomQueries.UPDATE_ROOM_TYPE
        await execute(query, (new_type.value, room_id))

        row = await fetch_one(RoomQueries.SELECT_ROOM_BY_ID, (room_id,))
        return Room(**row)

    # furniture
    async def get_furniture_catalog(self) -> List[FurnitureItem]:
        furniture_list = []
        for f in list(Furniture):
            furniture_list.append(
                FurnitureItem(
                    name=f,
                    image_path=furniture_path[f],
                    width=int(f[-1]),
                )
            )

        return furniture_list

    async def get_room_furnitures(self, room_id: int) -> RoomFurnitureResponse:
        rows = await fetch_all(RoomQueries.SELECT_ROOM_FURNITURE, (room_id,))
        furniture_placement_response = []
        for row in rows:
            furniture_placement_response.append(
                FurniturePlacementResponse(
                    furniture_name=row["furniture_name"],
                    x=row["x"],
                    y=row["y"],
                    image_path=furniture_path[row["furniture_name"]],
                )
            )
        row = await fetch_one(RoomQueries.SELECT_ROOM_BY_ID, (room_id,))
        return RoomFurnitureResponse(
            furniture=furniture_placement_response,
            room=RoomResponse(
                id=row["id"],
                user_id=row["user_id"],
                room_name=row["room_name"],
                room_type=row["room_type"],
                room_image_path=room_path[row["room_type"]],
            ),
        )

    async def place_furniture(self, room_id: int, request: FurniturePlacementRequest):
        is_oneone = furniture_path.get(request.furniture_name + "1") is not None

        placed_furnitures = await fetch_all(
            RoomQueries.SELECT_ROOM_FURNITURE, (room_id,)
        )

        for f in placed_furnitures:
            if f["x"] == request.x and f["y"] == request.y:
                raise HTTPException(status_code=409, detail="Furniture already placed")

        await execute(
            RoomQueries.INSERT_ROOM_FURNITURE,
            (room_id, request.furniture_name, request.x, request.y),
        )
        if not is_oneone:
            await execute(
                RoomQueries.INSERT_ROOM_FURNITURE,
                (room_id, "1", request.x - 1, request.y),
            )

    async def remove_furniture(self, room_id: int, x: int, y: int, furniture_name: str):
        is_oneone = furniture_path.get(furniture_name + "1") is not None
        await execute(RoomQueries.DELETE_FURNITURE, (room_id, x, y))
        if not is_oneone:
            await execute(RoomQueries.DELETE_FURNITURE, (room_id, x - 1, y))

    async def add_furniture(self, user_id: int, furniture_name: str):
        await execute(RoomQueries.INSERT_USER_FURNITURE, (user_id, furniture_name))

    async def get_user_furniture(self, user_id: int):
        rows = await fetch_all(RoomQueries.SELECT_USER_FURNITURE, (user_id,))
        furniture_list = []
        for row in rows:
            furniture_list.append(
                FurnitureItem(
                    name=row["furniture_name"],
                    image_path=furniture_path[row["furniture_name"]],
                    width=int(row["furniture_name"][-1]),
                )
            )

        return furniture_list