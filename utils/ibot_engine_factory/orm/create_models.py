from src.dbms.connection import cursor, conn


def create_tables(func):
    try:
        cursor.execute(
            func()
        )
        conn.commit()
    except Exception as e:
        print(f'Error while creating tables: {e}')
