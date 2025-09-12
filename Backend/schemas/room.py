import enum
from pydantic import BaseModel, field_validator
from typing import Optional, List


class RoomNameUpdateRequest(BaseModel):
    new_name: str


class RoomTypes(enum.Enum):
    ROOM_1 = "room_1"
    ROOM_2 = "room_2"


class UpdateRoomTypeRequest(BaseModel):
    type: RoomTypes


class RoomTypeResponse(BaseModel):
    type: str
    image_path: str


class RoomResponse(BaseModel):
    id: int
    user_id: int
    room_name: str
    room_type: RoomTypes
    room_image_path: str


room_path = {
    "room_1": "public/room/room_1.png",
    "room_2": "public/room/room_2.png",
}


class FurnitureItem(BaseModel):
    name: str
    image_path: str
    width: int


class Furniture(str, enum.Enum):
    BLACK_LAPTOP1_0 = "검정 노트북1-01"
    BLACK_LAPTOP1_180 = "검정 노트북1-1801"
    BLACK_LAPTOP1_270 = "검정 노트북1-2701"
    BLACK_LAPTOP1_90 = "검정 노트북1-901"
    BLACK_LAPTOP2_0 = "검정 노트북2-01"
    BLACK_LAPTOP2_180 = "검정 노트북2-1801"
    BLACK_LAPTOP2_270 = "검정 노트북2-2701"
    BLACK_LAPTOP2_90 = "검정 노트북2-901"
    BLACK_LAPTOP3_0 = "검정 노트북3-01"
    BLACK_LAPTOP3_180 = "검정 노트북3-1801"
    BLACK_LAPTOP3_270 = "검정 노트북3-2701"
    BLACK_LAPTOP3_90 = "검정 노트북3-901"
    WOODEN_TABLE_90 = "나무 탁자-901"
    WOODEN_TABLE_0 = "나무 탁자-01"
    LAPTOP1_0 = "노트북1-01"
    LAPTOP1_180 = "노트북1-1801"
    LAPTOP1_270 = "노트북1-2701"
    LAPTOP1_90 = "노트북1-901"
    LAPTOP2_0 = "노트북2-01"
    LAPTOP2_180 = "노트북2-1801"
    LAPTOP2_270 = "노트북2-2701"
    LAPTOP2_90 = "노트북2-901"
    LAPTOP3_0 = "노트북3-01"
    LAPTOP3_180 = "노트북3-1801"
    LAPTOP3_270 = "노트북3-2701"
    LAPTOP3_90 = "노트북3-901"
    GREEN_TABLE = "녹색 탁자1"
    MINI_FRIDGE_0 = "미니 냉장고-01"
    MINI_FRIDGE_180 = "미니 냉장고-1801"
    MINI_FRIDGE_90 = "미니 냉장고-901"
    BOX_0 = "박스-01"
    BOX_90 = "박스-901"
    PINK_TABLE = "분홍색 탁자1"
    SHELF_0 = "선반-01"
    SHELF_180 = "선반-1801"
    SHELF_270 = "선반-2701"
    SHELF_90 = "선반-901"
    TRASH_CAN_CLOSED = "쓰레기통 닫힘1"
    TRASH_CAN_OPEN = "쓰레기통 열림1"
    FISHBOWL_0 = "어항-01"
    FISHBOWL_180 = "어항-1801"
    FISHBOWL_270 = "어항-2701"
    FISHBOWL_90 = "어항-901"
    BEVERAGE_FRIDGE_0 = "음료 냉장고-01"
    BEVERAGE_FRIDGE_180 = "음료 냉장고-1801"
    BEVERAGE_FRIDGE_270 = "음료 냉장고-2701"
    BEVERAGE_FRIDGE_90 = "음료 냉장고-901"
    CHAIR_0 = "의자-01"
    CHAIR_180 = "의자-1801"
    CHAIR_270 = "의자-2701"
    CHAIR_90 = "의자-901"
    SMALL_SHELF_0 = "작은 선반-01"
    SMALL_SHELF_180 = "작은 선반-1801"
    SMALL_SHELF_270 = "작은 선반-2701"
    SMALL_SHELF_90 = "작은 선반-901"
    SMALL_PLANT = "작은 식물1"
    BOOKSHELF_0 = "책장-01"
    BOOKSHELF_180 = "책장-1801"
    BOOKSHELF_270 = "책장-2701"
    BOOKSHELF_90 = "책장-901"
    LARGE_PLANT = "큰 식물1"
    TV_0 = "티비-01"
    TV_180 = "티비-1801"
    TV_270 = "티비-2701"
    TV_90 = "티비-901"
    BLUE_TABLE = "파란색 탁자1"
    GRAY_TABLE = "회색 탁자1"
    WHITE_LAPTOP1_0 = "흰 노트북1-01"
    WHITE_LAPTOP1_180 = "흰 노트북1-1801"
    WHITE_LAPTOP1_270 = "흰 노트북1-2701"
    WHITE_LAPTOP1_90 = "흰 노트북1-901"
    WHITE_LAPTOP2_0 = "흰 노트북2-01"
    WHITE_LAPTOP2_180 = "흰 노트북2-1801"
    WHITE_LAPTOP2_270 = "흰 노트북2-2701"
    WHITE_LAPTOP2_90 = "흰 노트북2-901"
    WHITE_LAPTOP3_0 = "흰 노트북3-01"
    WHITE_LAPTOP3_180 = "흰 노트북3-1801"
    WHITE_LAPTOP3_270 = "흰 노트북3-2701"
    WHITE_LAPTOP3_90 = "흰 노트북3-901"
    WHITE_SHELF_0 = "흰색 선반-01"
    WHITE_SHELF_180 = "흰색 선반-1801"
    WHITE_SHELF_270 = "흰색 선반-2701"
    WHITE_SHELF_90 = "흰색 선반-901"
    WHITE_SMALL_SHELF_0 = "흰색 작은 선반-01"
    WHITE_SMALL_SHELF_180 = "흰색 작은 선반-1801"
    WHITE_SMALL_SHELF_270 = "흰색 작은 선반-2701"
    WHITE_SMALL_SHELF_90 = "흰색 작은 선반-901"
    WHITE_TABLE = "흰색 탁자1"
    EMPTY = "1"


