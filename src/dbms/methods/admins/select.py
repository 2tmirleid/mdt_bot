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

    async def select_events(self, city: str, offset=0) -> str:
        return f"""SELECT _id,
                         photo,
                         title,
                         city,
                         description,
                         event_date,
                         is_active
                      FROM events
                      WHERE LOWER(city)  = '{city.lower()}'
                      ORDER BY _id
                      LIMIT 1
                      OFFSET {offset}"""

    async def select_events_count(self, city: str) -> str:
        return f"""SELECT COUNT( * )
                    FROM events
                    WHERE city = '{city}'"""

    async def select_users_for_event(self, event_id, offset=0) -> str:
        return f"""
            SELECT u.full_name,
                   u.tg_username 
            FROM users_for_events ufe
                JOIN users u 
                    ON ufe.user_id = u._id
                WHERE event_id = '{event_id}'
                ORDER BY ufe.user_id
                LIMIT 1
                offset {offset}
        """

    async def select_users_count_for_event(self, event_id) -> str:
        return f"""
            SELECT COUNT ( * )
            FROM users_for_events
                WHERE event_id = '{event_id}'
        """
