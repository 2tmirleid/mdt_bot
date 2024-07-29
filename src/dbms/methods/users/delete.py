class DeleteUsers:
    def __init__(self):
        ...

    async def delete_user_for_event(self, user_id, event_id) -> str:
        return f"""
            DELETE FROM users_for_events WHERE user_id = '{user_id}' AND event_id = '{event_id}'
        """

    async def delete_user_from_unsubscribed_random_coffee(self, user_id) -> str:
        return f"""
            DELETE FROM unsubscribed_users_for_random_coffee
                WHERE user_id = '{user_id}'
        """
