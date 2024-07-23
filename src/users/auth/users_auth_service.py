from src.dbms.methods.users.insert import InsertUsers
from src.dbms.methods.users.update import UpdateUsers
from utils.RCS.service import Service


class UsersAuthService(Service):
    def __init__(self):
        super().__init__()

        self.insert: InsertUsers = InsertUsers()
        self.update: UpdateUsers = UpdateUsers()

    async def save_user(self, user: dict) -> bool:
        try:
            query = await self.insert.insert_user(user)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while saving user from db: {e}")

            return False

    async def save_tg_chat_id_and_tg_username(self, chat_id, username, phone) -> bool:
        try:
            query = await self.update.update_user_chat_id_and_username(chat_id, username, phone)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while updating user chat_id and username from db: {e}")

            return False
