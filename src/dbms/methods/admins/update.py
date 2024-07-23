class UpdateAdmins:
    def __init__(self):
        ...

    async def update_new_form_by_accepting(self, form_id) -> str:
        return f"""UPDATE users 
                    SET is_approved = '1' 
                        WHERE _id = '{form_id}'"""

    async def update_new_form_by_rejecting(self, form_id) -> str:
        return f"""UPDATE users
                   SET is_rejected = '1'
                        WHERE _id = '{form_id}'"""

    async def update_event_activity(self, event_id, event_activity) -> str:
        return f"""UPDATE events SET is_active = {not event_activity[0]['is_active']} WHERE _id = '{event_id}'"""

    async def update_event(self, event_id, property, value) -> str:
        return f"""UPDATE events SET {property} = '{value}' WHERE _id = '{event_id}'"""
