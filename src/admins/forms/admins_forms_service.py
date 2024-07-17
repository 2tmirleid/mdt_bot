from src.dbms.methods.admins.select import SelectAdmins
from utils.RCS.service import Service


class AdminsFormsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()
