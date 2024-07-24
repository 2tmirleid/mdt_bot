from src.dbms.methods.users.select import SelectUsers
from utils.RCS.service import Service


class UsersResidentsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()

    async def get_residents(self, property: str, value: str, offset=0) -> dict:
        query = await self.select.select_residents(
            property=property,
            value=value,
            offset=offset
        )

        return await self.exec(query=query, fetch=True)
