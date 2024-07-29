from src.dbms.methods.users.select import SelectUsers
from src.dbms.methods.users.update import UpdateUsers
from utils.RCS.service import Service


class UsersRandomCoffeeService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectUsers = SelectUsers()
        self.update: UpdateUsers = UpdateUsers()
