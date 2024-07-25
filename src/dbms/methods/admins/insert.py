class InsertAdmins:
    def __init__(self):
        ...

    async def insert_event(self, event: dict) -> str:
        return f"""
            INSERT INTO events 
                (photo, 
                title, 
                city, 
                description, 
                event_date)
            VALUES ('{event['photo']}',
                    '{event['title']}',
                    '{event['city']}',
                    '{event['description']}',
                    '{event['event_date']}')
        """