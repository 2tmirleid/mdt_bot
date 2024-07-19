from src.dbms.methods.admins.insert import InsertAdmins
from src.dbms.methods.admins.select import SelectAdmins
from utils.RCS.service import Service


class AdminsEventsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()
        self.insert: InsertAdmins = InsertAdmins()

    async def get_events(self, city: str, offset=0) -> dict:
        query = await self.select.select_events(city=city, offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_events_count(self, city: str) -> dict:
        query = await self.select.select_events_count(city=city)

        return await self.exec(query=query, fetch=True)

    async def add_event(self, event: dict) -> bool:
        try:
            query = await self.insert.insert_event(event=event)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while inserting event: {e}")

            return False

    async def get_users_for_event(self, event_id, offset=0) -> dict:
        query = await self.select.select_users_for_event(event_id=event_id, offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_users_count_for_event(self, event_id) -> dict:
        query = await self.select.select_users_count_for_event(event_id=event_id)

        return await self.exec(query=query, fetch=True)
