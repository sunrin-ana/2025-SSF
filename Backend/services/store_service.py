import httpx


class StoreService:
    def __init__(self):
        self.SERVER_URL = "https://dotory.ana.st"

    async def get_dotory_by_id(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.SERVER_URL}/")
            response_json = response.json()
            return 

    async def register_user(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.SERVER_URL}/", json={"user_id": user_id}
            )
            return 

    async def buy_product(self, product_id: int, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.SERVER_URL}/", json={"user_id": user_id}
            )
            return 

    async def update_user_dotory(self, user_id: int, dotoryNum: int):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.SERVER_URL}/", json={"num": dotoryNum}
            )
            return 