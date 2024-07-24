class SelectUsers:
    def __init__(self):
        ...

    async def select_user_chat_id_by_id(self, user_id) -> str:
        return f"""SELECT tg_chat_id, is_approved FROM users WHERE _id = '{user_id}'"""

    async def select_user_by_chat_id(self, user_id) -> str:
        return f"""SELECT tg_chat_id, is_approved, is_rejected FROM users WHERE tg_chat_id = '{user_id}'"""

    async def select_user_by_phone(self, phone) -> str:
        return f"""SELECT phone FROM users WHERE phone = '{phone}' AND is_approved = '1'"""

    async def select_user_profile_by_chat_id(self, chat_id) -> str:
        return f"""SELECT phone,
                          photo,
                          full_name,
                          birth_date,
                          city,
                          company,
                          position,
                          rm_status,
                          hobbies,
                          resources,
                          expertise
                    FROM users
                        WHERE tg_chat_id = '{chat_id}'"""

    async def select_residents(self, property: str, value: str, offset=0) -> str:
        return f"""SELECT tg_username,
                          photo,
                          phone,
                          full_name,
                          birth_date,
                          city,
                          company,
                          position,
                          rm_status,
                          hobbies,
                          resources,
                          expertise,
                          COUNT (_id) OVER() as count
                    FROM users
                     WHERE LOWER({property}) 
                     LIKE LOWER('%{value}%')
                     ORDER BY _id
                     LIMIT 1 
                     OFFSET {offset}"""
