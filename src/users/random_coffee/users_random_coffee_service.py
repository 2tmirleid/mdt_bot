from src.dbms.methods.users.select import SelectUsers
from src.dbms.methods.users.update import UpdateUsers
from utils.RCS.service import Service


class UsersRandomCoffeeService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()
        self.update: UpdateUsers = UpdateUsers()

    async def get_user_id_by_tg_chat_id(self, chat_id) -> dict:
        query = await self.select.select_user_id_by_tg_chat_id(chat_id=chat_id)

        return await self.exec(query=query, fetch=True)

    async def get_if_user_in_random_coffee(self, user_id) -> dict:
        query = await self.select.select_user_from_users_for_random_coffee(user_id=user_id)

        return await self.exec(query=query, fetch=True)
