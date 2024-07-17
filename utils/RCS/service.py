from psycopg2.extras import DictCursor

from src.dbms.connection import conn


class Service:
    def __init__(self):
        self.conn: conn = conn

    async def exec(self, query: str, fetch=False, commit=False):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query)

            if fetch:
                return cursor.fetchall()
            if commit:
                return self.conn.commit()
