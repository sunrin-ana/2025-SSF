# from typing import List, Optional
# from ..schemas.letter import LetterCreate, Letter, EmailRequest
# from ..utils.db import execute, fetch_one, fetch_all
# from ..utils.default_queries import LetterQueries
# from ..utils.email_processor import EmailProcessor
#
#
# class LetterService:
#     def __init__(self):
#         self.email_processor = EmailProcessor()
#
#     @staticmethod
#     async def init_db():
#         await execute(LetterQueries.CREATE_TABLE)
#
#     async def create_letter(self, sender_id: int, letter_data: LetterCreate) -> Letter:
#         query = LetterQueries.INSERT_LETTER
#
#         await execute(
#             query,
#             (sender_id, letter_data.content),
#         )
#
#         row = await fetch_one(
#             LetterQueries.SELECT_LATEST_USER_LETTER,
#             (sender_id,),
#         )
#
#         return Letter(**row)
#
#     async def get_user_letters(
#         self, sender_id: int, skip: int = 0, limit: int = 20
#     ) -> List[Letter]:
#         query = LetterQueries.SELECT_USER_LETTERS
#         rows = await fetch_all(query, (sender_id, limit, skip))
#         return [Letter(**row) for row in rows]
#
#     async def get_letter_by_id(
#         self, letter_id: int, sender_id: int
#     ) -> Optional[Letter]:
#         query = LetterQueries.SELECT_LETTER_BY_ID
#         row = await fetch_one(query, (letter_id, sender_id))
#         if not row:
#             return None
#         return Letter(**row)
#
#     async def delete_letter(self, letter_id: int, sender_id: int) -> bool:
#         try:
#             query = LetterQueries.DELETE_LETTER
#             await execute(
#                 query,
#                 (letter_id, sender_id),
#             )
#             return True
#         except Exception:
#             return False
#
#     async def update_letter(
#         self, letter_id: int, sender_id: int, content: str
#     ) -> Optional[Letter]:
#         query = LetterQueries.UPDATE_LETTER
#         await execute(
#             query,
#             (content, letter_id, sender_id),
#         )
#
#         row = await fetch_one(
#             LetterQueries.SELECT_LETTER_BY_ID,
#             (letter_id, sender_id),
#         )
#         if row is None:
#             return None
#
#         return Letter(**row)
#
#     async def send_letter(self, letter: Letter, data: EmailRequest):
#         subject = f"2025_SSF_LETTER_{data.sender_name}"
#         content = letter.content
#         await self.email_processor.send_email(
#             subject, content, data.sender_email, data.sender_password
#         )
