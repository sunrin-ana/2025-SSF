from typing import List

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from Backend.schemas.user import UserCreate, UserLogin, UserResponse, User, UserUpdate
from Backend.services.user_service import UserService
from Backend.core.security import create_access_token, get_current_user

router = APIRouter(prefix="/user", tags=["user"])

user_service = UserService()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate = Depends(UserCreate.as_form),
    profile_file: UploadFile = File(default=None),
) -> UserResponse:
    existing_user = # 작성 #
    if existing_user:
        raise HTTPException(
            status_code=# 작성 #
            detail="# 작성 #"
        )

    existing_email = # 작성 #
    if existing_email:
        raise HTTPException(
            status_code=# 작성 #
            detail="# 작성 #"
        )

    try:
        user = # 작성 #
        return user.to_response()
    except Exception as e:
        raise HTTPException(
            status_code=
            detail="# 작성 #"
        )

@router.post("/login")
async def login_user(login_data: UserLogin) -> dict:
    user = await user_service.authenticate_user(
        
    )

    if not user:
        raise HTTPException(
            status_code=
            detail=
        )

    if not user.is_active:
        raise HTTPException(
            status_code=, detail=""
        )

    access_token = 

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/profile/{username}", response_model=UserResponse)
async def get_user_profile(username: str) -> UserResponse:
    user = await user_service.get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user.to_response()


@router.get("/me", response_model=UserResponse)
async def get_user_me(user: User = Depends(get_current_user)) -> UserResponse:
    return user.to_response()


@router.delete("/{username}")
async def delete_user(username: str) -> dict:
    is_success = await user_service.delete_user(username)
    if not is_success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"detail": "User deleted"}


@router.get("/find/{username}", response_model=List[UserResponse])
async def find_user(username: str) -> List[UserResponse]:
    users = await user_service.find_user(username)
    return users


@router.put("/", response_model=UserResponse)
async def update_user(
    current_user: User = Depends(get_current_user),
    user_data: UserUpdate = Depends(UserUpdate.as_form),
    profile_file: UploadFile = File(default=None),
) -> UserResponse:
    try:
        updated_user = await user_service.update_user(
            user=current_user, user_data=user_data, profile_file=profile_file
        )
        return updated_user.to_response()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}",
        )
