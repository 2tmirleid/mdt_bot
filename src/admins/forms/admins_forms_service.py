from src.dbms.methods.admins.select import SelectAdmins
from src.dbms.methods.admins.update import UpdateAdmins
from utils.RCS.service import Service


class AdminsFormsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()
        self.update: UpdateAdmins = UpdateAdmins()

    async def get_new_forms(self, offset=0) -> dict:
        try:
            query = await self.select.select_admin_new_forms(offset=offset)

            return await self.exec(query=query, fetch=True)
        except Exception as e:
            print(f"Error while get new forms from db: {e}")

    async def get_new_forms_count(self) -> dict:
        query = await self.select.select_admin_new_forms_count()

        return await self.exec(query=query, fetch=True)

    async def accept_new_form(self, form_id) -> bool:
        try:
            query = await self.update.update_new_form_by_accepting(form_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while accepting new form from db: {e}")

            return False
