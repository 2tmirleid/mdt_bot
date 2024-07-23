from src.dbms.methods.users.select import SelectUsers
from utils.RCS.service import Service


class UsersService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()

    async def get_user_chat_id_by_id(self, user_id) -> dict:
        query = await self.select.select_user_chat_id_by_id(user_id)

        return await self.exec(query=query, fetch=True)

    async def get_user_by_chat_id(self, user_id) -> dict:
        query = await self.select.select_user_by_chat_id(user_id)

        return await self.exec(query=query, fetch=True)

    async def get_user_by_phone(self, phone) -> dict:
        query = await self.select.select_user_by_phone(phone)

        return await self.exec(query=query, fetch=True)
