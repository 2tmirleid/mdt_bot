class SelectUsers:
    def __init__(self):
        ...

    async def select_user_chat_id_by_id(self, user_id) -> str:
        return f"""SELECT tg_chat_id, is_approved FROM users WHERE _id = '{user_id}'"""

    async def select_user_by_chat_id(self, user_id) -> str:
        return f"""SELECT tg_chat_id, is_approved FROM users WHERE tg_chat_id = '{user_id}'"""

    async def select_user_by_phone(self, phone) -> str:
        return f"""SELECT phone FROM users WHERE phone = '{phone}' AND is_approved = '1'"""
