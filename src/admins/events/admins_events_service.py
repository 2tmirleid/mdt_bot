from src.dbms.connection import conn, cursor
from src.dbms.methods.admins.delete import DeleteAdmins
from src.dbms.methods.admins.insert import InsertAdmins
from src.dbms.methods.admins.select import SelectAdmins
from src.dbms.methods.admins.update import UpdateAdmins
from utils.RCS.service import Service


class AdminsEventsService(Service):
    def __init__(self):
        super().__init__()

        self.select: SelectAdmins = SelectAdmins()
        self.insert: InsertAdmins = InsertAdmins()
        self.delete: DeleteAdmins = DeleteAdmins()
        self.update: UpdateAdmins = UpdateAdmins()

    async def get_events(self, city: str, offset=0) -> dict:
        query = await self.select.select_events(city=city, offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_events_count(self, city: str) -> dict:
        query = await self.select.select_events_count(city=city)

        return await self.exec(query=query, fetch=True)

    async def add_event(self, event: dict) -> bool:
        try:
            cursor.execute(
                f"""
                        INSERT INTO events 
                            (photo, 
                            title, 
                            city, 
                            description, 
                            event_date)
                        VALUES (%s, %s, %s, %s, %s)""",
                (event['photo'],
                 event['title'],
                 event['city'],
                 event['description'],
                 event['event_date'])
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while inserting event: {e}")
            self.conn.rollback()
            return False

    async def get_users_for_event(self, event_id, offset=0) -> dict:
        query = await self.select.select_users_for_event(event_id=event_id, offset=offset)

        return await self.exec(query=query, fetch=True)

    async def get_users_count_for_event(self, event_id) -> dict:
        query = await self.select.select_users_count_for_event(event_id=event_id)

        return await self.exec(query=query, fetch=True)

    async def delete_event_by_id(self, event_id) -> bool:
        try:
            query = await self.delete.delete_event_by_id(event_id)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while deleting event: {e}")

            return False

    async def change_event_activity(self, event_id: str) -> bool:
        try:
            event_activity = await self.get_event_activity_by_id(event_id=event_id)

            query = await self.update.update_event_activity(event_id=event_id, event_activity=event_activity)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while change event activity: {e}")
            return False

    async def get_event_activity_by_id(self, event_id):
        query = await self.select.select_event_activity_by_id(event_id)

        return await self.exec(query=query, fetch=True)

    async def edit_event(self, event_id, property, value) -> bool:
        try:
            query = await self.update.update_event(event_id, property, value)

            await self.exec(query=query, commit=True)

            return True
        except Exception as e:
            print(f"Error while updating event: {e}")
            return False
