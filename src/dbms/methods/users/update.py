class UpdateUsers:
    def __init__(self):
        ...

    # async def update_user_chat_id_and_username(self, chat_id, username, phone) -> str:
    #     return f"""UPDATE users SET tg_chat_id = '{chat_id}', tg_username = '{username}' WHERE phone = '{phone}'"""

    async def update_user_chat_id_and_username(self, chat_id, username, phone) -> str:
        # Удаляем префикс +7, 7 или 8
        if phone.startswith('+7'):
            phone = phone[2:]  # Убираем +7
        elif phone.startswith('7') or phone.startswith('8'):
            phone = phone[1:]  # Убираем 7 или 8

        query = f"""UPDATE users 
                    SET 
                        tg_chat_id = '{chat_id}', 
                        tg_username = '{username}' 
                    WHERE RIGHT(phone, LENGTH(phone) - CASE 
                        WHEN phone LIKE '+7%' THEN 2 ELSE 1 END) = '{phone}'"""

        return query

    async def update_profile(self, chat_id, property, value) -> str:
        return f"""UPDATE users SET {property} = '{value}' WHERE tg_chat_id = '{chat_id}'"""

