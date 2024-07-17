class SelectUsers:
    def __init__(self):
        ...

    async def select_user_chat_id_by_id(self, user_id) -> str:
        return f"""SELECT tg_chat_id FROM users WHERE _id = '{user_id}'"""
