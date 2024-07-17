class SelectAdmins:
    def __init__(self):
        ...

    async def select_admin_full_name_by_chat_id(self, chat_id) -> str:
        return f"""
                    SELECT full_name 
                        FROM users 
                        WHERE tg_chat_id = '{chat_id}' 
                            AND is_admin = '1'
                                                """

    async def select_admin_new_forms(self, offset=0) -> str:
        return f"""
                    SELECT _id,
                           phone, 
                           photo_id,
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
                        WHERE is_approved = '0'
                            AND is_rejected = '0'
                        ORDER BY _id 
                        LIMIT 1
                        OFFSET {offset}"""

    async def select_admin_new_forms_count(self) -> str:
        return """SELECT COUNT( * )
                    FROM users
                    WHERE is_approved = '0'
                        AND is_rejected = '0'"""
