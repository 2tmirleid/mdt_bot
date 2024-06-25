from src.dbms.connection import cursor, conn


class Service:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn
