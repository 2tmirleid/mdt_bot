from src.dbms.methods.users.select import SelectUsers
from src.dbms.methods.users.update import UpdateUsers
from utils.RCS.service import Service


class UsersService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()
        self.update: UpdateUsers = UpdateUsers()

    async def get_user_chat_id_by_id(self, user_id) -> dict:
        query = await self.select.select_user_chat_id_by_id(user_id)

        return await self.exec(query=query, fetch=True)

    async def get_user_by_chat_id(self, user_id) -> dict:
        query = await self.select.select_user_by_chat_id(user_id)

        return await self.exec(query=query, fetch=True)

    async def get_user_by_phone(self, phone) -> dict:
        query = await self.select.select_user_by_phone(phone)

        return await self.exec(query=query, fetch=True)

    async def get_user_profile_by_chat_id(self, chat_id) -> dict:
        query = await self.select.select_user_profile_by_chat_id(chat_id)

        return await self.exec(query=query, fetch=True)

    async def edit_profile(self, chat_id, property, value) -> bool:
        try:
            query = await self.update.update_profile(chat_id, property, value)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while updating user from db: {e}")
            return False
