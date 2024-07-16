class SelectAdmins:
    def __init__(self):
        ...

    async def select_admin_by_chat_id(self, chat_id) -> str:
        return f"""SELECT full_name FROM users WHERE tg_chat_id = '{chat_id}' and is_admin = '1'"""
