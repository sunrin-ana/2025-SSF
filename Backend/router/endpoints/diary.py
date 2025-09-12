from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile,
    File,
)
from typing import List, Optional
from ...schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse, Diary
from ...services.diary_service import DiaryService
from ...core.security import get_current_user
from ...schemas.user import User

router = APIRouter(prefix="/diary", tags=["diary"])
diary_service = DiaryService()


@router.post("", response_model=DiaryResponse)
async def create_diary(
    diary_data: DiaryCreate = Depends(DiaryCreate.as_form),
    file: List[UploadFile] = File(default=None),
    current_user: User = Depends(get_current_user),
) -> DiaryResponse:
    try:
        diary = await diary_service.create_diary(current_user.id, diary_data, file)
        return diary.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[DiaryResponse])
async def get_user_diaries(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> List[DiaryResponse]:
    try:
        diaries = await diary_service.get_user_diaries(
            current_user.id, skip, limit, category
        )
        return [diary.to_response() for diary in diaries]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/w/{target_user_id}", response_model=List[DiaryResponse])
async def get_target_user_diaries(
    target_user_id: int,
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
) -> List[DiaryResponse]:
    try:
        diaries = await diary_service.get_user_diaries(
            target_user_id, skip, limit, category
        )
        return [diary.to_response() for diary in diaries]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(diary_id: int) -> DiaryResponse:
    try:
        diary = await diary_service.get_diary_by_id(diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")
        return diary.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    diary_data: DiaryUpdate = Depends(DiaryUpdate.as_form),
    file: List[UploadFile] = File(default=None),
    current_user: User = Depends(get_current_user),
) -> DiaryResponse:
    try:
        diary = await diary_service.update_diary(
            diary_id, current_user.id, diary_data, file
        )
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")
        return diary.to_response()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{diary_id}")
async def delete_diary(
    diary_id: int, current_user: User = Depends(get_current_user)
) -> dict:
    try:
        success = await diary_service.delete_diary(diary_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Diary not found")
        return {"message": "Diary deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
