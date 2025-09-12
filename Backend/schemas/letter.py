# from pydantic import BaseModel, field_validator, EmailStr
#
# # email validator 삭제 및 EmailStr 사용
#
#
# class LetterCreate(BaseModel):
#     content: str
#
#     @field_validator("content")
#     @classmethod
#     def validate_content(cls, v):
#         if len(v.strip()) < 1:
#             raise ValueError("Letter content cannot be empty")
#         if len(v) > 2000:
#             raise ValueError("Letter content must be less than 2000 characters")
#         return v.strip()
#
#
# class LetterResponse(BaseModel):
#     id: int
#     sender_id: int
#     content: str
#
#
# class Letter:
#     def __init__(
#         self,
#         id: int,
#         sender_id: int,
#         content: str,
#     ):
#         self.id = id
#         self.sender_id = sender_id
#         self.content = content
#
#     def to_response(self) -> LetterResponse:
#         return LetterResponse(
#             id=self.id,
#             sender_id=self.sender_id,
#             content=self.content,
#         )
#
#
# class EmailRequest(BaseModel):
#     sender_email: EmailStr
#     sender_password: str
#     sender_name: str
