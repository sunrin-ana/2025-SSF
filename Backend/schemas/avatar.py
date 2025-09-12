from pydantic import BaseModel
import enum


class AvatarType(str, enum.Enum):
    MALE = "남성"
    FEMALE = "여성"


class TopClothesType(str, enum.Enum):
    SCHOOL_CLOTHES = "교복"
    SCHOOL_CLOTHES_2 = "교복 조끼"
    ANA_CLOTHES = "AnA 동잠"
    SUSPENDERS_CLOTHES_1 = "멜빵 바지"
    SUSPENDERS_CLOTHES_2 = "멜빵 치마"
    RAINBOW_CLOTHES = "무지개 맨투맨"
    SANTA_CLOTHES = "산타"


class BottomClothesType(str, enum.Enum):
    SCHOOL_CLOTHES = "교복 바지"
    SCHOOL_CLOTHES_2 = "교복 치마"
    SCHOOL_CLOTHES_3 = "교복 조끼 바지"
    SCHOOL_CLOTHES_4 = "교복 조끼 치마"
    SANTA_CLOTHES = "산타 바지"
    JEANS = "청바지"


avatar_path_ = {"남성": "public/avatar/남자.png", "여성": "public/avatar/여자.png"}
top_clothe_path_ = {
    "교복": "public/avatar/교복상의.png",
    "교복 조끼": "public/avatar/교복조끼상의.png",
    "AnA 동잠": "public/avatar/동잠상의.png",
    "멜빵 바지": "public/avatar/멜빵바지상의.png",
    "멜빵 치마": "public/avatar/멜빵치마상의.png",
    "무지개 맨투맨": "public/avatar/무지개맨투맨상의.png",
    "산타": "public/avatar/산타상의.png",
}
bottom_clothe_path_ = {
    "교복 바지": "public/avatar/교복하의남.png",
    "교복 치마": "public/avatar/교복하의여.png",
    "교복 조끼 바지": "public/avatar/교복조끼하의남.png",
    "교복 조끼 치마": "public/avatar/교복조끼하의여.png",
    "산타 바지": "public/avatar/산타하의.png",
    "청바지": "public/avatar/청바지하의.png",
}


class AvatarTypeResponse(BaseModel):
    name: str
    path: str


class AvatarUpdate(BaseModel):
    avatar_type: AvatarType
    top_clothe_type: TopClothesType
    bottom_clothe_type: BottomClothesType


class AvatarResponse(BaseModel):
    id: int
    user_id: int
    avatar_type: AvatarTypeResponse
    top_clothe_type: AvatarTypeResponse
    bottom_clothe_type: AvatarTypeResponse


class AvatarOptions(BaseModel):
    avatar_types: list[str]
    top_clothe_types: list[str]
    bottom_clothe_types: list[str]



class Avatar:
    def __init__(
        self,
        id: int,
        user_id: int,
        avatar_type: AvatarType,
        top_clothe_type: TopClothesType,
        bottom_clothe_type: BottomClothesType,
    ):
        self.id = id
        self.user_id = user_id
        self.avatar_type = avatar_type
        self.top_clothe_type = top_clothe_type
        self.bottom_clothe_type = bottom_clothe_type

    def to_response(self) -> AvatarResponse:
        return AvatarResponse(
            id=self.id,
            user_id=self.user_id,
            avatar_type=AvatarTypeResponse(
                name=self.avatar_type,
                path=avatar_path_[self.avatar_type],
            ),
            top_clothe_type=AvatarTypeResponse(
                name=self.top_clothe_type,
                path=top_clothe_path_[self.top_clothe_type],
            ),
            bottom_clothe_type=AvatarTypeResponse(
                name=self.bottom_clothe_type,
                path=bottom_clothe_path_[self.bottom_clothe_type],
            ),
        )
