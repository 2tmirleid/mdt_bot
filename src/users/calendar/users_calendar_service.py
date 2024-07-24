from src.dbms.methods.users.delete import DeleteUsers
from src.dbms.methods.users.insert import InsertUsers
from src.dbms.methods.users.select import SelectUsers
from src.dbms.methods.users.update import UpdateUsers
from utils.RCS.service import Service


class UsersCalendarService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()
        self.update: UpdateUsers = UpdateUsers()
        self.insert: InsertUsers = InsertUsers()
        self.delete: DeleteUsers = DeleteUsers()

    async def get_events_count(self, city: str) -> dict:
        query = await self.select.select_active_events_count(city=city)

        return await self.exec(query=query, fetch=True)

    async def get_active_events(self, city: str, offset=0) -> dict:
        query = await self.select.select_active_events(offset=offset, city=city)

        return await self.exec(query=query, fetch=True)

    async def get_user_id_by_chat_id(self, chat_id) -> dict:
        query = await self.select.select_user_id_by_chat_id(chat_id)

        return await self.exec(query=query, fetch=True)

    async def is_user_for_event(self, user_id, event_id) -> dict:
        query = await self.select.select_is_user_for_event(user_id, event_id)

        return await self.exec(query=query, fetch=True)

    async def register_user_for_event(self, user_id, event_id) -> bool:
        try:
            query = await self.insert.insert_user_for_event(user_id=user_id, event_id=event_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while register user for event from db: {e}")
            return False

    async def unregister_user_for_event(self, user_id, event_id) -> bool:
        try:
            query = await self.delete.delete_user_for_event(user_id=user_id, event_id=event_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while unregister user for event from db: {e}")
            return False
