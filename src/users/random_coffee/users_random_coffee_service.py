from src.dbms.methods.users.delete import DeleteUsers
from src.dbms.methods.users.insert import InsertUsers
from src.dbms.methods.users.select import SelectUsers
from src.dbms.methods.users.update import UpdateUsers
from utils.RCS.service import Service


class UsersRandomCoffeeService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()
        self.update: UpdateUsers = UpdateUsers()
        self.insert: InsertUsers = InsertUsers()
        self.delete: DeleteUsers = DeleteUsers()

    async def get_user_id_by_tg_chat_id(self, chat_id) -> dict:
        query = await self.select.select_user_id_by_tg_chat_id(chat_id=chat_id)

        return await self.exec(query=query, fetch=True)

    async def get_if_user_in_random_coffee(self, user_id) -> dict:
        query = await self.select.select_user_from_users_for_random_coffee(user_id=user_id)

        return await self.exec(query=query, fetch=True)

    async def subscribe_user_for_random_coffee(self, user_id) -> bool:
        try:
            query = await self.insert.insert_user_for_random_coffee(user_id=user_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while subscribing user for random_coffee from db: {e}")

            return False

    async def get_if_user_unsubscribed_for_random_coffee(self, user_id) -> dict:
        query = await (self.select.
                       select_user_from_unsubscribed_users_for_random_coffee(user_id=user_id))

        return await self.exec(query=query, fetch=True)

    async def delete_user_from_unsubscribed_for_random_coffee(self, user_id) -> bool:
        try:
            query = await self.delete.delete_user_from_unsubscribed_random_coffee(user_id=user_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while deleting user from_unsubscribed_random_coffee from db: {e}")

            return False

    async def delete_user_from_users_for_random_coffee(self, user_id) -> bool:
        try:
            query = await self.delete.delete_user_from_subscribed_random_coffee(user_id=user_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while deleting user from_subscribed_random_coffee from db: {e}")

            return False

    async def unsubscribe_user_for_random_coffee(self, user_id) -> bool:
        try:
            query = await self.insert.insert_user_for_unsubscribed_users_for_random_coffee(user_id=user_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while unsubscribing user for random coffee from db: {e}")

            return False

    async def get_random_profile_for_random_coffee(self, offset, exclude_user_id=0) -> dict:
        query = await self.select.select_random_profile_for_random_coffee(offset)

        return await self.exec(query=query, fetch=True)

    async def get_count_subscribed_for_random_coffee(self) -> dict:
        query = await self.select.select_count_subscribed_users_for_random_coffee()

        return await self.exec(query=query, fetch=True)

    async def get_subscribed_users_for_random_coffee(self) -> dict:
        query = await self.select.select_subscribed_users_for_random_coffee()

        return await self.exec(query=query, fetch=True)

