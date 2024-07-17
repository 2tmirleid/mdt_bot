from src.dbms.methods.admins.select import SelectAdmins
from utils.RCS.service import Service


class AdminsFormsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()

    async def get_new_forms(self, offset=0) -> dict:
        try:
            query = await self.select.select_admin_new_forms(offset=offset)

            return await self.exec(query=query, fetch=True)
        except Exception as e:
            print(f"Error while get new forms from db: {e}")

    async def get_new_forms_count(self) -> dict:
        query = await self.select.select_admin_new_forms_count()

        return await self.exec(query=query, fetch=True)
