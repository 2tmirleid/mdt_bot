class UpdateUsers:
    def __init__(self):
        ...

    async def update_user_chat_id_and_username(self, chat_id, username, phone) -> str:
        return f"""UPDATE users SET tg_chat_id = '{chat_id}', tg_username = '{username}' WHERE phone = '{phone}'"""
