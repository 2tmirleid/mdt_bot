from src.dbms.connection import conn
from src.dbms.methods.users.select import SelectUsers
from utils.RCS.service import Service


class UsersResidentsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()

    async def get_residents(self, property: str, value: str, offset=0) -> dict:
        try:
            query = await self.select.select_residents(
                property=property,
                value=value,
                offset=offset
            )

            return await self.exec(query=query, fetch=True)
        except Exception as e:
            print(f"Error while getting residents from db: {e}")
            await conn.rollback()
