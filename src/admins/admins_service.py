from utils.RCS.service import Service
from src.dbms.methods.admins.select import SelectAdmins


class AdminsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()

    async def am_i_admin(self, chat_id) -> dict:
        query = await self.select.select_admin_by_chat_id(chat_id)

        return await self.exec(query=query, fetch=True)
