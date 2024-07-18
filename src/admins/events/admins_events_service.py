from src.dbms.methods.admins.select import SelectAdmins
from utils.RCS.service import Service


class AdminsEventsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()

    async def get_events(self, city: str, offset=0) -> dict:
        query = await self.select.select_events(city=city, offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_events_count(self, city: str) -> dict:
        query = await self.select.select_events_count(city=city)

        return await self.exec(query=query, fetch=True)
