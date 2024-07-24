class InsertUsers:
    def __init__(self):
        ...

    async def insert_user(self, user: dict) -> str:
        return f"""
            INSERT INTO users (
                tg_chat_id, 
                tg_username, 
                phone, 
                photo, 
                full_name, 
                birth_date, 
                city, 
                company, 
                position, 
                rm_status, 
                hobbies, 
                resources, 
                expertise)
                VALUES (
                    '{user['tg_chat_id']}',
                    '{user['tg_username']}',
                    '{user['phone']}',
                    '{user['photo']}',
                    '{user['full_name']}',
                    '{user['birth_date']}',
                    '{user['city']}',
                    '{user['company']}',
                    '{user['position']}',
                    '{user['rm_status']}',
                    '{user['hobbies']}',
                    '{user['resources']}',
                    '{user['expertise']}'
                )
        """

    async def insert_user_for_event(self, user_id, event_id) -> str:
        return f"""
            INSERT INTO users_for_events (
                        user_id, 
                        event_id) 
                        VALUES (
                            '{user_id}',
                            '{event_id}'
                        )
        """
