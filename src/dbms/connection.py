import os

import psycopg2
# !!! psycopg2-binary is lib for postgreSQL. You need replace it with lib which fits with yours DBMS
from dotenv import load_dotenv, find_dotenv
from psycopg2.extras import DictCursor

try:
    # Initialized env variables
    load_dotenv(find_dotenv())

    # Connect to the database
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
        port=os.environ['POSTGRES_PORT'],
    )

    cursor = conn.cursor()
except Exception as e:
    print(f'Error while connecting to the database: {e}')