class RoomFurniturePlacement(BaseModel):
    id: int
    room_id: int
    furniture_name: Furniture
    x: int
    y: int


class FurniturePlacementRequest(BaseModel):
    furniture_name: Furniture
    x: int
    y: int

    @field_validator("x", "y")
    @classmethod
    def validate_coordinates(cls, v):
        if v < 0 or v >= 10:
            raise ValueError("position must be between 0 and 10")
        return v


class FurniturePlacementResponse(BaseModel):
    furniture_name: Furniture
    x: int
    y: int
    image_path: str


class RoomFurnitureResponse(BaseModel):
    room: RoomResponse
    furniture: List[FurniturePlacementResponse]


furniture_path = {
    "검정 노트북1-01": "public/funiture/검정 노트북1-0.png",
    "검정 노트북1-1801": "public/funiture/검정 노트북1-180.png",
    "검정 노트북1-2701": "public/funiture/검정 노트북1-270.png",
    "검정 노트북1-901": "public/funiture/검정 노트북1-90.png",
    "검정 노트북2-01": "public/funiture/검정 노트북2-0.png",
    "검정 노트북2-1801": "public/funiture/검정 노트북2-180.png",
    "검정 노트북2-2701": "public/funiture/검정 노트북2-270.png",
    "검정 노트북2-901": "public/funiture/검정 노트북2-90.png",
    "검정 노트북3-01": "public/funiture/검정 노트북3-0.png",
    "검정 노트북3-1801": "public/funiture/검정 노트북3-180.png",
    "검정 노트북3-2701": "public/funiture/검정 노트북3-270.png",
    "검정 노트북3-901": "public/funiture/검정 노트북3-90.png",
    "나무 탁자-901": "public/funiture/나무 탁자-90.png",
    "나무 탁자-01": "public/funiture/나무탁자-0.png",
    "노트북1-01": "public/funiture/노트북1-0.png",
    "노트북1-1801": "public/funiture/노트북1-180.png",
    "노트북1-2701": "public/funiture/노트북1-270.png",
    "노트북1-901": "public/funiture/노트북1-90.png",
    "노트북2-01": "public/funiture/노트북2-0.png",
    "노트북2-1801": "public/funiture/노트북2-180.png",
    "노트북2-2701": "public/funiture/노트북2-270.png",
    "노트북2-901": "public/funiture/노트북2-90.png",
    "노트북3-01": "public/funiture/노트북3-0.png",
    "노트북3-1801": "public/funiture/노트북3-180.png",
    "노트북3-2701": "public/funiture/노트북3-270.png",
    "노트북3-901": "public/funiture/노트북3-90.png",
    "녹색 침대-02": "public/funiture/녹색 침대-0.png",
    "녹색 침대-1802": "public/funiture/녹색 침대-180.png",
    "녹색 침대-2702": "public/funiture/녹색 침대-270.png",
    "녹색 침대-902": "public/funiture/녹색 침대-90.png",
    "녹색 탁자1": "public/funiture/녹색 탁자.png",
    "미니 냉장고-01": "public/funiture/미니 냉장고-0.png",
    "미니 냉장고-1801": "public/funiture/미니 냉장고-180.png",
    "미니 냉장고-901": "public/funiture/미니 냉장고-90.png",
    "박스-01": "public/funiture/박스-0.png",
    "박스-901": "public/funiture/박스-90.png",
    "분홍색 탁자1": "public/funiture/분홍색 탁자.png",
    "빨간 침대-02": "public/funiture/빨간 침대-0.png",
    "빨간 침대-1802": "public/funiture/빨간 침대-180.png",
    "빨간 침대-2702": "public/funiture/빨간 침대-270.png",
    "빨간 침대-902": "public/funiture/빨간 침대-90.png",
    "선반-01": "public/funiture/선반-0.png",
    "선반-1801": "public/funiture/선반-180.png",
    "선반-2701": "public/funiture/선반-270.png",
    "선반-901": "public/funiture/선반-90.png",
    "소파-02": "public/funiture/소파-0.png",
    "소파-1802": "public/funiture/소파-180.png",
    "소파-2702": "public/funiture/소파-270.png",
    "소파-902": "public/funiture/소파-90.png",
    "쓰레기통 닫힘1": "public/funiture/쓰레기통닫힘.png",
    "쓰레기통 열림1": "public/funiture/쓰레기통열림.png",
    "어항-01": "public/funiture/어항-0.png",
    "어항-1801": "public/funiture/어항-180.png",
    "어항-2701": "public/funiture/어항-270.png",
    "어항-901": "public/funiture/어항-90.png",
    "음료 냉장고-01": "public/funiture/음료 냉장고-0.png",
    "음료 냉장고-1801": "public/funiture/음료 냉장고-180.png",
    "음료 냉장고-2701": "public/funiture/음료 냉장고-270.png",
    "음료 냉장고-901": "public/funiture/음료 냉장고-90.png",
    "의자-01": "public/funiture/의자-0.png",
    "의자-1801": "public/funiture/의자-180.png",
    "의자-2701": "public/funiture/의자-270.png",
    "의자-901": "public/funiture/의자-90.png",
    "작은 선반-01": "public/funiture/작은 선반-0.png",
    "작은 선반-1801": "public/funiture/작은 선반-180.png",
    "작은 선반-2701": "public/funiture/작은 선반-270.png",
    "작은 선반-901": "public/funiture/작은 선반-90.png",
    "작은 식물1": "public/funiture/작은 식물.png",
    "주황 침대-02": "public/funiture/주황 침대-0.png",
    "주황 침대-1802": "public/funiture/주황 침대-180.png",
    "주황 침대-2702": "public/funiture/주황 침대-270.png",
    "주황 침대-902": "public/funiture/주황 침대-90.png",
    "책장-01": "public/funiture/책장-0.png",
    "책장-1801": "public/funiture/책장-180.png",
    "책장-2701": "public/funiture/책장-270.png",
    "책장-901": "public/funiture/책장-90.png",
    "큰 식물1": "public/funiture/큰 식물.png",
    "티비-01": "public/funiture/티비-0.png",
    "티비-1801": "public/funiture/티비-180.png",
    "티비-2701": "public/funiture/티비-270.png",
    "티비-901": "public/funiture/티비-90.png",
    "파란 침대-02": "public/funiture/파란 침대-0.png",
    "파란 침대-1802": "public/funiture/파란 침대-180.png",
    "파란 침대-2702": "public/funiture/파란 침대-270.png",
    "파란 침대-902": "public/funiture/파란 침대-90.png",
    "파란색 탁자1": "public/funiture/파란색 탁자.png",
    "회색 탁자1": "public/funiture/회색 탁자.png",
    "흰 노트북1-01": "public/funiture/흰 노트북1-0.png",
    "흰 노트북1-1801": "public/funiture/흰 노트북1-180.png",
    "흰 노트북1-2701": "public/funiture/흰 노트북1-270.png",
    "흰 노트북1-901": "public/funiture/흰 노트북1-90.png",
    "흰 노트북2-01": "public/funiture/흰 노트북2-0.png",
    "흰 노트북2-1801": "public/funiture/흰 노트북2-180.png",
    "흰 노트북2-2701": "public/funiture/흰 노트북2-270.png",
    "흰 노트북2-901": "public/funiture/흰 노트북2-90.png",
    "흰 노트북3-01": "public/funiture/흰 노트북3-0.png",
    "흰 노트북3-1801": "public/funiture/흰 노트북3-180.png",
    "흰 노트북3-2701": "public/funiture/흰 노트북3-270.png",
    "흰 노트북3-901": "public/funiture/흰 노트북3-90.png",
    "흰색 선반-01": "public/funiture/흰색 선반-0.png",
    "흰색 선반-1801": "public/funiture/흰색 선반-180.png",
    "흰색 선반-2701": "public/funiture/흰색 선반-270.png",
    "흰색 선반-901": "public/funiture/흰색 선반-90.png",
    "흰색 작은 선반-01": "public/funiture/흰색 작은 선반-0.png",
    "흰색 작은 선반-1801": "public/funiture/흰색 작은 선반-180.png",
    "흰색 작은 선반-2701": "public/funiture/흰색 작은 선반-270.png",
    "흰색 작은 선반-901": "public/funiture/흰색 작은 선반-90.png",
    "흰색 탁자1": "public/funiture/흰색 탁자.png",
    "1": "1",
}


class Room:
    def __init__(self, id: int, user_id: int, room_name: str, room_type: RoomTypes):
        self.id = id
        self.user_id = user_id
        self.room_name = room_name
        self.room_type = room_type

    def to_response(self) -> RoomResponse:
        return RoomResponse(
            id=self.id,
            user_id=self.user_id,
            room_name=self.room_name,
            room_type=self.room_type,
            room_image_path=room_path[self.room_type],
        )
