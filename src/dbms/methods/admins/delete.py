class DeleteAdmins:
    def __init__(self):
        ...

    async def delete_event_by_id(self, event_id) -> str:
        return f"""DELETE FROM events WHERE _id = '{event_id}'"""
