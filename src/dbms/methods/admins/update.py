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
