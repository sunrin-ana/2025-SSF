# from fastapi import APIRouter, HTTPException, Depends
#
# from ...schemas.letter import LetterCreate, LetterResponse, EmailRequest
# from ...services.letter_service import LetterService
# from ...core.security import get_current_user
# from ...schemas.user import User
#
# router = APIRouter(prefix="/letter", tags=["letter"])
# letter_service = LetterService()
#
#
# @router.post("", response_model=LetterResponse)
# async def create_letter(
#     letter_data: LetterCreate,
#     current_user: User = Depends(get_current_user),
# ) -> LetterResponse:
#     try:
#         letter = await letter_service.create_letter(current_user.id, letter_data)
#         return letter.to_response()
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.get("/{letter_id}", response_model=LetterResponse)
# async def get_letter(
#     letter_id: int, current_user: User = Depends(get_current_user)
# ) -> LetterResponse:
#     try:
#         letter = await letter_service.get_letter_by_id(letter_id, current_user.id)
#         if not letter:
#             raise HTTPException(status_code=404, detail="Letter not found")
#         return letter.to_response()
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.delete("/{letter_id}")
# async def delete_letter(letter_id: int, current_user: User = Depends(get_current_user)):
#     try:
#         is_success = await letter_service.delete_letter(letter_id, current_user.id)
#         if not is_success:
#             raise HTTPException(status_code=404, detail="Letter not found")
#         return {"detail": "Letter deleted"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.put("/{letter_id}", response_model=LetterResponse)
# async def update_letter(
#     letter_id: int,
#     letter_data: LetterCreate,
#     current_user: User = Depends(get_current_user),
# ):
#     try:
#         letter = await letter_service.update_letter(
#             letter_id, current_user.id, letter_data.content
#         )
#         if not letter:
#             raise HTTPException(status_code=404, detail="Letter not found")
#         return letter.to_response()
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.post("/{letter_id}/send")
# async def send_letter(
#     letter_id: int,
#     letter_data: EmailRequest,
#     current_user: User = Depends(get_current_user),
# ):
#     try:
#         letter = await letter_service.get_letter_by_id(letter_id, current_user.id)
#         if not letter:
#             raise HTTPException(status_code=404, detail="Letter not found")
#
#         await letter_service.send_letter(letter, letter_data)
#         return {"message": "Email sent successfully!"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
