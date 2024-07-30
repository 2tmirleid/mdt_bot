from src.dbms.methods.admins.select import SelectAdmins
from utils.RCS.service import Service


class AdminsRandomCoffeeService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()

    async def get_subscribed_users_for_random_coffee(self, offset=0) -> dict:
        query = await self.select.select_subscribed_users_for_random_coffee(offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_count_subscribed_users_for_random_coffee(self) -> dict:
        query = await self.select.select_count_subscribed_users_for_random_coffe()

        return await self.exec(query=query, fetch=True)

    async def get_unsubscribed_users_for_random_coffee(self, offset=0) -> dict:
        query = await self.select.select_unsubscribed_users_for_random_coffee(offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_count_unsubscribed_users_for_random_coffee(self) -> dict:
        query = await self.select.select_count_unsubscribed_users_for_random_coffe()

        return await self.exec(query=query, fetch=True)
