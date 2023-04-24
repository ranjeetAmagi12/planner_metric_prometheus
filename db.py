import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus


import psycopg2

def get_connection():
    #establishing the connection
    conn = psycopg2.connect(
        database=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT')
    )
    return conn

def get_connection_cursor(conn):
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    return cursor
